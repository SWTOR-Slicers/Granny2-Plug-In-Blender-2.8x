# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic models into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired GR2 model file.
"""

import json

import bpy
from bpy_extras.wm_utils.progress_report import ProgressReport

from .import_gr2 import load as loadGR2

eyeMatInfo = None


class slot_obj():
    def __init__(self, dict_from_json, json_path):
        self.slot_name = dict_from_json['slotName']
        models = dict_from_json['models']
        self.models = []
        for m in models:
            self.models.append(json_path[:json_path.rfind("\\")] + "/models/" + self.slot_name + m[m.rfind("/"):])
        self.mat_info = dict_from_json['materialInfo']
        dds_dict = dict_from_json['materialInfo']['ddsPaths']
        textures = [
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['paletteMap'][dds_dict['paletteMap'].rfind("/"):] if 'paletteMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['paletteMaskMap'][dds_dict['paletteMaskMap'].rfind(
                "/"):] if 'paletteMaskMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['diffuseMap'][dds_dict['diffuseMap'].rfind("/"):] if 'diffuseMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['glossMap'][dds_dict['glossMap'].rfind("/"):] if 'glossMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['rotationMap'][dds_dict['rotationMap'].rfind("/"):] if 'rotationMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['ageMap'][dds_dict['ageMap'].rfind("/"):] if 'ageMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['complexionMap'][dds_dict['complexionMap'].rfind("/"):] if 'complexionMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['facepaintMap'][dds_dict['facepaintMap'].rfind("/"):] if 'facepaintMap' in dds_dict else None
        ]
        i = 0
        for key in self.mat_info['ddsPaths']:
            self.mat_info['ddsPaths'][key] = textures[i]
            i += 1

    def __repr__(self):
        return (
            "{\n"
            + "slotName: "
            + self.slot_name
            + "\n" + "models: "
            + ", ".join(self.models)
            + "\n"
            + "matInfo: "
            + json.dumps(self.mat_info, indent=4)
            + "\n"
            + "}"
        )


class slot_obj_mat_only():
    def __init__(self, dict_from_json, json_path):
        self.slot_name = "eye"
        self.mat_info = dict_from_json
        dds_dict = dict_from_json['ddsPaths']
        textures = [
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['paletteMap'][dds_dict['paletteMap'].rfind("/"):] if 'paletteMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['paletteMaskMap'][dds_dict['paletteMaskMap'].rfind(
                "/"):] if 'paletteMaskMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['diffuseMap'][dds_dict['diffuseMap'].rfind("/"):] if 'diffuseMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['glossMap'][dds_dict['glossMap'].rfind("/"):] if 'glossMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['rotationMap'][dds_dict['rotationMap'].rfind("/"):] if 'rotationMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['ageMap'][dds_dict['ageMap'].rfind("/"):] if 'ageMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['complexionMap'][dds_dict['complexionMap'].rfind("/"):] if 'complexionMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['facepaintMap'][dds_dict['facepaintMap'].rfind("/"):] if 'facepaintMap' in dds_dict else None
        ]
        i = 0
        for key in self.mat_info['ddsPaths']:
            self.mat_info['ddsPaths'][key] = textures[i]
            i += 1

    def __repr__(self):
        return "{\n" + "matInfo: " + json.dumps(self.mat_info, indent=4) + "\n" + "}"


class skin_mats_obj():
    def __init__(self, dict_from_json, json_path):
        self.slot_name = dict_from_json['slotName']
        self.mat_info = dict_from_json['materialInfo']
        self.mat_info["ddsPaths"] = dict_from_json['ddsPaths']
        self.mat_info["otherValues"] = dict_from_json['otherValues']
        dds_dict = dict_from_json['ddsPaths']
        textures = [
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['paletteMap'][dds_dict['paletteMap'].rfind("/"):] if 'paletteMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['paletteMaskMap'][dds_dict['paletteMaskMap'].rfind(
                "/"):] if 'paletteMaskMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['diffuseMap'][dds_dict['diffuseMap'].rfind("/"):] if 'diffuseMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['glossMap'][dds_dict['glossMap'].rfind("/"):] if 'glossMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['rotationMap'][dds_dict['rotationMap'].rfind("/"):] if 'rotationMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['ageMap'][dds_dict['ageMap'].rfind("/"):] if 'ageMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['complexionMap'][dds_dict['complexionMap'].rfind("/"):] if 'complexionMap' in dds_dict else None,
            json_path[:json_path.rfind("\\")] + "/materials/" + self.slot_name +
            dds_dict['facepaintMap'][dds_dict['facepaintMap'].rfind("/"):] if 'facepaintMap' in dds_dict else None
        ]
        i = 0
        for key in self.mat_info['ddsPaths']:
            self.mat_info['ddsPaths'][key] = textures[i]
            i += 1

    def __repr__(self):
        return "{\n" + "slotName: " + self.slot_name + "\n" + "}"


class skin_mats_list_obj():
    def __init__(self):
        self.slot_name = "skinMats"
        self.mats = []

    def __repr__(self):
        return "{\n" + "slotName: " + self.slot_name + "\n" + "mats: " + ", ".join(self.mats) + "\n" + "}"


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
            if entry['slotName'] == "skinMats":
                to_push = skin_mats_list_obj()
                for mat in entry['materialInfo']['mats']:
                    to_push.mats.append(skin_mats_obj(mat, self.filepath))

                skin_mats = to_push

            else:
                try:
                    s = slot_obj(entry, self.filepath)
                    if s.slot_name == "head":
                        eyeMatInfo = slot_obj_mat_only(entry["materialInfo"]["eyeMatInfo"], self.filepath)

                    parsed_objs.append(s)

                except:
                    print(".")

        self.slots = parsed_objs
        self.skin_mats = skin_mats

    def build(self, operator, context):
        for slot in self.slots:
            for model in slot.models:
                # import gr2
                loadGR2(operator, context, model)
                name = model[model.rfind("/") + 1: -4]

                # set material for model
                blender_obj = bpy.data.objects[name]
                i = 0
                for mat_slot in blender_obj.material_slots:
                    derived = slot.mat_info["otherValues"]["derived"]
                    if slot.slot_name == "head" and i == 1:
                        derived = "Eye"

                    new_mat = None
                    try:
                        new_mat = bpy.data.materials[slot.slot_name + derived]
                    except:
                        mat = bpy.data.materials["Template: " + derived + " Shader"]
                        uses_skin = False
                        try:
                            uses_skin = slot.mat_info["otherValues"]["materialSkinIndex"] == i
                        except:
                            uses_skin = False

                        if uses_skin:
                            mat = bpy.data.materials["Template: SkinB Shader"]

                        new_mat = mat.copy()
                        new_mat.name = "Eye Shader" if slot.slot_name == "head" and i == 1 else slot.slot_name + derived

                        if derived == "SkinB":
                            if slot.slot_name != "head":
                                uses_skin = True

                            skin_mat = next(
                                (mat for mat in self.skin_mats.mats if mat.slot_name == slot.slot_name), None)
                            vals_info = skin_mat.mat_info if uses_skin and slot.slot_name != "head" else slot.mat_info
                            vals = vals_info["otherValues"]

                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                "Palette1.X").default_value = float(vals["palette1"][0])
                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                "Palette1.Y").default_value = float(vals["palette1"][1])
                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                "Palette1.Z").default_value = float(vals["palette1"][2])
                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                "Palette1.W").default_value = float(vals["palette1"][3])

                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get("Palette1 Specular").default_value = (
                                float(vals["palette1Specular"][0]), float(vals["palette1Specular"][1]), float(vals["palette1Specular"][2]), 1)
                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get("Palette1 Metallic Specular").default_value = (float(
                                vals["palette1MetallicSpecular"][0]), float(vals["palette1MetallicSpecular"][1]), float(vals["palette1MetallicSpecular"][2]), 1)

                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                "FlushTone.X").default_value = float(vals["flush"][0])
                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                "FlushTone.Y").default_value = float(vals["flush"][1])
                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                "FlushTone.Z").default_value = float(vals["flush"][2])

                            new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                "FleshBrightness").default_value = float(vals["fleshBrightness"])

                            i1 = bpy.data.images.load(vals_info["ddsPaths"]["diffuseMap"])
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image = i1
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image.colorspace_settings.name = 'Raw'

                            i2 = bpy.data.images.load(vals_info["ddsPaths"]["rotationMap"])
                            new_mat.node_tree.nodes.get("_n RotationMap").image = i2
                            new_mat.node_tree.nodes.get("_n RotationMap").image.colorspace_settings.name = 'Raw'

                            i3 = bpy.data.images.load(vals_info["ddsPaths"]["glossMap"])
                            new_mat.node_tree.nodes.get("_s GlossMap").image = i3
                            new_mat.node_tree.nodes.get("_s GlossMap").image.colorspace_settings.name = 'Raw'

                            i4 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMap"])
                            new_mat.node_tree.nodes.get("_h PaletteMap").image = i4
                            new_mat.node_tree.nodes.get("_h PaletteMap").image.colorspace_settings.name = 'Raw'

                            i5 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMaskMap"])
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image = i5
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image.colorspace_settings.name = 'Raw'

                            if uses_skin:
                                l1 = new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                    "ComplexionMap Color").links[0]
                                new_mat.node_tree.links.remove(l1)
                                new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                    "ComplexionMap Color").default_value = (1, 1, 1, 1)

                                l2 = new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                    "FacepaintMap Color").links[0]
                                new_mat.node_tree.links.remove(l2)
                                new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                    "FacepaintMap Color").default_value = (1, 1, 1, 1)

                                l3 = new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                    "FacepaintMap Alpha").links[0]
                                new_mat.node_tree.links.remove(l3)
                                new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                    "FacepaintMap Alpha").default_value = 0.0
                            else:
                                try:
                                    i6 = bpy.data.images.load(vals_info["ddsPaths"]["complexionMap"])
                                    new_mat.node_tree.nodes.get("ComplexionMap").image = i6
                                    new_mat.node_tree.nodes.get("ComplexionMap").image.colorspace_settings.name = 'Raw'

                                except:
                                    l1 = new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                        "ComplexionMap Color").links[0]
                                    new_mat.node_tree.links.remove(l1)
                                    new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                        "ComplexionMap Color").default_value = (1, 1, 1, 1)

                                try:
                                    i7 = bpy.data.images.load(vals_info["ddsPaths"]["facepaintMap"])
                                    new_mat.node_tree.nodes.get("FacepaintMap").image = i7
                                    new_mat.node_tree.nodes.get("FacepaintMap").image.colorspace_settings.name = 'Raw'

                                except:
                                    l2 = new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                        "FacepaintMap Color").links[0]
                                    new_mat.node_tree.links.remove(l2)
                                    new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                        "FacepaintMap Color").default_value = (1, 1, 1, 1)

                                    l3 = new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                        "FacepaintMap Alpha").links[0]
                                    new_mat.node_tree.links.remove(l3)
                                    new_mat.node_tree.nodes.get("SkinB Shader").inputs.get(
                                        "FacepaintMap Alpha").default_value = 0.0

                        elif derived == "HairC":
                            vals_info = slot.mat_info
                            vals = vals_info["otherValues"]

                            new_mat.node_tree.nodes.get("HairC Shader").inputs.get(
                                "Palette1.X").default_value = float(vals["palette1"][0])
                            new_mat.node_tree.nodes.get("HairC Shader").inputs.get(
                                "Palette1.Y").default_value = float(vals["palette1"][1])
                            new_mat.node_tree.nodes.get("HairC Shader").inputs.get(
                                "Palette1.Z").default_value = float(vals["palette1"][2])
                            new_mat.node_tree.nodes.get("HairC Shader").inputs.get(
                                "Palette1.W").default_value = float(vals["palette1"][3])

                            new_mat.node_tree.nodes.get("HairC Shader").inputs.get("Palette1 Specular") \
                                .default_value = (
                                    float(vals["palette1Specular"][0]),
                                    float(vals["palette1Specular"][1]),
                                    float(vals["palette1Specular"][2]),
                                    1)
                            new_mat.node_tree.nodes.get("HairC Shader").inputs.get("Palette1 Metallic Specular") \
                                .default_value = (
                                    float(vals["palette1MetallicSpecular"][0]),
                                    float(vals["palette1MetallicSpecular"][1]),
                                    float(vals["palette1MetallicSpecular"][2]),
                                    1)

                            i1 = bpy.data.images.load(vals_info["ddsPaths"]["diffuseMap"])
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image = i1
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image.colorspace_settings.name = 'Raw'

                            i2 = bpy.data.images.load(vals_info["ddsPaths"]["rotationMap"])
                            new_mat.node_tree.nodes.get("_n RotationMap").image = i2
                            new_mat.node_tree.nodes.get("_n RotationMap").image.colorspace_settings.name = 'Raw'

                            i3 = bpy.data.images.load(vals_info["ddsPaths"]["glossMap"])
                            new_mat.node_tree.nodes.get("_s GlossMap").image = i3
                            new_mat.node_tree.nodes.get("_s GlossMap").image.colorspace_settings.name = 'Raw'

                            i4 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMap"])
                            new_mat.node_tree.nodes.get("_h PaletteMap").image = i4
                            new_mat.node_tree.nodes.get("_h PaletteMap").image.colorspace_settings.name = 'Raw'

                            i5 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMaskMap"])
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image = i5
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image.colorspace_settings.name = 'Raw'

                        elif derived == "Eye":
                            vals_info = eyeMatInfo.mat_info
                            vals = vals_info["otherValues"]

                            new_mat.node_tree.nodes.get("Eye Shader").inputs.get(
                                "Palette1.X").default_value = float(vals["palette1"][0])
                            new_mat.node_tree.nodes.get("Eye Shader").inputs.get(
                                "Palette1.Y").default_value = float(vals["palette1"][1])
                            new_mat.node_tree.nodes.get("Eye Shader").inputs.get(
                                "Palette1.Z").default_value = float(vals["palette1"][2])
                            new_mat.node_tree.nodes.get("Eye Shader").inputs.get(
                                "Palette1.W").default_value = float(vals["palette1"][3])

                            new_mat.node_tree.nodes.get("Eye Shader").inputs.get("Palette1 Specular") \
                                .default_value = (
                                    float(vals["palette1Specular"][0]),
                                    float(vals["palette1Specular"][1]),
                                    float(vals["palette1Specular"][2]),
                                    1)
                            new_mat.node_tree.nodes.get("Eye Shader").inputs.get("Palette1 Metallic Specular") \
                                .default_value = (
                                    float(vals["palette1MetallicSpecular"][0]),
                                    float(vals["palette1MetallicSpecular"][1]),
                                    float(vals["palette1MetallicSpecular"][2]),
                                    1)

                            i1 = bpy.data.images.load(vals_info["ddsPaths"]["diffuseMap"])
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image = i1
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image.colorspace_settings.name = 'Raw'

                            i2 = bpy.data.images.load(vals_info["ddsPaths"]["rotationMap"])
                            new_mat.node_tree.nodes.get("_n RotationMap").image = i2
                            new_mat.node_tree.nodes.get("_n RotationMap").image.colorspace_settings.name = 'Raw'

                            i3 = bpy.data.images.load(vals_info["ddsPaths"]["glossMap"])
                            new_mat.node_tree.nodes.get("_s GlossMap").image = i3
                            new_mat.node_tree.nodes.get("_s GlossMap").image.colorspace_settings.name = 'Raw'

                            i4 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMap"])
                            new_mat.node_tree.nodes.get("_h PaletteMap").image = i4
                            new_mat.node_tree.nodes.get("_h PaletteMap").image.colorspace_settings.name = 'Raw'

                            i5 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMaskMap"])
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image = i5
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image.colorspace_settings.name = 'Raw'

                        elif derived == "Garment":
                            vals_info = slot.mat_info
                            vals = vals_info["otherValues"]

                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get(
                                "Palette1.X").default_value = float(vals["palette1"][0])
                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get(
                                "Palette1.Y").default_value = float(vals["palette1"][1])
                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get(
                                "Palette1.Z").default_value = float(vals["palette1"][2])
                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get(
                                "Palette1.W").default_value = float(vals["palette1"][3])

                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get("Palette1 Specular") \
                                .default_value = (
                                    float(vals["palette1Specular"][0]),
                                    float(vals["palette1Specular"][1]),
                                    float(vals["palette1Specular"][2]),
                                    1)
                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get("Palette1 Metallic Specular") \
                                .default_value = (
                                    float(vals["palette1MetallicSpecular"][0]),
                                    float(vals["palette1MetallicSpecular"][1]),
                                    float(vals["palette1MetallicSpecular"][2]),
                                    1)

                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get(
                                "Palette2.X").default_value = float(vals["palette2"][0])
                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get(
                                "Palette2.Y").default_value = float(vals["palette2"][1])
                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get(
                                "Palette2.Z").default_value = float(vals["palette2"][2])
                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get(
                                "Palette2.W").default_value = float(vals["palette2"][3])

                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get("Palette2 Specular") \
                                .default_value = (
                                    float(vals["palette2Specular"][0]),
                                    float(vals["palette2Specular"][1]),
                                    float(vals["palette2Specular"][2]),
                                    1)
                            new_mat.node_tree.nodes.get("Garment Shader").inputs.get("Palette2 Metallic Specular") \
                                .default_value = (
                                    float(vals["palette2MetallicSpecular"][0]),
                                    float(vals["palette2MetallicSpecular"][1]),
                                    float(vals["palette2MetallicSpecular"][2]),
                                    1)

                            i1 = bpy.data.images.load(vals_info["ddsPaths"]["diffuseMap"])
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image = i1
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image.colorspace_settings.name = 'Raw'

                            i2 = bpy.data.images.load(vals_info["ddsPaths"]["rotationMap"])
                            new_mat.node_tree.nodes.get("_n RotationMap").image = i2
                            new_mat.node_tree.nodes.get("_n RotationMap").image.colorspace_settings.name = 'Raw'

                            i3 = bpy.data.images.load(vals_info["ddsPaths"]["glossMap"])
                            new_mat.node_tree.nodes.get("_s GlossMap").image = i3
                            new_mat.node_tree.nodes.get("_s GlossMap").image.colorspace_settings.name = 'Raw'

                            i4 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMap"])
                            new_mat.node_tree.nodes.get("_h PaletteMap").image = i4
                            new_mat.node_tree.nodes.get("_h PaletteMap").image.colorspace_settings.name = 'Raw'

                            i5 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMaskMap"])
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image = i5
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image.colorspace_settings.name = 'Raw'

                        elif derived == "Creature" or derived == "HighQualityCharacter":
                            vals_info = slot.mat_info
                            vals = vals_info["otherValues"]

                            i1 = bpy.data.images.load(vals_info["ddsPaths"]["diffuseMap"])
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image = i1
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image.colorspace_settings.name = 'Raw'

                            i2 = bpy.data.images.load(vals_info["ddsPaths"]["rotationMap"])
                            new_mat.node_tree.nodes.get("_n RotationMap").image = i2
                            new_mat.node_tree.nodes.get("_n RotationMap").image.colorspace_settings.name = 'Raw'

                            i3 = bpy.data.images.load(vals_info["ddsPaths"]["glossMap"])
                            new_mat.node_tree.nodes.get("_s GlossMap").image = i3
                            new_mat.node_tree.nodes.get("_s GlossMap").image.colorspace_settings.name = 'Raw'

                            i4 = bpy.data.images.load(vals_info["ddsPaths"]["paletteMaskMap"])
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image = i4
                            new_mat.node_tree.nodes.get("_m PaletteMaskMap").image.colorspace_settings.name = 'Raw'

                        elif derived == "Uber":
                            vals_info = slot.mat_info
                            vals = vals_info["otherValues"]

                            i1 = bpy.data.images.load(vals_info["ddsPaths"]["diffuseMap"])
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image = i1
                            new_mat.node_tree.nodes.get("_d DiffuseMap").image.colorspace_settings.name = 'Raw'

                            i2 = bpy.data.images.load(vals_info["ddsPaths"]["rotationMap"])
                            new_mat.node_tree.nodes.get("_n RotationMap").image = i2
                            new_mat.node_tree.nodes.get("_n RotationMap").image.colorspace_settings.name = 'Raw'

                            i3 = bpy.data.images.load(vals_info["ddsPaths"]["glossMap"])
                            new_mat.node_tree.nodes.get("_s GlossMap").image = i3
                            new_mat.node_tree.nodes.get("_s GlossMap").image.colorspace_settings.name = 'Raw'

                    mat_slot.material = new_mat

                    i += 1


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
