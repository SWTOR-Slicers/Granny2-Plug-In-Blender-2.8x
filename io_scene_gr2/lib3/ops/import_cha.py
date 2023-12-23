# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic characters into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired JSON file.
"""

import json
import os
from typing import Any, Dict, List, Optional, Set, Tuple

import bpy
from bpy import app
from bpy.props import BoolProperty, CollectionProperty, StringProperty
from bpy.types import Context, Operator, OperatorFileListElement
from bpy_extras.io_utils import ImportHelper

from ..utils.string import path_format, path_split


class ImportCHA(Operator, ImportHelper):
    """Import from JSON file format (.json)"""
    bl_idname = "import_mesh.gr2_json"
    bl_label = "Import SWTOR (.json)"
    bl_options = {'UNDO'}

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the JSON file",
        type=OperatorFileListElement,
    )

    if app.version < (2, 82, 0):
        directory = StringProperty(subtype='DIR_PATH')
    else:
        directory: StringProperty(subtype='DIR_PATH')

    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={'HIDDEN'})

    import_collision: BoolProperty(name="Import collision mesh", default=False)

    def execute(self, context):
        # type: (Context) -> Set[str]
        paths = [os.path.join(self.directory, file.name) for file in self.files]

        if not paths:
            paths.append(self.filepath)

        for path in paths:
            if not load(self, context, path):
                return {'CANCELLED'}

        return {'FINISHED'}


_eye_mat_info = None


def read(filepath):
    # type: (str) -> Tuple[List, Optional[Dict]]
    with open(filepath) as file:
        data: List[Dict[str, Any]] = json.load(file)

    parsed_objects = []
    skin_materials = None

    global _eye_mat_info

    for entry in data:
        if entry["slotName"] == "skinMats":
            to_push = {"slot_name": "skinMats", "mats": []}

            for mat in entry["materialInfo"]["mats"]:
                slot_name = mat["slotName"]
                mat_info = mat["materialInfo"]
                dds_dict = mat["ddsPaths"]
                mat_info["ddsPaths"] = dds_dict
                mat_info["otherValues"] = mat["otherValues"]

                for key in mat_info["ddsPaths"]:
                    tex = dds_dict[key][dds_dict[key].rfind('/'):]
                    if dds_dict[key] == "/.dds" or dds_dict[key] == ".dds":
                        tex = "/black.dds"

                    mat_info["ddsPaths"][key] = \
                        path_format(filepath,
                                    f"/materials/skinMats/{slot_name}"
                                    f"{tex}")

                to_push["mats"].append({"slot_name": slot_name, "mat_info": mat_info})

            skin_materials = to_push
        else:
            try:
                slot_name = entry["slotName"]
                models = [path_format(filepath, f"/models/{slot_name}{model[model.rfind('/'):]}")
                          for model in entry["models"]]
                mat_info = entry["materialInfo"]
                dds_dict = entry["materialInfo"]["ddsPaths"]

                for key in mat_info["ddsPaths"]:
                    tex = dds_dict[key][dds_dict[key].rfind('/'):]
                    if dds_dict[key] == "/.dds" or dds_dict[key] == ".dds":
                        tex = "/black.dds"

                    mat_info["ddsPaths"][key] = \
                        path_format(filepath,
                                    f"/materials/{slot_name}"
                                    f"{tex}")

                slot = {"slot_name": slot_name, "mat_info": mat_info, "models": models}

                if any(name in slot["slot_name"] for name in {'head', 'creature'}):
                    eye_mat_info = entry["materialInfo"]["eyeMatInfo"]
                    dds_dict = eye_mat_info["ddsPaths"]

                    for key in eye_mat_info["ddsPaths"]:
                        eye_mat_info["ddsPaths"][key] = \
                            path_format(filepath,
                                        f"/materials/eye{dds_dict[key][dds_dict[key].rfind('/'):]}")

                    _eye_mat_info = {"slot_name": "eye", "mat_info": eye_mat_info}

                parsed_objects.append(slot)
            except Exception:
                print("AN ERROR HAS OCCURED.")  # TODO: Improve this error handling!

    return parsed_objects, skin_materials


def build(operator, context, slots, skin_mats):
    # type: (Operator, Context, None, None) -> bool
    from .import_gr2 import load as load_gr2

    for slot in slots:
        for model in slot["models"]:
            # Import gr2
            load_gr2(operator, context, model)
            name = path_split(model)[:-4]

            # Set material for model
            ob = bpy.data.objects[name]

            for i, mat_slot in enumerate(ob.material_slots):
                derived = slot["mat_info"]["otherValues"]["derived"]
                derived = "Creature" if derived == "HighQualityCharacter" else derived
                derived = ("Eye" if any(x in slot["slot_name"] for x in {"head", "creature"})
                           and i == 1 else derived)
                new_mat = None
                mat_idx = '{:0>2}'.format(i + 1) if i + 1 < 10 else str(i + 1)
                slot_name = slot["slot_name"]

                try:
                    new_mat = bpy.data.materials[f"{mat_idx} {slot_name}{derived}"]
                except KeyError:
                    if "materialSkinIndex" in slot["mat_info"]["otherValues"]:
                        if int(slot["mat_info"]["otherValues"]["materialSkinIndex"]) == i:
                            derived = "SkinB"

                    new_mat = bpy.data.materials.new(f"{mat_idx} {slot_name}{derived}")
                    new_mat.use_nodes = True
                    
                    # Delete default Principled BSDF shader node
                    for nd in new_mat.node_tree.nodes:
                        if nd.type == "BSDF_PRINCIPLED":
                            new_mat.node_tree.nodes.remove(nd)
                            break

                    node = new_mat.node_tree.nodes.new(type="ShaderNodeHeroEngine")
                    node.location = (0.0, 300.0)

                    new_mat.node_tree.links.new(
                        node.outputs["Shader"],
                        new_mat.node_tree.nodes["Material Output"].inputs["Surface"],
                    )

                    imgs = bpy.data.images

                    if derived == 'Creature':
                        node.derived = 'CREATURE'
                        # TODO: Read Alpha parameters from paths.json
                        new_mat.alpha_threshold = node.alpha_test_value = 0.5
                        new_mat.blend_method = node.alpha_mode = 'CLIP'
                        new_mat.show_transparent_back = False

                        mat_info = slot["mat_info"]
                        other_values = mat_info['otherValues']

                        img = path_split(mat_info["ddsPaths"]["diffuseMap"])
                        if img in imgs:
                            node.diffuseMap = imgs[img]
                        else:
                            node.diffuseMap = imgs.load(mat_info["ddsPaths"]["diffuseMap"])

                        img = path_split(mat_info["ddsPaths"]["rotationMap"])
                        if img in imgs:
                            node.rotationMap = imgs[img]
                        else:
                            node.rotationMap = imgs.load(mat_info["ddsPaths"]["rotationMap"])

                        img = path_split(mat_info["ddsPaths"]["glossMap"])
                        if img in imgs:
                            node.glossMap = imgs[img]
                        else:
                            node.glossMap = imgs.load(mat_info["ddsPaths"]["glossMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMaskMap"])
                        if img in imgs:
                            node.paletteMaskMap = imgs[img]
                        else:
                            node.paletteMaskMap = imgs.load(mat_info["ddsPaths"]["paletteMaskMap"])

                        # try:
                        #     node.directionMap = imgs[path_split(mat_info["ddsPaths"]['directionMap'])]
                        # except KeyError:
                        #     node.directionMap = imgs.load(mat_info["ddsPaths"]['directionMap'])

                        node.flesh_brightness = float(other_values['fleshBrightness'])
                        node.flush_tone = [
                            float(other_values['flush'][0]),
                            float(other_values['flush'][1]),
                            float(other_values['flush'][2]),
                            1.0,
                        ]
                    elif derived == 'Eye':
                        node.derived = 'EYE'
                        # TODO: Read Alpha parameters from paths.json
                        new_mat.alpha_threshold = node.alpha_test_value = 0.5
                        new_mat.blend_method = node.alpha_mode = 'CLIP'
                        new_mat.show_transparent_back = False

                        mat_info = _eye_mat_info["mat_info"]
                        other_values = mat_info['otherValues']

                        img = path_split(mat_info["ddsPaths"]["diffuseMap"])
                        if img in imgs:
                            node.diffuseMap = imgs[img]
                        else:
                            node.diffuseMap = imgs.load(mat_info["ddsPaths"]["diffuseMap"])

                        img = path_split(mat_info["ddsPaths"]["rotationMap"])
                        if img in imgs:
                            node.rotationMap = imgs[img]
                        else:
                            node.rotationMap = imgs.load(mat_info["ddsPaths"]["rotationMap"])

                        img = path_split(mat_info["ddsPaths"]["glossMap"])
                        if img in imgs:
                            node.glossMap = imgs[img]
                        else:
                            node.glossMap = imgs.load(mat_info["ddsPaths"]["glossMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMap"])
                        if img in imgs:
                            node.paletteMap = imgs[img]
                        else:
                            node.paletteMap = imgs.load(mat_info["ddsPaths"]["paletteMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMaskMap"])
                        if img in imgs:
                            node.paletteMaskMap = imgs[img]
                        else:
                            node.paletteMaskMap = imgs.load(mat_info["ddsPaths"]["paletteMaskMap"])

                        node.palette1_hue = float(other_values['palette1'][0])
                        node.palette1_saturation = float(other_values['palette1'][1])
                        node.palette1_brightness = float(other_values['palette1'][2])
                        node.palette1_contrast = float(other_values['palette1'][3])
                        node.palette1_specular = [
                            float(other_values['palette1Specular'][0]),
                            float(other_values['palette1Specular'][1]),
                            float(other_values['palette1Specular'][2]),
                            1.0,
                        ]
                        node.palette1_metallic_specular = [
                            float(other_values['palette1MetallicSpecular'][0]),
                            float(other_values['palette1MetallicSpecular'][1]),
                            float(other_values['palette1MetallicSpecular'][2]),
                            1.0,
                        ]
                    elif derived == 'Garment' or derived == 'GarmentScrolling':
                        node.derived = 'GARMENT'
                        # TODO: Read Alpha parameters from paths.json
                        new_mat.alpha_threshold = node.alpha_test_value = 0.5
                        new_mat.blend_method = node.alpha_mode = 'CLIP'
                        new_mat.show_transparent_back = False

                        mat_info = slot["mat_info"]
                        other_values = mat_info['otherValues']

                        img = path_split(mat_info["ddsPaths"]["diffuseMap"])
                        if img in imgs:
                            node.diffuseMap = imgs[img]
                        else:
                            node.diffuseMap = imgs.load(mat_info["ddsPaths"]["diffuseMap"])

                        img = path_split(mat_info["ddsPaths"]["rotationMap"])
                        if img in imgs:
                            node.rotationMap = imgs[img]
                        else:
                            node.rotationMap = imgs.load(mat_info["ddsPaths"]["rotationMap"])

                        img = path_split(mat_info["ddsPaths"]["glossMap"])
                        if img in imgs:
                            node.glossMap = imgs[img]
                        else:
                            node.glossMap = imgs.load(mat_info["ddsPaths"]["glossMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMap"])
                        if img in imgs:
                            node.paletteMap = imgs[img]
                        else:
                            node.paletteMap = imgs.load(mat_info["ddsPaths"]["paletteMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMaskMap"])
                        if img in imgs:
                            node.paletteMaskMap = imgs[img]
                        else:
                            node.paletteMaskMap = imgs.load(mat_info["ddsPaths"]["paletteMaskMap"])

                        node.palette1_hue = float(other_values['palette1'][0])
                        node.palette1_saturation = float(other_values['palette1'][1])
                        node.palette1_brightness = float(other_values['palette1'][2])
                        node.palette1_contrast = float(other_values['palette1'][3])
                        node.palette1_specular = [
                            float(other_values['palette1Specular'][0]),
                            float(other_values['palette1Specular'][1]),
                            float(other_values['palette1Specular'][2]),
                            1.0,
                        ]
                        node.palette1_metallic_specular = [
                            float(other_values['palette1MetallicSpecular'][0]),
                            float(other_values['palette1MetallicSpecular'][1]),
                            float(other_values['palette1MetallicSpecular'][2]),
                            1.0,
                        ]

                        node.palette2_hue = float(other_values['palette2'][0])
                        node.palette2_saturation = float(other_values['palette2'][1])
                        node.palette2_brightness = float(other_values['palette2'][2])
                        node.palette2_contrast = float(other_values['palette2'][3])
                        node.palette2_specular = [
                            float(other_values['palette2Specular'][0]),
                            float(other_values['palette2Specular'][1]),
                            float(other_values['palette2Specular'][2]),
                            1.0,
                        ]
                        node.palette2_metallic_specular = [
                            float(other_values['palette2MetallicSpecular'][0]),
                            float(other_values['palette2MetallicSpecular'][1]),
                            float(other_values['palette2MetallicSpecular'][2]),
                            1.0,
                        ]
                    elif derived == 'HairC':
                        node.derived = 'HAIRC'
                        # TODO: Read Alpha parameters from paths.json
                        new_mat.alpha_threshold = node.alpha_test_value = 0.5
                        new_mat.blend_method = node.alpha_mode = 'CLIP'
                        new_mat.show_transparent_back = False

                        mat_info = slot["mat_info"]
                        other_values = mat_info['otherValues']

                        img = path_split(mat_info["ddsPaths"]["diffuseMap"])
                        if img in imgs:
                            node.diffuseMap = imgs[img]
                        else:
                            node.diffuseMap = imgs.load(mat_info["ddsPaths"]["diffuseMap"])

                        img = path_split(mat_info["ddsPaths"]["rotationMap"])
                        if img in imgs:
                            node.rotationMap = imgs[img]
                        else:
                            node.rotationMap = imgs.load(mat_info["ddsPaths"]["rotationMap"])

                        img = path_split(mat_info["ddsPaths"]["glossMap"])
                        if img in imgs:
                            node.glossMap = imgs[img]
                        else:
                            node.glossMap = imgs.load(mat_info["ddsPaths"]["glossMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMap"])
                        if img in imgs:
                            node.paletteMap = imgs[img]
                        else:
                            node.paletteMap = imgs.load(mat_info["ddsPaths"]["paletteMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMaskMap"])
                        if img in imgs:
                            node.paletteMaskMap = imgs[img]
                        else:
                            node.paletteMaskMap = imgs.load(mat_info["ddsPaths"]["paletteMaskMap"])

                        # img = path_split(mat_info["ddsPaths"]["directionMap"])
                        # if img in imgs:
                        #     node.directionMap = imgs[img]
                        # else:
                        #     node.directionMap = imgs.load(mat_info["ddsPaths"]["directionMap"])

                        node.palette1_hue = float(other_values['palette1'][0])
                        node.palette1_saturation = float(other_values['palette1'][1])
                        node.palette1_brightness = float(other_values['palette1'][2])
                        node.palette1_contrast = float(other_values['palette1'][3])
                        node.palette1_specular = [
                            float(other_values['palette1Specular'][0]),
                            float(other_values['palette1Specular'][1]),
                            float(other_values['palette1Specular'][2]),
                            1.0,
                        ]
                        node.palette1_metallic_specular = [
                            float(other_values['palette1MetallicSpecular'][0]),
                            float(other_values['palette1MetallicSpecular'][1]),
                            float(other_values['palette1MetallicSpecular'][2]),
                            1.0,
                        ]
                    elif derived == 'SkinB':
                        node.derived = 'SKINB'
                        # TODO: Read Alpha parameters from paths.json
                        new_mat.alpha_threshold = node.alpha_test_value = 0.5
                        new_mat.blend_method = node.alpha_mode = 'CLIP'
                        new_mat.show_transparent_back = False

                        skin_mat = next(
                            (mat for mat in skin_mats["mats"] if mat["slot_name"] == slot["slot_name"]),
                            None,
                        )
                        mat_info = skin_mat["mat_info"] if skin_mat is not None else slot["mat_info"]
                        other_values = mat_info['otherValues']

                        img = path_split(mat_info["ddsPaths"]["diffuseMap"])
                        if img in imgs:
                            node.diffuseMap = imgs[img]
                        else:
                            node.diffuseMap = imgs.load(mat_info["ddsPaths"]["diffuseMap"])

                        img = path_split(mat_info["ddsPaths"]["rotationMap"])
                        if img in imgs:
                            node.rotationMap = imgs[img]
                        else:
                            node.rotationMap = imgs.load(mat_info["ddsPaths"]["rotationMap"])

                        img = path_split(mat_info["ddsPaths"]["glossMap"])
                        if img in imgs:
                            node.glossMap = imgs[img]
                        else:
                            node.glossMap = imgs.load(mat_info["ddsPaths"]["glossMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMap"])
                        if img in imgs:
                            node.paletteMap = imgs[img]
                        else:
                            node.paletteMap = imgs.load(mat_info["ddsPaths"]["paletteMap"])

                        img = path_split(mat_info["ddsPaths"]["paletteMaskMap"])
                        if img in imgs:
                            node.paletteMaskMap = imgs[img]
                        else:
                            node.paletteMaskMap = imgs.load(mat_info["ddsPaths"]["paletteMaskMap"])

                        if "ageMap" in mat_info["ddsPaths"]:
                            img = path_split(mat_info["ddsPaths"]["ageMap"])
                            if img in imgs:
                                node.ageMap = imgs[img]
                            else:
                                node.ageMap = imgs.load(mat_info["ddsPaths"]["ageMap"])

                        if "complexionMap" in mat_info["ddsPaths"]:
                            img = path_split(mat_info["ddsPaths"]["complexionMap"])
                            if img in imgs:
                                node.complexionMap = imgs[img]
                            else:
                                node.complexionMap = imgs.load(mat_info["ddsPaths"]["complexionMap"])

                        if "facepaintMap" in mat_info["ddsPaths"]:
                            img = path_split(mat_info["ddsPaths"]["facepaintMap"])
                            if img in imgs:
                                node.facepaintMap = imgs[img]
                            else:
                                node.facepaintMap = imgs.load(mat_info["ddsPaths"]["facepaintMap"])

                        node.palette1_hue = float(other_values['palette1'][0])
                        node.palette1_saturation = float(other_values['palette1'][1])
                        node.palette1_brightness = float(other_values['palette1'][2])
                        node.palette1_contrast = float(other_values['palette1'][3])
                        node.palette1_specular = [
                            float(other_values['palette1Specular'][0]),
                            float(other_values['palette1Specular'][1]),
                            float(other_values['palette1Specular'][2]),
                            1.0,
                        ]
                        node.palette1_metallic_specular = [
                            float(other_values['palette1MetallicSpecular'][0]),
                            float(other_values['palette1MetallicSpecular'][1]),
                            float(other_values['palette1MetallicSpecular'][2]),
                            1.0,
                        ]

                        node.flesh_brightness = float(other_values['fleshBrightness'])
                        node.flush_tone = [
                            float(other_values['flush'][0]),
                            float(other_values['flush'][1]),
                            float(other_values['flush'][2]),
                            1.0,
                        ]
                    elif derived == 'Uber':
                        node.derived = 'UBER'
                        # TODO: Read Alpha parameters from paths.json
                        new_mat.alpha_threshold = node.alpha_test_value = 0.5
                        new_mat.blend_method = node.alpha_mode = 'CLIP'
                        new_mat.show_transparent_back = False

                        mat_info = slot["mat_info"]
                        other_values = mat_info['otherValues']

                        img = path_split(mat_info["ddsPaths"]["diffuseMap"])
                        if img in imgs:
                            node.diffuseMap = imgs[img]
                        else:
                            node.diffuseMap = imgs.load(mat_info["ddsPaths"]["diffuseMap"])

                        img = path_split(mat_info["ddsPaths"]["rotationMap"])
                        if img in imgs:
                            node.rotationMap = imgs[img]
                        else:
                            node.rotationMap = imgs.load(mat_info["ddsPaths"]["rotationMap"])

                        img = path_split(mat_info["ddsPaths"]["glossMap"])
                        if img in imgs:
                            node.glossMap = imgs[img]
                        else:
                            node.glossMap = imgs.load(mat_info["ddsPaths"]["glossMap"])

                mat_slot.material = new_mat

    return True


def load(operator, context, filepath=""):
    # type: (Operator, Context, str) -> bool
    from bpy_extras.wm_utils.progress_report import ProgressReport

    with ProgressReport(context.window_manager) as progress:
        progress.enter_substeps(3, f"Importing \'{filepath}\' ...")

        progress.step("Parsing file ...", 1)
        slots, skin_mats = read(filepath)

        if slots:
            progress.step("Done, building ...", 2)

            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            if build(operator, context, slots, skin_mats):
                progress.leave_substeps(f"Done, finished importing: \'{filepath}\'")
                return True

        return False
