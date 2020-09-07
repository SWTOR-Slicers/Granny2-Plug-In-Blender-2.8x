# <pep8 compliant>

import os
from struct import pack

import bpy

from mathutils import Matrix
from bpy_extras.wm_utils.progress_report import (
    ProgressReport,
    ProgressReportSubstep,
)


def uint8(val):
    return pack(b'B', val)


def float8(val):
    return int((val * 127.5) + 128).to_bytes(1, byteorder="little", signed=False)


def uint16(val):
    return pack(b'<H', val)


def float16(val):
    return pack(b'<e', val)


def uint32(val):
    return pack(b'<I', val)


def float32(val):
    return pack(b'<f', val)


def calc_padding(val):
    count = val
    while count % 16 != 0:
        count += 1
    return val + (count - val)


def zero_padding(val):
    count = val
    while count % 16 != 0:
        count += 1
    return bytes(count - val)


def name_compat(name):
    if name is None:
        return 'None'

    return name.replace(' ', '_')


def write_file(operator, filepath, objects, depsgraph, scene,
               EXPORT_GLOBAL_MATRIX=None,
               EXPORT_HAS_CLO=False,
               progress=ProgressReport(),
               ):

    if EXPORT_GLOBAL_MATRIX is None:
        EXPORT_GLOBAL_MATRIX = Matrix()

    def bx(bone, axis):
        blst = [v_dict[v][axis] for v in v_dict if bone in [
            v_dict[v]["B1"], v_dict[v]["B2"], v_dict[v]["B3"], v_dict[v]["B4"]]]
        return [0] if len(blst) == 0 else blst

    with ProgressReportSubstep(progress, 2, "GR2 Export path: \'%s\'" % filepath,
                               "GR2 Export Finished") as subprogress1:

        # Initialize totals, these are updated each object
        tot_v = tot_tex = tot_nor = 1

        # Check the number of objects selected and if there is more than one, cancel the export
        if len(objects) != 1:
            operator.report({'ERROR'},
                            ("Unable to complete export, %i objects selected. \n"
                             "This addon only supports exporting one object at a time.") % len(objects))
            return {'CANCELLED'}

        # Set-up dictionaries and lists to store or work with the mesh data
        v_dict = {}
        f_dict = {}

        # Collect the mesh data
        subprogress1.enter_substeps(
            1, "Parsing the geometry data via Blender's Data API")
        for i, ob_main in enumerate(objects):
            obs = [(ob_main, ob_main.matrix_world)]
            for ob, ob_mat in obs:
                with ProgressReportSubstep(subprogress1, 6) as subprogress2:
                    nor_unique_count = tan_unique_count = tex_unique_count = 0
                    ob_for_convert = ob.original

                    try:
                        me = ob_for_convert.to_mesh()
                    except RuntimeError:
                        me = None

                    if me is None:
                        continue

                    me.transform(EXPORT_GLOBAL_MATRIX @ ob_mat)
                    # If negative scaling, we have to invert the normals...
                    if ob_mat.determinant() < 0.0:
                        me.flip_normals()

                    f_tex = len(me.uv_layers) > 0
                    tex_layer = me.uv_layers.active.data[:] if f_tex else None

                    me_v = me.vertices[:]

                    # Make our own list so it can be sorted to reduce context switching
                    face_index_pairs = [(face, index)
                                        for index, face in enumerate(me.polygons)]

                    # Make sure there is something to write
                    if not len(face_index_pairs) + len(me.vertices):
                        # Clean up
                        ob_for_convert.to_mesh_clear()

                    if face_index_pairs:
                        me.calc_normals_split()

                    me_lp = me.loops

                    # Gather the materials used by this model
                    me_mats = me.materials[:]
                    mat_names = [m.name if m else None for m in me_mats]
                    num_mats = len(mat_names)

                    face_mats = {}
                    for face in me.polygons:
                        face_mats.setdefault(
                            face.material_index, []).append(face.index)

                    m_idx = {}
                    for j in range(num_mats):
                        m_idx[j] = len(
                            face_mats[j]) if j in face_mats.keys() else 0

                    # Mesh Name
                    obnamestring = name_compat(ob.name)

                    # Avoid bad index errors
                    if not me_mats:
                        me_mats = [None]
                        mat_names = [name_compat(None)]

                    subprogress2.step()  # 1

                    # VERTEX COORDS
                    for v in me_v:
                        v_dict[v.index] = {}
                        v_dict[v.index]['X'] = v.co[0]
                        v_dict[v.index]['Y'] = v.co[1]
                        v_dict[v.index]['Z'] = v.co[2]

                    subprogress2.step()

                    # BONE WEIGHTS
                    v_bon = {}
                    boneNames = ob.vertex_groups.keys()
                    if boneNames:
                        # Create a dictionary keyed by face id and listing, for each vertex, and the vertex
                        # groups it belongs to.
                        vgroupsMap = [[] for _i in range(len(me_v))]
                        for v_idx, v_ls in enumerate(vgroupsMap):
                            v_bon[v_idx] = {}
                            for g in me_v[v_idx].groups:
                                v_bon[v_idx][g.group] = g.weight
                        bon_names = {g.index: g.name for g in ob.vertex_groups}
                    else:
                        bon_names = {0: obnamestring}
                    num_b = len(bon_names)

                    subprogress2.step()  # 2

                    # NORMALS COORDS
                    v_nor = {}
                    nor_key = nor_val = None
                    normals_to_idx = {}
                    nor_get = normals_to_idx.get
                    loops_to_normals = [0] * len(me_lp)
                    for f, f_index in face_index_pairs:
                        for l_idx in f.loop_indices:
                            nor_key = (
                                me_lp[l_idx].normal[0], me_lp[l_idx].normal[1], me_lp[l_idx].normal[2])
                            nor_val = nor_get(nor_key)
                            if nor_val is None:
                                nor_val = normals_to_idx[nor_key] = nor_unique_count
                                v_nor[nor_val] = nor_key
                                nor_unique_count += 1
                            loops_to_normals[l_idx] = nor_val
                    del normals_to_idx, nor_get, nor_key, nor_val

                    subprogress2.step()  # 3

                    # TANGENTS COORDS
                    ctx = bpy.context.active_object.data
                    ctx.calc_tangents()

                    v_tan = {}
                    v_bts = {}
                    tan_key = tan_val = None
                    tangents_to_idx = {}
                    tan_get = tangents_to_idx.get
                    loops_to_tangents = [0] * len(ctx.loops)
                    # Loop faces
                    for face in ctx.polygons:
                        # Loop over face loop
                        for l_idx in [ctx.loops[i] for i in face.loop_indices]:
                            tan_key = (
                                l_idx.tangent[0], l_idx.tangent[1], l_idx.tangent[2])
                            bts_key = l_idx.bitangent_sign
                            tan_val = tan_get(tan_key)
                            if tan_val is None:
                                tan_val = tangents_to_idx[tan_key] = tan_unique_count
                                v_tan[tan_val] = tan_key
                                v_bts[tan_val] = bts_key
                                tan_unique_count += 1
                            loops_to_tangents[l_idx.index] = tan_val
                    del tangents_to_idx, tan_get, tan_key, tan_val

                    subprogress2.step()  # 4

                    # UV TEXTURE COORDS
                    v_tex = {}
                    if f_tex:
                        # In case removing some of these dont get defined.
                        tex = f_index = tex_index = tex_key = tex_val = tex_ls = None

                        tex_face_mapping = [None] * len(face_index_pairs)

                        tex_dict = {}
                        tex_get = tex_dict.get
                        for f, f_index in face_index_pairs:
                            tex_ls = tex_face_mapping[f_index] = []
                            for tex_index, l_index in enumerate(f.loop_indices):
                                tex = tex_layer[l_index].uv

                                # Include the vertex index in the key so we don't share UV's between vertices
                                tex_key = me_lp[l_index].vertex_index, (
                                    tex[0], tex[1])

                                tex_val = tex_get(tex_key)
                                if tex_val is None:
                                    tex_val = tex_dict[tex_key] = tex_unique_count
                                    v_tex[tex_val] = tex_key
                                    tex_unique_count += 1
                                tex_ls.append(tex_val)

                        del tex_dict, tex, f_index, tex_index, tex_ls, tex_get, tex_key, tex_val
                        # Only need tex_unique_count and uv_face_mapping

                    subprogress2.step()  # 5

                    # FACES
                    f_lst = []
                    for f, f_index in face_index_pairs:

                        f_v = [(vi, me_v[v_idx], l_idx) for vi, (v_idx, l_idx) in
                               enumerate(zip(f.vertices, f.loop_indices))]

                        for vi, v, li in f_v:

                            wn = 1
                            if boneNames:
                                if v.index in v_bon:
                                    for x, y in sorted(v_bon[v.index].items(), key=lambda xy: (xy[1], xy[0]),
                                                       reverse=True):
                                        v_dict[v.index]["W" + str(wn)] = y
                                        wn += 1
                                while wn <= 4:
                                    v_dict[v.index]["W" + str(wn)] = float(0.0)
                                    wn += 1

                            bn = 1
                            if boneNames:
                                for x, y in sorted(v_bon[v.index].items(), key=lambda xy: (xy[1], xy[0]),
                                                   reverse=True):
                                    v_dict[v.index]["B" + str(bn)] = x
                                    bn += 1
                                while bn <= 4:
                                    v_dict[v.index]["B" + str(bn)] = v_dict[v.index]["B1"] if \
                                        "B1" in v_dict[v.index].keys() else int(0)
                                    bn += 1

                            v_dict[v.index]["Nx"] = v_nor[loops_to_normals[li]][0]
                            v_dict[v.index]["Ny"] = v_nor[loops_to_normals[li]][1]
                            v_dict[v.index]["Nz"] = v_nor[loops_to_normals[li]][2]
                            v_dict[v.index]["Ns"] = v_bts[loops_to_tangents[li]]
                            v_dict[v.index]["Tx"] = v_tan[loops_to_tangents[li]][0]
                            v_dict[v.index]["Ty"] = v_tan[loops_to_tangents[li]][1]
                            v_dict[v.index]["Tz"] = v_tan[loops_to_tangents[li]][2]
                            v_dict[v.index]["Ts"] = int(
                                0 - v_bts[loops_to_tangents[li]])
                            v_dict[v.index]["U"] = v_tex[tex_face_mapping[f_index][vi]][1][0]
                            v_dict[v.index]["V"] = v_tex[tex_face_mapping[f_index][vi]][1][1]

                            f_lst.append(v.index)

                        f_dict[f_index] = list(f_lst)
                        f_lst.clear()

                    del v_bon, v_nor, v_tan, v_bts, v_tex

                    subprogress2.step()  # 6

                    # Make the indices global rather then per mesh
                    tot_v += len(me_v)
                    tot_tex += tex_unique_count
                    tot_nor += nor_unique_count

                    # List of keys in v_dict
                    if not boneNames:
                        keys = ["Nx", "Ny", "Nz", "Ns",
                                "Tx", "Ty", "Tz", "Ts", "U", "V"]
                    else:
                        keys = ["W1", "W2", "W3", "W4", "B1", "B2", "B3", "B4",
                                "Nx", "Ny", "Nz", "Ns", "Tx", "Ty", "Tz", "Ts", "U", "V"]

                    # Totals
                    num_v = len(v_dict)
                    num_f = len(f_dict)

                    min_x = min([[iv for ik, iv in ov.items()][0]
                                 for ok, ov in v_dict.items()])
                    min_y = min([[iv for ik, iv in ov.items()][1]
                                 for ok, ov in v_dict.items()])
                    min_z = min([[iv for ik, iv in ov.items()][2]
                                 for ok, ov in v_dict.items()])
                    max_x = max([[iv for ik, iv in ov.items()][0]
                                 for ok, ov in v_dict.items()])
                    max_y = max([[iv for ik, iv in ov.items()][1]
                                 for ok, ov in v_dict.items()])
                    max_z = max([[iv for ik, iv in ov.items()][2]
                                 for ok, ov in v_dict.items()])

                    # clean up
                    ob_for_convert.to_mesh_clear()

        # If the file doesn't exist, create it, if it does, clear it
        subprogress1.enter_substeps(
            1, "Parsing complete, writing the geometry data to file.")
        open(filepath, "wb")
        with open(filepath, "rb+") as f:
            fw = f.write

            with ProgressReportSubstep(subprogress1, 6) as subprogress2:
                # Pos 0x00
                # Write the MAGIC bytes
                fw(b'GAWB')
                # Write the Major Version
                fw(uint32(4))
                # Write the Minor Version
                fw(uint32(3))
                # Write the BNRY / LTLE offset
                off_0C0 = f.tell()
                fw(uint32(0))  # We'll populate this later

                subprogress2.step()  # 1

                # Pos 0x10
                # Write the number of cached offsets
                off_010 = f.tell()
                fw(uint32(0))  # We'll populate this later
                # Write the type of GR2 file
                fw(uint32(1)) if EXPORT_HAS_CLO else fw(uint32(0))
                # Write the number of meshes
                fw(uint16(1))
                # Write the number of materials
                fw(uint16(num_mats))
                # If this is a skeleton file, how many bones are there?
                fw(uint16(0))  # 0 - This isn't a skeleton file
                # Write the number of attachments
                # TODO Figure out how to handle attachments, 0 for now.
                fw(uint16(0))
                # Write 16 x 00 bytes
                fw(uint32(0) + uint32(0) + uint32(0) + uint32(0))

                subprogress2.step()  # 2

                # Pos 0x30
                fw(float32(min_x))  # Min X
                fw(float32(min_y))  # Min Y
                fw(float32(min_z))  # Min Z
                fw(float32(1))      # Always 00 00 80 3F
                fw(float32(max_x))  # Max X
                fw(float32(max_y))  # Max Y
                fw(float32(max_z))  # Max Z
                fw(float32(1))      # Always 00 00 80 3F

                subprogress2.step()  # 3

                # Pos 0x50
                off_050 = f.tell()
                # Write the offset of the cached offsets section
                fw(uint32(0))  # We'll populate this later
                # Write the offset of the mesh header
                off_054 = f.tell()
                fw(uint32(112))
                # Write the offset of the material names offsets section
                off_058 = f.tell()
                fw(uint32(112 + 48 + (num_mats * 48)))
                # Write 4 x 00
                fw(uint32(0))
                # Write the offset of the attachments section
                # TODO Figure out how to handle attachments, 0 for now.
                fw(uint32(0))
                # Write 00 byte until pos / 16 = int
                fw(zero_padding(f.tell()))

                subprogress2.step()  # 4

                # Pos 0x70
                off_070 = f.tell()
                # Write the mesh headers
                # Write the offset of the mesh name
                fw(uint32(0))  # We'll populate this later
                # Write bitFlag 1, 0 unles bones = 0, then 128
                fw(uint32(0)) if boneNames else fw(uint32(128))
                # Write the number of pieces that make-up the object
                fw(uint16(num_mats))
                # Write the number of bones used by this mesh
                fw(uint16(num_b))
                # Write bitFlag 2
                fw(uint8(47))
                fw(uint8(1))
                # Write the number of bytes used for each vertex
                fw(uint16(32 if boneNames else 24))
                # Write the number of vertices
                fw(uint32(len(me_v)))
                # Write the number of indices (3 x number of faces)
                fw(uint32(num_f * 3))
                # Write the offset of the mesh vertices section
                fw(uint32(160 + (num_mats * 48) + calc_padding(num_mats * 4)))
                # Write the offset of the mesh piece headers
                fw(uint32(160))
                # Write the offset of the mesh faces section
                fw(uint32(160 + (num_mats * 48) + calc_padding(num_mats *
                                                               4) + (num_v * (32 if boneNames else 24))))
                # Write the offset of the mesh bone section
                fw(uint32(160 + (num_mats * 48) + calc_padding(num_mats * 4) + (num_v * (32 if boneNames else 24)) +
                          calc_padding(num_f * 6)))
                # Write 00 byte until pos / 16 = int
                fw(zero_padding(f.tell()))

                subprogress2.step()  # 5

                # Write the mesh piece headers based on materials
                off_piece = f.tell()
                for piece in range(num_mats):
                    # Write the starting offset for the faces of this piece
                    if piece == 0:
                        fw(uint32(0))
                    else:
                        i = piece
                        i -= 1
                        fw(uint32(m_idx[i]))
                    # Write the number of faces used by this piece / material
                    fw(uint32(m_idx[piece]))
                    # Write the id of the material used by this piece
                    if num_mats < 0:
                        # If this piece has no material return int32: -1
                        fw(uint32(4294967295))
                        fw(uint32(4294967295))
                    else:
                        # Otherwise return the material id
                        fw(uint32(piece))
                        fw(uint32(piece))
                    # Write the bounding box for this piece
                    # TODO Figure out how to do this, for now use the global bounding box and hope for the best.
                    fw(float32(min_x))  # Min X
                    fw(float32(min_y))  # Min Y
                    fw(float32(min_z))  # Min Z
                    fw(float32(1))      # Always 00 00 80 3F
                    fw(float32(max_x))  # Max X
                    fw(float32(max_y))  # Max Y
                    fw(float32(max_z))  # Max Z
                    fw(float32(1))      # Always 00 00 80 3F

                subprogress2.step()  # 6

                # Write the offset for the name of each material
                off_mat_names = f.tell()
                for mat in range(num_mats):
                    fw(uint32(0))  # We'll populate this later
                # Write 00 byte until pos / 16 = int
                fw(zero_padding(f.tell()))

                # Write the attachments
                # TODO Figure out how to handle attachments.

                subprogress2.step()  # 7

                # Write the vertices
                off_verts = f.tell()
                for v in v_dict:
                    fw(float32(v_dict[v]["X"]))  # X
                    fw(float32(v_dict[v]["Y"]))  # Y
                    fw(float32(v_dict[v]["Z"]))  # Z
                    if all(key in v_dict[v] for key in keys):
                        if boneNames:  # Only dynamic models have bones
                            fw(uint8(int(v_dict[v]["W1"] * 255)))
                            fw(uint8(int(v_dict[v]["W2"] * 255)))
                            fw(uint8(int(v_dict[v]["W3"] * 255)))
                            fw(uint8(int(v_dict[v]["W4"] * 255)))
                            fw(uint8(v_dict[v]["B1"]))
                            fw(uint8(v_dict[v]["B2"]))
                            fw(uint8(v_dict[v]["B3"]))
                            fw(uint8(v_dict[v]["B4"]))
                        fw(float8(v_dict[v]["Nx"]))  # X
                        fw(float8(v_dict[v]["Ny"]))  # Y
                        fw(float8(v_dict[v]["Nz"]))  # Z
                        fw(float8(v_dict[v]["Ns"]))  # Binormal sign?
                        fw(float8(v_dict[v]["Tx"]))  # X
                        fw(float8(v_dict[v]["Ty"]))  # Y
                        fw(float8(v_dict[v]["Tz"]))  # Z
                        fw(float8(v_dict[v]["Ts"]))  # Bitangent sign?
                        fw(float16(v_dict[v]["U"]))  # U
                        fw(float16(1 - v_dict[v]["V"]))  # V
                    else:
                        fw(bytes(20))  # Just in case someone is dumb!

                subprogress2.step()  # 8

                # Write the face indices
                off_faces = f.tell()
                for face in range(num_f):
                    fw(uint16(f_dict[face][0]))  # v1
                    fw(uint16(f_dict[face][1]))  # v2
                    fw(uint16(f_dict[face][2]))  # v3
                fw(zero_padding(f.tell()))

                subprogress2.step()  # 9

                # Write the bones
                off_bones = f.tell()
                if not boneNames:  # This is a static model, which only have 1 root/default bone
                    fw(uint32(calc_padding(off_bones + (num_b * 28))))
                    fw(float32(min_x))  # Min X
                    fw(float32(min_y))  # Min Y
                    fw(float32(min_z))  # Min Z
                    fw(float32(max_x))  # Max X
                    fw(float32(max_y))  # Max Y
                    fw(float32(max_z))  # Max Z
                else:  # This is a dynamic model, which have 1 or more skeleton bones
                    bn = 0
                    for bo in range(num_b):
                        if bo == 0:
                            fw(uint32(calc_padding(off_bones + (num_b * 28)) + int(len(obnamestring) + 1) +
                                      len(''.join(mat_names)) + (1 * num_mats)))
                        else:
                            fw(uint32(calc_padding(off_bones + (num_b * 28)) + int(len(obnamestring) + 1) +
                                      len(''.join(mat_names)) + (1 * num_mats) + bn))
                        bn += int(len(bon_names[bo]) + 1)
                        fw(float32(min(bx(bo, "X"))))  # Min X Coord
                        fw(float32(min(bx(bo, "Y"))))  # Min Y Coord
                        fw(float32(min(bx(bo, "Z"))))  # Min Z Coord
                        fw(float32(max(bx(bo, "X"))))  # Max X Coord
                        fw(float32(max(bx(bo, "Y"))))  # Max Y Coord
                        fw(float32(max(bx(bo, "Z"))))  # Max Z Coord

                fw(zero_padding(f.tell()))

                subprogress2.step()  # 10

                # Write the strings
                off_mesh_string = f.tell()
                fw(bytes(obnamestring, 'utf-8'))  # Mesh Name
                fw(uint8(0))  # Terminate with 1 x 00 byte
                off_mat_strings = f.tell()
                for m in mat_names:
                    fw(bytes(m, 'utf-8'))  # Material name
                    fw(uint8(0))  # Terminate with 1 x 00 byte
                off_bone_strings = f.tell()
                if boneNames:
                    for b in bon_names:
                        fw(bytes(bon_names[b], 'utf-8'))  # Bone name
                        fw(uint8(0))  # Terminate with 1 x 00 byte
                fw(zero_padding(f.tell()))

                subprogress2.step()  # 11

                # Write the cached offsets
                off_cache = f.tell()
                fw(uint32(off_050))
                fw(uint32(f.tell() - 4))
                fw(uint32(off_054))
                fw(uint32(off_070))
                fw(uint32(off_058))
                fw(uint32(off_mat_names))
                fw(uint32(off_070))
                fw(uint32(off_mesh_string))
                fw(uint32(off_070 + 24))
                fw(uint32(off_verts))
                fw(uint32(off_070 + 28))
                fw(uint32(off_piece))
                fw(uint32(off_070 + 32))
                fw(uint32(off_faces))
                fw(uint32(off_070 + 36))
                fw(uint32(off_bones))
                m_len = 0
                for m in range(num_mats):
                    # First we write the offset address
                    fw(uint32(off_mat_names + (4 * m)))
                    # Second we write the value
                    if m == 0:
                        fw(uint32(off_mat_strings))
                    else:
                        m_len += (len(mat_names[m - 1]) + 1)
                        fw(uint32(off_mat_strings + m_len))
                b_len = 0
                for b in range(num_b):
                    # First we write the offset address
                    fw(uint32(off_bones + (28 * b)))
                    # Second we write the value
                    if b == 0:
                        fw(uint32(off_bone_strings))
                    else:
                        b_len += (len(bon_names[b - 1]) + 1)
                        fw(uint32(off_bone_strings + b_len))
                fw(zero_padding(f.tell()))

                subprogress2.step()  # 12

                # Write the BNRY/LTLE section as 32 x 00 byte
                off_BNRY = f.tell()
                fw(uint32(0) + uint32(0) + uint32(0) + uint32(0))
                fw(uint32(0) + uint32(0) + uint32(0) + uint32(0))

                subprogress2.step()  # 13

                # Write the bounding box of each mesh
                fw(float32(min_x))  # Min X
                fw(float32(min_y))  # Min Y
                fw(float32(min_z))  # Min Z
                fw(float32(max_x))  # Max X
                fw(float32(max_y))  # Max Y
                fw(float32(max_z))  # Max Z
                fw(float32(0))  # 4 x 00 byte for padding

                subprogress2.step()  # 14

                fw(b'EGCD')
                fw(uint32(5))
                fw(uint32(off_BNRY))  # offset of the BNRY/LTLE section

                subprogress2.step()  # 15

                # Go back and write offsets
                f.seek(off_0C0)
                fw(uint32(off_BNRY))
                f.seek(off_010)
                fw(uint32(7 + (1 if num_mats > 0 else 0) + num_mats + num_b))
                f.seek(off_050)
                fw(uint32(off_cache))
                f.seek(off_070)
                fw(uint32(off_mesh_string))
                f.seek(off_mat_names)
                mn = 0
                for m in range(num_mats):
                    if m == 0:
                        fw(uint32(off_mat_strings))
                    else:
                        fw(uint32(off_mat_strings + mn))
                    mn += int(len(mat_names[m]) + 1)


def _write(operator, context, filepath,
           EXPORT_GLOBAL_MATRIX,
           EXPORT_HAS_CLO,
           ):

    with ProgressReport(context.window_manager) as progress:
        base_name, ext = os.path.splitext(filepath)
        # Base name, scene name, extension
        context_name = [base_name, '', ext]

        depsgraph = context.evaluated_depsgraph_get()
        scene = context.scene

        # Exit edit mode before exporting, so current object states are exported properly.
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

        objects = context.selected_objects

        full_path = ''.join(context_name)

        # EXPORT THE FILE.
        progress.enter_substeps(1)
        write_file(operator, full_path, objects, depsgraph, scene,
                   EXPORT_GLOBAL_MATRIX,
                   EXPORT_HAS_CLO,
                   progress,
                   )
        progress.leave_substeps()


def save(operator,
         context,
         filepath,
         *,
         global_matrix=None,
         has_clo=False,
         ):

    _write(operator, context, filepath,
           EXPORT_GLOBAL_MATRIX=global_matrix,
           EXPORT_HAS_CLO=has_clo,
           )

    return {'FINISHED'}
