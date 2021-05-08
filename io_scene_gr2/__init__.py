# <pep8 compliant>

import bpy

from bpy.props import (
    BoolProperty,
    CollectionProperty,
    FloatProperty,
    StringProperty
)
from bpy_extras.io_utils import (
    axis_conversion,
    ImportHelper,
    ExportHelper,
    orientation_helper
)


bl_info = {
    "name": "Star Wars: The Old Republic (.gr2)",
    "author": "Darth Atroxa",
    "version": (2, 83, 0),
    "blender": (2, 83, 0),
    "location": "File > Import-Export",
    "description": "Import-Export SWTOR skeleton, or model with bone weights, UV's and materials",
    "support": 'COMMUNITY',
    "category": "Import-Export"
}


class ImportGR2(bpy.types.Operator, ImportHelper):
    """Import from SWTOR GR2 file format (.gr2)"""
    bl_idname = "import_scene.gr2"
    bl_label = "Import SWTOR (.gr2)"
    bl_options = {'UNDO'}

    filename_ext = ".gr2"
    filter_glob: StringProperty(default="*.gr2", options={'HIDDEN'})

    import_collision: BoolProperty(name="Import Collision Mesh", default=False)

    files: CollectionProperty(type=bpy.types.PropertyGroup)

    # directory
    directory = StringProperty(subtype='DIR_PATH')
    print(directory)

    from . import import_gr2
    def execute(self, context):
        import os
        status = ""
        for j, i in enumerate(self.files):
            path = os.path.join(self.directory, i.name)
            print(path)
            status = import_gr2.load(self, context, path)

        return {"FINISHED"}

class ImportToon(bpy.types.Operator, ImportHelper):
    """Import from JSON file format (.json)"""
    bl_idname = "import_scene.json"
    bl_label = "Import SWTOR (.json)"
    bl_options = {'UNDO'}

    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={'HIDDEN'})

    import_collision: BoolProperty(name="Import Collision Mesh", default=False)

    files: CollectionProperty(type=bpy.types.PropertyGroup)

    # directory
    directory = StringProperty(subtype='DIR_PATH')
    print(directory)

    from . import import_toon
    def execute(self, context):
        import os
        status = ""
        for j, i in enumerate(self.files):
            path = os.path.join(self.directory, i.name)
            print(path)
            status = import_toon.load(self, context, path)

        return {"FINISHED"}


@orientation_helper(axis_forward='-Z', axis_up='Y')
class ExportGR2(bpy.types.Operator, ExportHelper):
    """Export to SWTOR GR2 file format (.gr2)"""
    bl_idname = "export_scene.gr2"
    bl_label = "Export SWTOR (.gr2)"
    bl_options = {'PRESET'}

    filename_ext = ".gr2"
    filter_glob: StringProperty(default="*.gr2", options={'HIDDEN'})

    has_clo: BoolProperty(
        name="Has .clo file?",
        description="Enable if there is a corresponding .clo file to go with this model.",
        default=False)

    check_extension = True

    def execute(self, context):
        from . import export_gr2

        # from mathutils import Matrix
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "check_existing",
                                            "filter_glob",
                                            ))

        global_matrix = axis_conversion(to_forward=self.axis_forward,
                                        to_up=self.axis_up,
                                        ).to_4x4()

        keywords["global_matrix"] = global_matrix
        return export_gr2.save(self, context, **keywords)


class ImportJBA(bpy.types.Operator, ImportHelper):
    """Import from SWTOR JBA file format (.jba)"""
    bl_idname = "import_scene.jba"
    bl_label = "Import SWTOR (.jba)"
    bl_options = {'UNDO'}

    filename_ext = ".jba"
    filter_glob: StringProperty(default="*.jba", options={'HIDDEN'})

    scale_factor: FloatProperty(name="Scale Factor", description="Scale factor of the animation (try 1.05 for character animations)", default=1.0, soft_min=0.1, soft_max=2.0)
    ignore_facial_bones: BoolProperty(name="Ignore Facial Bones", description="Ignore translation keyframes for facial bones", default=True)

    files: CollectionProperty(type=bpy.types.PropertyGroup)

    # directory
    directory = StringProperty(subtype='DIR_PATH')
    print(directory)

    from . import import_jba
    def execute(self, context):
        import os
        status = ""
        for j, i in enumerate(self.files):
            path = os.path.join(self.directory, i.name)
            print(path)
            status = import_jba.load(self, context, path)

        return {"FINISHED"}


class ImportCLO(bpy.types.Operator, ImportHelper):
    """Import from SWTOR CLO file format (.clo)"""
    bl_idname = "import_scene.clo"
    bl_label = "Import SWTOR (.clo)"
    bl_options = {'UNDO'}

    filename_ext = ".clo"
    filter_glob: StringProperty(default="*.clo", options={'HIDDEN'})

    files: CollectionProperty(type=bpy.types.PropertyGroup)

    # directory
    directory = StringProperty(subtype='DIR_PATH')
    print(directory)

    from . import import_clo
    def execute(self, context):
        import os
        status = ""
        for j, i in enumerate(self.files):
            path = os.path.join(self.directory, i.name)
            print(path)
            status = import_clo.load(self, context, path)

        return {"FINISHED"}


def menu_func_import_gr2(self, context):
    self.layout.operator(ImportGR2.bl_idname, text="SW:TOR (.gr2)")


def menu_func_export_gr2(self, context):
    self.layout.operator(ExportGR2.bl_idname, text="SW:TOR (.gr2)")


def menu_func_import_jba(self, context):
    self.layout.operator(ImportJBA.bl_idname, text="SW:TOR (.jba)")


def menu_func_import_clo(self, context):
    self.layout.operator(ImportCLO.bl_idname, text="SW:TOR (.clo)")

def menu_func_import_toon(self, context):
    self.layout.operator(ImportToon.bl_idname, text="SW:TOR (.json)")


classes = (
    ImportGR2,
    ExportGR2,
    ImportJBA,
    ImportCLO,
    ImportToon
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_gr2)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_gr2)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_jba)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_clo)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_toon)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_gr2)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_gr2)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_jba)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_clo)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_toon)

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
