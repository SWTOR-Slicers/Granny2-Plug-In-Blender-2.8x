# <pep8 compliant>

import bpy

from . import shaders
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    PointerProperty)
from bpy.types import Image, Operator, ShaderNodeCustomGroup, UILayout
from nodeitems_utils import NodeCategory, NodeItem


def update_ageMap(self, context):
    if self.ageMap:
        self.ageMap.alpha_mode = 'CHANNEL_PACKED'
        self.ageMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['ageMap'].image = self.ageMap
        self.node_tree.nodes['ageMap'].mute = False
    else:
        self.node_tree.nodes['ageMap'].image = None
        self.node_tree.nodes['ageMap'].mute = True


def update_alpha_mode(self, context):
    mat = context.space_data.id
    mat.blend_method = self.alpha_mode
    mat.show_transparent_back = False
    update_alpha_test_value(self, context)


def update_alpha_test_value(self, context):
    context.space_data.id.alpha_threshold = self.alpha_test_value


def update_complexionMap(self, context):
    if self.complexionMap:
        self.complexionMap.alpha_mode = 'CHANNEL_PACKED'
        self.complexionMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['complexionMap'].image = self.complexionMap
        self.node_tree.nodes['complexionMap'].mute = False
    else:
        if 'white.dds' in bpy.data.images:
            self.node_tree.nodes['complexionMap'].image = bpy.data.images['white.dds']
        else:
            img = bpy.data.images.new('white.dds', 4, 4)
            img.generated_color = [1.0, 1.0, 1.0, 1.0]
            self.node_tree.nodes['complexionMap'].image = img


def update_derived(self, context):
    if self.derived == 'CREATURE':
        self.node_tree.nodes.clear()
        shaders.Creature(self.node_tree)
        update_diffuseMap(self, context)
        update_directionMap(self, context)
        update_glossMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_flesh_brightness(self, context)
        update_flush_tone(self, context)
    elif self.derived == 'EYE':
        self.node_tree.nodes.clear()
        shaders.Eye(self.node_tree)
        update_diffuseMap(self, context)
        update_glossMap(self, context)
        update_paletteMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_palette(self, context)
    elif self.derived == 'GARMENT':
        self.node_tree.nodes.clear()
        shaders.Garment(self.node_tree)
        update_diffuseMap(self, context)
        update_glossMap(self, context)
        update_paletteMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_palette(self, context)
    elif self.derived == 'HAIRC':
        self.node_tree.nodes.clear()
        shaders.HairC(self.node_tree)
        update_diffuseMap(self, context)
        update_directionMap(self, context)
        update_glossMap(self, context)
        update_paletteMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_palette(self, context)
    elif self.derived == 'SKINB':
        self.node_tree.nodes.clear()
        shaders.SkinB(self.node_tree)
        update_ageMap(self, context)
        update_complexionMap(self, context)
        update_diffuseMap(self, context)
        update_facepaintMap(self, context)
        update_glossMap(self, context)
        update_paletteMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_palette(self, context)
        update_flesh_brightness(self, context)
        update_flush_tone(self, context)
    elif self.derived == 'UBER':
        self.node_tree.nodes.clear()
        shaders.Uber(self.node_tree)
        update_diffuseMap(self, context)
        update_glossMap(self, context)
        update_rotationMap(self, context)
    else:
        raise ValueError


def update_diffuseMap(self, context):
    if self.diffuseMap:
        self.diffuseMap.alpha_mode = 'CHANNEL_PACKED'
        self.diffuseMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['_d'].image = self.diffuseMap
    else:
        self.node_tree.nodes['_d'].image = None


def update_directionMap(self, context):
    if self.directionMap:
        self.directionMap.alpha_mode = 'CHANNEL_PACKED'
        self.directionMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['directionMap'].image = self.directionMap
    else:
        self.node_tree.nodes['directionMap'].image = None
        self.node_tree.nodes['directionMap'].mute = True


def update_facepaintMap(self, context):
    if self.facepaintMap:
        self.facepaintMap.alpha_mode = 'CHANNEL_PACKED'
        self.facepaintMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['facepaintMap'].image = self.facepaintMap
        self.node_tree.nodes['facepaintMap'].mute = False
    else:
        self.node_tree.nodes['facepaintMap'].image = None
        self.node_tree.nodes['facepaintMap'].mute = True


def update_flesh_brightness(self, context):
    if 'GetFlushColor' in self.node_tree.nodes:
        self.node_tree.nodes['GetFlushColor'].inputs['Flesh Brightness'].default_value = self.flesh_brightness


