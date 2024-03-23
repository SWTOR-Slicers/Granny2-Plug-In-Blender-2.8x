# <pep8 compliant>

import importlib
import os
import sys
from typing import List

import bpy

from bpy.app import version_string
from bpy.app.handlers import depsgraph_update_post
from bpy.props import FloatVectorProperty
from bpy.types import Context, KeyMap, Menu, PropertyGroup


# Modules subfolder selection. lib3 covers from Blender 2.8.x to 3.6.x.
blender_version = float(version_string[:3])


# "Manual" module imports (the Add-on could still evolve so that
# there are lib4 modules with no lib3 counterparts and viceversa)
if blender_version >= 4:
    from .lib4.ops.export_gr2    import ExportGR2
    from .lib4.ops.export_gr2_32 import ExportGR2_32
    from .lib4.ops.import_cha    import ImportCHA
    from .lib4.ops.import_clo    import ImportCLO
    from .lib4.ops.import_gr2    import ImportGR2
    from .lib4.ops.import_jba    import ImportJBA
    from .lib4.types.node        import ShaderNodeHeroEngine, NODE_OT_ngroup_edit
    from .lib4.ops.add_swtor_shaders_menu import *  # classes and fn for Sheader Editor's Add menu functionality in 4.x
else:
    from .lib3.ops.export_gr2    import ExportGR2
    from .lib3.ops.export_gr2_32 import ExportGR2_32
    from .lib3.ops.import_cha    import ImportCHA
    from .lib3.ops.import_clo    import ImportCLO
    from .lib3.ops.import_gr2    import ImportGR2
    from .lib3.ops.import_jba    import ImportJBA
    from .lib3.types.node        import ShaderNodeHeroEngine, NODE_OT_ngroup_edit


bl_info = {
    "name": "Star Wars: The Old Republic (.gr2)",
    "author": "Darth Atroxa, SWTOR Slicers",
    "version": (4, 0, 1),
    "blender": (2, 82, 0),
    "location": "File > Import-Export",
    "description": "Import-Export SWTOR skeleton, or model with bone weights, UV's and materials",
    "support": 'COMMUNITY',
    "category": "Import-Export"
}


# Python doesn't reload package sub-modules at the same time as __init__.py!

working_lib_path = (os.path.dirname(os.path.realpath(__file__)) + f'/lib{int(blender_version)}/')

for directory in [os.path.join(working_lib_path, entry) for entry in {'ops','types','utils'}]:
        for entry in os.listdir(directory):
            if entry.endswith('.py'):
                module = sys.modules.get(f"{__name__}.{entry[:-3]}")

                if module:
                    importlib.reload(module)

# Clear out any scene update funcs hanging around, e.g. after a script reload
for func in depsgraph_update_post:
    if func.__module__.startswith(__name__):
        depsgraph_update_post.remove(func)

del importlib, os, sys, depsgraph_update_post


# Import/Export functions to append to Import/Export menus in register() 
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

def _export_gr2_32(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ExportGR2_32.bl_idname, text="SW:TOR (.gr2 32bit)")


class BoneBounds(PropertyGroup):
    bounds: FloatVectorProperty(default=[0.0] * 6, name="Bounds", precision=6, size=6)


classes = (
    BoneBounds,
    ExportGR2,
    ExportGR2_32,
    ImportCHA,
    ImportCLO,
    ImportGR2,
    ImportJBA,
    ShaderNodeHeroEngine,
    NODE_OT_ngroup_edit,
)
if blender_version >= 4:
    classes = classes + (NODE_MT_add_swtor_shader, NODE_MT_swtor_shaders_menu)

keymaps: List[KeyMap] = []


def register():
    # type: () -> None
    import bpy

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


    # Additions to Import-Export menu
    from bpy.types import TOPBAR_MT_file_export, TOPBAR_MT_file_import
    TOPBAR_MT_file_import.append(_import_cha)
    TOPBAR_MT_file_import.append(_import_clo)
    TOPBAR_MT_file_import.append(_import_gr2)
    TOPBAR_MT_file_import.append(_import_jba)
    TOPBAR_MT_file_export.append(_export_gr2)
    TOPBAR_MT_file_export.append(_export_gr2_32)


    from bpy.props import CollectionProperty
    from bpy.types import Object
    Object.bone_bounds = CollectionProperty(name="Bone Bounds", type=BoneBounds)


    # Additions to Shader Editor's Add menu
    blender_version = float(version_string[:3])
    if blender_version >= 4:
        from .lib4.types import node
        
        # Append fn with separator bar plus SWTOR menu to the Shader Editor's Add menu
        # (swtor_shaders_submenu_element comes from .lib4.ops.add_swtor_shaders_menu).
        # This is a conventional way to extend menus.
        bpy.types.NODE_MT_add.append(swtor_shaders_submenu_element)
        
    else:
        from .lib3.types import node

        # This was the specific way to extend shader menu categories
        # that has been deprecated in 4.x.
        from nodeitems_utils import register_node_categories
        register_node_categories('SWTOR', node.node_categories)


    # TAB-into-Nodegroup functionality
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
    kmi = km.keymap_items.new(node.NODE_OT_ngroup_edit.bl_idname, 'TAB', 'PRESS')
    kmi.properties.exit = False
    kmi = km.keymap_items.new(node.NODE_OT_ngroup_edit.bl_idname, 'TAB', 'PRESS', ctrl=True)
    kmi.properties.exit = True
    keymaps.append(km)


def unregister():
    if blender_version >= 4:
        bpy.types.NODE_MT_add.remove(swtor_shaders_submenu_element)
    else:
        from nodeitems_utils import unregister_node_categories
        unregister_node_categories('SWTOR')

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
    TOPBAR_MT_file_export.remove(_export_gr2_32)

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

if __name__ == '__main__':
    try:
        unregister()
    except Exception:
        pass

    register()
