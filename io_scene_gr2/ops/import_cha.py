# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic characters into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired JSON file.
"""

import json
from re import A
import xml.etree.ElementTree as ET  # for parsing .mat files looking for directionMaps
import os
from typing import Any, Dict, List, Optional, Set, Tuple
import time

import bpy
from bpy import app
from bpy.props import BoolProperty, FloatProperty, CollectionProperty, StringProperty
from bpy.types import Context, Operator, OperatorFileListElement
from bpy_extras.io_utils import ImportHelper


from .import_gr2 import load as ImportGR2_load  # .gr2 importing function used by this module 


from ..utils.string import path_format, path_split

from ..types.shared import job_results  # add-on-wide global-like dict



# Detect Blender version
major, minor, _ = bpy.app.version
blender_version = major + minor / 100



class ImportCHA(Operator):
    """
    Import from JSON file format (.json)
    
    Produces a file browser for manually
    selecting a TORCommunity.com-formatted
    paths.json file describing a SWTOR character
    and their gear.
    """
    bl_idname = "import_mesh.gr2_json"  # DO NOT CHANGE
    bl_description = "(UNLESS TRYING TO DIAGNOSE AN ISSUE,\nUSE THE ZG SWTOR TOOLS ADD-ON'S\nCHARACTER ASSEMBLER INSTEAD\n\nThe Character Assembler calls this importer under the hood\nafter gathering the game assets listed in the .json file for you.\nWe keep this direct import option for diagnosing purposes)\n\n\nImport a 'paths.json' file inside a character folder generated\nby TORCommunity.com's Character Designer\nor its NPC database's 3D Viewers.\n\n• The folder needs to have been filled with the requisite assets\n   by a Character Assembler tool or manually"
    bl_label = "Import SWTOR (.json)"
    bl_options = {'UNDO'}



    # File Browser properties
    
    # This class used to be based on ImportHelper
    # but we now use invoke() to be able to use
    # the Add-on's Preferences settings when
    # called from the Import menu and launching
    # a File Browser.
    
    # filepath is explicitly declared because
    # omitting ImportHelper omits it, too.
    # invoke() handles what to do if it is
    # filled as a param in an external call.
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    if app.version < (2, 82, 0):
        directory = StringProperty(subtype='DIR_PATH')
    else:
        directory: StringProperty(subtype='DIR_PATH')

    filename_ext = ".json"

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the JSON file",
        type=OperatorFileListElement,
    )

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'}
    )



    # Importing parameters' properties.
    # THEY AREN'T SPECIFIC TO THE CHARACTER ASSEMBLER BUT
    # TO THE .GR2 OBJECTS IMPORTER WORKING UNDER THE HOOD.
    #
    # When being called from the Import menu, invoke()
    # will copy the Add-on's prefs settings to them.
    #
    # When called from external code, filled arguments
    # will override current prefs settings.

    import_collision: BoolProperty(
        name="Import Collision Mesh",
        description="Imports objects' collision boundary mesh if present in the files\n(it can be of use when exporting models to other apps and game engines)",
        default=False,
    )

    npc_uses_skin: bpy.props.BoolProperty(
        name="NPC Gear Uses Skin ",
        description="When importing a non-Creature-type NPC, assume that any 2nd. Material Slots\nin armor or clothes are skin. If unticked, use a garment material instead.\n\nMOST NPC GEAR LACK SECOND MATERIALS, ANYWAY.\nTypical case actually using this checkbox: cantina dancers.\n\nIn mixed use cases, the Material Slots' assignments can be easily corrected\nmanually. Skin materials are always created, no matter if not in use.\n\n(TORCommunity.com's non-Creature NPC database exports don't include\n'materialSkinIndex' data indicating whether a piece of garment with\ntwo material slots uses skin or garment for the 2nd one. Hence this\ncheckbox)",
        default = True,
        # options={'HIDDEN'}
    )

    name_as_filename: BoolProperty(
        name="Name As Filename",
        description="Names the imported Blender objects with their filenames instead of their\ninternal 'art names' (the object's mesh data always keeps the 'art name').\n\n.gr2 objects' internal 'art names' typically match their files' names,\nbut sometimes they difer, which can break some tools and workflows.\n\nIn case of multiple mesh files (containing a main object plus secondary ones\nand / or Engine Objects such as Colliders), only the main object is renamed",
        default=True,
    )

    use_modernization: BoolProperty(
        name="Use Modernized Assets",
        description="Uses the texture maps stored in a character's folder's 'materials_modernization' subfolder\ninstead of the ones in the plain 'materials' one",
        default=False,
    )

    apply_axis_conversion: BoolProperty(
        name="Axis Conversion",
        description="Permanently converts the Character's imported object to Blender's 'Z-is-Up' coordinate system\nby 'applying' a x=90º rotation.\n\nSWTOR's coordinate system is 'Y-is-up' vs. Blender's 'Z-is-up'.\nTo compensate for that in a reversible manner, this importer\nnormally sets the object's rotation to X=90º at the Object level.\n\nAs this can be a nuisance outside a modding use case,\nthis option applies it at the Mesh level, instead",
        default=False,
    )

    scale_object: BoolProperty(
        name="Scale Object",
        description="Scales Characters' objects and armatures\nat the Mesh level.\n\nSWTOR sizes objects in decimeters, while Blender defaults to meters.\nThis mismatch, while innocuous, is an obstacle when doing physics\nsimulations, automatic weighting from bones, or other processes\nwhere Blender requires real world-like sizes to succeed",
        default=False,
    )

    scale_factor: FloatProperty(
        name="Scale factor",
        description="Recommended values are:\n\n- 10 for simplicity (characters are superhero-like tall, over 2 m.).\n- Around 8 for accuracy (characters show more realistic heights).\n\nRemember that, if binding to a skeleton later on, the skeleton\nmust match the scale of the objects to work correctly (which\ncan be done on import, or manually afterwards)",
        min = 1.0,
        max = 100.0,
        soft_min = 1.0,
        soft_max = 10.0,
        step = 10,
        precision = 2,
        default=1.0,
    )

    enforce_neutral_settings: BoolProperty(
        name="Enforce Neutral Settings",
        description="Temporarily overrides the settings of the .gr2 Importer that\nthis Character Importer uses with those of older versions\nfor compatibility with similarly imported assets",
        options={'HIDDEN'},
        default=False,
    )

    job_results_rich: BoolProperty(
        name="Rich results Info",
        description="For easier interaction with third party code, this add-on fills 'bpy.context.scene.io_scene_gr2_last_job'\nwith info about its most recent job (imported objects's names) in .json format.\nSet to Rich, it provides additional data such as their relationships to filenames",
        options={'HIDDEN'},
        default=False,
    )

    job_results_accumulate: BoolProperty(
        name="Accumulate Jobs' Results Info between ImportGR2 calls",
        description="By default, .gr2 import requests will clear the information about previous ones.\nThis option lets them accumulate, needed for cases such as a Character Import where\nImportGR2 is called several times in succession",
        options={'HIDDEN'},
        default=True,
    )



    def invoke(self, context, event):
        # To be able to set the class' properties to the values in the
        # Add-on's preferences and show them in the File Browser's options,
        # we use an Invoke function instead of directly using ImportHelper in
        # the class definition, to be able to put there the required code.              
        
        prefs = context.preferences.addons["io_scene_gr2"].preferences
        
        self.import_collision           = prefs.gr2_import_collision
        self.name_as_filename           = prefs.gr2_name_as_filename
        self.use_modernization          = False
        self.apply_axis_conversion      = prefs.gr2_apply_axis_conversion
        self.scale_object               = prefs.gr2_scale_object
        self.scale_factor               = prefs.gr2_scale_factor
        self.enforce_neutral_settings   = False
        self.job_results_rich           = False
        self.job_results_accumulate     = True
        self.npc_uses_skin              = True


        # Handling of filepath in case of being
        # filled as a param in an external call.
        if not self.filepath:
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            return self.execute(context)        


    def execute(self, context):
        # type: (Context) -> Set[str]

        bpy.context.window.cursor_set("WAIT")

        # Clear job_results data before starting a job
        job_results['objs_names'] = []
        job_results['files_objs_names'] = {}
        job_results['job_origin'] = self.bl_idname
            
            
        paths = [os.path.join(self.directory, file.name) for file in self.files]

        if not paths:
            paths.append(self.filepath)

        # Clear filebrowser-related properties now
        # that they have been read and have no more
        # use so that they don't persist if the class
        # breaks before finishing its execution
        # (it makes debugging difficult).
        self.files.clear()
        self.filepath = ""

        for path in paths:
            if not load(self, context, path):
                return {'CANCELLED'}


        bpy.context.scene.io_scene_gr2_last_job = json.dumps(job_results)

        bpy.context.window.cursor_set("DEFAULT")

        return {'FINISHED'}


_eye_mat_info = None


def read(self, filepath):
    # type: (str) -> Tuple[List, Optional[Dict]]
    '''
    Parses a TORCommunity.com's Character Designer-formatted .json file
    returning objects and materials data to process
    '''
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
                    # if dds_dict[key] == "/.dds" or dds_dict[key] == ".dds":
                    #     tex = "/black.dds"

                    if self.use_modernization:
                        mat_info["ddsPaths"][key] = \
                            path_format(filepath,
                                        f"/materials_modernization/skinMats/{slot_name}"
                                        f"{tex}")
                    else:
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

                # As paths.json lacks directionMap data, read it from the .mat file
                # that was gathered in the relevant materials' subfolders and add it
                # to the dds_dict when the materialInfo's derived is Creature or
                # HairC.
                if mat_info["otherValues"]["derived"] in ['Creature', 'HairC']:
                    mat_path = entry["materialInfo"]["matPath"]
                    if self.use_modernization:
                        mat_path = path_format( filepath, f"/materials_modernization/{slot_name}/{os.path.basename(mat_path)}" )
                    else:
                        mat_path = path_format( filepath, f"/materials/{slot_name}/{os.path.basename(mat_path)}" )
                        
                    try:
                        mat_file = open(mat_path)
                    except FileNotFoundError:
                        print(f".mat file {mat_path} couldn't be opened to read directionMap data")
                    else:
                        with mat_file:
                            xml_tree = ET.parse(mat_file)
                            xml_root = xml_tree.getroot()
                            # (DirectionMap's PascalCase comes from the .mat file)
                            DirectionMap = xml_root.find("./input/[semantic='DirectionMap']")
                            if DirectionMap != None:
                                texturemap_path = DirectionMap.find("value").text + ".dds"
                                texturemap_path = texturemap_path.replace("\\", "/")
                                if texturemap_path[0:1] != "/":
                                    texturemap_path = f"/{texturemap_path}" 
                                dds_dict['directionMap'] = texturemap_path

                for key in mat_info["ddsPaths"]:
                    tex = dds_dict[key][dds_dict[key].rfind('/'):]
                    # if dds_dict[key] == "/.dds" or dds_dict[key] == ".dds":
                    #     tex = "/black.dds"

                    if self.use_modernization:
                        mat_info["ddsPaths"][key] = \
                            path_format(filepath,
                                        f"/materials_modernization/{slot_name}"
                                        f"{tex}")
                    else:
                        mat_info["ddsPaths"][key] = \
                            path_format(filepath,
                                        f"/materials/{slot_name}"
                                        f"{tex}")

                slot = {"slot_name": slot_name, "mat_info": mat_info, "models": models}

                if any(name in slot["slot_name"] for name in {'head', 'creature'}):
                    if "eyeMatInfo" in entry["materialInfo"]:
                        eye_mat_info = entry["materialInfo"]["eyeMatInfo"]
                        dds_dict = eye_mat_info["ddsPaths"]

                        for key in eye_mat_info["ddsPaths"]:
                            if self.use_modernization:
                                eye_mat_info["ddsPaths"][key] = \
                                    path_format(filepath,
                                                f"/materials_modernization/eye{dds_dict[key][dds_dict[key].rfind('/'):]}")
                            else:
                                eye_mat_info["ddsPaths"][key] = \
                                    path_format(filepath,
                                                f"/materials/eye{dds_dict[key][dds_dict[key].rfind('/'):]}")

                        _eye_mat_info = {"slot_name": "eye", "mat_info": eye_mat_info}

                parsed_objects.append(slot)
            except Exception:
                print("AN ERROR HAS OCCURED.")  # TODO: Improve this error handling! - Crunch Note, Fix for Single Material Creatures
    #print(parsed_objects)
    return parsed_objects, skin_materials


def build(operator, context, slots, skin_mats,
          job_results_rich = False):
    # type: (Operator, Context, None, None, False) -> bool
    '''
    Imports .gr2 object files and assigns them
    materials using this add-on's SWTOR shaders
    '''



    for slot in slots:
        print()
        print()
        print(f"{slot['slot_name'].upper()} OBJECTS:")
        print("-" * 80)
        for model in slot["models"]:
            # Import gr2. The .gr2 import module will
            # read parameters from this module's class'
            # properties via the operator param (it
            # carries the class' self.)
            ImportGR2_load(operator, context, model)
            
            name = path_split(model)[:-4]


            # Set material for model
            ob = bpy.data.objects[name]

            for i, mat_slot in enumerate(ob.material_slots):
                derived = slot["mat_info"]["otherValues"]["derived"]
                derived = "Creature" if derived == "HighQualityCharacter" else derived
                derived = ("Eye" if any(x in slot["slot_name"] for x in {"head", "creature"})
                           and i == 1 else derived)
                
                # HORRIBLE HACK FOR CREATURE IMPORTS WHERE THE SECOND MATERIAL
                # ISN'T REALLY AN EYE BUT A HIGHQUALITYCHARACTER/CREATURE ONE:
                # We are using the presence of a malformed paletteMap "/.dds"
                # texturemap filename (necessary in Eye shaders but not in
                # Creature ones) as a criteria to change the Derived to Creature
                # (we used to manually correct those entries in the .json data.
                # Now we must NOT correct it, as its presence helps us here).
                
                creature_2nd_mat_is_creature_instead_of_eye = False
                if i == 1:
                    if slot["slot_name"] == 'creature' and (
                        slot['mat_info']['eyeMatInfo']['ddsPaths']['paletteMap'].endswith("\\.dds") or
                        slot['mat_info']['eyeMatInfo']['ddsPaths']['paletteMap'].endswith("/.dds")
                        ):
                        derived = "Creature"
                        creature_2nd_mat_is_creature_instead_of_eye = True

                
                
                new_mat = None
                mat_idx = '{:0>2}'.format(i + 1) if i + 1 < 10 else str(i + 1)
                slot_name = slot["slot_name"]

                try:
                    if not creature_2nd_mat_is_creature_instead_of_eye:
                        new_mat = bpy.data.materials[f"{mat_idx} {slot_name}{derived}"]
                    else:
                        new_mat = bpy.data.materials[f"{mat_idx} {slot_name}Creature"]
                except KeyError:
                    # This part failed for TORCommunity.com's creature NPC exports because
                    # the last server restore didn't have the correction to include
                    # their materialSkinIndex data:
                    #
                    # So, in its absence, we use the npc_uses_skin parameter (which
                    # defaults to True because it's the most typical case)
                    
                    
                    if "materialSkinIndex" in slot["mat_info"]["otherValues"]:
                        if int(slot["mat_info"]["otherValues"]["materialSkinIndex"]) == i:
                            derived = "SkinB"
                    else:
                        if not creature_2nd_mat_is_creature_instead_of_eye:
                            if i == 1 and (slot_name != "head" and slot_name != 'creature'):
                                if operator.npc_uses_skin:
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

                    if derived == 'Creature' and creature_2nd_mat_is_creature_instead_of_eye is False:
                        
                        node.derived = 'CREATURE'
                        # TODO: Read Alpha parameters from paths.json
                        new_mat.alpha_threshold = node.alpha_test_value = 0.5
                        node.alpha_mode = 'CLIP'
                        if blender_version < 4.2:
                            new_mat.blend_method = 'CLIP'
                            new_mat.show_transparent_back = False
                        else:
                            new_mat.surface_render_method = "DITHERED"
                            new_mat.use_transparency_overlap = False

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

                        if "directionMap" in mat_info["ddsPaths"]:
                            img = path_split(mat_info["ddsPaths"]["directionMap"])
                            if img in imgs:
                                node.directionMap = imgs[img]
                            else:
                                node.directionMap = imgs.load(mat_info["ddsPaths"]["directionMap"])

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
                        
                    elif derived == 'Creature' and creature_2nd_mat_is_creature_instead_of_eye is True:
                        # It feeds a 'Creature' shader but the data it grabs comes from the parsed
                        # paths.json file's 'eye' shader data. I rather don't try to generalize that
                        # into a single chunk of code.
                        
                        node.derived = 'CREATURE'
                        # TODO: Read Alpha parameters from paths.json
                        new_mat.alpha_threshold = node.alpha_test_value = 0.5
                        node.alpha_mode = 'CLIP'
                        if blender_version < 4.2:
                            new_mat.blend_method = 'CLIP'
                            new_mat.show_transparent_back = False
                        else:
                            new_mat.surface_render_method = "DITHERED"
                            new_mat.use_transparency_overlap = False

                        mat_info = slot["mat_info"]
                        other_values = mat_info['eyeMatInfo']['otherValues']

                        img = path_split(mat_info['eyeMatInfo']["ddsPaths"]["diffuseMap"])
                        if img in imgs:
                            node.diffuseMap = imgs[img]
                        else:
                            node.diffuseMap = imgs.load(mat_info['eyeMatInfo']["ddsPaths"]["diffuseMap"])

                        img = path_split(mat_info['eyeMatInfo']["ddsPaths"]["rotationMap"])
                        if img in imgs:
                            node.rotationMap = imgs[img]
                        else:
                            node.rotationMap = imgs.load(mat_info['eyeMatInfo']["ddsPaths"]["rotationMap"])

                        img = path_split(mat_info['eyeMatInfo']["ddsPaths"]["glossMap"])
                        if img in imgs:
                            node.glossMap = imgs[img]
                        else:
                            node.glossMap = imgs.load(mat_info["ddsPaths"]["glossMap"])

                        img = path_split(mat_info['eyeMatInfo']["ddsPaths"]["paletteMaskMap"])
                        if img in imgs:
                            node.paletteMaskMap = imgs[img]
                        else:
                            node.paletteMaskMap = imgs.load(mat_info['eyeMatInfo']["ddsPaths"]["paletteMaskMap"])

                        if "directionMap" in mat_info['eyeMatInfo']["ddsPaths"]:
                            img = path_split(mat_info['eyeMatInfo']["ddsPaths"]["directionMap"])
                            if img in imgs:
                                node.directionMap = imgs[img]
                            else:
                                node.directionMap = imgs.load(mat_info['eyeMatInfo']["ddsPaths"]["directionMap"])

                        # try:
                        #     node.directionMap = imgs[path_split(mat_info['eyeMatInfo']["ddsPaths"]['directionMap'])]
                        # except KeyError:
                        #     node.directionMap = imgs.load(mat_info['eyeMatInfo']["ddsPaths"]['directionMap'])

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
                        new_mat.show_transparent_back = False
                        node.alpha_mode = 'CLIP'
                        if blender_version < 4.2:
                            new_mat.blend_method = 'CLIP'
                        else:
                            new_mat.surface_render_method = "DITHERED"


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
                        new_mat.show_transparent_back = False
                        node.alpha_mode = 'CLIP'
                        if blender_version < 4.2:
                            new_mat.blend_method = 'CLIP'
                        else:
                            new_mat.surface_render_method = "DITHERED"

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
                        new_mat.show_transparent_back = False
                        node.alpha_mode = 'CLIP'
                        if blender_version < 4.2:
                            new_mat.blend_method = 'CLIP'
                        else:
                            new_mat.surface_render_method = "DITHERED"

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

                        img = path_split(mat_info["ddsPaths"]["directionMap"])
                        if img in imgs:
                            node.directionMap = imgs[img]
                        else:
                            node.directionMap = imgs.load(mat_info["ddsPaths"]["directionMap"])

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
                        new_mat.show_transparent_back = False
                        node.alpha_mode = 'CLIP'
                        if blender_version < 4.2:
                            new_mat.blend_method = 'CLIP'
                        else:
                            new_mat.surface_render_method = "DITHERED"

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
                        new_mat.show_transparent_back = False
                        node.alpha_mode = 'CLIP'
                        if blender_version < 4.2:
                            new_mat.blend_method = 'CLIP'
                        else:
                            new_mat.surface_render_method = "DITHERED"

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
    
    start_time = time.time()
    
    print( "----------")
    print(f"JSON FILE: {filepath}")
    print( "----------")

    slots, skin_mats = read(operator, filepath)

    if slots:

        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        if build(operator, context, slots, skin_mats):

            elapsed_time = time.time() - start_time
            print()
            print()
            print( "----------------------")
            print(f"TOTAL PROCESSING TIME: {elapsed_time:.3f} s.")
            print( "----------------------")

            return True

        return False
