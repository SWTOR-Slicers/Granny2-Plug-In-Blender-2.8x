# <pep8 compliant>

"""
Merged SWTOR NPC/Character importer created by Crunch.

Replaces the old import_cha.py (IO Scene GR2) + char_character_assembler.py
(ZG_Tools) split. Reads directly from a local "resources" folder (mirroring
the game's extracted asset layout) instead of copying assets into a
per-character folder first.

Targets Jedipedia.net's json export format exclusively.
No support for older TORC exports with none planned.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import bpy
import bmesh
from mathutils import Vector, Matrix

from .import_gr2 import load as ImportGR2_load
from ..types.shared import job_results


# ---------------------------------------------------------------------------
# Path resolution (spec §4)
# ---------------------------------------------------------------------------

def resolve_resource_path(resources_root, relative_path):
    # type: (str, Optional[str]) -> Optional[str]
    """
    Resolves a Jedipedia json path (e.g. "/art/dynamic/head/model/x.gr2")
    against a local resources root folder that contains an "art" subfolder
    directly, mirroring the game's own asset layout.

    Defensively strips:
    - a single leading slash or backslash
    - a redundant leading "resources" path segment, in case a path
      includes one (historically seen on the old meta.skeletonModel
      field, before skeleton resolution moved to the .dyc-based lookup
      in import_skeleton() -- kept as a general safety net)

    Returns None if relative_path is falsy, so callers can skip absent
    optional paths without extra checks.
    """
    if not relative_path:
        return None

    # Normalize to forward slashes regardless of which slash style the
    # json used, so splitting is consistent.
    normalized = relative_path.replace("\\", "/").lstrip("/")

    parts = normalized.split("/")
    if parts and parts[0].lower() == "resources":
        parts = parts[1:]

    return str(Path(resources_root, *parts))


# ---------------------------------------------------------------------------
# JSON parsing (spec §3, §5)
# ---------------------------------------------------------------------------

def read(filepath):
    # type: (str) -> Tuple[Dict[str, Any], Dict[str, List[Dict]], List[Dict]]
    """
    Parses a Jedipedia-formatted NPC/PC json file.

    This is a pure parser: it doesn't touch the resources folder, doesn't
    validate that the file "looks like" a character file, and doesn't
    raise on a missing "meta" entry (current live Jedipedia exports don't
    emit one yet) — callers decide how to handle those cases.

    Returns:
        meta:
            Dict of the parsed "meta" entry's fields (charType, charName,
            nppPath, bodyType, errors). Empty dict if no "meta" entry is
            present. bodyType drives skeleton resolution -- see
            import_skeleton()'s docstring for how.

        slots:
            Dict mapping slotName -> ordered list of raw entry dicts, in
            the order they appeared in the file. A slotName with more
            than one entry represents multiple import variants (spec §5)
            — e.g. two "head" entries for two alternate head sculpts.
            The reserved "skinMats" slotName is excluded here; see
            skin_mats below.

        skin_mats:
            List of {"slot_name": ..., "mat_info": ...} dicts drawn from
            the "skinMats" entry's materialInfo.mats, flattened for easy
            lookup later (spec §6's SkinB heuristic). Empty list if the
            "skinMats" entry is absent or has no mats.
    """
    with open(filepath, encoding="utf-8") as file:
        data: List[Dict[str, Any]] = json.load(file)

    meta: Dict[str, Any] = {}
    slots: Dict[str, List[Dict]] = {}
    skin_mats: List[Dict] = []

    for entry in data:
        slot_name = entry.get("slotName")
        if not slot_name:
            # Forward-compat: entries we don't recognize (yet) are
            # skipped rather than breaking the importer.
            continue

        if slot_name == "meta":
            meta = {
                "charType": entry.get("charType"),
                "charName": entry.get("charName"),
                "nppPath": entry.get("nppPath"),
                "bodyType": entry.get("bodyType"),
                "errors": entry.get("errors", []),
            }
            continue

        if slot_name == "skinMats":
            mats = entry.get("materialInfo", {}).get("mats", [])
            for mat in mats:
                # The source shape spreads matPath (inside "materialInfo"),
                # "ddsPaths" and "otherValues" across three separate keys
                # on the same mat dict. Consolidate them into a single
                # mat_info dict shaped the same way an ordinary slot
                # entry's materialInfo is, so downstream code (§6) can
                # treat skin_mats entries and ordinary slot mat_infos
                # uniformly.
                mat_info = dict(mat.get("materialInfo", {}))
                mat_info["ddsPaths"] = mat.get("ddsPaths", {})
                mat_info["otherValues"] = mat.get("otherValues", {})
                skin_mats.append({
                    "slot_name": mat.get("slotName"),
                    "mat_info": mat_info,
                })
            continue

        slots.setdefault(slot_name, []).append(entry)

    return meta, slots, skin_mats


# ---------------------------------------------------------------------------
# Material building (spec §6)
# ---------------------------------------------------------------------------

def _load_or_get_image(resources_root, relative_path):
    """
    Loads a .dds texture from the resources root, reusing an already-loaded
    Blender image with the same filename if one exists (mirrors the
    dedup-by-basename convention the original importer used for images --
    distinct from the new dedup-by-.mat-filename convention used for
    materials themselves, see get_or_create_material()).
    """
    path = resolve_resource_path(resources_root, relative_path)
    if not path:
        return None
    name = Path(path).name
    existing = bpy.data.images.get(name)
    if existing:
        return existing
    return bpy.data.images.load(path)


def _set_palette(node, other_values, index, include_metallic_specular):
    """Populates a HeroEngine shader node's palette<index>_* properties."""
    prefix = "palette%d" % index
    other_palette = other_values[prefix]
    setattr(node, prefix + "_hue", float(other_palette[0]))
    setattr(node, prefix + "_saturation", float(other_palette[1]))
    setattr(node, prefix + "_brightness", float(other_palette[2]))
    setattr(node, prefix + "_contrast", float(other_palette[3]))

    specular = other_values[prefix + "Specular"]
    setattr(node, prefix + "_specular", [
        float(specular[0]), float(specular[1]), float(specular[2]), 1.0,
    ])

    if include_metallic_specular:
        metallic_specular = other_values[prefix + "MetallicSpecular"]
        setattr(node, prefix + "_metallic_specular", [
            float(metallic_specular[0]),
            float(metallic_specular[1]),
            float(metallic_specular[2]),
            1.0,
        ])


# Per-derived-type configuration, replacing the original's per-branch node
# wiring (largely copy-pasted across ~700 lines) with a single data-driven
# function. Each "maps" tuple is (json ddsPaths key, shader node property,
# required); required maps are read unconditionally -- same as the
# original, a missing required key raises -- optional maps are only read
# if present. Each "palettes" tuple is (palette index, include a
# metallic_specular value too?).
DERIVED_CONFIGS = {
    "Creature": {
        "shader_derived": "CREATURE",
        "maps": [
            ("diffuseMap", "diffuseMap", True),
            ("rotationMap", "rotationMap", True),
            ("glossMap", "glossMap", True),
            ("paletteMaskMap", "paletteMaskMap", True),
            ("directionMap", "directionMap", False),
        ],
        "palettes": [],
        "flesh": True,
    },
    "Eye": {
        "shader_derived": "EYE",
        "maps": [
            ("diffuseMap", "diffuseMap", True),
            ("rotationMap", "rotationMap", True),
            ("glossMap", "glossMap", True),
            ("paletteMap", "paletteMap", True),
            ("paletteMaskMap", "paletteMaskMap", True),
        ],
        "palettes": [(1, False)],
        "flesh": False,
    },
    "Garment": {
        "shader_derived": "GARMENT",
        "maps": [
            ("diffuseMap", "diffuseMap", True),
            ("rotationMap", "rotationMap", True),
            ("glossMap", "glossMap", True),
            ("paletteMap", "paletteMap", True),
            ("paletteMaskMap", "paletteMaskMap", True),
        ],
        "palettes": [(1, True), (2, True)],
        "flesh": False,
    },
    "HairC": {
        "shader_derived": "HAIRC",
        "maps": [
            ("diffuseMap", "diffuseMap", True),
            ("rotationMap", "rotationMap", True),
            ("glossMap", "glossMap", True),
            ("paletteMap", "paletteMap", True),
            ("paletteMaskMap", "paletteMaskMap", True),
            ("directionMap", "directionMap", True),
        ],
        "palettes": [(1, True)],
        "flesh": False,
    },
    "SkinB": {
        "shader_derived": "SKINB",
        "maps": [
            ("diffuseMap", "diffuseMap", True),
            ("rotationMap", "rotationMap", True),
            ("glossMap", "glossMap", True),
            ("paletteMap", "paletteMap", True),
            ("paletteMaskMap", "paletteMaskMap", True),
            ("ageMap", "ageMap", False),
            ("complexionMap", "complexionMap", False),
            ("facepaintMap", "facepaintMap", False),
        ],
        "palettes": [(1, True)],
        "flesh": True,
    },
    "Uber": {
        "shader_derived": "UBER",
        "maps": [
            ("diffuseMap", "diffuseMap", True),
            ("rotationMap", "rotationMap", True),
            ("glossMap", "glossMap", True),
        ],
        "palettes": [],
        "flesh": False,
    },
}
DERIVED_CONFIGS["GarmentScrolling"] = DERIVED_CONFIGS["Garment"]


def _has_hero_engine_node(material):
    """
    True if this material already has a ShaderNodeHeroEngine node -- i.e.
    it was actually built by get_or_create_material() at some point,
    as opposed to merely existing under this name.
    """
    if not material.use_nodes or material.node_tree is None:
        return False
    return any(node.bl_idname == "ShaderNodeHeroEngine" for node in material.node_tree.nodes)


def get_or_create_material(resources_root, mat_name, derived, mat_info):
    # type: (str, str, str, Dict[str, Any]) -> Any
    """
    Returns a Blender material for the given governing .mat data, (re)
    building its node graph only if it doesn't already have one.

    mat_name is the .mat file's own basename, extension stripped (spec
    §6) -- e.g. "hair_twilek_non_a08_v02" -- replacing the original's
    "{idx} {slotName}{derived}" naming. Lookup is by name, so identical
    .mat files reused across slots or separate NPC imports collapse into
    one shared material automatically.

    Dedup is NOT a bare bpy.data.materials.get(mat_name) existence check:
    import_gr2.py's own low-level .gr2 reader unconditionally creates a
    default-BSDF placeholder material for every material name embedded
    *inside* the .gr2 file itself (see its build()'s "NOTE: Create
    Materials" step) -- entirely independent of this json-driven code.
    SWTOR .gr2 files can embed a material name that happens to exactly
    match a real .mat file's basename (confirmed real case:
    "boot_dancer01_light_ge_a21dancer01_f"), which would collide with
    our own naming/dedup convention. So existence alone isn't a signal
    that a material was actually already built by this function -- only
    the presence of our own ShaderNodeHeroEngine node is. If a same-named
    material exists but wasn't built by us, its node graph is rebuilt
    from scratch (rather than ever creating a second, differently-
    suffixed material for the same logical .mat).
    """
    new_mat = bpy.data.materials.get(mat_name)
    if new_mat is not None and _has_hero_engine_node(new_mat):
        return new_mat

    if new_mat is None:
        new_mat = bpy.data.materials.new(mat_name)

    # "HighQualityCharacter" is an older/alternate name occasionally seen
    # for what is otherwise a Creature material.
    derived = "Creature" if derived == "HighQualityCharacter" else derived

    config = DERIVED_CONFIGS.get(derived)
    if config is None:
        raise ValueError("Unrecognized derived material type: %r" % (derived,))

    other_values = mat_info.get("otherValues", {})
    dds_paths = mat_info.get("ddsPaths", {})

    new_mat.use_nodes = True

    # Clear every existing node (not just the default Principled BSDF --
    # this material may be a gr2-created placeholder we're repurposing,
    # see docstring above) and rebuild from scratch.
    for nd in list(new_mat.node_tree.nodes):
        new_mat.node_tree.nodes.remove(nd)

    node = new_mat.node_tree.nodes.new(type="ShaderNodeHeroEngine")
    node.location = (0.0, 300.0)
    output = new_mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (300.0, 300.0)
    new_mat.node_tree.links.new(node.outputs["Shader"], output.inputs["Surface"])

    node.derived = config["shader_derived"]

    # Alpha / transparency: unified across every derived type (confirmed:
    # Blender 4.2 LTS/4.5 LTS only, so no pre-4.2 blend_method branch is
    # needed, and Creature no longer needs special-cased handling).
    new_mat.alpha_threshold = node.alpha_test_value = 0.5
    new_mat.show_transparent_back = False
    node.alpha_mode = 'CLIP'
    new_mat.surface_render_method = "DITHERED"

    for json_key, node_attr, required in config["maps"]:
        if required or json_key in dds_paths:
            image = _load_or_get_image(resources_root, dds_paths[json_key])
            setattr(node, node_attr, image)

    for palette_index, include_metallic_specular in config["palettes"]:
        _set_palette(node, other_values, palette_index, include_metallic_specular)

    if config["flesh"]:
        node.flesh_brightness = float(other_values["fleshBrightness"])
        flush = other_values["flush"]
        node.flush_tone = [float(flush[0]), float(flush[1]), float(flush[2]), 1.0]

    return new_mat


# ---------------------------------------------------------------------------
# Material-slot-index -> json-material-data heuristics (spec §6)
# ---------------------------------------------------------------------------

def _find_skin_mat(skin_mats, slot_name):
    for skin_mat in skin_mats:
        if skin_mat.get("slot_name") == slot_name:
            return skin_mat
    return None


def resolve_material_source(entry, index, skin_mats, npc_uses_skin):
    # type: (Dict[str, Any], int, List[Dict], bool) -> Tuple[str, Dict[str, Any]]
    """
    Determines which json material data (and which "derived" shader type)
    governs a given material-slot index on an imported mesh.

    The json only ever fully describes material-slot 0 (the entry's own
    materialInfo) and, for head/creature slots, an additional eyeMatInfo
    block -- it does not say which mesh material-slot indices actually
    exist, or what a 2nd slot on non-head/creature gear represents. This
    heuristic chain is inherited from the original importer, since
    Jedipedia exports don't include "materialSkinIndex" data that would
    make this unambiguous.

    Returns (derived, mat_info).
    """
    slot_name = entry["slotName"]
    mat_info = entry["materialInfo"]
    other_values = mat_info.get("otherValues", {})
    derived = other_values.get("derived")
    derived = "Creature" if derived == "HighQualityCharacter" else derived

    if index == 1:
        if slot_name in ("head", "creature"):
            eye_mat_info = mat_info.get("eyeMatInfo", {})

            # eyeMatInfo self-describes its own type via its own
            # otherValues.derived -- confirmed against real data: a
            # genuine Eye's eyeMatInfo.otherValues.derived is "Eye"
            # (Tatooine/Balmorra heads), while a 2nd material slot that
            # is actually a second Creature material (not an eye at
            # all) has eyeMatInfo.otherValues.derived == 
            # "HighQualityCharacter" (-> Creature) instead, e.g. Malgus.
            # This replaces an earlier, less reliable heuristic (a
            # malformed paletteMap path as the signal) that was written
            # before any real "creature"-slot data was available to
            # check it against, and which only applied to slot_name ==
            # "creature", never "head" -- this direct read applies
            # equally to both, and generalizes correctly to whatever
            # eyeMatInfo actually says.
            eye_other_values = eye_mat_info.get("otherValues", {})
            eye_derived = eye_other_values.get("derived", "Eye")
            eye_derived = "Creature" if eye_derived == "HighQualityCharacter" else eye_derived

            return eye_derived, eye_mat_info

        material_skin_index = other_values.get("materialSkinIndex")
        if material_skin_index is not None:
            if int(material_skin_index) == index:
                derived = "SkinB"
        else:
            # Jedipedia doesn't currently emit materialSkinIndex at all,
            # so this operator-toggle guess is the normal path in
            # practice.
            if npc_uses_skin:
                derived = "SkinB"

    # Whenever the resolved derived is SkinB -- whether natively so on
    # the slot's own primary materialInfo (e.g. "hand", which can BE
    # skin at index 0, no override needed), or via the guess/
    # materialSkinIndex path above at index 1 -- a matching skinMats
    # entry for this slot_name, if one exists, is preferred over the
    # slot's own mat_info. Confirmed bug fix: the original importer's
    # "elif derived == 'SkinB':" branch always did this lookup
    # regardless of why derived ended up being SkinB; an earlier
    # revision of this rewrite only did it for the index-1 guess path,
    # silently using a slot's own (sometimes placeholder/wrong) palette
    # data whenever it was natively SkinB already.
    if derived == "SkinB":
        skin_mat = _find_skin_mat(skin_mats, slot_name)
        if skin_mat is not None:
            return "SkinB", skin_mat["mat_info"]

    return derived, mat_info


# ---------------------------------------------------------------------------
# Variant import (spec §5, §10's import_variant())
# ---------------------------------------------------------------------------

def _job_results_key(filepath):
    """
    Mirrors import_gr2.py's own key-normalization for
    job_results['files_objs_names'], so lookups against it line up. See
    that module's load() for the authoritative version of this logic.
    """
    normalized = filepath.replace("\\", "/")
    if "resources" in normalized:
        return normalized.partition("resources/")[2]
    return normalized


def import_variant(operator, context, resources_root, entry, skin_mats):
    # type: (Any, Any, str, Dict[str, Any], List[Dict]) -> List[Any]
    """
    Imports every model listed in a single slot entry (spec §5's "one
    variant") and assigns materials to every resulting Blender object --
    a single .gr2 can produce more than one object (multi-mesh files),
    and all of them get materials now, not just the first one (confirmed
    fix; the original importer only handled the first).

    Returns the list of imported Objects. Empty if entry["models"] is
    empty -- a valid "none" variant (e.g. a bald/clean-shaven option),
    not an error.
    """
    imported_objects = []

    for model_path in entry.get("models", []):
        resolved_path = resolve_resource_path(resources_root, model_path)

        # Rich results are required so we can look up exactly which
        # object(s) this specific import call produced -- a plain
        # bpy.data.objects[name] guess breaks whenever two variants
        # share the same source .gr2 filename (confirmed real case:
        # multiple head sculpts reusing one mesh with different
        # materials).
        operator.job_results_rich = True

        ImportGR2_load(operator, context, resolved_path)

        object_names = job_results.get("files_objs_names", {}).get(
            _job_results_key(resolved_path), []
        )

        for object_name in object_names:
            ob = bpy.data.objects[object_name]
            imported_objects.append(ob)

            for index in range(len(ob.material_slots)):
                derived, mat_info = resolve_material_source(
                    entry, index, skin_mats, operator.npc_uses_skin,
                )
                mat_path = mat_info.get("matPath")
                if not mat_path:
                    continue

                mat_name = Path(mat_path).stem
                material = get_or_create_material(
                    resources_root, mat_name, derived, mat_info,
                )
                ob.material_slots[index].material = material

    return imported_objects


# ---------------------------------------------------------------------------
# Skeleton import + binding (spec §8)
# ---------------------------------------------------------------------------

def _parse_dyc_skeleton(dyc_path):
    # type: (str) -> Optional[str]
    """
    Extracts the "Skeleton=..." filename from a .dyc file's [SETTINGS]
    section (e.g. "Skeleton=bmnnew_skeleton.gr2" -> "bmnnew_skeleton.gr2").

    .dyc files are INI-like, but this is a hand-rolled line scan rather
    than configparser: other sections (e.g. [MASKS]) contain repeated
    keys ("mask=...") and unlabeled indented sub-entries that aren't
    valid strict INI and would trip configparser's stricter parsing long
    before ever reaching [SETTINGS].

    Returns the skeleton filename, or None if not found.
    """
    current_section = None

    with open(dyc_path, encoding="utf-8", errors="replace") as file:
        for line in file:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].upper()
                continue

            if current_section == "SETTINGS" and "=" in stripped:
                key, _, value = stripped.partition("=")
                if key.strip().lower() == "skeleton":
                    return value.strip()

    return None


