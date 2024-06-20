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
        default=1.0,
        update=update_jba_scale,
    )
    
    gr2_apply_axis_conversion: bpy.props.BoolProperty(
        name="Apply Axis Conversion",
        description="Permanently converts the imported object\nto Blender's 'Z-is-Up' coordinate system\nby 'applying' a x=90º rotation.\n\nSWTOR's coordinate system is 'Y-is-up' vs. Blender's 'Z-is-up'.\nTo compensate for that in a reversible manner, this importer\nnormally sets the object's rotation to X=90º at the Object level.\n\nAs this can be a nuisance outside a modding use case,\nthis option applies it at the Mesh level, instead",
        default=False,
    )

    jba_ignore_facial_bones: bpy.props.BoolProperty(
        name="Ignore Facial Transl.",
        description="Ignores the data in the facial bones' translation keyframes\nand only uses their rotation keyframes",
        default=True,
    )
    
    jba_scale_animation: bpy.props.BoolProperty(
        name="Scale Animation",
        description="Scales the bones' translation data by a factor.\nIt must match the scale of the skeleton\nand objects to be animated for good results.\n\nWhenever possible, this setting will try to match\nthe Objects' Scale Factor automatically.\nIt will still allow for setting different values manually",
        default=False,
    )

    jba_scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        description="Imported Animations' Scaling factor",
        default=1.0,
        soft_min=0.1,
        soft_max=2.0,
    )
    
    jba_delete_180: bpy.props.BoolProperty(
        name="Delete 180º rotation",
        description="Keeps the animation data from turning the skeleton 180º by deleting\nthe keyframes assigned to the Bip01 bone and setting its rotation to zero.\n\nSWTOR animations turn characters so that they face away from the camera,\nas normally shown in the gameplay. That is not just a nuisance but a problem\nwhen adding cloth or physics simulations to capes or lekku: the instantaneous\nturn plays havok with them",
        default=False,
    )

    # UI ----------------------------------------
    
    def draw(self, context):        
        
        layout = self.layout
        
        split = layout.split(factor=0.5)
        
        col=split.column(align=True)
        col.scale_y = 0.80

        col.label(text="You can set your preferred settings for this")
        col.label(text="Add-on's importers and exporters here.")
        col.label(text="(They can be modified on the fly, too).")

        col=split.column(align=True)
        col.scale_y = 0.80
        col.label(text="This Menu provides sensible settings for")
        col.label(text="most typical tasks as a starting point.")
        col.menu('import_mesh.gr2_presets', text="QUICK PRESETS MENU",)


        col = layout.column()
        col.scale_y = 0.70
        col.label()
        col.label(text="BEFORE CHANGING ANY SETTING, CAREFULLY CONSIDER HOW THEY MIGHT AFFECT")
        col.label(text="YOUR WORKFLOW!!!  Use the 'NEUTRAL' preset to return to the default settings.")
        
        split = layout.split(factor=0.5)
        
        boxcol = split.box().column(align=True, heading=".GR2 OBJECTS IMPORT SETTINGS:")
        boxcol.scale_y = 0.90
        boxcol.prop(self,'gr2_import_collision')
        boxcol.prop(self,'gr2_name_as_filename', text="Name Imported Objects As Filenames")
        boxcol.prop(self,'gr2_apply_axis_conversion', text="'Apply' Axis Conversion")
        boxcol.prop(self,'gr2_scale_object', text="Scale Imported Objects/Characters")
        slider_split = boxcol.split(factor=0.1)
        slider_split.enabled = self.gr2_scale_object
        slider_split.label()
        slider_split.prop(self,'gr2_scale_factor', text="Scale factor")
        
        boxcol = split.box().column(align=True, heading=".JBA ANIMATIONS IMPORT SETTINGS:")
        boxcol.scale_y = 0.90
        boxcol.prop(self,'jba_ignore_facial_bones', text="Ignore Facial Bones' Translation Data")
        boxcol.prop(self,'jba_delete_180')
        boxcol.label()
        boxcol.prop(self,'jba_scale_animation', text="Scale Animation Translations")
        slider_split = boxcol.split(factor=0.1)
        slider_split.enabled = self.jba_scale_animation
        slider_split.label()
        slider_split.prop(self,'jba_scale_factor', text="Animations' Scale factor",)



