# <pep8 compliant>

from typing import Dict, Iterator, Sequence, Tuple, Union

from mathutils import Color, Vector


class Granny2:
    """
    """

    __slots__ = ("offset_BNRY", "type_flag", "bounds", "offset_cached_offsets",
                 "offset_mesh_headers", "offset_material_name_offsets", "mesh_buffer",
                 "bone_buffer", "material_names", "num_bytes")

    class Bone:
        """
        """

        __slots__ = ("name", "parent_index", "root_to_bone")

        name: str
        parent_index: int
        root_to_bone: int

    class BoundingBox:
        """
        """

        __slots__ = ("min_x", "min_y", "min_z", "min_w", "max_x", "max_y", "max_z", "max_w")

        min_x: float
        min_y: float
        min_z: float
        min_w: float
        max_x: float
        max_y: float
        max_z: float
        max_w: float

        def __init__(self, seq=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)):
            # type: (Sequence[Union[float, int]]) -> None
            self.min_x = float(seq[0]) if len(seq) >= 1 else 0.0
            self.min_y = float(seq[1]) if len(seq) >= 2 else 0.0
            self.min_z = float(seq[2]) if len(seq) >= 3 else 0.0
            self.min_w = float(seq[3]) if len(seq) >= 4 else 0.0
            self.max_x = float(seq[4]) if len(seq) >= 5 else 0.0
            self.max_y = float(seq[5]) if len(seq) >= 6 else 0.0
            self.max_z = float(seq[6]) if len(seq) >= 7 else 0.0
            self.max_w = float(seq[7]) if len(seq) >= 8 else 0.0

        def __iter__(self):
            # type: () -> Iterator[Union[float, int]]
            return iter(
                [
                    self.min_x,
                    self.min_y,
                    self.min_z,
                    self.min_w,
                    self.max_x,
                    self.max_y,
                    self.max_z,
                    self.max_w,
                ]
            )

    class Piece:
        """
        """

        __slots__ = ("offset_indices", "num_polygons", "material_index", "index", "bounds")

        offset_indices: int
        num_polygons: int
        material_index: int
        index: int

        bounds: "Granny2.BoundingBox"

    class Mesh:
        """
        """

        __slots__ = ("_mesh_name", "offset_mesh_name", "offset_vertex_buffer",
                     "offset_piece_headers", "offset_indices_buffer", "offset_bones_buffer",
                     "piece_header_buffer", "vertex_buffer", "indices_buffer", "bone_names")

        def __init__(self, name):
            # type: (str) -> None
            self._mesh_name = name

        offset_mesh_name: int          # 0x70 Uint32

        @property
        def name(self):
            # type: () -> str
            if getattr(self, "_mesh_name", None):
                return self._mesh_name.replace(' ', '_')
            else:
                return "None"

        @property
        def bit_flag1(self):           # 0x74 Uint32
            # type: () -> int
            return 0 if getattr(self, "bone_names", None) else 128

        @property
        def num_pieces(self):          # 0x78 Uint16
            # type: () -> int
            if getattr(self, "piece_header_buffer", None):
                return len(self.piece_header_buffer)
            else:
                return 0

        @property
        def num_used_bones(self):      # 0x7A Uint16
            # type: () -> int
            if getattr(self, "bone_names", None):
                return len(self.bone_names)
            else:
                return 0

        @property
        def bit_flag2(self):           # 0x7C Uint16
            # type: () -> int
            flag = 0
            if getattr(self, "vertex_buffer", None):
                vertex = self.vertex_buffer[0]
                if getattr(vertex, "position", None):
                    flag |= 1
                if getattr(vertex, "normals", None) and getattr(vertex, "tangents", None):
                    flag |= 2 | 4 | 8
                if getattr(vertex, "color", None):
                    flag |= 16
                if getattr(vertex, "uv_layer0", None):
                    flag |= 32
                if getattr(vertex, "uv_layer1", None):
                    flag |= 64
                if getattr(vertex, "uv_layer2", None):
                    flag |= 128
                if getattr(vertex, "bone_indices", None) and getattr(vertex, "bone_weights", None):
                    flag |= 256
            return flag

        @property
        def vertex_size(self):         # 0x7E Uint16
            # type: () -> int
            size = 0
            if getattr(self, "bit_flag2", None):
                if self.bit_flag2 & 1:
                    size += 12
                if self.bit_flag2 & 2:
                    size += 8
                if self.bit_flag2 & 16:
                    size += 4
                if self.bit_flag2 & 32:
                    size += 4
                if self.bit_flag2 & 64:
                    size += 4
                if self.bit_flag2 & 128:
                    size += 4
                if self.bit_flag2 & 256:
                    size += 8
            return size

        @property
        def num_vertices(self):        # 0x80 Uint32
            # type: () -> int
            if getattr(self, "vertex_buffer", None):
                return len(self.vertex_buffer)
            else:
                return 0

        @property
        def num_polygons(self):        # 0x84 Uint32
            # type: () -> int
            if getattr(self, "indices_buffer", None):
                return len(self.indices_buffer)
            else:
                return 0

        offset_vertex_buffer: int      # 0x88 Uint32
        offset_piece_headers: int      # 0x8C Uint32
        offset_indices_buffer: int     # 0x90 Uint32
        offset_bones_buffer: int       # 0x94 Uint32

        piece_header_buffer: Dict[int, "Granny2.Piece"]
        vertex_buffer: Dict[int, "Granny2.Vertex"]
        indices_buffer: Dict[int, Tuple[int]]
        bone_names: Dict[int, str]

    class Vertex:
        """
        """

        __slots__ = ("position", "bone_weights", "bone_indices", "color", "normals", "tangents",
                     "uv_layer0", "uv_layer1", "uv_layer2")

        position: Vector      # vec3
        bone_weights: Vector  # vec4
        bone_indices: Vector  # vec4
        color: Color          # rgb
        normals: Vector       # vec4
        tangents: Vector      # vec4
        uv_layer0: Vector     # vec2
        uv_layer1: Vector     # vec2
        uv_layer2: Vector     # vec2

        def __init__(self, seq=(0.0, 0.0, 0.0)):
            # type: (Sequence[Union[float, int]]) -> None
            self.position = Vector(seq)

    @property
    def magic_bytes(self):             # 0x00 Uint32
        # type: () -> int
        return 1113014599

    @property
    def version_major(self):           # 0x04 Uint32
        # type: () -> int
        return 4

    @property
    def version_minor(self):           # 0x08 Uint32
        # type: () -> int
        return 3

    offset_BNRY: int                   # 0x0C Uint32

    @property
    def num_cached_offsets(self):      # 0x10 Uint32
        # type: () -> int
        count = 3
        if getattr(self, "mesh_buffer", None):
            for _ in self.mesh_buffer:
                count += 5
        if self.num_materials:
            count += self.num_materials
        if getattr(self, "mesh_buffer"):
            for mesh in self.mesh_buffer.values():
                if getattr(mesh, "bone_names", None):
                    count += mesh.num_used_bones
        return count

    type_flag: int                     # 0x14 Uint32

    @property
    def num_meshes(self):              # 0x18 Uint16
        # type: () -> int
        if getattr(self, "mesh_buffer", None):
            return len(self.mesh_buffer)
        else:
            return 0

    @property
    def num_materials(self):           # 0x1A Uint16
        # type: () -> int
        if getattr(self, "material_names", None):
            return len(self.material_names)
        else:
            return 0

    @property
    def num_skeleton_bones(self):      # 0x1C Uint16
        # type: () -> int
        if getattr(self, "bone_buffer", None):
            return len(self.bone_buffer)
        else:
            return 0

    @property
    def num_attachments(self):         # 0x1E Uint16
        # type: () -> int
        return 0

    bounds: BoundingBox                # 0x30 Float32 x 8

    offset_cached_offsets: int         # 0x50 Uint32
    offset_mesh_headers: int           # 0x54 Uint32
    offset_material_name_offsets: int  # 0x58 Uint32

    @property
    def offset_attachments(self):      # 0x60 Uint32
        # type: () -> int
        return 0

    mesh_buffer: Dict[int, "Granny2.Mesh"]
    bone_buffer: Dict[int, "Granny2.Bone"]
    material_names: Dict[int, str]

    num_bytes: int

    def calculate_offsets(self):
        # type: () -> None
        count = 0
        # Header
        count += 32
        # 16 x 0x00
        count += 16
        # Bounding Box
        count += 32
        # Offsets
        count += 20
        while (count % 16) != 0:
            count += 1
        # Mesh header(s)
        self.offset_mesh_headers = count
        count += 40 * len(self.mesh_buffer)
        while (count % 16) != 0:
            count += 1
        # Sub mesh header(s)
        for mesh in self.mesh_buffer.values():
            mesh.offset_piece_headers = count
            count += 48 * mesh.num_pieces
        # Offset of each Material Name string
        self.offset_material_name_offsets = count
        for _ in range(self.num_materials):
            count += 4
        while (count % 16) != 0:
            count += 1
        # Vertex Buffer
        for mesh in self.mesh_buffer.values():
            mesh.offset_vertex_buffer = count
            count += mesh.vertex_size * mesh.num_vertices
        while (count % 16) != 0:
            count += 1
        # Indices Buffer
        for mesh in self.mesh_buffer.values():
            mesh.offset_indices_buffer = count
            count += mesh.num_polygons * 6
        while (count % 16) != 0:
            count += 1
        # Bones Buffer
        for mesh in self.mesh_buffer.values():
            mesh.offset_bones_buffer = count
            if mesh.bone_names:
                count += 28 * mesh.num_used_bones
            else:
                count += 28
        while (count % 16) != 0:
            count += 1
        # Strings buffer
        for mesh in self.mesh_buffer.values():
            mesh.offset_mesh_name = count
            count += len(mesh.name) + 1
        for name in self.material_names.values():
            count += len(name) + 1
        for mesh in self.mesh_buffer.values():
            if mesh.bone_names:
                for name in mesh.bone_names.values():
                    count += len(name) + 1
        while (count % 16) != 0:
            count += 1
        # Cached Offsets
        self.offset_cached_offsets = count
        count += 24
        count += 40 * self.num_meshes
        count += 8 * self.num_materials
        for mesh in self.mesh_buffer.values():
            count += 8 * mesh.num_used_bones
        while (count % 16) != 0:
            count += 1
        # BNRY/LTLE
        self.offset_BNRY = count
        count += 32
        # Bounding Box
        count += 28
        # EGCD
        count += 12
        self.num_bytes = count