def import_skeleton(operator, context, resources_root, meta):
    # type: (Any, Any, str, Dict[str, Any]) -> Optional[Any]
    """
    Imports the skeleton for this NPC, resolved via meta["bodyType"]
    rather than a direct path in the json.

    This moved server-side (Jedipedia) -> local resolution: Jedipedia
    can't reliably determine the actual skeleton file server-side, but
    it's straightforward locally, in two steps:

        1. "/art/dynamic/spec/<bodyType>.dyc" is read directly (e.g.
           "bmn.dyc" for bodyType "bmn"). This is an INI-like file whose
           [SETTINGS] section has a "Skeleton=<filename>.gr2" line
           giving the actual skeleton filename (e.g.
           "bmnnew_skeleton.gr2") -- confirmed this filename does NOT
           always match "<bodyType>_skeleton.gr2" or similar, hence
           needing to actually read it rather than guessing a pattern.
        2. That filename lives in the same /art/dynamic/spec/ directory
           as the .dyc file itself.

    Tolerant by design: a missing/empty bodyType, a missing .dyc file, a
    .dyc with no [SETTINGS] Skeleton= line, or a skeleton path that
    doesn't resolve to an existing file, is not an error -- it just
    means no skeleton gets imported (spec §8: "should be able to handle
    skeletons but not require them").

    Returns the imported armature Object, or None.
    """
    body_type = meta.get("bodyType")
    if not body_type:
        return None

    dyc_path = resolve_resource_path(resources_root, "/art/dynamic/spec/%s.dyc" % body_type)
    if not dyc_path or not Path(dyc_path).exists():
        operator.report(
            {'WARNING'},
            "Skeleton definition file not found, skipping: %s" % (dyc_path or body_type,),
        )
        return None

    skeleton_filename = _parse_dyc_skeleton(dyc_path)
    if not skeleton_filename:
        operator.report(
            {'WARNING'},
            "No [SETTINGS] Skeleton= entry found in %s, skipping." % (dyc_path,),
        )
        return None

    resolved_path = resolve_resource_path(resources_root, "/art/dynamic/spec/%s" % skeleton_filename)
    if not resolved_path or not Path(resolved_path).exists():
        operator.report(
            {'WARNING'},
            "Skeleton file not found, skipping: %s" % (resolved_path or skeleton_filename,),
        )
        return None

    operator.job_results_rich = True
    ImportGR2_load(operator, context, resolved_path)

    object_names = job_results.get("files_objs_names", {}).get(
        _job_results_key(resolved_path), []
    )
    if not object_names:
        return None

    # A skeleton .gr2 is expected to produce a single armature object;
    # if it somehow produces more, the first is treated as the main one
    # (same "first object is main" assumption used elsewhere in this
    # add-on for multi-object imports).
    skeleton_ob = bpy.data.objects[object_names[0]]
    skeleton_ob.show_in_front = True

    return skeleton_ob


