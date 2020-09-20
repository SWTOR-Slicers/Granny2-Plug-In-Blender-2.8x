# <pep8 compliant>

import bpy

from bpy.props import (
    BoolProperty,
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
    "version": (2, 80, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Export SWTOR skeleton, or model with bone weights, UV's and materials",
    "support": 'COMMUNITY',
    "category": "Import-Export"}


class ImportGR2(bpy.types.Operator, ImportHelper):
    """Import from SWTOR GR2 file format (.gr2)"""
    bl_idname = "import_scene.gr2"
    bl_label = "Import SWTOR (.gr2)"
    bl_options = {'UNDO'}

    filename_ext = ".gr2"
    filter_glob: StringProperty(default="*.gr2", options={'HIDDEN'})

    import_collision: BoolProperty(name="Import Collision Mesh", default=False)

    def execute(self, context):
        from . import import_gr2
        return import_gr2.load(self, context, self.filepath)


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


def menu_func_import(self, context):
    self.layout.operator(ImportGR2.bl_idname, text="SW:TOR (.gr2)")


def menu_func_export(self, context):
    self.layout.operator(ExportGR2.bl_idname, text="SW:TOR (.gr2)")


classes = (ImportGR2, ExportGR2)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
