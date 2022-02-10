# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic models into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired GR2 model file.
"""

import array
import bpy
import math
import os

from bpy_extras.wm_utils.progress_report import ProgressReport
from mathutils import Matrix
# from .shaders import (
#     CreatureShader,
#     EyeShader,
#     GarmentShader,
#     HairCShader,
#     SkinBShader,
#     UberShader)
from .utils import (
    ruint8,
    ruint16,
    ruint32,
    rfloat8,
    rfloat16,
    rfloat32,
    rstring,
    unpack)


class GR2MeshPiece():
    def __init__(self, f, offset):
        f.seek(offset)

        self.startIndex = ruint32(f)    # Relative offset for this piece's faces
        self.numFaces = ruint32(f)      # Number of faces used by this piece
        self.materialIdx = ruint32(f)   # Mesh piece material id
        self.pieceIndex = ruint32(f)    # Mesh piece enumerator (1 x uint32)
        f.seek(0x24, 1)                 # Bounding box (8 x 4 bytes)


class GR2Vertex():
    def __init__(self, f, offset, bitFlag2):
        f.seek(offset)

        self.x = rfloat32(f)  # X Coordinate
        self.y = rfloat32(f)  # Y Coordinate
        self.z = rfloat32(f)  # Z Coordinate

        if bitFlag2 & 0x100:
            self.weights = [ruint8(f), ruint8(f), ruint8(f), ruint8(f)]  # Bone Weights
            self.bones = [ruint8(f), ruint8(f), ruint8(f), ruint8(f)]    # Bone Indices

        if bitFlag2 & 0x02:
            self.nx = rfloat8(f)  # Normals (X)
            self.ny = rfloat8(f)  # Normals (Y)
            self.nz = rfloat8(f)  # Normals (Z)
            f.seek(0x05, 1)

        if bitFlag2 & 0x10:
            f.seek(0x04, 1)       # Color (RGBA)

        if bitFlag2 & 0x20:
            self.u = rfloat16(f)  # Texture Map (U)
            self.v = rfloat16(f)  # Texture Map (V)

        if bitFlag2 & 0x40:
            f.seek(0x04, 1)       # Texture Map 2 (UV)

        if bitFlag2 & 0x80:
            f.seek(0x04, 1)       # Texture Map 3 (UV)

    def __iter__(self):
        return iter([self.x, self.y, self.z])


class GR2Face():
    def __init__(self, f, offset):
        f.seek(offset)

        self.v1 = ruint16(f)  # Vertex 1
        self.v2 = ruint16(f)  # Vertex 2
        self.v3 = ruint16(f)  # Vertex 3

    def __iter__(self):
        return iter([self.v1, self.v2, self.v3])


class GR2MeshBone():
    def __init__(self, f, offset):
        f.seek(offset)

        self.name = rstring(f)
        self.bounds = [rfloat32(f) for _ in range(6)]


class GR2Mesh():
    def __init__(self, f, offset):
        f.seek(offset)

        self.name = rstring(f)            # Mesh name

        f.seek(0x04, 1)

        self.numPieces = ruint16(f)       # Number of pieces that make up this mesh
        self.numUsedBones = ruint16(f)    # Number of bones used by this mesh
        self.bitFlag2 = ruint16(f)        # BitFlag2
        self.vertexSize = ruint16(f)      # 12 = collision, 24 = static, 32/36 = dynamic
        self.numVertices = ruint32(f)     # The total number of vertices used by this mesh
        self.numIndicies = ruint32(f)     # The total number of face indicies used by this mesh
        self.offsetVertices = ruint32(f)  # The start address (offset) of the vertices of this mesh
        self.offsetPieces = ruint32(f)    # The start address (offset) of the mesh piece headers
        self.offsetIndicies = ruint32(f)  # The start address (offset) of the face indices of this mesh
        self.offsetBones = ruint32(f)     # The start address (offset) of the bone list of this mesh

        # Mesh pieces
        self.pieces = [GR2MeshPiece(f, self.offsetPieces + p * 0x30)
                       for p in range(self.numPieces)]

        # Vertices
        self.vertices = [GR2Vertex(f, self.offsetVertices + v * self.vertexSize, self.bitFlag2)
                         for v in range(self.numVertices)]

        # Face indicies
        self.faces = [GR2Face(f, self.offsetIndicies + i * 0x06)
                      for i in range(self.numIndicies // 3)]

        # Bones
        self.bones = [GR2MeshBone(f, self.offsetBones + b * 0x1C)
                      for b in range(self.numUsedBones)]

    def build(self, meshLoader):
        me = bpy.data.meshes.new(self.name)
        me.from_pydata([list(xyz) for xyz in self.vertices], [], [list(v) for v in self.faces])

        if self.bitFlag2 & 0x20:
            # Link Materials
            materialIndex = []
            for enm, pc in enumerate(self.pieces):
                if pc.materialIdx == 4294967295:  # UInt32: -1
                    me.materials.append(bpy.data.materials[meshLoader.materials[enm]])
                else:
                    me.materials.append(bpy.data.materials[meshLoader.materials[pc.materialIdx]])
                for _ in range(pc.numFaces):
                    materialIndex.append(enm)

            # NOTE: We store 'temp' normals in loops, since validate() may alter final mesh,
            #       we can only set custom loop normals *after* calling it.
            me.create_normals_split()
            me.uv_layers.new(do_init=False)
            for i, poly in enumerate(me.polygons):
                loopIndices = list(poly.loop_indices)
                for e, loop_index in enumerate(loopIndices):
                    v = self.vertices[list(self.faces[i])[e]]
                    me.loops[loop_index].normal = [v.nx, v.ny, v.nz]      # Loop Normals
                    me.uv_layers[0].data[loop_index].uv = [v.u, 1 - v.v]  # Loop UVs
                # Map Materials to Faces
                poly.material_index = materialIndex[i]

            me.validate(clean_customdata=False)

            # Mesh Normals
            customLoopNormals = array.array('f', [0.0] * (len(me.loops) * 3))
            me.loops.foreach_get("normal", customLoopNormals)
            me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
            me.normals_split_custom_set(tuple(zip(*(iter(customLoopNormals),) * 3)))
            me.use_auto_smooth = True

        # Create Blender object
        obj = bpy.data.objects.new(self.name, me)

        # Create Vertex Groups
        for i, v in enumerate(self.vertices):
            if not self.bitFlag2 & 0x100:
                for b in self.bones:
                    if b.name not in obj.vertex_groups:
                        obj.vertex_groups.new(name=b.name)

            else:
                for w in range(4):
                    b = self.bones[v.bones[w]]

                    if b.name not in obj.vertex_groups:
                        obj.vertex_groups.new(name=b.name)

                    obj.vertex_groups[b.name].add([i], float(v.weights[w] / 255), 'ADD')

        # Link Blender object
        bpy.context.collection.objects.link(obj)

        # Adjust the orientation of the model
        obj.matrix_local = Matrix.Rotation(math.pi * 0.5, 4, [1, 0, 0])

        # Deselect all, then select imported model
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj


class GR2Bone():
    def __init__(self, f, offset):

        f.seek(offset)

        self.name = rstring(f)
        self.parentIndex = unpack(b'<i', f.read(4))[0]
        f.seek(0x40, 1)
        self.rootToBone = [rfloat32(f) for _ in range(16)]


class GR2Loader():
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self, operator):
        with open(self.filepath, 'rb') as f:

            # Cancel import if this is a non Bio-Ware Austin / SWTOR GR2 file
            if f.read(4) != b'GAWB':
                operator.report({'ERROR'}, ("\'%s\' is not a valid SWTOR gr2 file.")
                                % self.filepath)
                return {'CANCELLED'}

            f.seek(0x14)

            self.fileType = ruint32(f)  # GR2 file type, 0 = geometry, 1 = geometry with .clo file, 2 = skeleton

            self.numMeshes = ruint16(f)              # Number of meshes in this file
            self.numMaterials = ruint16(f)           # Number of materials in this file
            self.numBones = ruint16(f)               # Number of bones in this file

            f.seek(0x54)

            self.offsetMeshHeader = ruint32(f)       # Mesh header offset address
            self.offsetMaterialHeader = ruint32(f)   # Material header offset address
            self.offsetBoneStructure = ruint32(f)    # Bone structure offset address

            # Meshes
            self.meshes = [GR2Mesh(f, self.offsetMeshHeader + mesh * 0x28)
                           for mesh in range(self.numMeshes)]

            # Materials
            # NOTE: I wish there was a more efficient way to do this!
            self.materials = []
            if self.numMaterials == 0:
                for mesh in self.meshes:
                    if mesh.bitFlag2 & 0x20:
                        for enum, _ in enumerate(mesh.pieces):  # Use "mesh name".00x for name
                            self.materials.append(mesh.name + "." + str(f'{enum:03d}'))
            else:
                f.seek(self.offsetMaterialHeader)
                for _ in range(self.numMaterials):              # Use string name for name
                    self.materials.append(rstring(f))

            # Skeleton bones
            self.bones = []
            for b in range(self.numBones):
                self.bones.append(GR2Bone(f, self.offsetBoneStructure + b * 0x88))

    def build(self, import_collision=False):
        # Create Materials
        for material in self.materials:
            newMaterial = bpy.data.materials.new(name=material)
            newMaterial.use_nodes = True

        # Create Meshes
        for mesh in self.meshes:
            if "collision" in mesh.name and not import_collision:
                continue
            mesh.build(self)

        # Create Armature
        if self.fileType == 2 and len(self.bones) > 0:
            bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
            armature = bpy.context.object.data
            armature.name = os.path.splitext(os.path.split(self.filepath)[1])[0]
            armature.display_type = 'STICK'

            for b in self.bones:
                bone = armature.edit_bones.new(b.name)
                bone.tail = [0, 0.00001, 0]

            for i, b in enumerate(self.bones):
                bone = armature.edit_bones[i]
                if b.parentIndex >= 0:
                    bone.parent = armature.edit_bones[b.parentIndex]

                matrix = Matrix([b.rootToBone[u*4:u*4+4] for u in range(4)])
                matrix.transpose()
                bone.transform(matrix.inverted())

            bpy.context.object.name = armature.name
            bpy.context.object.matrix_local = Matrix.Rotation(math.pi * 0.5, 4, 'X')
            bpy.ops.object.mode_set(mode='OBJECT')

            self.armature = bpy.context.object


def load(operator, context, filepath=""):
    with ProgressReport(context.window_manager) as progress:
        progress.enter_substeps(3, "Importing \'%s\' ..." % filepath)

        mainLoader = GR2Loader(filepath)

        progress.step("Parsing file ...", 1)
        mainLoader.parse(operator)
        progress.step("Done, building ...", 2)

        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        mainLoader.build(operator.import_collision)
        progress.leave_substeps("Done, finished importing: \'%s\'" % filepath)

    return {'FINISHED'}