def bind_objects_to_armature(objects, armature, single_armature_only=True):
    # type: (List[Any], Any, bool) -> None
    """
    Binds a set of objects to an armature via Armature modifiers, ported
    unchanged from the original ZG_Tools assembler.

    :param objects: list of Objects to bind
    :param armature: the armature Object
    :param single_armature_only: skip objects that already have an
        Armature modifier, rather than adding a second one
    """
    for obj in objects:
        if obj.type != 'MESH':
            continue

        if single_armature_only and any(mod.type == 'ARMATURE' for mod in obj.modifiers):
            continue

        mod = obj.modifiers.new(name="Armature", type='ARMATURE')
        mod.object = armature

        # Create a parent relationship. Don't use a parent_type of
        # 'ARMATURE' -- the modifier above is already doing that job.
        obj.parent = armature
        obj.matrix_parent_inverse = armature.matrix_world.inverted()
        
        # Enable Preserve Volume on Armature Modifier by Default
        obj.modifiers["Armature"].use_deform_preserve_volume = True

        # Automatic weight assignment needs the operator context
        # (bpy.ops.object.parent_set(type='ARMATURE_AUTO')) and isn't
        # done here; weights are assumed to be assigned manually or via
        # another process.


# ---------------------------------------------------------------------------
# Collection assembly (spec §7)
# ---------------------------------------------------------------------------

