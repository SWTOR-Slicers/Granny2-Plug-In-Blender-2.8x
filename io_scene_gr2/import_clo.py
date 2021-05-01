# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic cloth simulation file into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired CLO animation file.

https://github.com/SWTOR-Slicers/WikiPedia/wiki/CLO-File-Structure
"""

import os
import math

import bpy
from bpy_extras.wm_utils.progress_report import ProgressReport

from .parse import *


class CLOBone():
    def __init__(self):
        self.name = ""
        self.index = 0
        self.parent_index = -1
        self.constraints1 = []
        self.constraints2 = []
        self.constraints3 = []
        self.unk1 = []
        self.unk2 = []
        self.is_cloth = False

    def __str__(self):
        return str(vars(self))


class CLOCloth():
    def __init__(self, num_bones_total):
        self.num_bones_total = num_bones_total
        self.bones = [None]*num_bones_total
        for i in range(num_bones_total):
            self.bones[i] = CLOBone()


class CLOLoader():
    def __init__(self, filepath):
        self.filepath = filepath
        self.off_data = 0
        self.cloth = None
        self.num_cloth_bones = 0
        self.off_bone_data1 = 0

    def parse(self, operator):
        with open(self.filepath, "rb") as f:
            # Cancel import if this is a non Bio-Ware Austin / SWTOR CLO file
            if f.read(4) != b'OLCB':
                operator.report({'ERROR'}, ("\'%s\' is not a valid SWTOR clo file.") % self.filepath)
                raise RuntimeError()

            self._read_file_header(f)
            self._read_data_header(f)
            self._read_bone_names(f)
            self._read_bone_data1(f)
            self._read_bone_data2(f)
            self._read_bone_data3(f)
            self._read_bone_data4(f)

    def _read_file_header(self, file):
        unk1 = ruint32(file)
        assert(unk1 == 1)
        self.off_data = ruint32(file)
        assert(self.off_data == 0x10)
        data_size = ruint32(file)

    def _read_data_header(self, file):
        unk1 = ruint32(file)
        assert(unk1 == 0)
        unk2 = round(rfloat32(file))
        unk3 = [round(rfloat32(file)) for i in range(3)]
        assert(unk3.count(0.0) == 3)
        unk4 = round(rfloat32(file))
        unk5 = [round(rfloat32(file), 6) for i in range(4)]
        assert(unk5.count(-1.0) == 4)
        num_bones_total = ruint32(file)
        off_bone_names = ruint32(file)
        self.num_cloth_bones = ruint32(file)
        self.off_bone_data1 = ruint32(file)
        num_cloth_bones2 = ruint32(file)
        assert(num_cloth_bones2 == self.num_cloth_bones)
        off_bone_data2 = ruint32(file)
        unk6 = [ruint32(file) for i in range(3)]
        num_bone_data3 = ruint32(file)
        off_bone_data3 = ruint32(file)
        unk7 = [ruint32(file) for i in range(4)]
        num_bone_data4 = ruint32(file)
        off_bone_data4 = ruint32(file)
        unk8 = ruint32(file)

        self.cloth = CLOCloth(num_bones_total)

    def _read_bone_names(self, file):
        file.seek((file.tell() + 0x7f) & -0x80)
        names = [file.read(32).decode().split('\0')[0] for i in range(self.cloth.num_bones_total)]
        for bone, name in zip(self.cloth.bones, names):
            bone.name = name

    def _read_bone_data1(self, file):
        file.seek(self.off_data + self.off_bone_data1)
        for i in range(self.num_cloth_bones):
            constraints1 = [round(rfloat32(file), 6) for i in range(4)]
            constraints2 = [round(rfloat32(file), 6) for i in range(6)]
            constraints3 = [round(rfloat32(file), 6) for i in range(6)]
            unk1 = [round(rfloat32(file), 6) for i in range(4)]
            unk2 = [rint32(file) for i in range(2)]
            bone_index = ruint32(file)
            parent_index = rint32(file)
            bone = self.cloth.bones[bone_index]
            bone.index = bone_index
            bone.parent_index = parent_index
            bone.constraints1 = constraints1
            bone.constraints2 = constraints2
            bone.constraints3 = constraints3
            bone.unk1 = unk1
            bone.unk2 = unk2
            bone.is_cloth = True

    def _read_bone_data2(self, file):
        pass

    def _read_bone_data3(self, file):
        pass

    def _read_bone_data4(self, file):
        pass

    def build(self, operator):
        obj = bpy.context.active_object
        if not bpy.context.active_object or bpy.context.active_object.type != 'MESH':
            operator.report({'INFO'}, "Object of type Mesh must be active")
            return

        # Enter Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        pin_group = None

        # Select vertex groups by cloth bone names
        bpy.ops.mesh.select_all(action='DESELECT')
        for bone in self.cloth.bones:
            if (not bone.is_cloth) or (not bone.name in obj.vertex_groups):
                continue
            bpy.ops.object.vertex_group_set_active(group=bone.name)
            bpy.ops.object.vertex_group_select()
            if pin_group is None:
                pin_group = bone.name

        # Separate selected vertices into another object
        bpy.ops.mesh.separate()
        if len(bpy.context.selected_objects) > 1:
            cloth_obj = bpy.context.selected_objects[1]
            cloth_obj.name = obj.name + "_Cloth"
            cloth_obj.parent = obj
            cloth_obj.matrix_parent_inverse = obj.matrix_world.inverted()
            modifier = cloth_obj.modifiers.new("Cloth", 'CLOTH')
            if pin_group:
                modifier.settings.vertex_group_mass = pin_group

        # Enter Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')


def load(operator, context, filepath=""):
    with ProgressReport(context.window_manager) as progress:
        try:
            progress.enter_substeps(3, "Importing \'%s\' ..." % filepath)
            mainLoader = CLOLoader(filepath)

            progress.step("Parsing file ...", 1)
            mainLoader.parse(operator)

            progress.step("Done, building ...", 2)
            mainLoader.build(operator)

            progress.leave_substeps("Done, finished importing: \'%s\'" % filepath)
        except RuntimeError:
            return {'CANCELED'}

    return {'FINISHED'}
