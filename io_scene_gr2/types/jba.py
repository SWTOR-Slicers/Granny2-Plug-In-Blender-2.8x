# <pep8 compliant>

from typing import List

from mathutils import Quaternion, Vector


class JointBoneAnimation:

    class Block:

        num_frames: int
        size: int
        start_frame: int

        def __init__(self, start_frame, size):
            # type: (int, int) -> None
            self.size = size
            self.start_frame = start_frame

    class Bone:

        name: str
        rotation_base: Vector
        rotation_stride: Vector
        rotations: List[Quaternion]
        translation_base: Vector
        translation_stride: Vector
        translations: List[Vector]

        def __init__(self, rotation_base, rotation_stride, translation_base, translation_stride):
            # type: (Vector, Vector, Vector, Vector) -> None
            self.rotation_base = rotation_base
            self.rotation_stride = rotation_stride
            self.translation_base = translation_base
            self.translation_stride = translation_stride

    class WorldSpace:

        rotations: List[Quaternion]
        translations: List[Vector]

        def __init__(self, rotations, translations):
            # type: (List[Quaternion], List[Vector]) -> None
            self.rotations = rotations
            self.translations = translations

    bones: List[Bone]
    fps: int
    length: int
    num_frames: int
    world_space: WorldSpace

    def __init__(self, length, fps, num_frames, bones, world_space):
        # type: (int, int, int, List[Bone], WorldSpace) -> None
        self.bones = bones
        self.fps = fps
        self.length = length
        self.num_frames = num_frames
        self.world_space = world_space
