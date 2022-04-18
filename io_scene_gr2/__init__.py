# <pep8 compliant>

import importlib
import os
import sys
from typing import List, Set

import bpy
from bpy.app.handlers import depsgraph_update_post
from bpy.props import BoolProperty, CollectionProperty, FloatProperty, StringProperty
from bpy.types import Context, KeyMap, Menu, Operator, OperatorFileListElement
from bpy_extras.io_utils import ExportHelper, ImportHelper, axis_conversion, orientation_helper

from .types.node import ShaderNodeHeroEngine, NODE_OT_ngroup_edit

bl_info = {
    "name": "Star Wars: The Old Republic (.gr2)",
    "author": "Darth Atroxa",
    "version": (2, 93, 1),
    "blender": (2, 82, 0),
    "location": "File > Import-Export",
    "description": "Import-Export SWTOR skeleton, or model with bone weights, UV's and materials",
    "support": 'COMMUNITY',
    "category": "Import-Export"
}

# Python doesn't reload package sub-modules at the same time as __init__.py!
for filename in [file for file in os.listdir(os.path.dirname(os.path.realpath(__file__)))
                 if file.endswith('.py')]:
    if filename == os.path.basename(__file__):
        continue

    module = sys.modules.get("{}.{}".format(__name__, filename[:-3]))

    if module:
        importlib.reload(module)

# clear out any scene update funcs hanging around, e.g. after a script reload
for func in depsgraph_update_post:
    if func.__module__.startswith(__name__):
        depsgraph_update_post.remove(func)

del importlib, os, sys, depsgraph_update_post


@orientation_helper(axis_forward='-Z', axis_up='Y')
class ExportGR2(Operator, ExportHelper):
    """Export SWTOR GR2 file format (.gr2)"""
    bl_idname = "export_mesh.gr2"
    bl_label = "Export SWTOR (.gr2)"
    bl_options = {'PRESET'}

    filename_ext = ".gr2"
    filter_glob: StringProperty(default="*.gr2", options={'HIDDEN'})

    has_clo: BoolProperty(
        name="Has .clo file?",
        description="Enable if there is a corresponding .clo file to go with this model",
        default=False)

    def execute(self, context):
        # type: (Context) -> Set[str]
        from .funcs import export_gr2

        import os
        # from mathutils import Matrix

        global_matrix = axis_conversion(to_forward=self.axis_forward, to_up=self.axis_up).to_4x4()

        # global_matrix = axis_conversion(
        #     to_forward=self.axis_forward,
        #     to_up=self.axis_up
        # ).to_4x4() @ Matrix.Scale(0.1, 4)  # Scale down to 10%

        # Cache selected objects.
        obs = context.selected_objects

        path, _ = os.path.split(self.filepath)

        for ob in obs:
            # Clear selected object(s).
            bpy.ops.object.select_all(action='DESELECT')

            # Select ob
            ob.select_set(True)

            # Export ob
            if not export_gr2.save(self, context, path, ob, global_matrix=global_matrix):
                return {'CANCELLED'}

        return {'FINISHED'}


class ImportCHA(Operator, ImportHelper):
    """Import from JSON file format (.json)"""
    bl_idname = "import_mesh.gr2_json"
    bl_label = "Import SWTOR (.json)"
    bl_options = {'UNDO'}

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the JSON file",
        type=OperatorFileListElement,
    )

    if bpy.app.version < (2, 82, 0):
        directory = StringProperty(subtype='DIR_PATH')
    else:
        directory: StringProperty(subtype='DIR_PATH')

    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={'HIDDEN'})

    import_collision: BoolProperty(name="Import collision mesh", default=False)

    def execute(self, context):
        # type: (Context) -> Set[str]
        import os

        paths = [os.path.join(self.directory, file.name) for file in self.files]

        if not paths:
            paths.append(self.filepath)

        from .funcs import import_cha

        for path in paths:
            if not import_cha.load(self, context, path):
                return {'CANCELLED'}

        return {'FINISHED'}


class ImportCLO(Operator, ImportHelper):
    """Import SWTOR CLO file format (.clo)"""
    bl_idname = "import_cloth.clo"
    bl_label = "Import SWTOR (.clo)"
    bl_options = {'UNDO'}

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the CLO file",
        type=OperatorFileListElement,
    )

    if bpy.app.version < (2, 82, 0):
        directory = StringProperty(subtype='DIR_PATH')
    else:
        directory: StringProperty(subtype='DIR_PATH')

    filename_ext = ".clo"
    filter_glob: StringProperty(default="*.clo", options={'HIDDEN'})

    def execute(self, context):
        # type: (Context) -> Set[str]
        import os

        paths = [os.path.join(self.directory, file.name) for file in self.files]

        if not paths:
            paths.append(self.filepath)

        from .funcs import import_clo

        for path in paths:
            if not import_clo.load(self, context, path):
                return {'CANCELLED'}

        return {'FINISHED'}


