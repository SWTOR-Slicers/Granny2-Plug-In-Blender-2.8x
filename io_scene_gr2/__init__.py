# <pep8 compliant>

bl_info = {
    "name": "Star Wars: The Old Republic (.gr2)",
    "author": "Darth Atroxa, SWTOR Slicers",
    "version": (4, 0, 1),
    "blender": (2, 82, 0),
    "location": "File > Import-Export",
    "description": "Import-Export SWTOR skeleton, or model with bone weights, UV's and materials",
    "support": 'COMMUNITY',
    "category": "Import-Export",
}


import importlib
import os
import sys
from typing import List

import bpy

from bpy.app import version_string
from bpy.app.handlers import depsgraph_update_post
from bpy.props import FloatVectorProperty
from bpy.types import Context, KeyMap, Menu, PropertyGroup

from .addon_prefs import Prefs, GR2PREFS_MT_presets_menu, GR2PREFS_OT_set_preset

from .ops.export_gr2             import ExportGR2
from .ops.export_gr2_32          import ExportGR2_32
from .ops.import_cha             import ImportCHA
from .ops.import_clo             import ImportCLO
from .ops.import_gr2             import ImportGR2
from .ops.import_jba             import ImportJBA

from .types.node        import ShaderNodeHeroEngine, NODE_OT_ngroup_edit

# Detect Blender version
major, minor, _ = bpy.app.version
blender_version = major + minor / 100

if blender_version >= 4.0:
    from .ops.add_swtor_shaders_menu import *  # classes and fn for Shader Editor's Add menu functionality in 4.x



# Python doesn't reload package sub-modules at the same time as __init__.py!

# reload modules in subfolder for current Blender version
addon_root_path = os.path.dirname(os.path.realpath(__file__))

directories = [os.path.join(addon_root_path, entry) for entry in {'ops','types','utils'}]
                              
for directory in directories:
    for entry in os.listdir(directory):
        if entry.endswith('.py'):
            module = sys.modules.get(f"{__name__}.{entry[:-3]}")

            if module:
                importlib.reload(module)

# …And reload common preferences module in root of add-on
module = sys.modules.get("addon_prefs")
if module:
    importlib.reload(module)


# Clear out any scene update funcs hanging around, e.g. after a script reload
for func in depsgraph_update_post:
    if func.__module__.startswith(__name__):
        depsgraph_update_post.remove(func)

del importlib, os, sys, depsgraph_update_post


# Import/Export functions to append to Import/Export menus in register()
def _import_gr2(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ImportGR2.bl_idname, text="SWTOR 32/64-bit Objects / Skeletons (.gr2)")

def _import_cha(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ImportCHA.bl_idname, text="SWTOR Player Characters / NPCs (.json)")

def _import_jba(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ImportJBA.bl_idname, text="SWTOR 32-bit Animations (.jba)")

def _import_clo(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ImportCLO.bl_idname, text="SWTOR 32-bit Cloth Physics (.clo)")


def _export_gr2(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ExportGR2.bl_idname, text="SWTOR 64-bit Objects (.gr2)")

def _export_gr2_32(self, _context):
    # type: (Menu, Context) -> None
    self.layout.operator(ExportGR2_32.bl_idname, text="SWTOR 32-bit Objects (.gr2)")


class BoneBounds(PropertyGroup):
    bounds: FloatVectorProperty(default=[0.0] * 6, name="Bounds", precision=6, size=6)


classes = (
    Prefs, GR2PREFS_MT_presets_menu, GR2PREFS_OT_set_preset,
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
if blender_version >= 4.0:
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

    
    from bpy.props import StringProperty
    bpy.types.Scene.io_scene_gr2_last_job = StringProperty(
        name="io_scene_gr2 Add-on's Last Activity",
        description=".json-format info about the results of the use of this add-on\n (e.g., objects imported) that external operators can use",
        default='',
        )
    
    
    # Additions to Shader Editor's Add menu
    if blender_version < 4.0:
        from .types import node

        # This was the specific way to extend shader menu categories
        # that has been deprecated in 4.x.
        # (Oddly enough, it seems it was deprecated in 3.4
        # but still it works in 3.6.x ?)
        from nodeitems_utils import register_node_categories
        register_node_categories('SWTOR', node.node_categories)

    else:
        
        from .types import node
        
        # Appends fn with separator bar plus SWTOR menu to the Shader Editor's Add menu
        # This is a conventional way to extend menus.
        bpy.types.NODE_MT_add.append(swtor_shaders_submenu_element)


    # TAB-into-Nodegroup functionality
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
    kmi = km.keymap_items.new(node.NODE_OT_ngroup_edit.bl_idname, 'TAB', 'PRESS')
    kmi.properties.exit = False
    kmi = km.keymap_items.new(node.NODE_OT_ngroup_edit.bl_idname, 'TAB', 'PRESS', ctrl=True)
    kmi.properties.exit = True
    keymaps.append(km)


def unregister():
    if blender_version < 4.0:
        from nodeitems_utils import unregister_node_categories
        unregister_node_categories('SWTOR')
    else:
        bpy.types.NODE_MT_add.remove(swtor_shaders_submenu_element)

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
        
    del bpy.types.Scene.io_scene_gr2_last_job


if __name__ == '__main__':
    try:
        unregister()
    except Exception:
        pass

    register()
