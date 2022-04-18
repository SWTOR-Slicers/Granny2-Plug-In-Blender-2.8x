# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic cloth simulation file into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired CLO animation file.

https://github.com/SWTOR-Slicers/WikiPedia/wiki/CLO-File-Structure
"""

from typing import Union

from bpy.types import Context, Object, Operator

from ..types.clo import Cloth
from ..utils.binary import DataView


def read(operator, filepath):
    # type: (Operator, str) -> Union[Cloth, None]
    with open(filepath, 'rb') as file:
        dv = DataView(file)
        pos = 0

        if dv.getUint32(pos, True) != 0x42434C4F:  # b'OLCB'
            operator.report({'ERROR'}, f"\'{filepath}\' is not a valid SWTOR clo file.")
            return None

        pos += 4

        # NOTE: Read file header.
        unk1 = dv.getUint32(pos, True)
        pos += 4

        assert(unk1 == 1)

        offset_data = dv.getUint32(pos, True)
        pos += 4

        assert(offset_data == 16)  # 0x10

        # data_size = dv.getUint32(pos, True)
        pos += 4

        # NOTE: Read data header.
        unk1 = dv.getUint32(pos, True)
        pos += 4

        assert(unk1 == 0)

        # unk2 = round(dv.getFloat32(pos, True))
        pos += 4
        unk3 = [round(dv.getFloat32(pos + (i * 4), True)) for i in range(3)]
        pos += 12

        assert(unk3.count(0) == 3)

        # unk4 = round(dv.getFloat32(pos, True))
        pos += 4
        unk5 = [round(dv.getFloat32(pos + (i * 4), True), 6) for i in range(4)]
        pos += 16

        assert (unk5.count(-1) == 4)

        num_bones_total = dv.getUint32(pos, True)
        pos += 4
        # offset_bone_names = dv.getUint32(pos, True)
        pos += 4
        num_cloth_bones1 = dv.getUint32(pos, True)
        pos += 4
        offset_bone_data1 = dv.getUint32(pos, True)
        pos += 4
        num_cloth_bones2 = dv.getUint32(pos, True)
        pos += 4

        assert(num_cloth_bones2 == num_cloth_bones1)

        # offset_bone_data2 = dv.getUint32(pos, True);
        pos += 4
        # unk6 = [dv.getUint32(pos + (i * 4), True) for i in range(3)]
        pos += 12
        # num_bone_data3 = dv.getUint32(pos, True)
        pos += 4
        # off_bone_data3 = dv.getUint32(pos, True)
        pos += 4
        # unk7 = [dv.getUint32(pos + (i * 4), True) for i in range(4)]
        pos += 16
        # num_bone_data4 = dv.getUint32(pos, True)
        pos += 4
        # off_bone_data4 = dv.getUint32(pos, True)
        pos += 4
        # unk8 = dv.getUint32(pos, True)
        pos += 4

        cloth = Cloth(num_bones_total)

        # NOTE: Read bone names.
        pos = (pos + 127) & -128
        names = []

        for _ in range(num_bones_total):
            name = ""

            for _ in range(32):
                name += chr(dv.getUint8(pos))
                pos += 1

            names.append(name.split('\0')[0])

        for bone, name in zip(cloth.bones, names):
            bone.name = name

        # NOTE: Read bone data (1)
        pos = offset_data + offset_bone_data1

        for _ in range(num_cloth_bones1):
            constraints1 = [round(dv.getFloat32(pos + (i * 4), True), 6) for i in range(4)]
            pos += 16
            constraints2 = [round(dv.getFloat32(pos + (i * 4), True), 6) for i in range(6)]
            pos += 24
            constraints3 = [round(dv.getFloat32(pos + (i * 4), True), 6) for i in range(6)]
            pos += 24
            unk1 = [round(dv.getFloat32(pos + (i * 4), True), 6) for i in range(4)]
            pos += 16
            unk2 = [dv.getInt32(pos + (i * 4), True) for i in range(2)]
            pos += 8
            bone_index = dv.getUint32(pos, True)
            pos += 4
            parent_index = dv.getUint32(pos, True)
            pos += 4

            bone = cloth.bones[bone_index]
            bone.index = bone_index
            bone.parent_index = parent_index
            bone.constraints1 = constraints1
            bone.constraints2 = constraints2
            bone.constraints3 = constraints3
            bone.unk1 = unk1
            bone.unk2 = unk2
            bone.is_cloth = True

        return cloth


def build(operator, context, cloth):
    # type: (Operator, Context, Cloth) -> bool
    import bpy

    ob: Object = context.active_object

    if not ob or ob.type != 'MESH':
        operator.report({'INFO'}, f"Require object of type Mesh to be active, not {ob.type}")
        return False

    # Enter edit mode.
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='EDIT')
    else:
        return False

    pin_group = None

    # Select vertex groups by cloth bone name.
    bpy.ops.mesh.select_all(action='DESELECT')

    for bone in cloth.bones:
        if (getattr(bone, "is_cloth", False) is False) or (bone.name not in ob.vertex_groups):
            continue

        bpy.ops.object.vertex_group_set_active(group=bone.name)
        bpy.ops.object.vertex_group_select()

        if pin_group is None:
            pin_group = bone.name

    # Separate selected vertices into another object.
    bpy.ops.mesh.separate()

    if len(context.selected_objects) > 1:
        cloth_ob = context.selected_objects[1]
        cloth_ob.name = ob.name + "_clo"
        cloth_ob.parent = ob
        cloth_ob.matrix_parent_inverse = ob.matrix_world.inverted()
        modifier = cloth_ob.modifiers.new("Cloth", 'CLOTH')

        if pin_group:
            modifier.settings.vertex_group_mass = pin_group

    # Exit edit mode.
    bpy.ops.object.mode_set(mode='OBJECT')

    return True


def load(operator, context, filepath=""):
    # type: (Operator, Context, str) -> bool
    from bpy_extras.wm_utils.progress_report import ProgressReport

    with ProgressReport(context.window_manager) as progress:
        progress.enter_substeps(3, f"Importing \'{filepath}\' ...")

        progress.step("Parsing file ...", 1)
        cloth = read(operator, filepath)

        if cloth:
            progress.step("Done, building ...", 2)

            if build(operator, context, cloth):
                progress.leave_substeps(f"Done, finished importing: \'{filepath}\'")
                return True

        return False
