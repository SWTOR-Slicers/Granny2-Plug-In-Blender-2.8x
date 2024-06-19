# <pep8 compliant>

from typing import List


class Cloth:

    class Bone:

        name: str
        index: int
        parent_index: int
        constraints1: List[float]
        constraints2: List[float]
        constraints3: List[float]
        unk1: List[float]
        unk2: List[int]
        is_cloth: bool

        def __str__(self):
            # type: () -> str
            return str(vars(self))

    num_bones: int
    bones: List[Bone]

    def __init__(self, num_bones):
        self.num_bones = num_bones
        self.bones = [Cloth.Bone() for _ in range(num_bones)]