def assemble_collections(context, npc_name, slot_objects, skeleton_ob=None, character_name_suffix=None):
    # type: (Any, str, Dict[str, List[Any]], Optional[Any], Optional[str]) -> Any
    """
    Builds the NPC's Collection hierarchy:

        <NPC Collection>              # named from npc_name
         |-- <SlotName>                # one per slot that produced objects
         |    |-- variant object 1     # (capitalized -- "head" -> "Head")
         |    `-- variant object 2
         |-- ...
         |-- <creature slot's object(s)>  # directly in the NPC Collection,
         |                                # no "Creature" sub-collection --
         |                                # it's effectively the whole NPC
         `-- <skeleton object>        # directly in the NPC Collection, if any

    slot_objects: dict mapping slotName -> list of imported Objects for
    that slot. A slot with no objects (an all-empty-models variant, e.g.
    a bald/clean-shaven "none" option -- spec §5) is simply skipped, no
    empty Collection is created for it.

    character_name_suffix: if given, appended to every per-slot
    Collection's name as " - <suffix>" (e.g. "Boot" -> "Boot - Republic
    Officer"). Only meant to be passed when the "Append Character Name
    to Collections" import option is on AND the json's meta.charName is
    actually present -- callers decide that, this function just appends
    whatever string it's given (or nothing, if None). Not applied to the
    NPC root Collection itself, since that's already named from npc_name.

    Every Collection is created fresh via bpy.data.collections.new()
    rather than looked up/reused by name -- seebpy.data.collections is a
    global namespace, not scoped by nesting; reusing an existing
    same-named Collection across two different NPC imports in the same
    file would merge their objects together, which is never wanted here.
    Letting Blender auto-suffix duplicate names (".001", ".002", ...) is
    the safe default.

    Returns the NPC root Collection.
    """
    npc_collection = bpy.data.collections.new(npc_name)
    context.scene.collection.children.link(npc_collection)

    for slot_name, objects in slot_objects.items():
        if not objects:
            continue

        # The "creature" slot is effectively the whole NPC on
        # creature-type imports (e.g. Malgus) -- it doesn't get its own
        # sub-collection, its objects go straight into the NPC root,
        # same as the skeleton.
        target_collection = npc_collection
        if slot_name != "creature":
            collection_name = slot_name.capitalize()
            if character_name_suffix:
                collection_name = "%s - %s" % (collection_name, character_name_suffix)
            target_collection = bpy.data.collections.new(collection_name)
            npc_collection.children.link(target_collection)

        for ob in objects:
            target_collection.objects.link(ob)
            # ImportGR2_load() links newly created objects into whatever
            # collection is active in the view layer at import time --
            # remove that link now that the object has its proper home.
            for existing_collection in list(ob.users_collection):
                if existing_collection is not target_collection:
                    existing_collection.objects.unlink(ob)

    if skeleton_ob is not None:
        npc_collection.objects.link(skeleton_ob)
        for existing_collection in list(skeleton_ob.users_collection):
            if existing_collection is not npc_collection:
                existing_collection.objects.unlink(skeleton_ob)

    return npc_collection