class GR2PREFS_MT_presets_menu(bpy.types.Menu):
    bl_idname = "import_mesh.gr2_presets"
    bl_label = "Quick Presets Menu"
    bl_description = "Easy Presets for the SWTOR Importers/Exporters:\nthey adjust the settings to sensible values depending on our goals.\n\nBEFORE CHOOSING A PRESET, CAREFULLY CONSIDER\nHOW IT MIGHT AFFECT YOUR WORKFLOW!"
        
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator('import_mesh.gr2_set_preset', text="NEUTRAL:  replicates the default settings of older versions of this Add-on"              ).preset = 'NEUTRAL'

        layout.operator('import_mesh.gr2_set_preset', text="PORTING:  for porting assets to other Game Engines and VR apps (send us feedback!)."                   ).preset = 'PORTING'

        layout.operator('import_mesh.gr2_set_preset', text="BLENDER:  for creating art directly in Blender or in combination with other 3D Art apps.").preset = 'BLENDER'
        
        # layout.operator('import_mesh.gr2_set_preset', text="MODDING:  for modifying SWTOR assets in such a manner that they can be reinserted back." ).preset = 'MODDING'


class GR2PREFS_OT_set_preset(bpy.types.Operator):
    bl_idname = "import_mesh.gr2_set_preset"
    bl_label = "SW:TOR Importers' Preferences Presets Menu"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Easy Presets for the SW:TOR Importers"

    preset: bpy.props.StringProperty(
        name=".gr2 Add-on's Presets",
        default="BLENDER",)

    def execute(self, context):

        prefs = context.preferences.addons["io_scene_gr2"].preferences
        
        if self.preset == 'BLENDER' or self.options is None:

            prefs.gr2_import_collision    = True
            prefs.gr2_name_as_filename    = True
            prefs.gr2_scale_object        = True
            prefs.gr2_scale_factor        = 10.0
            prefs.gr2_apply_axis_conversion  = True

            prefs.jba_ignore_facial_bones = True
            prefs.jba_scale_animation     = prefs.gr2_scale_object
            prefs.jba_scale_factor        = prefs.gr2_scale_factor
            prefs.jba_delete_180          = True

        if self.preset == 'PORTING':

            prefs.gr2_import_collision    = True
            prefs.gr2_name_as_filename    = True
            prefs.gr2_scale_object        = False
            prefs.gr2_scale_factor        = 1.0
            prefs.gr2_apply_axis_conversion  = True

            # SWTOR animations aren't typically
            # used here. Still…
            prefs.jba_ignore_facial_bones = True
            prefs.jba_scale_animation     = prefs.gr2_scale_object
            prefs.jba_scale_factor        = prefs.gr2_scale_factor
            prefs.jba_delete_180          = False
        
        if self.preset == 'MODDING':

            prefs.gr2_import_collision    = True
            prefs.gr2_name_as_filename    = False
            prefs.gr2_scale_object        = False
            prefs.gr2_scale_factor        = 1.0
            prefs.gr2_apply_axis_conversion  = False

            # SWTOR animations aren't typically
            # used here. Still…
            prefs.jba_ignore_facial_bones = True
            prefs.jba_scale_animation     = prefs.gr2_scale_object
            prefs.jba_scale_factor        = prefs.gr2_scale_factor
            prefs.jba_delete_180          = False

        if self.preset == 'NEUTRAL':

            prefs.gr2_import_collision    = True
            prefs.gr2_name_as_filename    = False
            prefs.gr2_scale_object        = False
            prefs.gr2_scale_factor        = 1.0
            prefs.gr2_apply_axis_conversion  = False

            prefs.jba_ignore_facial_bones = False
            prefs.jba_scale_animation     = prefs.gr2_scale_object
            prefs.jba_scale_factor        = prefs.gr2_scale_factor
            prefs.jba_delete_180          = False
           
        return {"FINISHED"}
    
    

# Registrations

def register():
    bpy.utils.register_class(Prefs)
    bpy.utils.register_class(GR2PREFS_MT_presets_menu)
    bpy.utils.register_class(GR2PREFS_OT_set_preset)


def unregister():
    bpy.utils.unregister_class(GR2PREFS_OT_set_preset)
    bpy.utils.unregister_class(GR2PREFS_MT_presets_menu)
    bpy.utils.unregister_class(Prefs)

if __name__ == "__main__":
    register()