def update_flush_tone(self, context):
    if 'ageDarkening' in self.node_tree.nodes:
        self.node_tree.nodes['ageDarkening'].inputs['Color1'].default_value = self.flush_tone

    if 'GetFlushColor' in self.node_tree.nodes:
        self.node_tree.nodes['GetFlushColor'].inputs['Flush Tone'].default_value = self.flush_tone


def update_glossMap(self, context):
    if self.glossMap:
        self.glossMap.alpha_mode = 'CHANNEL_PACKED'
        self.glossMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['_s'].image = self.glossMap
    else:
        self.node_tree.nodes['_s'].image = None


def update_palette(self, context):
    if 'ChosenPalette' in self.node_tree.nodes:
        inputs = self.node_tree.nodes['ChosenPalette'].inputs
        inputs['Palette1 Hue'].default_value = self.palette1_hue
        inputs['Palette1 Saturation'].default_value = self.palette1_saturation
        inputs['Palette1 Brightness'].default_value = self.palette1_brightness
        inputs['Palette1 Contrast'].default_value = self.palette1_contrast
        inputs['Palette1 Specular'].default_value = self.palette1_specular
        inputs['Palette1 Metallic Specular'].default_value = self.palette1_metallic_specular
        inputs['Palette2 Hue'].default_value = self.palette2_hue
        inputs['Palette2 Saturation'].default_value = self.palette2_saturation
        inputs['Palette2 Brightness'].default_value = self.palette2_brightness
        inputs['Palette2 Contrast'].default_value = self.palette2_contrast
        inputs['Palette2 Specular'].default_value = self.palette2_specular
        inputs['Palette2 Metallic Specular'].default_value = self.palette2_metallic_specular
    elif 'HuePixel' in self.node_tree.nodes:
        inputs = self.node_tree.nodes['HuePixel'].inputs
        inputs['Hue'].default_value = self.palette1_hue
        inputs['Saturation'].default_value = self.palette1_saturation
        inputs['Brightness'].default_value = self.palette1_brightness
        inputs['Contrast'].default_value = self.palette1_contrast
        inputs['Specular'].default_value = self.palette1_specular
        inputs['Metallic Specular'].default_value = self.palette1_metallic_specular
    elif 'HueSkinPixel' in self.node_tree.nodes:
        inputs = self.node_tree.nodes['HueSkinPixel'].inputs
        inputs['Hue'].default_value = self.palette1_hue
        inputs['Saturation'].default_value = self.palette1_saturation
        inputs['Brightness'].default_value = self.palette1_brightness
        inputs['Contrast'].default_value = self.palette1_contrast
        inputs['Specular'].default_value = self.palette1_specular
        inputs['Metallic Specular'].default_value = self.palette1_metallic_specular


def update_paletteMap(self, context):
    if self.paletteMap:
        self.paletteMap.alpha_mode = 'CHANNEL_PACKED'
        self.paletteMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['_h'].image = self.paletteMap
        self.node_tree.nodes['_h'].mute = False
    else:
        self.node_tree.nodes['_h'].image = None
        self.node_tree.nodes['_h'].mute = True


def update_paletteMaskMap(self, context):
    if self.paletteMaskMap:
        self.paletteMaskMap.alpha_mode = 'CHANNEL_PACKED'
        self.paletteMaskMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['_m'].image = self.paletteMaskMap
        self.node_tree.nodes['_m'].mute = False
    else:
        self.node_tree.nodes['_m'].image = None
        self.node_tree.nodes['_m'].mute = True


def update_rotationMap(self, context):
    if self.rotationMap:
        self.rotationMap.alpha_mode = 'CHANNEL_PACKED'
        self.rotationMap.colorspace_settings.name = 'Raw'
        self.node_tree.nodes['_n'].image = self.rotationMap
    else:
        self.node_tree.nodes['_n'].image = None