# ---------------------------------------------------------------------------
# Twi'lek eyes UV fix + eye separation (spec §9, ported from ZG_Tools)
# ---------------------------------------------------------------------------

def translate_uv_coordinates(mesh_object, material_slot=None, uv_offset=(0, 0)):
    """
    Offsets an object's polys' UVs, either all of them or only those
    associated with a specific material slot. Motivated by Twi'lek
    heads' off-image-bounds eye UVs producing black bakes.

    Ported unchanged from the original ZG_Tools assembler.
    """
    if mesh_object.type != 'MESH':
        return

    mesh = mesh_object.data
    if not mesh.uv_layers.active:
        return

    uv_layer = mesh.uv_layers.active.data

    for face in mesh.polygons:
        if material_slot is None or face.material_index == material_slot:
            for loop_index in face.loop_indices:
                uv = uv_layer[loop_index].uv
                if uv.y <= 1:
                    return
                uv.x += uv_offset[0]
                uv.y += uv_offset[1]


def duplicate_obj(obj_or_obj_name):
    """
    Creates a full duplicate of an object (mesh data, transforms,
    modifiers, constraints, animation data, custom properties), linked
    into the same Collection(s) as the original.

    Ported unchanged from the original ZG_Tools assembler.
    """
    if isinstance(obj_or_obj_name, str):
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name

    new_data = obj.data.copy()
    new_obj = bpy.data.objects.new(obj.name + ".copy", new_data)

    for col in obj.users_collection:
        col.objects.link(new_obj)

    new_obj.location = obj.location.copy()
    new_obj.rotation_euler = obj.rotation_euler.copy()
    new_obj.rotation_quaternion = obj.rotation_quaternion.copy()
    new_obj.scale = obj.scale.copy()
    new_obj.data = new_data

    for prop in obj.keys():
        if prop != "_RNA_UI":
            new_obj[prop] = obj[prop]

    for mod in obj.modifiers:
        new_mod = new_obj.modifiers.new(name=mod.name, type=mod.type)
        for attr in dir(mod):
            if not attr.startswith("_") and attr not in {"type", "name", "rna_type"}:
                try:
                    setattr(new_mod, attr, getattr(mod, attr))
                except AttributeError:
                    pass

        if mod.type == 'ARMATURE':
            new_mod.object = mod.object

    if obj.animation_data:
        new_obj.animation_data_create()
        new_obj.animation_data.action = obj.animation_data.action
        new_obj.animation_data.action = obj.animation_data.action.copy()

    for constr in obj.constraints:
        new_constr = new_obj.constraints.new(type=constr.type)
        for attr in dir(constr):
            if not attr.startswith("_") and attr not in {"type", "name", "rna_type"}:
                try:
                    setattr(new_constr, attr, getattr(constr, attr))
                except AttributeError:
                    pass

    return new_obj


