# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic models into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired GR2 model file.

https://github.com/SWTOR-Slicers/WikiPedia/wiki/GR2-File-Structure
"""

from os import path, sep
from math import pi
from typing import Union

import bpy
from bpy.types import Context, Operator
from mathutils import Color, Matrix, Vector

from ..types.gr2 import Granny2
from ..utils.binary import ArrayBuffer, DataView
from ..utils.string import readString
from ..utils.number import decodeHalfFloat


def read(operator, filepath):
    # type: (Operator, str) -> Union[Granny2, None]
    """
    """
    with open(filepath, 'rb') as file:
        buffer = ArrayBuffer()
        buffer.fromfile(file, path.getsize(filepath))

    dv = DataView(buffer)
    pos = 0

    # Cancel import if this is not a BioWare Austin / SWTOR GR2 file.
    if dv.getUint32(pos, 1) != 0x42574147:
        operator.report({'ERROR'}, f"{filepath} is not a valid SWTOR gr2 file.")
        return None

    gr2 = Granny2()

    pos = 20  # 0x14

    # GR2 file type, 0 = geometry, 1 = geometry with .clo file, 2 = skeleton
    gr2.type_flag = dv.getUint32(pos, 1)
    pos += 4
    num_meshes = dv.getUint16(pos, 1)                    # Number of meshes in this file
    pos += 2
    num_materials = dv.getUint16(pos, 1)                 # Number of materials in this file
    pos += 2
    num_bones = dv.getUint16(pos, 1)                     # Number of bones in this file
    pos += 2

    pos += 18

    # gr2.bounds = Granny2.BoundingBox([dv.getFloat32(pos + (i * 4), 1) for i in range(8)])
    pos += 32

    pos += 4  # 0x54

    offset_mesh_header = dv.getUint32(pos, 1)            # Mesh header offset address
    pos += 4
    offset_material_name_offsets = dv.getUint32(pos, 1)  # Material header offset address
    pos += 4
    offset_bone_struct = dv.getUint32(pos, 1)            # Bone structure offset address
    pos += 4

    # Meshes
    gr2.mesh_buffer = {}
    for i in range(num_meshes):
        pos = offset_mesh_header + (i * 40)
        # Mesh name
        mesh = Granny2.Mesh(readString(dv, pos))
        pos += 4
        # BitFlag1
        pos += 4
        # Number of sub meshes that make up this mesh
        num_pieces = dv.getUint16(pos, 1)
        pos += 2
        # Number of bones used by this mesh
        num_used_bones = dv.getUint16(pos, 1)
        pos += 2
        # BitFlag2
        bit_flag2 = dv.getUint16(pos, 1)
        pos += 2
        # 12 = collision, 24 = static, 32+ = dynamic
        vertex_size = dv.getUint16(pos, 1)
        pos += 2
        # Total number of vertices used by this mesh
        num_vertices = dv.getUint32(pos, 1)
        pos += 4
        # Total number of polygons used by this mesh
        num_polygons = dv.getUint32(pos, 1)
        pos += 4
        # Offset of the vertices buffer for this mesh
        mesh.offset_vertex_buffer = dv.getUint32(pos, 1)
        pos += 4
        # Offset of the sub mesh header(s)
        mesh.offset_piece_headers = dv.getUint32(pos, 1)
        pos += 4
        # Offset of the indices buffer for this mesh
        mesh.offset_indices_buffer = dv.getUint32(pos, 1)
        pos += 4
        # Offset of the bone buffer for this mesh
        mesh.offset_bones_buffer = dv.getUint32(pos, 1)
        pos += 4

        # Sub mesh header(s)
        mesh.piece_header_buffer = {}
        for j in range(num_pieces):
            pos = mesh.offset_piece_headers + (j * 48)

            piece = Granny2.Piece()

            piece.offset_indices = dv.getUint32(pos, 1)     # Relative offset for this piece's faces
            pos += 4
            piece.num_polygons = dv.getUint32(pos, 1)       # Number of faces used by this piece
            pos += 4
            piece.material_index = dv.getUint32(pos, 1)     # Mesh piece material id
            pos += 4
            piece.index = dv.getUint32(pos, 1)              # Mesh piece enumerator (1 x uint32)
            pos += 4
            # piece.bounds = Granny2.BoundingBox(           # Bounding box (8 x 4 bytes)
            #     [dv.getFloat32(pos + (k * 4), 1) for k in range(8)])
            pos += 32

            mesh.piece_header_buffer[j] = piece

        # Vertex buffer
        mesh.vertex_buffer = {}
        for j in range(num_vertices):
            pos = mesh.offset_vertex_buffer + (j * vertex_size)

            vertex = Granny2.Vertex([dv.getFloat32(pos + (k * 4), 1) for k in range(3)])
            pos += 12

            if bit_flag2 & 256:  # 0x100
                vertex.bone_weights = Vector([dv.getUint8(pos + k) for k in range(4)])
                pos += 4
                vertex.bone_indices = Vector([dv.getUint8(pos + k) for k in range(4)])
                pos += 4

            if bit_flag2 & 2:  # 0x02
                vertex.normals = Vector(
                    [(dv.getUint8(pos + k) - 127.5) / 127.5 for k in range(4)])
                pos += 4
                vertex.tangents = Vector(
                    [(dv.getUint8(pos + k) - 127.5) / 127.5 for k in range(4)])
                pos += 4

            if bit_flag2 & 16:  # 0x10
                vertex.color = Color([dv.getUint8(pos + k) for k in range(3)])
                pos += 4

            if bit_flag2 & 32:  # 0x20
                vertex.uv_layer0 = Vector(
                    [decodeHalfFloat(dv.getUint16(pos + (k * 2), 1)) for k in range(2)])
                pos += 4

            if bit_flag2 & 64:  # 0x40
                vertex.uv_layer1 = Vector(
                    [decodeHalfFloat(dv.getUint16(pos + (k * 2), 1)) for k in range(2)])
                pos += 4

            if bit_flag2 & 128:  # 0x80
                vertex.uv_layer2 = Vector(
                    [decodeHalfFloat(dv.getUint16(pos + (k * 2), 1)) for k in range(2)])

            mesh.vertex_buffer[j] = vertex

        # Indices buffer
        mesh.indices_buffer = {}
        for j in range(int(num_polygons / 3)):
            pos = mesh.offset_indices_buffer + (j * 6)
            mesh.indices_buffer[j] = tuple([dv.getUint16(pos + (k * 2), 1) for k in range(3)])

        # Bone(s) buffer
        mesh.bone_names = {j: readString(dv, mesh.offset_bones_buffer + (j * 28))
                           for j in range(num_used_bones)}

        gr2.mesh_buffer[i] = mesh

    # Materials
    # NOTE: I wish there was a more efficient way to do this!
    gr2.material_names = {}
    if num_materials:
        pos = offset_material_name_offsets
        for i in range(num_materials):                         # Use string name for name
            gr2.material_names[i] = readString(dv, pos)
            pos += 4
    else:
        count = 0
        for mesh in gr2.mesh_buffer.values():
            if mesh.bit_flag2 & 32:
                for j in mesh.piece_header_buffer.keys():  # Use "mesh name".00x for name
                    gr2.material_names[count] = f"{mesh.name}.{j:03d}"
                    count += 1

    # Skeleton Bones
    gr2.bone_buffer = {}
    for i in range(num_bones):
        pos = offset_bone_struct + (i * 136)
        bone = Granny2.Bone()
        bone.name = readString(dv, pos)
        pos += 4
        bone.parent_index = dv.getInt32(pos, 1)
        pos += 4
        # bone.bone_to_parent = [dv.getFloat32(pos + (j * 4), 1) for j in range(16)]
        pos += 64
        bone.root_to_bone = [dv.getFloat32(pos + (j * 4), 1) for j in range(16)]
        pos += 64
        gr2.bone_buffer[i] = bone

    return gr2


def build(gr2, filepath="", import_collision=False):
    # type: (Granny2, str, bool) -> None
    """
    """
    # NOTE: Create Materials
    for i, material in gr2.material_names.items():
        new_material = bpy.data.materials.new(name=material)
        new_material.use_nodes = True

    # NOTE: Create Meshes
    for i, mesh in gr2.mesh_buffer.items():
        if "collision" in mesh.name and not import_collision:
            continue

        bmesh = bpy.data.meshes.new(mesh.name)
        bmesh.from_pydata([vert.position for vert in mesh.vertex_buffer.values()],
                          [],
                          [index for index in mesh.indices_buffer.values()])

        if mesh.bit_flag2 & 32:  # 0x20
            # Link Materials
            material_indices = []
            for j, piece in mesh.piece_header_buffer.items():
                material_index = j if piece.material_index == 4294967295 else piece.material_index
                bmesh.materials.append(bpy.data.materials[material_index])

                for _ in range(piece.num_polygons):
                    material_indices.append(j)

        if mesh.bit_flag2 & 2:   # 0x02
            # NOTE: We store 'temp' normals in loops, since validate() may alter final mesh,
            #       we can only set custom loop normals *after* calling it.
            bmesh.create_normals_split()
            bmesh.uv_layers.new(do_init=False)

            for j, polygon in enumerate(bmesh.polygons):
                loop_indices = polygon.loop_indices

                for k, loop_index in enumerate(loop_indices):
                    v = mesh.vertex_buffer[mesh.indices_buffer[j][k]]
                    bmesh.loops[loop_index].normal = [v.normals.x, v.normals.y, v.normals.z]
                    bmesh.uv_layers[0].data[loop_index].uv = [v.uv_layer0.x, 1 - v.uv_layer0.y]

                polygon.material_index = material_indices[j]

            bmesh.validate(clean_customdata=False)

            # Mesh Normals
            custom_loop_normals = [0.0] * (len(bmesh.loops) * 3)
            bmesh.loops.foreach_get("normal", custom_loop_normals)
            bmesh.polygons.foreach_set("use_smooth", [True] * len(bmesh.polygons))
            bmesh.normals_split_custom_set(tuple(zip(*(iter(custom_loop_normals),) * 3)))
            bmesh.use_auto_smooth = True

        # Create Blender Object
        ob = bpy.data.objects.new(mesh.name, bmesh)

        # Create Vertex Groups
        for j, vertex in mesh.vertex_buffer.items():
            if mesh.bit_flag2 & 256:
                for index in range(4):
                    bone = mesh.bone_names[vertex.bone_indices[index]]

                    if bone not in ob.vertex_groups:
                        ob.vertex_groups.new(name=bone)

                    ob.vertex_groups[bone].add([j], float(vertex.bone_weights[index] / 255), 'ADD')

        # Link Blender Object
        bpy.context.collection.objects.link(ob)

        # Adjust the orientation of the model
        ob.matrix_local = Matrix.Rotation(pi * 0.5, 4, 'X')

        # Deselect all, then select imported model
        bpy.ops.object.select_all(action='DESELECT')
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob

    # Create Armature
    if gr2.type_flag == 2 and len(gr2.bone_buffer) > 0:
        bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
        armature: bpy.types.Armature = bpy.context.object.data
        armature.name = filepath.split(sep)[-1][:-4]
        armature.display_type = 'STICK'

        for bone in gr2.bone_buffer.values():
            new_bone = armature.edit_bones.new(bone.name)
            new_bone.tail = [0, 0.00001, 0]

        for i, bone in gr2.bone_buffer.items():
            armature_bone = armature.edit_bones[i]

            if bone.parent_index >= 0:
                armature_bone.parent = armature.edit_bones[bone.parent_index]

            matrix = Matrix([bone.root_to_bone[j*4:j*4+4] for j in range(4)])
            matrix.transpose()
            armature_bone.transform(matrix.inverted())

        bpy.context.object.name = armature.name
        bpy.context.object.matrix_local = Matrix.Rotation(pi * 0.5, 4, 'X')
        bpy.ops.object.mode_set(mode='OBJECT')


def load(operator, context, filepath=""):
    # type: (Operator, Context, str) -> bool
    from bpy_extras.wm_utils.progress_report import ProgressReport

    with ProgressReport(context.window_manager) as progress:
        progress.enter_substeps(3, f"Importing \'{filepath}\' ...")

        progress.step("Reading file ...", 1)
        mesh = read(operator, filepath=filepath)

        if mesh:
            progress.step("Done, building ...", 2)

            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            build(mesh, filepath=filepath, import_collision=operator.import_collision)
            progress.leave_substeps(f"Done, finished importing: \'{filepath}\'")

            return True
        else:
            return False
