# <pep8 compliant>

"""
This script imports Star Wars: The Old Republic models into Blender.

Usage:
Run this script from "File->Import" menu and then load the desired GR2 model file.

https://github.com/SWTOR-Slicers/WikiPedia/wiki/GR2-File-Structure
(32-bit version. 64-bit version is implemented in the Add-on but not documented)

About the Add-on's structure and entry points:

class ImportJBA
    invoke()       <- Called by File->Import menu option
    Execute()      <- Called by other Add-ons and scripts.
        Load()     <- Called by other modules in this Add-on.
            Read()
            Build()
"""

import json  # For dict-to-stringProperty translations 
import os
from math import pi as PI
from tracemalloc import start
from typing import Optional, Set
import time

import bpy
from bpy import app
from bpy.props import BoolProperty, CollectionProperty, FloatProperty, StringProperty
from bpy.types import Context, Operator, OperatorFileListElement
# from bpy_extras.io_utils import ImportHelper
from mathutils import Color, Matrix, Vector

from ..types.gr2 import Granny2
from ..utils.binary import ArrayBuffer, DataView
from ..utils.number import decodeHalfFloat
from ..utils.string import readString

from ..types.shared import job_results  # add-on-wide global-like dict


# Some bones lists for cosmetic differentiation
hook_bones = ['Camera',
              'NamePlate',
              'attach_nameplate_fallback',
              'socket_saber_right',
              'socket_saber_left',
              'socket_pistol_right',
              'socket_pistol_left',
              ]



class ImportGR2(Operator):
    """
    Import SWTOR GR2 file format (.gr2)
    
    Produces a file browser for manually
    selecting one or multiple .gr2 object
    files, including skeleton ones.
    """
    bl_idname = "import_mesh.gr2"  # DO NOT CHANGE
    bl_description = "Import SWTOR game objects and skeletons (armatures).\n\n• Compatible with both SWTOR 32 and 64-bit files\n   (before and after Game Update 7.2.1).\n\n• Can import selections of multiple files at once"
    bl_label = "Import SWTOR (.gr2)"
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

    filename_ext = ".gr2"

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the GR2 file",
        type=OperatorFileListElement,
    )
    
    filter_glob: StringProperty(
        default="*.gr2",
        options={'HIDDEN'},
    )



    # Importing parameters' properties

    import_collision: BoolProperty(
        name="Import Collision Mesh",
        description="Imports the object's collision boundary mesh if present in the file\n(it can be of use when exporting models to other apps and game engines)",
        default=False,
    )

    name_as_filename: BoolProperty(
        name="Name As Filename",
        description="Names the imported Blender objects with their filenames instead of their\ninternal 'art names' (the object's mesh data always keeps the 'art name').\n\n.gr2 objects' internal 'art names' typically match their files' names,\nbut sometimes they difer, which can break some tools and workflows.\n\nIn case of multiple mesh files (containing a main object plus secondary ones\nand / or Engine Objects such as Colliders), only the main object is renamed",
        # default=True,
    )

    apply_axis_conversion: BoolProperty(
        name="Axis Conversion",
        description="Permanently converts the imported object\nto Blender's 'Z-is-Up' coordinate system\nby 'applying' a x=90º rotation.\n\nNOT RECOMMENDED FOR MODDING SWTOR.\n\nSWTOR's coordinate system is 'Y-is-up' vs. Blender's 'Z-is-up'.\nTo compensate for that in a reversible manner, this importer\nnormally sets the object's rotation to X=90º at the Object level.\n\nAs this can be a nuisance outside a modding use case,\nthis option applies it at the Mesh level, instead",
        default=False,
    )

    scale_object: BoolProperty(
        name="Scale Object",
        description="Scales imported objects, characters and armatures\nat the Mesh level.\n\nNOT RECOMMENDED FOR MODDING SWTOR OR EXPORTING\nTO OTHER APPS AND ENGINES: Check their requirements and test first.\n\nSWTOR sizes objects in decimeters, while Blender defaults to meters.\nThis mismatch, while innocuous, is an obstacle when doing physics\nsimulations, automatic weighting from bones, or other processes\nwhere Blender requires real world-like sizes to succeed",
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
        description="Temporarily overrides this Add-on's settings\with those of older versions for compatibility with older tools",
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
        default=False,
    )



    def invoke(self, context, event):
        # To be able to set the class' properties to the values in the
        # Add-on's preferences and show them in the File Browser's options,
        # we use an Invoke function instead of directly using ImportHelper in
        # the class definition, to be able to put there the required code.              
        
        prefs = context.preferences.addons["io_scene_gr2"].preferences
        
        self.import_collision       = prefs.gr2_import_collision
        self.name_as_filename       = prefs.gr2_name_as_filename
        self.apply_axis_conversion  = prefs.gr2_apply_axis_conversion
        self.scale_object           = prefs.gr2_scale_object
        self.scale_factor           = prefs.gr2_scale_factor
        self.job_results_rich       = False
        self.job_results_accumulate = False

        # Handling of filepath in case of being
        # filled as a param in an external call.
        if not self.filepath:
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            return self.execute(context)        


    def execute(self, context):
        # type: (Context) -> Set[str]

        if not self.job_results_accumulate:
            job_results['objs_names'] = []
            job_results['files_objs_names'] = {}

        job_results['job_origin'] = self.bl_idname
                    
        if self.job_results_rich and not 'files_objs_names' in job_results:
            job_results['files_objs_names'] = {}


        paths = [os.path.join(self.directory, file.name) for file in self.files if file.name.lower().endswith(self.filename_ext)]

        if not paths:
            paths.append(self.filepath)

        # Clear filebrowser-related properties now
        # that they have been read and have no more
        # use so that they don't persist if the class
        # breaks before finishing its execution
        # (it makes debugging difficult, otherwise).
        self.files.clear()
        self.filepath = ""

        print()

        for path in paths:
            if not load(self, context, path):
                return {'CANCELLED'}

        bpy.context.scene.io_scene_gr2_last_job = json.dumps(job_results)

        return {"FINISHED"}