def separate_obj_by_specific_materials(obj_or_obj_name, material_names, separate=True):
    """
    Separates an object's polys associated with the given material(s)
    into a new object per material. By default, also deletes those
    polys and material slots from the original object.

    :param material_names: a material name, or a list of material names.

    Ported from the original ZG_Tools assembler, with one clarity fix:
    the original accepted a single material name string and tested
    membership via Python's substring-`in` on that string, despite its
    own docstring describing it as "a list of materials names" --
    happened to work for how it was actually called (the exact same
    string on both sides of `in`), but is genuinely a list-membership
    check now, matching the docstring.
    """
    if isinstance(material_names, str):
        material_names = [material_names]

    if isinstance(obj_or_obj_name, str):
        original_obj = bpy.data.objects[obj_or_obj_name]
    else:
        original_obj = obj_or_obj_name

    original_mesh = original_obj.data
    new_objs = []

    mat_indices = [
        i for i, mat in enumerate(original_mesh.materials) if mat.name in material_names
    ]

    if separate:
        for mat_index in mat_indices:
            new_obj = original_obj.copy()
            new_obj.data = original_obj.data.copy()
            bpy.context.collection.objects.link(new_obj)
            new_obj.name = "%s_%s" % (original_obj.name, original_mesh.materials[mat_index].name)

            bm = bmesh.new()
            bm.from_mesh(new_obj.data)
            faces_to_delete = [f for f in bm.faces if f.material_index != mat_index]
            bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
            bm.to_mesh(new_obj.data)
            bm.free()

            new_objs.append(new_obj)

    bm = bmesh.new()
    bm.from_mesh(original_mesh)
    faces_to_delete = [f for f in bm.faces if f.material_index in mat_indices]
    bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
    bm.to_mesh(original_mesh)
    bm.free()

    for i, slot in enumerate(original_obj.material_slots[:]):
        if slot.material and slot.material.name in material_names:
            original_obj.data.materials.pop(index=i)

    return new_objs


