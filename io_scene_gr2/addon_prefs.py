import bpy

def update_jba_scale(self, context):
    '''
    update jba_scale_factor
    when gr2_scale_factor is updated.
    
    Must be placed here, it seems.
    '''
    self.jba_scale_factor = self.gr2_scale_factor


class Prefs(bpy.types.AddonPreferences):
    bl_idname = "io_scene_gr2"

    # Preferences properties --------------------

    # .gr2 import ones:
    
    gr2_import_collision: bpy.props.BoolProperty(
        name="Import Collision Mesh",
        description="Imports the object's collision boundary mesh if present in the file\n(it can be of use when exporting models to other apps and game engines)",
        default=False,
    )
    
    gr2_name_as_filename: bpy.props.BoolProperty(
        name="Name As Filename",
        description="Names the imported Blender objects with their filenames instead of their\ninternal 'art names' (the object's mesh data always keeps the 'art name').\n\n.gr2 objects' internal 'art names' typically match their files' names,\nbut sometimes they difer, which can break some tools and workflows.\n\nIn case of multiple mesh files (containing a main object plus secondary ones\nand / or Engine Objects such as Colliders), only the main object is renamed",
        default=False,
    )

    gr2_scale_object: bpy.props.BoolProperty(
        name="Scale Object",
        description="Scales imported objects, characters and armatures\nat the Mesh level.\n\nSWTOR sizes objects in decimeters, while Blender defaults to meters.\nThis mismatch, while innocuous, is an obstacle when doing physics\nsimulations, automatic weighting from bones, or other processes\nwhere Blender requires real world-like sizes to succeed",
        default=False,
    )

    gr2_scale_factor: bpy.props.FloatProperty(
        name="Scale factor",
        description="Recommended values are:\n\n- 10 for simplicity (characters are superhero-like tall, over 2 m.).\n- Around 8 for accuracy (characters show more realistic heights).\n\nRemember that, if binding to a skeleton later on, the skeleton\nmust match the scale of the objects to work correctly (which\ncan be done on import, or manually afterwards)",
        min = 1.0,
        max = 100.0,
        soft_min = 1.0,
        soft_max = 10.0,
        step = 10,
        precision = 2,
        default=10.0,
        update=update_jba_scale,
    )
    
    gr2_apply_axis_conversion: bpy.props.BoolProperty(
        name="Apply Axis Conversion",
        description="Permanently converts the imported object\nto Blender's 'Z-is-Up' coordinate system\nby 'applying' a x=90º rotation.\n\nSWTOR's coordinate system is 'Y-is-up' vs. Blender's 'Z-is-up'.\nTo compensate for that in a reversible manner, this importer\nnormally sets the object's rotation to X=90º at the Object level.\n\nAs this can be a nuisance outside a modding use case,\nthis option applies it at the Mesh level, instead",
        default=False,
    )


    # NPC/Character (.json) import ones:

    swtor_resources_dir: bpy.props.StringProperty(
        name="Resources Directory",
        description="Local folder containing your SWTOR assets extraction, mirroring the game's\nown layout directly (this folder should directly contain an 'art' subfolder).\n\nUsed by the NPC/Character (.json) importer to read .gr2/.mat/.dds files\ndirectly from here, without a separate asset-gathering/copying step.",
        subtype='DIR_PATH',
        default="",
    )
    
    swtor_legacy_resources_dir: bpy.props.StringProperty(
        name="Legacy Resources Directory",
        description="Local folder containing your Legacy SWTOR assets extraction, mirroring the game's\nown layout directly (this folder should directly contain an 'art' subfolder).\n\nUsed by the NPC/Character (.json) importer to read .gr2/.mat/.dds files\ndirectly from here, without a separate asset-gathering/copying step.",
        subtype='DIR_PATH',
        default="",
    )

    gr2_import_skeleton_default: bpy.props.BoolProperty(
        name="Import Skeleton By Default",
        description="Default state of the NPC/Character importer's 'Import Skeleton' option.\n\nCan still be switched per-import in the importer's own panel",
        default=False,
    )

    gr2_bind_to_skeleton_default: bpy.props.BoolProperty(
        name="Bind To Skeleton By Default",
        description="Default state of the NPC/Character importer's 'Bind To Skeleton' option.\n\nCan still be switched per-import in the importer's own panel",
        default=False,
    )

    gr2_append_character_name_to_collections_default: bpy.props.BoolProperty(
        name="Append Character Name to Collections By Default",
        description="Default state of the NPC/Character importer's 'Append Character Name to Collections' option.\n\nCan still be switched per-import in the importer's own panel",
        default=False,
    )


    # .jba import ones:

    jba_ignore_facial_bones: bpy.props.BoolProperty(
        name="Ignore Facial Transl.",
        description="Ignores the data in the facial bones' translation keyframes\nand only uses their rotation keyframes",
        default=True,
    )
        
    jba_delete_180: bpy.props.BoolProperty(
        name="Delete 180º rotation",
        description="Keeps the animation data from turning the skeleton 180º by deleting\nthe keyframes assigned to the Bip01 bone and setting its rotation to zero.\n\nSWTOR animations turn characters so that they face away from the camera,\nas normally shown in the gameplay. That is not just a nuisance but a problem\nwhen adding cloth or physics simulations to capes or lekku: the instantaneous\nturn plays havok with them",
        default=False,
    )

    # UI ----------------------------------------
    
    def draw(self, context):        
        
        layout = self.layout
        
        box = layout.box().column(align=True)
        box.label(text="Common Directories:")
        box.scale_y = 0.90
        box.prop(self, 'swtor_resources_dir', text="Resources Directory")
        box.prop(self, 'swtor_legacy_resources_dir', text="Legacy Resources Directory")

        box = layout.box().column(align=True)
        box.label(text="NPC/CHARACTER (.JSON) IMPORT SETTINGS:")
        box.scale_y = 0.90
        row = box.row(align=True)
        row.prop(self, 'gr2_import_skeleton_default', text="Import Skeleton By Default")
        row.prop(self, 'gr2_bind_to_skeleton_default', text="Bind To Skeleton By Default")
        box.prop(self, 'gr2_append_character_name_to_collections_default', text="Append Character Name to Collections By Default")

        split = layout.split(factor=0.5)
        split_left = split
        split_right = split
        
        boxcol = split_left.box().column(align=True)
        boxcol.label(text=".GR2 OBJECTS IMPORT SETTINGS:")
        boxcol.scale_y = 0.90
        boxcol.prop(self,'gr2_import_collision')
        boxcol.prop(self,'gr2_name_as_filename', text="Name Imported Objects As Filenames")
        boxcol.prop(self,'gr2_apply_axis_conversion', text="'Apply' Axis Conversion")
        boxcol.prop(self,'gr2_scale_object', text="Scale Imported Objects/Characters")
        slider_split = boxcol.split(factor=0.1)
        slider_split.enabled = self.gr2_scale_object
        slider_split.label()
        slider_split.prop(self,'gr2_scale_factor', text="Scale factor")
        
        boxcol = split_right.box().column(align=True)
        boxcol.label(text=".JBA ANIMATIONS IMPORT SETTINGS:")
        boxcol.scale_y = 0.90
        boxcol.prop(self,'jba_ignore_facial_bones', text="Ignore Facial Bones' Translation Data")
        boxcol.prop(self,'jba_delete_180')
        boxcol.label()
        boxcol.label(text="The Animation and Character Importers")
        boxcol.label(text="use all the applicable .gr2 Object settings.")



# Registrations

def register():
    bpy.utils.register_class(Prefs)


def unregister():
    bpy.utils.unregister_class(Prefs)

if __name__ == "__main__":
    register()