def read(operator, filepath):
    # type: (Operator, str) -> Optional[Granny2]
    with open(filepath, 'rb') as file:
        buffer = ArrayBuffer()
        buffer.fromfile(file, os.path.getsize(filepath))

    dv = DataView(buffer)
    pos = 0

    # Cancel import if this is not a BioWare Austin / SWTOR GR2 file.
    if dv.getUint32(pos, 1) != 0x42574147:
        operator.report({'ERROR'}, f"{filepath} is not a valid SWTOR gr2 file.")
        return None

    gr2 = Granny2()

    pos = 4

    gr2.version = dv.getUint32(pos, 1)                   # GR2 file version


    pos = 20  # 0x14, skipping the version numbers, magic numbers and collision offset

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



    offset_mesh_header = None
    offset_material_name_offsets = None
    offset_bone_struct = None
    # 0x50
    # skipping offset CachedOffset as we don't use it
    if gr2.version == 5:
        pos += 8  # 0x54
        offset_mesh_header = dv.getUint64(pos, 1)            # Mesh header offset address
        pos += 8
        offset_material_name_offsets = dv.getUint64(pos, 1)  # Material header offset address
        pos += 8
        offset_bone_struct = dv.getUint64(pos, 1)            # Bone structure offset address
        pos += 8
    else:	
        pos += 4  # 0x54
        offset_mesh_header = dv.getUint32(pos, 1)            # Mesh header offset address
        pos += 4
        offset_material_name_offsets = dv.getUint32(pos, 1)  # Material header offset address
        pos += 4
        offset_bone_struct = dv.getUint32(pos, 1)            # Bone structure offset address
        pos += 4


    # Meshes
    gr2.mesh_buffer = {}

    mesh_bin_size = 40

    if gr2.version == 5:
        mesh_bin_size = 64

    for i in range(num_meshes):
        pos = offset_mesh_header + (i * mesh_bin_size)
        # Mesh name

        mesh = None

        if gr2.version == 5:
            mesh = Granny2.Mesh(readString(dv, pos, posOverride= dv.getUint64(pos, True)))
            pos += 8
        else:
            mesh = Granny2.Mesh(readString(dv, pos))
            pos += 4
        
        # operator.report({'INFO'}, f"Read the header for mesh {mesh.name}... {pos}")  # for diagnostics

        # BitFlag1
        pos += 4
        # Number of sub meshes that make up this mesh
        num_pieces = dv.getUint16(pos, 1)
        pos += 2
        # Number of bones used by this mesh
        num_used_bones = dv.getUint16(pos, 1)
        pos += 2
        # BitFlag2

        bit_flag2 = None
        vertex_size = None

        if gr2.version == 5:
            bit_flag2 = dv.getUint32(pos, 1)
            pos += 4
            # 12 = collision, 24 = static, 32+ = dynamic
            vertex_size = dv.getUint32(pos, 1)
            pos += 4
        else:
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

        if gr2.version == 5:
            # Offset of the vertices buffer for this mesh
            mesh.offset_vertex_buffer = dv.getUint64(pos, 1)
            pos += 8
             # Offset of the sub mesh header(s)
            mesh.offset_piece_headers = dv.getUint64(pos, 1)
            pos += 8
            # Offset of the indices buffer for this mesh
            mesh.offset_indices_buffer = dv.getUint64(pos, 1)
            pos += 8
            # Offset of the bones buffer for this mesh
            mesh.offset_bones_buffer = dv.getUint64(pos, 1)
            pos += 8
        else:
            mesh.offset_vertex_buffer = dv.getUint32(pos, 1)
            pos += 4
            mesh.offset_piece_headers = dv.getUint32(pos, 1)
            pos += 4
            mesh.offset_indices_buffer = dv.getUint32(pos, 1)
            pos += 4
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
                    [(dv.getUint8(pos + k) - 127) / 127 for k in range(4)])
                pos += 4
                vertex.tangents = Vector(
                    [(dv.getUint8(pos + k) - 127) / 127 for k in range(4)])
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

        boneSize = 32 if gr2.version == 5 else 28

        mesh.bone_buffer = {j: Granny2.Bone(dv, mesh.offset_bones_buffer + (j * boneSize), gr2.version, True)
                            for j in range(num_used_bones)}

        gr2.mesh_buffer[i] = mesh

    # Materials
    # NOTE: I wish there was a more efficient way to do this!
    gr2.material_names = {}
    if num_materials:
        pos = offset_material_name_offsets
        for i in range(num_materials):

            if gr2.version == 5:
                gr2.material_names[i] = readString(dv, pos, posOverride=dv.getUint64(pos, 1))
                pos += 8
            else:
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

    bone_size_of_mem = 144 if gr2.version == 5 else 136

    gr2.bone_buffer = {i: Granny2.Bone(dv, offset_bone_struct + (i * bone_size_of_mem), gr2.version)
                       for i in range(num_bones)}

    return gr2

