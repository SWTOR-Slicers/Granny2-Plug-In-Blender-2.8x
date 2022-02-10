# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic models into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired GR2 model file.
"""

import bpy
import json
import os

from bpy_extras.wm_utils.progress_report import ProgressReport

from .import_gr2 import load as loadGR2

eyeMatInfo = None


class slot_obj():
    def __init__(self, dict_from_json, json_path):
        self.slot_name = dict_from_json['slotName']
        models = dict_from_json['models']
        self.models = []

        for m in models:

            if os.name == 'nt':
                path = json_path[:json_path.rfind('\\')]
            else:
                path = json_path[:json_path.rfind('/')]

            self.models.append(f"{path}/models/{self.slot_name}{m[m.rfind('/'):]}")

        self.mat_info = dict_from_json['materialInfo']
        dds_dict = dict_from_json['materialInfo']['ddsPaths']

        for key in self.mat_info['ddsPaths']:
            value = f"{path}/materials/{self.slot_name}{dds_dict[key][dds_dict[key].rfind('/'):]}"
            self.mat_info['ddsPaths'][key] = value

    def __repr__(self):
        return (
            "{\n"
            + f"slotName: {self.slot_name}\n"
            + f"models: {', '.join(self.models)}\n"
            + f"matInfo: {json.dumps(self.mat_info, indent=4)}\n"
            + "}"
        )


class slot_obj_mat_only():
    def __init__(self, dict_from_json, json_path):
        self.slot_name = 'eye'
        self.mat_info = dict_from_json
        dds_dict = dict_from_json['ddsPaths']

        if os.name == 'nt':
            path = json_path[:json_path.rfind('\\')]
        else:
            path = json_path[:json_path.rfind('/')]

        for key in self.mat_info['ddsPaths']:
            value = f"{path}/materials/{self.slot_name}{dds_dict[key][dds_dict[key].rfind('/'):]}"
            self.mat_info['ddsPaths'][key] = value

    def __repr__(self):
        return "{\n" + f"matInfo: {json.dumps(self.mat_info, indent=4)}\n" + "}"


class skin_mats_obj():
    def __init__(self, dict_from_json, json_path):
        self.slot_name = dict_from_json['slotName']
        self.mat_info = dict_from_json['materialInfo']
        self.mat_info['ddsPaths'] = dict_from_json['ddsPaths']
        self.mat_info['otherValues'] = dict_from_json['otherValues']
        dds_dict = dict_from_json['ddsPaths']

        if os.name == 'nt':
            path = json_path[:json_path.rfind('\\')]
        else:
            path = json_path[:json_path.rfind('/')]

        for key in self.mat_info['ddsPaths']:
            value = f"{path}/materials/skinMats/{self.slot_name}{dds_dict[key][dds_dict[key].rfind('/'):]}"
            self.mat_info['ddsPaths'][key] = value

    def __repr__(self):
        return "{\n" + f"slotName: {self.slot_name}\n" + "}"


class skin_mats_list_obj():
    def __init__(self):
        self.slot_name = 'skinMats'
        self.mats = []

    def __repr__(self):
        return "{\n" + f"slotName: {self.slot_name}\n" + f"mats: {', '.join(self.mats)}\n" + "}"


class ToonLoader():
    def __init__(self, filepath):
        self.filepath = filepath

    def read_paths(self, paths_json_path):
        with open(paths_json_path) as json_file:
            data = json.load(json_file)

        return data

    def parse(self, operator):
        data = self.read_paths(self.filepath)
        parsed_objs = []
        skin_mats = None
        global eyeMatInfo
        for entry in data:
            if entry['slotName'] == 'skinMats':
                to_push = skin_mats_list_obj()

                for mat in entry['materialInfo']['mats']:
                    to_push.mats.append(skin_mats_obj(mat, self.filepath))

                skin_mats = to_push
            else:
                try:
                    s = slot_obj(entry, self.filepath)

                    if any(x in s.slot_name for x in ['head', 'creature']):
                        eyeMatInfo = slot_obj_mat_only(entry['materialInfo']['eyeMatInfo'], self.filepath)

                    parsed_objs.append(s)

                except Exception:
                    print("AN ERROR HAS OCCURED!")

        self.slots = parsed_objs
        self.skin_mats = skin_mats

    def build(self, operator, context):
        for slot in self.slots:
            for model in slot.models:
                # Import gr2
                loadGR2(operator, context, model)
                name = model[model.rfind("/") + 1: -4]

                # Set material for model
                blender_obj = bpy.data.objects[name]

                for i, mat_slot in enumerate(blender_obj.material_slots):
                    derived = slot.mat_info['otherValues']['derived']
                    derived = 'Eye' if any(x in slot.slot_name for x in ['head', 'creature']) and i == 1 else derived
                    derived = 'Creature' if derived == 'HighQualityCharacter' else derived
                    new_mat = None
                    mat_idx = '{:0>2}'.format(i + 1) if i + 1 < 10 else str(i + 1)

                    try:
                        new_mat = bpy.data.materials[f'{mat_idx} {slot.slot_name}{derived}']
                    except KeyError:
                        new_mat = bpy.data.materials.new(f'{mat_idx} {slot.slot_name}{derived}')
                        new_mat.use_nodes = True
                        new_mat.node_tree.nodes.remove(new_mat.node_tree.nodes['Principled BSDF'])
                        new_mat.node_tree.nodes.new(type='ShaderNodeHeroEngine')
                        new_mat.node_tree.nodes['SWTOR'].location = (0.0, 300.0)
                        new_mat.node_tree.links.new(
                            new_mat.node_tree.nodes['SWTOR'].outputs['Shader'],
                            new_mat.node_tree.nodes['Material Output'].inputs['Surface'])

                        imgs = bpy.data.images
                        node = new_mat.node_tree.nodes['SWTOR']

                        if derived == 'SkinB':
                            node.derived = 'SKINB'
                            # TODO: Read Alpha parameters from paths.json
                            node.alpha_mode = 'CLIP'
                            node.alpha_test_value = 0.5

                            skin_mat = next(
                                (mat for mat in self.skin_mats.mats if mat.slot_name == slot.slot_name),
                                None)
                            vals_info = skin_mat.mat_info if skin_mat is not None else slot.mat_info
                            vals = vals_info['otherValues']

                            try:
                                node.diffuseMap = imgs[vals_info['ddsPaths']['diffuseMap'].split('/')[-1]]
                            except KeyError:
                                node.diffuseMap = imgs.load(vals_info['ddsPaths']['diffuseMap'])

                            try:
                                node.rotationMap = imgs[vals_info['ddsPaths']['rotationMap'].split('/')[-1]]
                            except KeyError:
                                node.rotationMap = imgs.load(vals_info['ddsPaths']['rotationMap'])

                            try:
                                node.glossMap = imgs[vals_info['ddsPaths']['glossMap'].split('/')[-1]]
                            except KeyError:
                                node.glossMap = imgs.load(vals_info['ddsPaths']['glossMap'])

                            try:
                                node.paletteMap = imgs[vals_info['ddsPaths']['paletteMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMap = imgs.load(vals_info['ddsPaths']['paletteMap'])

                            try:
                                node.paletteMaskMap = imgs[vals_info['ddsPaths']['paletteMaskMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMaskMap = imgs.load(vals_info['ddsPaths']['paletteMaskMap'])

                            if 'ageMap' in vals_info['ddsPaths']:
                                try:
                                    node.ageMap = imgs[vals_info['ddsPaths']['ageMap'].split('/')[-1]]
                                except KeyError:
                                    node.ageMap = imgs.load(vals_info['ddsPaths']['ageMap'])

                            if 'complexionMap' in vals_info['ddsPaths']:
                                try:
                                    node.complexionMap = imgs[vals_info['ddsPaths']['complexionMap'].split('/')[-1]]
                                except KeyError:
                                    node.complexionMap = imgs.load(vals_info['ddsPaths']['complexionMap'])

                            if 'facepaintMap' in vals_info['ddsPaths']:
                                try:
                                    node.facepaintMap = imgs[vals_info['ddsPaths']['facepaintMap'].split('/')[-1]]
                                except KeyError:
                                    node.facepaintMap = imgs.load(vals_info['ddsPaths']['facepaintMap'])

                            node.palette1_hue = float(vals['palette1'][0])
                            node.palette1_saturation = float(vals['palette1'][1])
                            node.palette1_brightness = float(vals['palette1'][2])
                            node.palette1_contrast = float(vals['palette1'][3])
                            node.palette1_specular = [
                                float(vals['palette1Specular'][0]),
                                float(vals['palette1Specular'][1]),
                                float(vals['palette1Specular'][2]),
                                1.0]
                            node.palette1_metallic_specular = [
                                float(vals['palette1MetallicSpecular'][0]),
                                float(vals['palette1MetallicSpecular'][1]),
                                float(vals['palette1MetallicSpecular'][2]),
                                1.0]

                            node.flesh_brightness = float(vals['fleshBrightness'])
                            node.flush_tone = [
                                float(vals['flush'][0]),
                                float(vals['flush'][1]),
                                float(vals['flush'][2]),
                                1.0]
                        elif derived == 'HairC':
                            node.derived = 'HAIRC'
                            # TODO: Read Alpha parameters from paths.json
                            node.alpha_mode = 'CLIP'
                            node.alpha_test_value = 0.5

                            vals_info = slot.mat_info
                            vals = vals_info['otherValues']

                            try:
                                node.diffuseMap = imgs[vals_info['ddsPaths']['diffuseMap'].split('/')[-1]]
                            except KeyError:
                                node.diffuseMap = imgs.load(vals_info['ddsPaths']['diffuseMap'])

                            try:
                                node.rotationMap = imgs[vals_info['ddsPaths']['rotationMap'].split('/')[-1]]
                            except KeyError:
                                node.rotationMap = imgs.load(vals_info['ddsPaths']['rotationMap'])

                            try:
                                node.glossMap = imgs[vals_info['ddsPaths']['glossMap'].split('/')[-1]]
                            except KeyError:
                                node.glossMap = imgs.load(vals_info['ddsPaths']['glossMap'])

                            try:
                                node.paletteMap = imgs[vals_info['ddsPaths']['paletteMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMap = imgs.load(vals_info['ddsPaths']['paletteMap'])

                            try:
                                node.paletteMaskMap = imgs[vals_info['ddsPaths']['paletteMaskMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMaskMap = imgs.load(vals_info['ddsPaths']['paletteMaskMap'])

                            # try:
                            #     node.directionMap = imgs[vals_info['ddsPaths']['directionMap'].split('/')[-1]]
                            # except KeyError:
                            #     node.directionMap = imgs.load(vals_info['ddsPaths']['directionMap'])

                            node.palette1_hue = float(vals['palette1'][0])
                            node.palette1_saturation = float(vals['palette1'][1])
                            node.palette1_brightness = float(vals['palette1'][2])
                            node.palette1_contrast = float(vals['palette1'][3])
                            node.palette1_specular = [
                                float(vals['palette1Specular'][0]),
                                float(vals['palette1Specular'][1]),
                                float(vals['palette1Specular'][2]),
                                1.0]
                            node.palette1_metallic_specular = [
                                float(vals['palette1MetallicSpecular'][0]),
                                float(vals['palette1MetallicSpecular'][1]),
                                float(vals['palette1MetallicSpecular'][2]),
                                1.0]
                        elif derived == 'Eye':
                            node.derived = 'EYE'
                            # TODO: Read Alpha parameters from paths.json
                            node.alpha_mode = 'CLIP'
                            node.alpha_test_value = 0.5

                            vals_info = eyeMatInfo.mat_info
                            vals = vals_info['otherValues']

                            try:
                                node.diffuseMap = imgs[vals_info['ddsPaths']['diffuseMap'].split('/')[-1]]
                            except KeyError:
                                node.diffuseMap = imgs.load(vals_info['ddsPaths']['diffuseMap'])

                            try:
                                node.rotationMap = imgs[vals_info['ddsPaths']['rotationMap'].split('/')[-1]]
                            except KeyError:
                                node.rotationMap = imgs.load(vals_info['ddsPaths']['rotationMap'])

                            try:
                                node.glossMap = imgs[vals_info['ddsPaths']['glossMap'].split('/')[-1]]
                            except KeyError:
                                node.glossMap = imgs.load(vals_info['ddsPaths']['glossMap'])

                            try:
                                node.paletteMap = imgs[vals_info['ddsPaths']['paletteMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMap = imgs.load(vals_info['ddsPaths']['paletteMap'])

                            try:
                                node.paletteMaskMap = imgs[vals_info['ddsPaths']['paletteMaskMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMaskMap = imgs.load(vals_info['ddsPaths']['paletteMaskMap'])

                            node.palette1_hue = float(vals['palette1'][0])
                            node.palette1_saturation = float(vals['palette1'][1])
                            node.palette1_brightness = float(vals['palette1'][2])
                            node.palette1_contrast = float(vals['palette1'][3])
                            node.palette1_specular = [
                                float(vals['palette1Specular'][0]),
                                float(vals['palette1Specular'][1]),
                                float(vals['palette1Specular'][2]),
                                1.0]
                            node.palette1_metallic_specular = [
                                float(vals['palette1MetallicSpecular'][0]),
                                float(vals['palette1MetallicSpecular'][1]),
                                float(vals['palette1MetallicSpecular'][2]),
                                1.0]
                        elif derived == 'Garment':
                            node.derived = 'GARMENT'
                            # TODO: Read Alpha parameters from paths.json
                            node.alpha_mode = 'CLIP'
                            node.alpha_test_value = 0.5

                            vals_info = slot.mat_info
                            vals = vals_info['otherValues']

                            try:
                                node.diffuseMap = imgs[vals_info['ddsPaths']['diffuseMap'].split('/')[-1]]
                            except KeyError:
                                node.diffuseMap = imgs.load(vals_info['ddsPaths']['diffuseMap'])

                            try:
                                node.rotationMap = imgs[vals_info['ddsPaths']['rotationMap'].split('/')[-1]]
                            except KeyError:
                                node.rotationMap = imgs.load(vals_info['ddsPaths']['rotationMap'])

                            try:
                                node.glossMap = imgs[vals_info['ddsPaths']['glossMap'].split('/')[-1]]
                            except KeyError:
                                node.glossMap = imgs.load(vals_info['ddsPaths']['glossMap'])

                            try:
                                node.paletteMap = imgs[vals_info['ddsPaths']['paletteMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMap = imgs.load(vals_info['ddsPaths']['paletteMap'])

                            try:
                                node.paletteMaskMap = imgs[vals_info['ddsPaths']['paletteMaskMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMaskMap = imgs.load(vals_info['ddsPaths']['paletteMaskMap'])

                            node.palette1_hue = float(vals['palette1'][0])
                            node.palette1_saturation = float(vals['palette1'][1])
                            node.palette1_brightness = float(vals['palette1'][2])
                            node.palette1_contrast = float(vals['palette1'][3])
                            node.palette1_specular = [
                                float(vals['palette1Specular'][0]),
                                float(vals['palette1Specular'][1]),
                                float(vals['palette1Specular'][2]),
                                1.0]
                            node.palette1_metallic_specular = [
                                float(vals['palette1MetallicSpecular'][0]),
                                float(vals['palette1MetallicSpecular'][1]),
                                float(vals['palette1MetallicSpecular'][2]),
                                1.0]

                            node.palette2_hue = float(vals['palette2'][0])
                            node.palette2_saturation = float(vals['palette2'][1])
                            node.palette2_brightness = float(vals['palette2'][2])
                            node.palette2_contrast = float(vals['palette2'][3])
                            node.palette2_specular = [
                                float(vals['palette2Specular'][0]),
                                float(vals['palette2Specular'][1]),
                                float(vals['palette2Specular'][2]),
                                1.0]
                            node.palette2_metallic_specular = [
                                float(vals['palette2MetallicSpecular'][0]),
                                float(vals['palette2MetallicSpecular'][1]),
                                float(vals['palette2MetallicSpecular'][2]),
                                1.0]
                        elif derived == 'Creature':
                            node.derived = 'CREATURE'
                            # TODO: Read Alpha parameters from paths.json
                            node.alpha_mode = 'CLIP'
                            node.alpha_test_value = 0.5

                            vals_info = slot.mat_info
                            vals = vals_info['otherValues']

                            try:
                                node.diffuseMap = imgs[vals_info['ddsPaths']['diffuseMap'].split('/')[-1]]
                            except KeyError:
                                node.diffuseMap = imgs.load(vals_info['ddsPaths']['diffuseMap'])

                            try:
                                node.rotationMap = imgs[vals_info['ddsPaths']['rotationMap'].split('/')[-1]]
                            except KeyError:
                                node.rotationMap = imgs.load(vals_info['ddsPaths']['rotationMap'])

                            try:
                                node.glossMap = imgs[vals_info['ddsPaths']['glossMap'].split('/')[-1]]
                            except KeyError:
                                node.glossMap = imgs.load(vals_info['ddsPaths']['glossMap'])

                            try:
                                node.paletteMaskMap = imgs[vals_info['ddsPaths']['paletteMaskMap'].split('/')[-1]]
                            except KeyError:
                                node.paletteMaskMap = imgs.load(vals_info['ddsPaths']['paletteMaskMap'])

                            # try:
                            #     node.directionMap = imgs[vals_info['ddsPaths']['directionMap'].split('/')[-1]]
                            # except KeyError:
                            #     node.directionMap = imgs.load(vals_info['ddsPaths']['directionMap'])

                            node.flesh_brightness = float(vals['fleshBrightness'])
                            node.flush_tone = [
                                float(vals['flush'][0]),
                                float(vals['flush'][1]),
                                float(vals['flush'][2]),
                                1.0]
                        elif derived == 'Uber':
                            node.derived = 'UBER'
                            # TODO: Read Alpha parameters from paths.json
                            node.alpha_mode = 'CLIP'
                            node.alpha_test_value = 0.5

                            vals_info = slot.mat_info
                            vals = vals_info['otherValues']

                            try:
                                node.diffuseMap = imgs[vals_info['ddsPaths']['diffuseMap'].split('/')[-1]]
                            except KeyError:
                                node.diffuseMap = imgs.load(vals_info['ddsPaths']['diffuseMap'])

                            try:
                                node.rotationMap = imgs[vals_info['ddsPaths']['rotationMap'].split('/')[-1]]
                            except KeyError:
                                node.rotationMap = imgs.load(vals_info['ddsPaths']['rotationMap'])

                            try:
                                node.glossMap = imgs[vals_info['ddsPaths']['glossMap'].split('/')[-1]]
                            except KeyError:
                                node.glossMap = imgs.load(vals_info['ddsPaths']['glossMap'])

                    mat_slot.material = new_mat


def load(operator, context, filepath=""):
    with ProgressReport(context.window_manager) as progress:

        progress.enter_substeps(3, "Importing \'%s\' ..." % filepath)

        mainLoader = ToonLoader(filepath)

        progress.step("Parsing file ...", 1)

        mainLoader.parse(operator)

        progress.step("Done, building ...", 2)

        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        mainLoader.build(operator, context)

        progress.leave_substeps("Done, finished importing: \'%s\'" % filepath)

    return {'FINISHED'}