def delete_polygons_on_side(obj_or_obj_name, side='LEFT'):
    """
    Deletes every polygon on the given side of local X == 0.

    Ported unchanged from the original ZG_Tools assembler.
    """
    if isinstance(obj_or_obj_name, str):
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name

    if obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    faces_to_delete = []
    for face in bm.faces:
        center = face.calc_center_median()
        if side == 'LEFT' and center.x < 0:
            faces_to_delete.append(face)
        elif side == 'RIGHT' and center.x >= 0:
            faces_to_delete.append(face)

    bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
    bm.to_mesh(mesh)
    bm.free()


def get_highest_and_lowest_vertices(obj_or_obj_name):
    """
    Returns (highest_vertex, lowest_vertex) world-space coordinates by Z.

    Ported unchanged from the original ZG_Tools assembler.
    """
    if isinstance(obj_or_obj_name, str):
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name

    bpy.ops.object.mode_set(mode='OBJECT')

    bm = bmesh.new()
    bm.from_mesh(obj.data)

    global_matrix = obj.matrix_world
    highest_vertex = None
    lowest_vertex = None

    for v in bm.verts:
        global_coord = global_matrix @ v.co
        if highest_vertex is None or global_coord.z > highest_vertex.z:
            highest_vertex = global_coord
        if lowest_vertex is None or global_coord.z < lowest_vertex.z:
            lowest_vertex = global_coord

    bm.free()

    return highest_vertex, lowest_vertex


def set_obj_origin(obj_or_obj_name, new_origin):
    """
    Moves an object's origin to new_origin (world space), preserving its
    visual position by compensating the mesh data's transform.

    Ported unchanged from the original ZG_Tools assembler.
    """
    if isinstance(obj_or_obj_name, str):
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name

    new_origin = Vector(new_origin)

    obj_matrix = obj.matrix_world
    current_origin_world = obj_matrix @ Vector((0, 0, 0))
    delta_world = new_origin - current_origin_world
    delta_object_space = obj_matrix.inverted() @ delta_world

    obj.location += delta_world
    obj.data.transform(Matrix.Translation(-delta_object_space))
    obj.data.update()


def apply_twilek_eyes_uv_fix(slot_objects):
    # type: (Dict[str, List[Any]]) -> None
    """
    Applies translate_uv_coordinates() to every Twi'lek head object's
    Eye material slot (index 1), in place.

    Deviates from the original in one way: the original stopped after
    the first Twi'lek head object found across the whole NPC. Now that
    a single NPC can have multiple head variants (spec §5), this applies
    to every matching head variant instead.
    """
    for head_ob in slot_objects.get("head", []):
        if "head_twilek" in head_ob.name:
            translate_uv_coordinates(head_ob, 1, (0, -2))


def separate_head_eyes(slot_objects, separate_each_eye):
    # type: (Dict[str, List[Any]], bool) -> None
    """
    For every head object with an Eye material in its 2nd material slot,
    splits the eyes out into their own object (or two objects, one per
    eye, if separate_each_eye is set) and appends them into
    slot_objects["head"] so they end up correctly placed by
    assemble_collections().

    Iterates over a snapshot of slot_objects["head"] rather than the
    live list, since new eye objects get appended into that same list
    as this runs.
    """
    for head_ob in list(slot_objects.get("head", [])):
        if len(head_ob.material_slots) <= 1:
            continue
        if "eye" not in head_ob.material_slots[1].name.lower():
            continue

        eyes_ob = duplicate_obj(head_ob)

        # Delete the eyes' polys/material from the head object, and the
        # head's polys/material from the eyes object (the duplicate).
        separate_obj_by_specific_materials(
            head_ob, head_ob.material_slots[1].name, separate=False,
        )
        separate_obj_by_specific_materials(
            eyes_ob, eyes_ob.material_slots[0].name, separate=False,
        )

        if not separate_each_eye:
            eyes_ob.name = "%s.eyes" % head_ob.name
            slot_objects.setdefault("head", []).append(eyes_ob)
            continue

        eyes_ob_right = eyes_ob
        eyes_ob_left = duplicate_obj(eyes_ob)

        delete_polygons_on_side(eyes_ob_right, side='LEFT')
        highest_vertex, lowest_vertex = get_highest_and_lowest_vertices(eyes_ob_right)
        set_obj_origin(
            eyes_ob_right,
            (highest_vertex.x, highest_vertex.y, (highest_vertex.z + lowest_vertex.z) / 2),
        )
        eyes_ob_right.name = "%s.eyes.right" % head_ob.name
        slot_objects.setdefault("head", []).append(eyes_ob_right)

        delete_polygons_on_side(eyes_ob_left, side='RIGHT')
        highest_vertex, lowest_vertex = get_highest_and_lowest_vertices(eyes_ob_left)
        set_obj_origin(
            eyes_ob_left,
            (highest_vertex.x, highest_vertex.y, (highest_vertex.z + lowest_vertex.z) / 2),
        )
        eyes_ob_left.name = "%s.eyes.left" % head_ob.name
        slot_objects.setdefault("head", []).append(eyes_ob_left)


# ---------------------------------------------------------------------------
# Orchestrator + Operator (spec §10)
# ---------------------------------------------------------------------------

