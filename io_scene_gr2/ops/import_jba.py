# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic animations into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired JBA animation file.

https://github.com/SWTOR-Slicers/WikiPedia/wiki/JBA-File-Structure
"""

import math
import os
from typing import Optional, Set

from bpy import app
from bpy.props import BoolProperty, CollectionProperty, FloatProperty, StringProperty
from bpy.types import Context, Object, Operator, OperatorFileListElement
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix, Quaternion, Vector

from ..types.jba import JointBoneAnimation
from ..utils.binary import ArrayBuffer, DataView
from ..utils.string import path_split, readCString


class ImportJBA(Operator):
    """Import from SWTOR JBA file format (.jba)"""
    bl_idname = "import_animation.jba"  # DO NOT CHANGE
    bl_description = "Import and apply an animation to the active SWTOR skeleton in the scene.\n\n• Only compatible with .jba files extracted from SWTOR 32-bit\n   (before Game Update 7.2.1)"
    bl_label = "Import SWTOR (.jba)"
    bl_options = {'UNDO'}

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the JBA file",
        type=OperatorFileListElement,
    )

    if app.version < (2, 82, 0):
        directory = StringProperty(subtype='DIR_PATH')
    else:
        directory: StringProperty(subtype='DIR_PATH')

    filename_ext = ".jba"

    filter_glob: StringProperty(
        default="*.jba",
        options={'HIDDEN'},
    )
    
    ignore_facial_bones: BoolProperty(
        name="Ignore Facial Transl.",
        description="Ignores the data in the facial bones' translation keyframes\nand only uses their rotation keyframes",
        default=True,
    )

    scale_animation: BoolProperty(
        name="Scale Animation",
        description="Scales the bones' translation data by a factor.\nIt must match the scale of the skeleton\nand objects to be animated for good results.\n\nWhenever possible, this setting will try to match\nthe Objects' Scale Factor automatically.\nIt will still allow for setting different values manually",
        default=False,
    )

    scale_factor: FloatProperty(
        name="Scale Factor",
        description="Scales the bones' translation data by a factor.\nIt must match the scale of the skeleton\nand objects to be animated.\n\nWhenever possible, this setting will try to match\nthe Objects Import Settings automatically\n(it still allows for setting different values)",
        default=1.0,
        soft_min=0.1,
        soft_max=2.0,
        precision=2,
    )
    
    delete_180: BoolProperty(
        name="Delete 180º rotation",
        description="Keeps the animation data from turning the skeleton 180º by deleting\nthe keyframes assigned to the Bip01 bone and setting its rotation to zero.\n\nSWTOR animations turn characters so that they face away from the camera,\nas normally shown in the gameplay. That is not just a nuisance but a problem\nwhen adding cloth or physics simulations to capes or lekku: the instantaneous\nturn plays havok with them",
        default=False,
    )

    def invoke(self, context, event):
        # To be able to set the class' properties to the values in the
        # Add-on's preferences and show them in the File Browser's options,
        # we use an Invoke function instead of directly using ImportHelper in
        # the class definition, to be able to put there the required code.
        
        prefs = context.preferences.addons["io_scene_gr2"].preferences
        
        self.ignore_facial_bones = prefs.jba_ignore_facial_bones
        self.scale_animation     = prefs.jba_scale_animation
        self.scale_factor        = prefs.jba_scale_factor
        self.delete_180          = prefs.jba_delete_180

        context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}



    def execute(self, context):
        # type: (Context) -> Set[str]

        paths = [os.path.join(self.directory, file.name) for file in self.files if file.name.lower().endswith(self.filename_ext)]

        if not paths:
            paths.append(self.filepath)

        for path in paths:
            if not load(self, context, path):
                return {'CANCELLED'}

        return {'FINISHED'}


def _read_rotation_compressed(dv, pos, base, stride):
    # type: (DataView, int, Vector, Vector) -> Quaternion
    rot_x_raw = dv.getUint16(pos, True)
    rot_x = base.x + (rot_x_raw & 32767) * stride.x
    rot_y = base.y + dv.getUint16(pos + 2, True) * stride.y
    rot_z = base.z + dv.getUint16(pos + 4, True) * stride.z
    pos += 6
    rot_dot = rot_x * rot_x + rot_y * rot_y + rot_z * rot_z
    rot_w = 0.0 if rot_dot > 1.0 else math.sqrt(1.0 - rot_dot)

    if rot_x_raw & 32768:
        rot_w *= -1.0

    return Quaternion((rot_w, rot_x, rot_y, rot_z)).normalized()


def _read_translation_compressed(dv, pos, base, stride):
    # type: (DataView, int, Vector, Vector) -> Vector
    val = dv.getUint32(pos, True)
    pos += 4

    pos_x = base.x + (val >> 21) * stride.x
    pos_y = base.y + ((val >> 10) & 2047) * stride.y
    pos_z = base.z + (val & 1023) * stride.z

    return Vector((pos_x, pos_y, pos_z))


def read(operator, filepath):
    # type: (Operator, str) -> Optional[JointBoneAnimation]
    with open(filepath, 'rb') as file:
        buffer = ArrayBuffer()
        buffer.fromfile(file, os.path.getsize(filepath))

    dv = DataView(buffer)
    pos = 0

    # Cancel import if this is not a BioWare Austin / SWTOR JBA file
    if dv.getUint32(pos, True) != 0:
        operator.report({'ERROR'}, f"\'{filepath}\' is not a valid SWTOR jba file.")
        return None
    pos += 4

    # NOTE: File header
    length = dv.getFloat32(pos, True)
    pos += 4
    fps = dv.getFloat32(pos, True)
    pos += 4
    num_blocks = dv.getUint32(pos, True)
    pos += 4
    pos += 8  # unknown
    num_bones = dv.getUint32(pos, True)
    pos += 4
    pos += 12  # unknown

    # NOTE: Block headers
    num_frames = round(length * fps) + 1
    blocks = [None] * num_blocks
    for i in range(num_blocks):
        start_frame = dv.getUint32(pos, True)
        pos += 4
        block_size = dv.getUint32(pos, True)
        pos += 4
        blocks[i] = JointBoneAnimation.Block(start_frame, block_size)
        if i > 0:
            blocks[i - 1].num_frames = 1 + blocks[i].start_frame - blocks[i - 1].start_frame
        if i + 1 == num_blocks:
            blocks[i].num_frames = num_frames - blocks[i].start_frame
    pos += num_blocks * 4  # unknown

    # NOTE: Bone data
    pos = (pos + 127) & -128
    bones = [None] * num_bones
    for i in range(num_bones):
        translation_stride = Vector([dv.getFloat32(pos + (j * 4), True) for j in range(3)])
        pos += 12
        translation_base = Vector([dv.getFloat32(pos + (j * 4), True) for j in range(3)])
        pos += 12
        rotation_stride = Vector([dv.getFloat32(pos + (j * 4), True) for j in range(3)])
        pos += 12
        rotation_base = Vector([dv.getFloat32(pos + (j * 4), True) for j in range(3)])
        pos += 12
        bone = JointBoneAnimation.Bone(rotation_base, rotation_stride, translation_base, translation_stride)
        bone.rotations = [None] * num_frames
        bone.translations = [None] * num_frames
        bones[i] = bone

    # NOTE: Block data
    pos = (pos + 127) & -128
    for i in range(num_blocks):
        block = blocks[i]
        block_end = pos + block.size

        num_block_bones = dv.getUint32(pos, True)
        pos += 4
        assert(num_block_bones == num_bones)
        pos += 4  # unknown

        # Keyframe layout
        has_translations = [None] * num_block_bones
        for j in range(num_block_bones):
            # num_rotations = dv.getUint32(pos, True)
            pos += 4
            pos += 4  # unknown
            num_translations = dv.getUint32(pos, True)
            pos += 4
            pos += 4  # unknown
            has_translations[j] = num_translations > 0

        # Keyframes
        for j in range(num_bones):
            bone = bones[j]

            # Rotations
            for k in range(block.num_frames):
                bone.rotations[block.start_frame + k] = _read_rotation_compressed(
                    dv, pos, bone.rotation_base, bone.rotation_stride)
                pos += 6

            # Translations
            pos = (pos + 3) & -4
            if has_translations[j]:
                for k in range(block.num_frames):
                    bone.translations[block.start_frame + k] = _read_translation_compressed(
                        dv, pos, bone.translation_base, bone.translation_stride)
                    pos += 4
            else:
                for k in range(block.num_frames):
                    pos_x = bone.translation_base.x + 2047 * bone.translation_stride.x
                    pos_y = bone.translation_base.y + 2047 * bone.translation_stride.y
                    pos_z = bone.translation_base.z + 1023 * bone.translation_stride.z
                    bone.translations[block.start_frame + k] = Vector((pos_x, pos_y, pos_z))

        pos = block_end

    # World space
    pos += 4  # unknown
    # fps = dv.getFloat32(pos, True)
    pos += 4
    translation_stride = Vector([dv.getFloat32(pos + (i * 4), True) for i in range(3)])
    pos += 12
    translation_base = Vector([dv.getFloat32(pos + (i * 4), True) for i in range(3)])
    pos += 12
    rotation_stride = Vector([dv.getFloat32(pos + (i * 4), True) for i in range(3)])
    pos += 12
    rotation_base = Vector([dv.getFloat32(pos + (i * 4), True) for i in range(3)])
    pos += 12
    num_rotations = dv.getUint32(pos, True)
    pos += 4
    assert(num_rotations == num_frames)
    pos += 4  # unknown
    # num_translations = dv.getUint32(pos, True)
    pos += 4
    # assert(num_translations == num_faces)
    pos += 4  # unknown

    rotations = [_read_rotation_compressed(dv, pos + (i * 8), rotation_base, rotation_stride)
                 for i in range(num_frames)]
    pos += num_frames * 6

    pos = (pos + 3) & -4

    translations = [_read_translation_compressed(dv, pos + (i * 4), translation_base, translation_stride)
                    for i in range(num_frames)]
    pos += num_frames * 4

    world_space = JointBoneAnimation.WorldSpace(rotations, translations)

    # Bone names
    names_start = pos
    num_names = dv.getUint32(pos, True)
    pos += 4
    pos += 4  # unknown
    # off_indices = dv.getUint32(pos, True)
    pos += 4
    # off_offsets = dv.getUint32(pos, True)
    pos += 4
    off_names = dv.getUint32(pos, True)
    pos += 4
    pos += num_names * 4  # numbers from 0 to num_names - 1
    name_offsets = [dv.getUint32(pos + (i * 4), True) for i in range(num_names)]
    pos += num_names * 4
    bone_names = [readCString(dv, names_start + off_names + name_offsets[i]) for i in range(num_names)]

    for i, name in enumerate(bone_names):
        bones[i].name = name if name != "GOD" else "Bip01"

    return JointBoneAnimation(length, fps, num_frames, bones, world_space)


def build(operator, context, filepath, jba):
    # type: (Operator, Context, str, JointBoneAnimation) -> bool
    import bpy
    # import os

    ob: Object = context.active_object

    if not ob or ob.type != 'ARMATURE':
        operator.report({'INFO'}, f"Requires object of type Armature to be active, not {ob.type}")
        return False

    # Create armature action
    # anim_name, _ = os.path.splitext(os.path.basename(filepath))
    anim_name = path_split(filepath)[:-4]

    if not ob.animation_data:
        ob.animation_data_create()

    action = bpy.data.actions.new(anim_name)
    ob.animation_data.action = action

    # Enter pose mode
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='POSE')

    # Create armature keyframes
    # scale = 1000 * operator.scale_factor  # This was the original calculation, but it seems to work as an inverse, so…
    # Check if the armature object has import scale custom property data. If not, use the add-on's prefs settings.
    if 'gr2_scale' in ob:
        scale = 1000 * (1 / ob['gr2_scale'])
    else:
        if operator.scale_animation:
            scale = 1000 * (1 / operator.scale_factor)
        else:
            scale = 1000
        
    morpheme_space = Matrix(((scale, 0, 0, 0), (0, 0, -scale, 0), (0, scale, 0, 0), (0, 0, 0, 1)))
    morpheme_space_inv = morpheme_space.inverted()

    for anim_frame in range(jba.num_frames):
        for anim_bone in jba.bones:
            bone_name = getattr(anim_bone, "name", "")

            if bone_name in ob.pose.bones:
                pose_bone = ob.pose.bones[bone_name]
                mat_rest = pose_bone.bone.matrix_local

                if pose_bone.parent:
                    mat_rest = pose_bone.parent.bone.matrix_local.inverted() @ mat_rest

                mat_rot = anim_bone.rotations[anim_frame].to_matrix().to_4x4()

                if operator.ignore_facial_bones and bone_name.lower().startswith("fc_"):
                    mat_trans = Matrix.Translation(mat_rest.to_translation())
                    mat_bone = mat_trans @ morpheme_space_inv @ mat_rot @ morpheme_space
                else:
                    mat_trans = Matrix.Translation(anim_bone.translations[anim_frame])
                    mat_bone = morpheme_space_inv @ mat_trans @ mat_rot @ morpheme_space

                frame = jba.fps * jba.length * anim_frame / jba.num_frames + 1
                pose_bone.matrix_basis = mat_rest.inverted() @ mat_bone
                pose_bone.keyframe_insert(data_path="location", frame=frame)
                if not (operator.delete_180 and bone_name == "Bip01"):
                    pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)

    if operator.delete_180 and "Bip01" in ob.pose.bones:
        # CHECK THAT THIS QUATERNION ROTATION IS VALID IN ALL CASES!!!
        ob.pose.bones["Bip01"].rotation_quaternion = (1, 0, 0, 0)

    return True


def load(operator, context, filepath=""):
    # type: (Operator, Context, str) -> bool
    from bpy_extras.wm_utils.progress_report import ProgressReport

    with ProgressReport(context.window_manager) as progress:
        progress.enter_substeps(3, f"Importing \'{filepath}\' ...")

        progress.step("Parsing file ...", 1)
        animation = read(operator, filepath)

        if animation:
            progress.step("Done, building ...", 2)

            if build(operator, context, filepath, animation):
                progress.leave_substeps(f"Done, finished importing: \'{filepath}\'")
                return True

        return False
