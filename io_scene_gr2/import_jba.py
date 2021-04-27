# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic animations into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired JBA animation file.

https://github.com/SWTOR-Slicers/WikiPedia/wiki/JBA-File-Structure
"""

import os
import math

import bpy
from bpy_extras.wm_utils.progress_report import ProgressReport
from mathutils import Matrix, Quaternion, Vector

from .parse import *


class JBAAnimation():
    def __init__(self, length, fps, num_frames, bones, world_space):
        self.length = length
        self.fps = fps
        self.num_frames = num_frames
        self.bones = bones
        self.world_space = world_space


class JBABone():
    def __init__(self, translation_stride, translation_base, rotation_stride, rotation_base, num_frames):
        self.translation_stride = translation_stride
        self.translation_base = translation_base
        self.rotation_stride = rotation_stride
        self.rotation_base = rotation_base
        self.translations = [None]*num_frames
        self.rotations = [None]*num_frames
        self.name = ""


class JBABlock():
    def __init__(self, start_frame, size):
        self.start_frame = start_frame
        self.size = size
        self.num_frames = 0


class JBAWorldSpace():
    def __init__(self, rotations, translations):
        self.rotations = rotations
        self.translations = translations


class JBALoader():
    def __init__(self, filepath):
        self.filepath = filepath
        self.animation = None

    def parse(self, operator):
        with open(self.filepath, "rb") as f:
            # Cancel import if this is a non Bio-Ware Austin / SWTOR JBA file
            if f.read(4) != b'\0\0\0\0':
                operator.report({'ERROR'}, ("\'%s\' is not a valid SWTOR jba file.") % self.filepath)
                raise RuntimeError()

            # File Header
            length = rfloat32(f)
            fps = rfloat32(f)
            num_blocks = ruint32(f)
            ignore(f, 2 * 4) # unknown
            num_bones = ruint32(f)
            ignore(f, 3 * 4) # unknown

            # Block Headers
            num_frames = round(length * fps) + 1
            blocks = self._read_block_headers(f, num_blocks, num_frames)

            # Bone Data
            f.seek((f.tell() + 0x7f) & -0x80)
            bones = self._read_bone_data(f, num_bones, num_frames)

            # Block Data
            f.seek((f.tell() + 0x7f) & -0x80)
            for i in range(num_blocks):
                block = blocks[i]
                block_end = f.tell() + block.size

                num_block_bones = ruint32(f)
                assert(num_block_bones == num_bones)
                ignore(f, 4) # unknown

                # Keyframe Layout
                has_translations = [None]*num_block_bones
                for j in range(num_block_bones):
                    num_rotations = ruint32(f)
                    ignore(f, 4) # unknown
                    num_translations = ruint32(f)
                    ignore(f, 4) # unknown
                    has_translations[j] = num_translations > 0

                # Keyframes
                for j in range(num_bones):
                    bone = bones[j]

                    # Rotations
                    for k in range(block.num_frames):
                        bone.rotations[block.start_frame + k] = self._read_rotation_compressed(f, bone.rotation_base, bone.rotation_stride)

                    # Translations
                    f.seek((f.tell() + 3) & -4)
                    if has_translations[j]:
                        for k in range(block.num_frames):
                            bone.translations[block.start_frame + k] = self._read_translation_compressed(f, bone.translation_base, bone.translation_stride)
                    else:
                        for k in range(block.num_frames):
                            pos_x = bone.translation_base.x + 0x7ff * bone.translation_stride.x
                            pos_y = bone.translation_base.y + 0x7ff * bone.translation_stride.y
                            pos_z = bone.translation_base.z + 0x3ff * bone.translation_stride.z
                            bone.translations[block.start_frame + k] = Vector((pos_x, pos_y, pos_z))

                f.seek(block_end)

            # World Space
            world_space = self._read_world_space(f, num_frames)

            # Bone Names
            bone_names = self._read_bone_names(f)
            for i, name in enumerate(bone_names):
                bones[i].name = name if name != "GOD" else "Bip01"

            self.animation = JBAAnimation(length, fps, num_frames, bones, world_space)

    def _read_block_headers(self, file, num_blocks, num_frames):
        blocks = [None]*num_blocks
        for i in range(num_blocks):
            start_frame = ruint32(file)
            block_size = ruint32(file)
            blocks[i] = JBABlock(start_frame, block_size)
            if i > 0:
                blocks[i - 1].num_frames = 1 + blocks[i].start_frame - blocks[i - 1].start_frame
            if i + 1 == num_blocks:
                blocks[i].num_frames = num_frames - blocks[i].start_frame
        ignore(file, num_blocks * 4) # unknown
        return blocks

    def _read_bone_data(self, file, num_bones, num_frames):
        bones = [None]*num_bones
        for i in range(num_bones):
            translation_stride = Vector([rfloat32(file) for _ in range(3)])
            translation_base = Vector([rfloat32(file) for _ in range(3)])
            rotation_stride = Vector([rfloat32(file) for _ in range(3)])
            rotation_base = Vector([rfloat32(file) for _ in range(3)])
            bones[i] = JBABone(translation_stride, translation_base, rotation_stride, rotation_base, num_frames)
        return bones

    def _read_rotation_compressed(self, file, base, stride):
        rot_x_raw = ruint16(file)
        rot_x = base.x + (rot_x_raw & 0x7fff) * stride.x
        rot_y = base.y + ruint16(file) * stride.y
        rot_z = base.z + ruint16(file) * stride.z
        rot_dot = rot_x * rot_x + rot_y * rot_y + rot_z * rot_z
        rot_w = 0.0 if rot_dot > 1.0 else math.sqrt(1.0 - rot_dot)
        if rot_x_raw & 0x8000:
            rot_w *= -1.0
        return Quaternion((rot_w, rot_x, rot_y, rot_z)).normalized()

    def _read_translation_compressed(self, file, base, stride):
        val = ruint32(file)
        pos_x = base.x + (val >> 21) * stride.x
        pos_y = base.y + ((val >> 10) & 0x7ff) * stride.y
        pos_z = base.z + (val & 0x3ff) * stride.z
        return Vector((pos_x, pos_y, pos_z))

    def _read_world_space(self, file, num_frames):
        ignore(file, 4) # unknown
        fps = rfloat32(file)
        translation_stride = Vector([rfloat32(file) for _ in range(3)])
        translation_base = Vector([rfloat32(file) for _ in range(3)])
        rotation_stride = Vector([rfloat32(file) for _ in range(3)])
        rotation_base = Vector([rfloat32(file) for _ in range(3)])
        num_rotations = ruint32(file)
        assert(num_rotations == num_frames)
        ignore(file, 4) # unknown
        num_translations = ruint32(file)
        assert(num_rotations == num_frames)
        ignore(file, 4) # unknown
        rotations = [self._read_rotation_compressed(file, rotation_base, rotation_stride) for _ in range(num_frames)]
        file.seek((file.tell() + 3) & -4)
        translations = [self._read_translation_compressed(file, translation_base, translation_stride) for _ in range(num_frames)]
        return JBAWorldSpace(rotations, translations)

    def _read_bone_names(self, file):
        names_start = file.tell()
        num_names = ruint32(file)
        ignore(file, 4) # unknown
        off_indices = ruint32(file)
        off_offsets = ruint32(file)
        off_names = ruint32(file)
        ignore(file, num_names * 4) # numbers from 0 to number of names - 1
        name_offsets = [ruint32(file) for _ in range(num_names)]
        names = [None]*num_names
        for i in range(num_names):
            file.seek(names_start + off_names + name_offsets[i])
            names[i] = rcstring(file)
        return names

    def build(self, operator):
        obj = bpy.context.active_object
        if not bpy.context.active_object or bpy.context.active_object.type != 'ARMATURE':
            operator.report({'INFO'}, "Object of type Armature must be active")
            return

        # Create armature action
        anim_name, _ = os.path.splitext(os.path.basename(self.filepath))
        if not obj.animation_data:
            obj.animation_data_create()
        action = bpy.data.actions.new(anim_name)
        obj.animation_data.action = action

        # Enter Pose mode
        bpy.ops.object.mode_set(mode='POSE')

        # Create armature keyframes
        morpheme_space = Matrix([[1000, 0, 0, 0], [0, 0, -1000, 0], [0, 1000, 0, 0], [0, 0, 0, 1]])
        morpheme_space_inv = morpheme_space.inverted()
        for anim_frame in range(self.animation.num_frames):
            for anim_bone in self.animation.bones:
                bone_name = anim_bone.name
                if bone_name in obj.pose.bones:
                    pose_bone = obj.pose.bones[bone_name]
                    mat_rest = pose_bone.bone.matrix_local
                    if pose_bone.parent:
                        mat_rest = pose_bone.parent.bone.matrix_local.inverted() @ mat_rest
                    mat_trans = Matrix.Translation(anim_bone.translations[anim_frame])
                    mat_rot = anim_bone.rotations[anim_frame].to_matrix().to_4x4()
                    pose_bone.matrix_basis = mat_rest.inverted() @ morpheme_space_inv @ mat_trans @ mat_rot @ morpheme_space
                    frame = self.animation.fps * self.animation.length * anim_frame / self.animation.num_frames + 1
                    pose_bone.keyframe_insert(data_path="location", frame=frame)
                    pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)


def load(operator, context, filepath=""):
    with ProgressReport(context.window_manager) as progress:
        try:
            progress.enter_substeps(3, "Importing \'%s\' ..." % filepath)
            mainLoader = JBALoader(filepath)

            progress.step("Parsing file ...", 1)
            mainLoader.parse(operator)

            progress.step("Done, building ...", 2)
            mainLoader.build(operator)

            progress.leave_substeps("Done, finished importing: \'%s\'" % filepath)
        except RuntimeError:
            return {'CANCELED'}

    return {'FINISHED'}