def build(gr2,
          filepath="",
          import_collision      = None,
          name_as_filename      = None,
          scale_object          = None,
          scale_factor          = None,
          apply_axis_conversion = None,
          ):
    # type: (Granny2, str, bool, bool, bool, float, bool) -> None

    # Data that will be used for publishing results
    # via scene props to other add-ons
    resulting_single_mesh_blender_objects = []
    
    # NOTE: Create Materials
    for i, material in gr2.material_names.items():
        bpy.data.materials.new(name=material).use_nodes = True

    # NOTE: Create Meshes
    for i, mesh in gr2.mesh_buffer.items():

        # When using the name_as_filename option, we assume that, in the case of
        # multiple mesh models/files (which get separated into multiple objects,
        # as Blender doesn't support more than one mesh data block per object),
        # the first mesh in the list is the main one. If not so, some heuristics
        # could be added.
        use_file_name_as_object_name = (i == 0 and name_as_filename is True)


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
                material = gr2.material_names[j if piece.material_index == 4294967295 else piece.material_index]
                bmesh.materials.append(bpy.data.materials[material])

                for _ in range(piece.num_polygons):
                    material_indices.append(j)

        if mesh.bit_flag2 & 2:   # 0x02
            # NOTE: We store 'temp' normals in loops, since validate() may alter final mesh,
            #       we can only set custom loop normals *after* calling it.
            bmesh.create_normals_split()  # DEPRECATED IN BLENDER 4.1
            bmesh.uv_layers.new(do_init=False)
            if mesh.bit_flag2 & 64:  # 0x40
                bmesh.uv_layers.new(do_init=False)
            if mesh.bit_flag2 & 128:  # 0x80
                bmesh.uv_layers.new(do_init=False)

            for j, polygon in enumerate(bmesh.polygons):
                loop_indices = polygon.loop_indices

                for k, loop_index in enumerate(loop_indices):
                    v = mesh.vertex_buffer[mesh.indices_buffer[j][k]]
                    bmesh.loops[loop_index].normal = [v.normals.x, v.normals.y, v.normals.z]  # DEPRECATED IN BLENDER 4.1
                    bmesh.uv_layers[0].data[loop_index].uv = [v.uv_layer0.x, 1 - v.uv_layer0.y]

                    if mesh.bit_flag2 & 64:  # 0x40
                        bmesh.uv_layers[1].data[loop_index].uv = [v.uv_layer1.x, 1 - v.uv_layer1.y]

                    if mesh.bit_flag2 & 128:  # 0x80
                        bmesh.uv_layers[2].data[loop_index].uv = [v.uv_layer2.x, 1 - v.uv_layer2.y]

                polygon.material_index = material_indices[j]

            bmesh.validate(clean_customdata=False)

            # Mesh Normals
            custom_loop_normals = [0.0] * (len(bmesh.loops) * 3)
            bmesh.loops.foreach_get("normal", custom_loop_normals)
            bmesh.polygons.foreach_set("use_smooth", [True] * len(bmesh.polygons))
            bmesh.normals_split_custom_set(tuple(zip(*(iter(custom_loop_normals),) * 3)))
            bmesh.use_auto_smooth = True  # DEPRECATED IN BLENDER 4.1

        # Create Blender Object
        if use_file_name_as_object_name:
            # Crude filepath separator-agnostic handling
            if "\\" in filepath:
                dir_sep = "\\"
            else:
                dir_sep = "/"
            file_name = filepath.split(dir_sep)[-1][:-4]
            ob = bpy.data.objects.new(file_name, bmesh)
        else:
            ob = bpy.data.objects.new(mesh.name, bmesh)

        resulting_single_mesh_blender_objects.append(ob.name)


        # Create Vertex Groups
        for bone in mesh.bone_buffer.values():
            ob.vertex_groups.new(name=bone.name)
            entry = ob.bone_bounds.add()
            entry.name = bone.name
            entry.bounds = bone.bounds

        # Populate Vertex Groups
        for j, vertex in mesh.vertex_buffer.items():
            if mesh.bit_flag2 & 256:
                for index in range(4):
                    bone = mesh.bone_buffer[vertex.bone_indices[index]].name
                    ob.vertex_groups[bone].add([j], float(vertex.bone_weights[index] / 255), 'ADD')

        # Link Blender Object
        bpy.context.collection.objects.link(ob)

        # Adjust the orientation of the model
        ob.matrix_local = Matrix.Rotation(PI * 0.5, 4, 'X')

        # Deselect all, then select imported model
        bpy.ops.object.select_all(action='DESELECT')
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        
        # Apply transformation options and record them
        # in custom object properties 
        if scale_object or apply_axis_conversion:
            if scale_object:
                ob.scale *= scale_factor
                
            bpy.ops.object.transform_apply(location=False, rotation=apply_axis_conversion, scale=scale_object, properties=True)
            
        ob["gr2_scale"] = scale_factor
        ob["gr2_axis_conversion"] = apply_axis_conversion
            


    # Create Armature
    if gr2.type_flag == 2 and len(gr2.bone_buffer) > 0:
        bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
        armature: bpy.types.Armature = bpy.context.object.data
        armature.name = filepath.split(os.sep)[-1][:-4]
        armature.display_type = 'STICK'

        # Bones creation
        for bone in gr2.bone_buffer.values():
            new_bone = armature.edit_bones.new(bone.name)
            new_bone.tail = [0, 0.00001, 0]

        # Bones hierarchy organization
        for i, bone in gr2.bone_buffer.items():
            armature_bone = armature.edit_bones[i]

            if bone.parent_index >= 0:
                armature_bone.parent = armature.edit_bones[bone.parent_index]

            matrix = Matrix([bone.root_to_bone[j*4:j*4+4] for j in range(4)])
            # print(matrix, i , bone.name)  # for diagnostics
            matrix.transpose()
            armature_bone.transform(matrix.inverted())

        bpy.context.object.name = armature.name
        resulting_single_mesh_blender_objects.append(bpy.context.object.name)

        bpy.context.object.matrix_local = Matrix.Rotation(PI * 0.5, 4, 'X')
        
        # Apply transformation options and record them
        # in custom object properties 
        if scale_object:
            bpy.context.object.scale *= scale_factor
            bpy.context.object["gr2_scale"] = scale_factor
        else:
            bpy.context.object["gr2_scale"] = 1.0

        bpy.ops.object.mode_set(mode='OBJECT')

        if apply_axis_conversion:
            bpy.ops.object.select_all(action='DESELECT')
            ob=bpy.data.objects[armature.name]
            ob.select_set(True)
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=scale_object, properties=True )
            ob["gr2_axis_conversion"] = True
        else:
            ob=bpy.data.objects[armature.name]
            ob["gr2_axis_conversion"] = False

        
    return resulting_single_mesh_blender_objects