class HeroNodeGroup(ShaderNodeCustomGroup):
    """Hero Engine Shader Node"""
    bl_idname = "ShaderNodeHeroEngine"
    bl_label = "SWTOR"
    bl_icon = 'NODE'

    # PARAMETERS
    derived: EnumProperty(
        default='CREATURE',
        description="Which shader to use when rendering this material",
        items=[
            ('CREATURE', "Creature", ""),
            ('EYE', "Eye", ""),
            ('GARMENT', "Garment", ""),
            ('HAIRC', "HairC", ""),
            ('SKINB', "SkinB", ""),
            ('UBER', "Uber", "")
        ],
        name="Derived",
        options={'HIDDEN'},
        update=update_derived)
    alpha_mode: EnumProperty(
        default='OPAQUE',
        description="How to handle transparancy",
        items=[
            ('BLEND', "Blend", ""),
            ('CLIP', "Test", ""),
            ('OPAQUE', "None", "")
        ],
        name="Alpha Mode",
        options={'HIDDEN'},
        update=update_alpha_mode)
    alpha_test_value: FloatProperty(
        default=0.5,
        description="At what alpha value to fully discard a pixel",
        max=1.0,
        min=0.0,
        name="Alpha Test",
        options={'HIDDEN'},
        subtype='FACTOR',
        update=update_alpha_test_value)

    # TEXTURE MAPS
    ageMap: PointerProperty(
        name='AgeMap',
        options={'HIDDEN'},
        type=Image,
        update=update_ageMap)
    complexionMap: PointerProperty(
        name='AgeMap',
        options={'HIDDEN'},
        type=Image,
        update=update_complexionMap)
    diffuseMap: PointerProperty(
        name="DiffuseMap",
        options={'HIDDEN'},
        type=Image,
        update=update_diffuseMap)
    directionMap: PointerProperty(
        name='DirectionMap',
        options={'HIDDEN'},
        type=Image,
        update=update_directionMap)
    facepaintMap: PointerProperty(
        name='AgeMap',
        options={'HIDDEN'},
        type=Image,
        update=update_facepaintMap)
    glossMap: PointerProperty(
        name="GlossMap",
        options={'HIDDEN'},
        type=Image,
        update=update_glossMap)
    paletteMap: PointerProperty(
        name="PaletteMap",
        options={'HIDDEN'},
        type=Image,
        update=update_paletteMap)
    paletteMaskMap: PointerProperty(
        name="PaletteMaskMap",
        options={'HIDDEN'},
        type=Image,
        update=update_paletteMaskMap)
    rotationMap: PointerProperty(
        name="RotationMap",
        options={'HIDDEN'},
        type=Image,
        update=update_rotationMap)

    # PALETTE1
    palette1_hue: FloatProperty(
        default=0.0,
        description='',
        max=1.0,
        min=0.0,
        name='Palette1 Hue',
        options={'HIDDEN'},
        precision=3,
        step=10,
        subtype='NONE',
        update=update_palette)
    palette1_saturation: FloatProperty(
        default=0.5,
        description='',
        max=1.0,
        min=0.0,
        name='Palette1 Saturation',
        options={'HIDDEN'},
        precision=3,
        step=10,
        subtype='NONE',
        update=update_palette)
    palette1_brightness: FloatProperty(
        default=0.0,
        description='',
        max=1.0,
        min=-1.0,
        name='Palette1 Brightness',
        options={'HIDDEN'},
        precision=3,
        step=10,
        subtype='NONE',
        update=update_palette)
    palette1_contrast: FloatProperty(
        default=1.0,
        description='',
        max=3.0,
        min=0.0,
        name='Palette1 Contrast',
        options={'HIDDEN'},
        precision=3,
        step=10,
        subtype='NONE',
        update=update_palette)
    palette1_specular: FloatVectorProperty(
        default=[0.0, 0.5, 0.0, 1.0],
        description='',
        max=1.0,
        min=0.0,
        name='Palette1 Specular',
        options={'HIDDEN'},
        precision=3,
        size=4,
        step=10,
        subtype='COLOR',
        update=update_palette)
    palette1_metallic_specular: FloatVectorProperty(
        default=[0.0, 0.5, 0.0, 1.0],
        description='',
        max=1.0,
        min=0.0,
        name='Palette1 Metallic Specular',
        options={'HIDDEN'},
        precision=3,
        size=4,
        step=10,
        subtype='COLOR',
        update=update_palette)

    # PALETTE2
    palette2_hue: FloatProperty(
        default=0.0,
        description='',
        max=1.0,
        min=0.0,
        name='Palette2 Hue',
        options={'HIDDEN'},
        precision=3,
        step=10,
        subtype='NONE',
        update=update_palette)
    palette2_saturation: FloatProperty(
        default=0.5,
        description='',
        max=1.0,
        min=0.0,
        name='Palette2 Saturation',
        options={'HIDDEN'},
        precision=3,
        step=10,
        subtype='NONE',
        update=update_palette)
    palette2_brightness: FloatProperty(
        default=0.0,
        description='',
        max=1.0,
        min=-1.0,
        name='Palette2 Brightness',
        options={'HIDDEN'},
        precision=3,
        step=10,
        subtype='NONE',
        update=update_palette)
    palette2_contrast: FloatProperty(
        default=1.0,
        description='',
        max=3.0,
        min=0.0,
        name='Palette2 Contrast',
        options={'HIDDEN'},
        precision=3,
        step=10,
        subtype='NONE',
        update=update_palette)
    palette2_specular: FloatVectorProperty(
        default=[0.0, 0.5, 0.0, 1.0],
        description='',
        max=1.0,
        min=0.0,
        name='Palette2 Specular',
        options={'HIDDEN'},
        precision=3,
        size=4,
        step=10,
        subtype='COLOR',
        update=update_palette)
    palette2_metallic_specular: FloatVectorProperty(
        default=[0.0, 0.5, 0.0, 1.0],
        description='',
        max=1.0,
        min=0.0,
        name='Palette2 Metallic Specular',
        options={'HIDDEN'},
        precision=3,
        size=4,
        step=10,
        subtype='COLOR',
        update=update_palette)

    # INPUTS
    flesh_brightness: FloatProperty(
        default=0.0,
        description='',
        max=1.0,
        min=0.0,
        name='Flesh Brightness',
        options={'HIDDEN'},
        precision=3,
        subtype='FACTOR',
        update=update_flesh_brightness)
    flush_tone: FloatVectorProperty(
        default=[0.0, 0.0, 0.0, 1.0],
        description='',
        max=1.0,
        min=0.0,
        name='Flush Tone',
        options={'HIDDEN'},
        size=4,
        subtype='COLOR',
        update=update_flush_tone)

    # Initialization function, called when a new node is created.
    def init(self, context):
        self.node_tree = bpy.data.node_groups.new(name=self.name, type='ShaderNodeTree')
        update_derived(self, context)
        self.width = 240.0

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout: UILayout):
        # PARAMETERS
        row = layout.row()
        col = row.column()
        col.ui_units_x = 8.5
        col.label(text='Derived:')
        col = row.column()
        col.prop(data=self, property="derived", text='')

        row = layout.row()
        col = row.column()
        col.ui_units_x = 8.5
        col.label(text='Alpha Mode:')
        col = row.column()
        col.prop(data=self, property='alpha_mode', text='')

        if self.alpha_mode == 'CLIP':
            row = layout.row()
            col = row.column()
            col.ui_units_x = 8.5
            col.label(text='Alpha Test Value:')
            col = row.column()
            col.prop(data=self, property="alpha_test_value", text='')

        layout.separator()

        # TEXTURE MAPS
        box = layout.box()
        col = box.column()

        col.label(text='DiffuseMap:')
        col.template_ID(data=self, new='image.new', open='image.open', property='diffuseMap')
        col.label(text='RotationMap:')
        col.template_ID(data=self, new='image.new', open='image.open', property='rotationMap')
        col.label(text='GlossMap:')
        col.template_ID(data=self, new='image.new', open='image.open', property='glossMap')

        if self.derived in ['EYE', 'GARMENT', 'HAIRC', 'SKINB']:
            col.label(text='PaletteMap:')
            col.template_ID(data=self, new='image.new', open='image.open', property='paletteMap')

        if self.derived in ['CREATURE', 'EYE', 'GARMENT', 'HAIRC', 'SKINB']:
            col.label(text='PaletteMaskMap:')
            col.template_ID(
                data=self,
                new='image.new',
                open='image.open',
                property='paletteMaskMap')

        if self.derived in ['CREATURE', 'HAIRC']:
            col.label(text='DirectionMap:')
            col.template_ID(data=self, new='image.new', open='image.open', property='directionMap')

        if self.derived == 'SKINB':
            col.label(text='AgeMap:')
            col.template_ID(data=self, new='image.new', open='image.open', property='ageMap')
            col.label(text='ComplexionMap:')
            col.template_ID(data=self, new='image.new', open='image.open', property='complexionMap')
            col.label(text='FacepaintMap')
            col.template_ID(data=self, new='image.new', open='image.open', property='facepaintMap')

        # INPUTS
        if self.derived in ['EYE', 'HAIRC', 'SKINB']:
            box = layout.box()
            col = box.column()
            col.label(text='Palette:')
            col.prop(data=self, property='palette1_hue', text='Hue')
            col.prop(data=self, property='palette1_saturation', text='Saturation')
            col.prop(data=self, property='palette1_brightness', text='Brightness')
            col.prop(data=self, property='palette1_contrast', text='Contrast')
            row = box.row()
            row.prop(data=self, property='palette1_specular', text='Specular')
            row = box.row()
            row.prop(data=self, property='palette1_metallic_specular', text='Metallic Specular')

        if self.derived in ['CREATURE', 'SKINB']:
            box = layout.box()
            col = box.column()
            col.label(text='Inputs:')
            col.prop(data=self, property='flesh_brightness', slider=True, text='Flesh Brightness')
            row = col.row()
            row.prop(data=self, property='flush_tone', text='Flush Tone')

        if self.derived == 'GARMENT':
            box = layout.box()
            col = box.column()
            col.label(text='Primary Palette:')
            col.prop(data=self, property='palette1_hue', text='Hue')
            col.prop(data=self, property='palette1_saturation', text='Saturation')
            col.prop(data=self, property='palette1_brightness', text='Brightness')
            col.prop(data=self, property='palette1_contrast', text='Contrast')
            row = col.row()
            row.prop(data=self, property='palette1_specular', text='Specular')
            row = col.row()
            row.prop(data=self, property='palette1_metallic_specular', text='Metallic Specular')

            box = layout.box()
            col = box.column()
            col.label(text='Secondary Palette:')
            col.prop(data=self, property='palette2_hue', text='Hue')
            col.prop(data=self, property='palette2_saturation', text='Saturation')
            col.prop(data=self, property='palette2_brightness', text='Brightness')
            col.prop(data=self, property='palette2_contrast', text='Contrast')
            row = col.row()
            row.prop(data=self, property='palette2_specular', text='Specular')
            row = col.row()
            row.prop(data=self, property='palette2_metallic_specular', text='Metallic Specular')

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    # def draw_buttons_ext(self, context, layout):
    #     layout.template_ID(data=self, property="node_tree")

    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        if self.derived == 'CREATURE':
            return "SWTOR: Creature Shader"
        elif self.derived == 'EYE':
            return "SWTOR: Eye Shader"
        elif self.derived == 'GARMENT':
            return "SWTOR: Garment Shader"
        elif self.derived == 'HAIRC':
            return "SWTOR: HairC Shader"
        elif self.derived == 'SKINB':
            return "SWTOR: SkinB Shader"
        elif self.derived == 'UBER':
            return "SWTOR: Uber Shader"


class HeroNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return (context.space_data.type == 'NODE_EDITOR' and
                context.space_data.tree_type == 'ShaderNodeTree')


node_categories = [
    HeroNodeCategory('HeroEngine', "SWTOR", items=[
        NodeItem('ShaderNodeHeroEngine', label="Creature Shader", settings={
            'derived': repr('CREATURE')
        }),
        NodeItem('ShaderNodeHeroEngine', label="Eye Shader", settings={
            'derived': repr('EYE')
        }),
        NodeItem('ShaderNodeHeroEngine', label="Garment Shader", settings={
            'derived': repr('GARMENT')
        }),
        NodeItem('ShaderNodeHeroEngine', label="Hair Shader", settings={
            'derived': repr('HAIRC')
        }),
        NodeItem('ShaderNodeHeroEngine', label="Skin Shader", settings={
            'derived': repr('SKINB')
        }),
        NodeItem('ShaderNodeHeroEngine', label="Uber Shader", settings={
            'derived': repr('UBER')
        })
    ])
]


class NODE_OT_ngroup_edit(Operator):
    bl_label = "Edit Group"
    bl_description = "Edit Hero node group"
    bl_idname = "node.ngroup_edit"
    bl_options = {'REGISTER', 'UNDO'}

    exit: BoolProperty(name="Exit", description="", default=False)

    @classmethod
    def poll(cls, context):
        space = context.space_data
        if space.type != 'NODE_EDITOR':
            return False
        if space.tree_type not in ["CompositorNodeTree", "ShaderNodeTree", "TextureNodeTree"]:
            return False
        return True

    def execute(self, context):
        space = context.space_data

        if hasattr(context, "node"):
            node = context.node
        else:
            node = getattr(context, "active_node", None)

        valid_ngroups = [
            "ShaderNodeHeroEngine",
            "CompositorNodeGroup",
            "ShaderNodeGroup",
            "TextureNodeGroup"
        ]

        if node and node.bl_idname in valid_ngroups and not self.exit:
            space.path.append(node_tree=node.node_tree, node=node)
        else:
            space.path.pop()

        return {'FINISHED'}