def load(operator, context, filepath=""):
    # type: (Any, Any, str) -> bool
    """
    Does the actual work of importing a Jedipedia-formatted NPC/Character
    json file: parse -> import every slot's variants -> optionally import
    a skeleton -> assemble Collections -> optionally bind to skeleton.

    Returns True on success, False on failure (mirrors import_gr2.py's
    own load() return convention).
    """
    prefs = bpy.context.preferences.addons["io_scene_gr2"].preferences
    resources_root = prefs.swtor_resources_dir

    if not resources_root or not Path(resources_root).is_dir():
        operator.report(
            {'ERROR'},
            "Set a valid Resources Folder in IO Scene GR2's add-on preferences first.",
        )
        return False

    try:
        meta, slots, skin_mats = read(filepath)
    except (OSError, json.JSONDecodeError) as exc:
        operator.report({'ERROR'}, "Couldn't read %s: %s" % (filepath, exc))
        return False

    if not slots:
        operator.report({'WARNING'}, "No recognizable slot entries found in this file.")
        return False

    npc_name = meta.get("charName") or Path(filepath).stem

    job_results['job_origin'] = operator.bl_idname
    if not operator.job_results_accumulate:
        job_results['objs_names'] = []
        job_results['files_objs_names'] = {}

    slot_objects = {}
    for slot_name, entries in slots.items():
        objects_for_slot = []
        for entry in entries:
            objects_for_slot.extend(
                import_variant(operator, context, resources_root, entry, skin_mats)
            )
        slot_objects[slot_name] = objects_for_slot

    skeleton_ob = None
    if operator.import_skeleton:
        skeleton_ob = import_skeleton(operator, context, resources_root, meta)

    if operator.correct_twilek_eyes_uv:
        apply_twilek_eyes_uv_fix(slot_objects)

    if operator.separate_eyes:
        separate_head_eyes(slot_objects, operator.separate_each_eye)

    assemble_collections(
        context,
        npc_name,
        slot_objects,
        skeleton_ob,
        character_name_suffix=meta.get("charName") if operator.append_character_name_to_collections else None,
    )

    if operator.bind_to_skeleton and skeleton_ob is not None:
        all_objects = [ob for objects in slot_objects.values() for ob in objects]
        bind_objects_to_armature(all_objects, skeleton_ob)

    return True


class ImportCHA(bpy.types.Operator):
    """
    Import a Jedipedia.net-formatted NPC/Character json file.

    Reads .gr2, .mat, and .dds assets directly from the Resources Folder
    configured in this add-on's Preferences -- no separate asset
    gathering/copying step is needed.
    """
    bl_idname = "import_mesh.gr2_json"  # DO NOT CHANGE -- external tools call this by name
    bl_label = "Import SWTOR NPC/Character (.json)"
    bl_description = "Import a Jedipedia.net-formatted NPC/Character .json file"
    bl_options = {'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    append_character_name_to_collections: bpy.props.BoolProperty(
        name="Append Name to Collections",
        description=(
            "Appends the character's name to every per-slot Collection, "
            "e.g. \"Boot\" -> \"Boot - Republic Officer\".\n\n"
            "Only takes effect if the json's meta data actually includes "
            "a character name -- has no effect otherwise"
        ),
        default=False,
    )

    npc_uses_skin: bpy.props.BoolProperty(
        name="Gear Uses Skin",
        description=(
            "When importing a non-Creature-type characters, assume that any 2nd "
            "Material Slot in armor or clothes is skin rather than "
            "garment.\n\n"
            "Typical case actually needing this: revealing clothing."
        ),
        default=True,
    )

    import_skeleton: bpy.props.BoolProperty(
        name="Import Skeleton",
        description="Imports the skeleton referenced by the json file's meta data, if present",
        default=False,  # seeded from add-on Preferences in invoke()
    )

    bind_to_skeleton: bpy.props.BoolProperty(
        name="Bind To Skeleton",
        description="Binds all imported objects to the imported skeleton via Armature modifiers",
        default=False,  # seeded from add-on Preferences in invoke()
    )

    correct_twilek_eyes_uv: bpy.props.BoolProperty(
        name="Correct Twi'lek Eyes UV",
        description="Corrects a known UV offset issue on Twi'lek eyes",
        default=True,
    )

    separate_eyes: bpy.props.BoolProperty(
        name="Separate Eyes",
        description="Separates the eyes from the head object into their own object, useful for rigging",
        default=False,
    )

    separate_each_eye: bpy.props.BoolProperty(
        name="Separate Eyes Individually",
        description=(
        "When separating eyes, makes each eye its own object with its own origin.\n\n"
        "Requires \"Separate Eyes\" to be enabled as well."
        ),
        default=False,
    )

    job_results_rich: bpy.props.BoolProperty(
        name="Rich Results Info",
        options={'HIDDEN'},
        default=False,
    )

    job_results_accumulate: bpy.props.BoolProperty(
        name="Accumulate Jobs' Results Info",
        options={'HIDDEN'},
        default=True,
    )

    # Not exposed in the panel, and always False: import_gr2.py's load()
    # reads this attribute unconditionally before it even checks
    # bl_idname to decide where the *other* import settings come from,
    # so it has to exist regardless. Unlike import_collision/
    # name_as_filename/etc. (genuinely decorative for this operator,
    # since those are always sourced from add-on Preferences instead),
    # this one isn't optional to declare.
    enforce_neutral_settings: bpy.props.BoolProperty(
        options={'HIDDEN'},
        default=False,
    )

    def invoke(self, context, event):
        prefs = bpy.context.preferences.addons["io_scene_gr2"].preferences
        self.import_skeleton = prefs.gr2_import_skeleton_default
        self.bind_to_skeleton = prefs.gr2_bind_to_skeleton_default
        self.append_character_name_to_collections = prefs.gr2_append_character_name_to_collections_default
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if load(self, context, filepath=self.filepath):
            return {'FINISHED'}
        return {'CANCELLED'}