class ImportGR2(Operator, ImportHelper):
    """Import SWTOR GR2 file format (.gr2)"""
    bl_idname = "import_mesh.gr2"
    bl_label = "Import SWTOR (.gr2)"
    bl_options = {'UNDO'}

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the GR2 file",
        type=OperatorFileListElement,
    )

    if bpy.app.version < (2, 82, 0):
        directory = StringProperty(subtype='DIR_PATH')
    else:
        directory: StringProperty(subtype='DIR_PATH')

    filename_ext = ".gr2"
    filter_glob: StringProperty(default="*.gr2", options={'HIDDEN'})

    import_collision: BoolProperty(name="Import Collision Mesh", default=False)

    def execute(self, context):
        # type: (Context) -> Set[str]
        import os

        paths = [os.path.join(self.directory, file.name) for file in self.files]

        if not paths:
            paths.append(self.filepath)

        from .funcs import import_gr2

        for path in paths:
            if not import_gr2.load(self, context, path):
                return {'CANCELLED'}

        return {"FINISHED"}


class ImportJBA(Operator, ImportHelper):
    """Import from SWTOR JBA file format (.jba)"""
    bl_idname = "import_animation.jba"
    bl_label = "Import SWTOR (.jba)"
    bl_options = {'UNDO'}

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the JBA file",
        type=OperatorFileListElement,
    )

    if bpy.app.version < (2, 82, 0):
        directory = StringProperty(subtype='DIR_PATH')
    else:
        directory: StringProperty(subtype='DIR_PATH')

    filename_ext = ".jba"
    filter_glob: StringProperty(default="*.jba", options={'HIDDEN'})

    ignore_facial_bones: BoolProperty(
        name="Import Facial Bones",
        description="Ignore translation keyframe for facial bones",
        default=True,
    )
    scale_factor: FloatProperty(
        name="Scale Factor",
        description="Scale factor of the animation (try 1.05 for character animations)",
        default=1.0,
        soft_min=0.1,
        soft_max=2.0,
    )

    def execute(self, context):
        # type: (Context) -> Set[str]
        import os

        paths = [os.path.join(self.directory, file.name) for file in self.files]

        if not paths:
            paths.append(self.filepath)

        from .funcs import import_jba

        for path in paths:
            if not import_jba.load(self, context, path):
                return {'CANCELLED'}

        return {'FINISHED'}


def _import_cha(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ImportCHA.bl_idname, text="SW:TOR (.json)")


def _import_clo(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ImportCLO.bl_idname, text="SW:TOR (.clo)")


def _import_gr2(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ImportGR2.bl_idname, text="SW:TOR (.gr2)")


def _import_jba(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ImportJBA.bl_idname, text="SW:TOR (.jba)")


def _export_gr2(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ExportGR2.bl_idname, text="SW:TOR (.gr2)")


classes = (
    ExportGR2,
    ImportCHA,
    ImportCLO,
    ImportGR2,
    ImportJBA,
    ShaderNodeHeroEngine,
    NODE_OT_ngroup_edit,
)

keymaps: List[KeyMap] = []


def register():
    # type: () -> None
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    from nodeitems_utils import register_node_categories
    from .types import node
    register_node_categories('SWTOR', node.node_categories)

    from bpy.types import TOPBAR_MT_file_export, TOPBAR_MT_file_import
    TOPBAR_MT_file_import.append(_import_cha)
    TOPBAR_MT_file_import.append(_import_clo)
    TOPBAR_MT_file_import.append(_import_gr2)
    TOPBAR_MT_file_import.append(_import_jba)
    TOPBAR_MT_file_export.append(_export_gr2)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
    kmi = km.keymap_items.new(node.NODE_OT_ngroup_edit.bl_idname, 'TAB', 'PRESS')
    kmi.properties.exit = False
    kmi = km.keymap_items.new(node.NODE_OT_ngroup_edit.bl_idname, 'TAB', 'PRESS', ctrl=True)
    kmi.properties.exit = True
    keymaps.append(km)


def unregister():
    # type: () -> None
    for km in keymaps:
        for kmi in km.keymap_items:
            km.restore_item_to_default(kmi)
    keymaps.clear()

    from bpy.types import TOPBAR_MT_file_export, TOPBAR_MT_file_import

    TOPBAR_MT_file_import.remove(_import_cha)
    TOPBAR_MT_file_import.remove(_import_clo)
    TOPBAR_MT_file_import.remove(_import_gr2)
    TOPBAR_MT_file_import.remove(_import_jba)
    TOPBAR_MT_file_export.remove(_export_gr2)

    from nodeitems_utils import unregister_node_categories
    unregister_node_categories('SWTOR')

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)


if __name__ == "__main__":
    try:
        unregister()
    except (KeyError, RuntimeError):
        pass

    register()
