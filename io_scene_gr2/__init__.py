# <pep8 compliant>

import importlib
import os
import sys
from typing import List

from bpy.app.handlers import depsgraph_update_post
from bpy.types import Context, KeyMap, Menu

from .ops.export_gr2 import ExportGR2
from .ops.import_cha import ImportCHA
from .ops.import_clo import ImportCLO
from .ops.import_gr2 import ImportGR2
from .ops.import_jba import ImportJBA

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
for directory in [os.path.join(os.path.dirname(os.path.realpath(__file__)), entry)
                  for entry in {'ops', 'types', 'utils'}]:
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

    import bpy
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


if __name__ == '__main__':
    try:
        unregister()
    except Exception:
        pass

    register()