def load(operator, context, filepath = ""):
    # type: (Operator, Context, str) -> bool
    """
    This is the operator called by all other tools (either in this Add-on
    or in other ones) for actual object importing operations. Externally,
    it is exposed as bpy.ops.import_mesh.gr2().
    
    The operator param is being passed the calling class' self.
    """

    # .gr2 data parsing and mesh assembling section
    mesh = read(operator, filepath=filepath)
    
    print(f"FILE: {filepath}")


    # Blender object from mesh section
    if mesh:

        start_time = time.time()
        
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        if operator.enforce_neutral_settings:
            objects_names = build(mesh,
                                  filepath              = filepath,
                                  import_collision      = False,
                                  name_as_filename      = False,
                                  scale_object          = False,
                                  scale_factor          = 1.0,
                                  apply_axis_conversion = False,
                                  )
        else:
            if operator.bl_idname == 'IMPORT_MESH_OT_gr2' and operator.options.is_invoke:
                # Called via Blender's Import Menu's Import .gr2 option:
                # use the possibly user-manually altered properties
                # exposed in the File Browser.
                # (operator was passed self.)
                objects_names = build(mesh,
                                      filepath              = filepath,
                                      import_collision      = operator.import_collision,
                                      name_as_filename      = operator.name_as_filename,
                                      scale_object          = operator.scale_object,
                                      scale_factor          = operator.scale_factor,
                                      apply_axis_conversion = operator.apply_axis_conversion,
                                      )
            else:
                # Called via other Import Menu options (such as the
                # .json Character importer) or code not from this Add-on:
                # use the preferences' settings.
                prefs = bpy.context.preferences.addons["io_scene_gr2"].preferences
                objects_names = build(mesh,
                                      filepath              = filepath,
                                      import_collision      = prefs.gr2_import_collision,
                                      name_as_filename      = prefs.gr2_name_as_filename,
                                      scale_object          = prefs.gr2_scale_object,
                                      scale_factor          = prefs.gr2_scale_factor,
                                      apply_axis_conversion = prefs.gr2_apply_axis_conversion,
                                      )

        
        # job_results-filling section
        
        job_results['job_origin'] = operator.bl_idname

        job_results['objs_names'].extend(objects_names)

        if operator.job_results_rich:
            if 'resources' in filepath:
                job_results['files_objs_names'][ filepath.replace("\\", "/").partition("resources/")[2] ] = objects_names
            else:
                job_results['files_objs_names'][ filepath.replace("\\", "/") ] = objects_names

        elapsed_time = time.time() - start_time
        if objects_names:
            print(f"OBJS: {objects_names}")
            print(f"TIME: {elapsed_time:.3f} s.")
            print()
        else:
            print("FAILED!!!")
            print()

        
        return True
    else:
        return False