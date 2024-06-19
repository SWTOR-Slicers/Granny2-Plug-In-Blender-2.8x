# <pep8 compliant>

from typing import Set

import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    PointerProperty
)
from bpy.types import Context, Image, Operator, ShaderNodeCustomGroup, UILayout
from nodeitems_utils import NodeCategory, NodeItem

# Derived enums
CREATURE = ('CREATURE', "Creature", "")
EYE = ('EYE', "Eye", "")
GARMENT = ('GARMENT', "Garment", "")
HAIRC = ('HAIRC', "HairC", "")
SKINB = ('SKINB', "SkinB", "")
UBER = ('UBER', "Uber", "")

# Alpha mode enums
BLEND = ('BLEND', "Blend", "")
CLIP = ('CLIP', "Test", "")
OPAQUE = ('OPAQUE', "None", "")


def update_ageMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.ageMap:
        self.ageMap.alpha_mode = 'CHANNEL_PACKED'
        self.ageMap.colorspace_settings.name = 'Non-Color'
        self.node_tree.nodes["ageMap"].image = self.ageMap
        self.node_tree.nodes["ageMap"].mute = False
    else:
        self.node_tree.nodes["ageMap"].image = None
        self.node_tree.nodes["ageMap"].mute = True


def update_alpha_mode(self, context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if context.space_data.type in {'NODE_EDITOR', 'PROPERTIES'}:
        mat = context.material
        mat.blend_method = self.alpha_mode
        mat.show_transparent_back = False
        update_alpha_test_value(self, context)


def update_alpha_test_value(self, context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if context.space_data.type in {'NODE_EDITOR', 'PROPERTIES'}:
        context.material.alpha_threshold = self.alpha_test_value


def update_complexionMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.complexionMap:
        self.complexionMap.alpha_mode = 'CHANNEL_PACKED'
        self.complexionMap.colorspace_settings.name = 'Non-Color'
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
    # type: ("ShaderNodeHeroEngine", Context) -> None
    from .node_tree import (
        creature,
        eye,
        garment,
        hairc,
        skinb,
        uber,
    )

    if self.derived == CREATURE[0]:
        self.node_tree.nodes.clear()
        creature(self.node_tree)
        update_diffuseMap(self, context)
        update_directionMap(self, context)
        update_glossMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_flesh_brightness(self, context)
        update_flush_tone(self, context)
    elif self.derived == EYE[0]:
        self.node_tree.nodes.clear()
        eye(self.node_tree)
        update_diffuseMap(self, context)
        update_glossMap(self, context)
        update_paletteMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_palette(self, context)
    elif self.derived == GARMENT[0]:
        self.node_tree.nodes.clear()
        garment(self.node_tree)
        update_diffuseMap(self, context)
        update_glossMap(self, context)
        update_paletteMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_palette(self, context)
    elif self.derived == HAIRC[0]:
        self.node_tree.nodes.clear()
        hairc(self.node_tree)
        update_diffuseMap(self, context)
        update_directionMap(self, context)
        update_glossMap(self, context)
        update_paletteMap(self, context)
        update_paletteMaskMap(self, context)
        update_rotationMap(self, context)
        update_palette(self, context)
    elif self.derived == SKINB[0]:
        self.node_tree.nodes.clear()
        skinb(self.node_tree)
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
    elif self.derived == UBER[0]:
        self.node_tree.nodes.clear()
        uber(self.node_tree)
        update_diffuseMap(self, context)
        update_glossMap(self, context)
        update_rotationMap(self, context)


def update_diffuseMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.diffuseMap:
        self.diffuseMap.alpha_mode = 'CHANNEL_PACKED'
        self.diffuseMap.colorspace_settings.name = 'Non-Color'
        self.node_tree.nodes['_d'].image = self.diffuseMap
    else:
        self.node_tree.nodes['_d'].image = None


def update_directionMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.directionMap:
        self.directionMap.alpha_mode = 'CHANNEL_PACKED'
        self.directionMap.colorspace_settings.name = 'Non-Color'
        self.node_tree.nodes['directionMap'].image = self.directionMap
    else:
        self.node_tree.nodes['directionMap'].image = None
        self.node_tree.nodes['directionMap'].mute = True


def update_facepaintMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.facepaintMap:
        self.facepaintMap.alpha_mode = 'CHANNEL_PACKED'
        self.facepaintMap.colorspace_settings.name = 'Non-Color'
        self.node_tree.nodes['facepaintMap'].image = self.facepaintMap
        self.node_tree.nodes['facepaintMap'].mute = False
    else:
        self.node_tree.nodes['facepaintMap'].image = None
        self.node_tree.nodes['facepaintMap'].mute = True


def update_flesh_brightness(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if 'GetFlushColor' in self.node_tree.nodes:
        self.node_tree.nodes['GetFlushColor'].inputs['Flesh Brightness'].default_value = self.flesh_brightness


def update_flush_tone(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if 'ageDarkening' in self.node_tree.nodes:
        self.node_tree.nodes['ageDarkening'].inputs['Color1'].default_value = self.flush_tone

    if 'GetFlushColor' in self.node_tree.nodes:
        self.node_tree.nodes['GetFlushColor'].inputs['Flush Tone'].default_value = self.flush_tone


def update_glossMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.glossMap:
        self.glossMap.alpha_mode = 'CHANNEL_PACKED'
        self.glossMap.colorspace_settings.name = 'Non-Color'
        self.node_tree.nodes['_s'].image = self.glossMap
    else:
        self.node_tree.nodes['_s'].image = None


def update_palette(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
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


def update_paletteMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.paletteMap:
        self.paletteMap.alpha_mode = 'CHANNEL_PACKED'
        self.paletteMap.colorspace_settings.name = 'Non-Color'
        self.node_tree.nodes['_h'].image = self.paletteMap
        self.node_tree.nodes['_h'].mute = False
    else:
        self.node_tree.nodes['_h'].image = None
        self.node_tree.nodes['_h'].mute = True


def update_paletteMaskMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.paletteMaskMap:
        self.paletteMaskMap.alpha_mode = 'CHANNEL_PACKED'
        self.paletteMaskMap.colorspace_settings.name = 'Non-Color'
        self.node_tree.nodes['_m'].image = self.paletteMaskMap
        self.node_tree.nodes['_m'].mute = False
    else:
        self.node_tree.nodes['_m'].image = None
        self.node_tree.nodes['_m'].mute = True


def update_rotationMap(self, _context):
    # type: ("ShaderNodeHeroEngine", Context) -> None
    if self.rotationMap:
        self.rotationMap.alpha_mode = 'CHANNEL_PACKED'
        self.rotationMap.colorspace_settings.name = 'Non-Color'
        self.node_tree.nodes['_n'].image = self.rotationMap
    else:
        self.node_tree.nodes['_n'].image = None


class ShaderNodeHeroEngine(ShaderNodeCustomGroup):
    """ Hero Engine Shader Node """
    bl_idname = "ShaderNodeHeroEngine"
    bl_label = "SWTOR"
    bl_icon = 'NODE'

    # NOTE: Parameters
    derived: EnumProperty(
        default=CREATURE[0],
        description="Which shader to use when rendering this material",
        items=[CREATURE, EYE, GARMENT, HAIRC, SKINB, UBER],
        name="Derived",
        options={'HIDDEN'},
        update=update_derived)
    alpha_mode: EnumProperty(
        default=OPAQUE[0],
        description="How to handle transparancy",
        items=[BLEND, CLIP, OPAQUE],
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

    # NOTE: Texture maps
    ageMap: PointerProperty(
        type=Image,
        name="AgeMap",
        options={'HIDDEN'},
        update=update_ageMap)
    complexionMap: PointerProperty(
        type=Image,
        name="ComplexionMap",
        options={'HIDDEN'},
        update=update_complexionMap)
    diffuseMap: PointerProperty(
        type=Image,
        name="DiffuseMap",
        options={'HIDDEN'},
        update=update_diffuseMap)
    directionMap: PointerProperty(
        type=Image,
        name="DirectionMap",
        options={'HIDDEN'},
        update=update_directionMap)
    facepaintMap: PointerProperty(
        type=Image,
        name="FacepaintMap",
        options={'HIDDEN'},
        update=update_facepaintMap)
    glossMap: PointerProperty(
        type=Image,
        name="GlossMap",
        options={'HIDDEN'},
        update=update_glossMap)
    paletteMap: PointerProperty(
        type=Image,
        name="PaletteMap",
        options={'HIDDEN'},
        update=update_paletteMap)
    paletteMaskMap: PointerProperty(
        type=Image,
        name="PaletteMaskMap",
        options={'HIDDEN'},
        update=update_paletteMaskMap)
    rotationMap: PointerProperty(
        type=Image,
        name="RotationMap",
        options={'HIDDEN'},
        update=update_rotationMap)

    # NOTE: Palette1
    palette1_hue: FloatProperty(
        max=1.0,
        min=0.0,
        name="Palette1 Hue",
        options={'HIDDEN'},
        precision=3,
        step=10,
        update=update_palette)
    palette1_saturation: FloatProperty(
        default=0.5,
        max=1.0,
        min=0.0,
        name="Palette1 Saturation",
        options={'HIDDEN'},
        precision=3,
        step=10,
        update=update_palette)
    palette1_brightness: FloatProperty(
        max=1.0,
        min=-1.0,
        name="Palette1 Brightness",
        options={'HIDDEN'},
        precision=3,
        step=10,
        update=update_palette)
    palette1_contrast: FloatProperty(
        default=1.0,
        max=3.0,
        min=0.0,
        name="Palette1 Contrast",
        options={'HIDDEN'},
        precision=3,
        step=10,
        update=update_palette)
    palette1_specular: FloatVectorProperty(
        default=[0.0, 0.5, 0.0, 1.0],
        max=1.0,
        min=0.0,
        name="Palette1 Specular",
        options={'HIDDEN'},
        precision=3,
        size=4,
        step=10,
        subtype='COLOR',
        update=update_palette)
    palette1_metallic_specular: FloatVectorProperty(
        default=[0.0, 0.5, 0.0, 1.0],
        max=1.0,
        min=0.0,
        name="Palette1 Metallic Specular",
        options={'HIDDEN'},
        precision=3,
        size=4,
        step=10,
        subtype='COLOR',
        update=update_palette)

    # NOTE: Palette2
    palette2_hue: FloatProperty(
        max=1.0,
        min=0.0,
        name="Palette2 Hue",
        options={'HIDDEN'},
        precision=3,
        step=10,
        update=update_palette)
    palette2_saturation: FloatProperty(
        default=0.5,
        max=1.0,
        min=0.0,
        name="Palette2 Saturation",
        options={'HIDDEN'},
        precision=3,
        step=10,
        update=update_palette)
    palette2_brightness: FloatProperty(
        max=1.0,
        min=-1.0,
        name="Palette2 Brightness",
        options={'HIDDEN'},
        precision=3,
        step=10,
        update=update_palette)
    palette2_contrast: FloatProperty(
        default=1.0,
        max=3.0,
        min=0.0,
        name="Palette2 Contrast",
        options={'HIDDEN'},
        precision=3,
        step=10,
        update=update_palette)
    palette2_specular: FloatVectorProperty(
        default=[0.0, 0.5, 0.0, 1.0],
        max=1.0,
        min=0.0,
        name="Palette2 Specular",
        options={'HIDDEN'},
        precision=3,
        size=4,
        step=10,
        subtype='COLOR',
        update=update_palette)
    palette2_metallic_specular: FloatVectorProperty(
        default=[0.0, 0.5, 0.0, 1.0],
        max=1.0,
        min=0.0,
        name="Palette2 Metallic Specular",
        options={'HIDDEN'},
        precision=3,
        size=4,
        step=10,
        subtype='COLOR',
        update=update_palette)

    # NOTE: Inputs
    flesh_brightness: FloatProperty(
        max=1.0,
        min=0.0,
        name="Flesh Brightness",
        options={'HIDDEN'},
        precision=3,
        subtype='FACTOR',
        update=update_flesh_brightness)
    flush_tone: FloatVectorProperty(
        default=[0.0, 0.0, 0.0, 1.0],
        max=1.0,
        min=0.0,
        name="Flush Tone",
        options={'HIDDEN'},
        size=4,
        subtype='COLOR',
        update=update_flush_tone)

    # NOTE: Initialization function, called when a new node is created.
    def init(self, context):
        # type: (Context) -> None
        self.node_tree = bpy.data.node_groups.new(self.name, "ShaderNodeTree")
        self.width = 240.0
        update_derived(self, context)

    # NOTE: Additional buttons displayed on the node.
    def draw_buttons(self, _context, layout):
        # type: (Context, UILayout) -> None
        split = layout.split(factor=0.33)

        col = split.column()
        col.label(text="Derived:")
        col.label(text="Alpha Mode:")
        if self.alpha_mode == CLIP[0]:
            col.label(text="Alpha Test Value:")

        col = split.column()
        col.prop(self, "derived", text="")
        col.prop(self, "alpha_mode", text="")
        if self.alpha_mode == CLIP[0]:
            col.prop(self, "alpha_test_value", text="")

        layout.separator()

        box = layout.box()
        col = box.column()
        col.label(text="DiffuseMap:")
        col.template_ID(self, "diffuseMap", new="image.new", open="image.open")
        col.label(text="RotationMap:")
        col.template_ID(self, "rotationMap", new="image.new", open="image.open")
        col.label(text="GlossMap:")
        col.template_ID(self, "glossMap", new="image.new", open="image.open")
        if self.derived in {EYE[0], GARMENT[0], HAIRC[0], SKINB[0]}:
            col.label(text="PaletteMap:")
            col.template_ID(self, "paletteMap", new="image.new", open="image.open")
        if self.derived in {CREATURE[0], EYE[0], GARMENT[0], HAIRC[0], SKINB[0]}:
            col.label(text="PaletteMaskMap:")
            col.template_ID(self, "paletteMaskMap", new="image.new", open="image.open")
        if self.derived in {CREATURE[0], HAIRC[0]}:
            col.label(text="DirectionMap:")
            col.template_ID(self, "directionMap", new="image.new", open="image.open")
        if self.derived == SKINB[0]:
            col.label(text="AgeMap:")
            col.template_ID(self, "ageMap", new="image.new", open="image.open")
            col.label(text="ComplexionMap:")
            col.template_ID(self, "complexionMap", new="image.new", open="image.open")
            col.label(text="FacepaintMap:")
            col.template_ID(self, "facepaintMap", new="image.new", open="image.open")

        box = layout.box()
        col = box.column()
        if self.derived in {EYE[0], GARMENT[0], HAIRC[0], SKINB[0]}:
            col.label(text="Palette:" if self.derived != GARMENT[0] else "Primary Palette:")
            col.prop(self, "palette1_hue", text="Hue")
            col.prop(self, "palette1_saturation", text="Saturation")
            col.prop(self, "palette1_brightness", text="Brightness")
            col.prop(self, "palette1_contrast", text="Contrast")
            col.separator()
            row = col.row()
            row.prop(self, "palette1_specular", text="Specular")
            row = col.row()
            row.prop(self, "palette1_metallic_specular", text="Metallic Specular")
        if self.derived in {CREATURE[0], SKINB[0]}:
            col.label(text="Inputs:")
            col.prop(self, "flesh_brightness", text="Flesh Brightness", slider=True)
            row = col.row()
            row.prop(self, "flush_tone", text="Flush Tone")
        if self.derived == GARMENT[0]:
            box = layout.box()
            col = box.column()
            col.label(text="Secondary Palette:")
            col.prop(self, "palette2_hue", text="Hue")
            col.prop(self, "palette2_saturation", text="Saturation")
            col.prop(self, "palette2_brightness", text="Brightness")
            col.prop(self, "palette2_contrast", text="Contrast")
            row = col.row()
            row.prop(self, "palette2_specular", text="Specular")
            row = col.row()
            row.prop(self, "palette2_metallic_specular", text="Metallic Specular")

    # NOTE: Detail button in the sidebar.
    #       If this function is not defined, the draw_buttons function is used instead.
    def draw_buttons_ext(self, context, layout):
        # type: (Context, UILayout) -> None
        self.draw_buttons(context, layout)

    # NOTE: Explicit user label overrides this, but here we can define a label dynamically.
    def draw_label(self):
        # type: () -> str
        for enum in {CREATURE, EYE, GARMENT, HAIRC, SKINB, UBER}:
            if self.derived == enum[0]:
                return f"SWTOR: {enum[1]} Shader"


class HeroNodeCategory(NodeCategory):

    @classmethod
    def poll(cls, context):
        # type: (Context) -> bool
        return (context.space_data.type == 'NODE_EDITOR' and
                context.space_data.tree_type == 'ShaderNodeTree')


node_categories = [
    HeroNodeCategory("HeroEngine", "SWTOR", items=[
        NodeItem("ShaderNodeHeroEngine",
                 label=f"{enum[1]} Shader",
                 settings={"Derived": repr(enum[0])}
                 ) for enum in {CREATURE, EYE, GARMENT, HAIRC, SKINB, UBER}]
    )
]


class NODE_OT_ngroup_edit(Operator):
    bl_label = "Edit Group"
    bl_description = "Edit Hero node group"
    bl_idname = "node.ngroup_edit"
    bl_options = {'REGISTER', 'UNDO'}

    exit: BoolProperty(name="Exit", description="", default=False)

    @classmethod
    def poll(cls, context):
        # type: (Context) -> bool
        space = context.space_data

        if space.type != 'NODE_EDITOR':
            return False
        if space.tree_type not in {"CompositorNodeTree", "ShaderNodeTree", "TextureNodeTree"}:
            return False

        return True

    def execute(self, context):
        # type: (Context) -> Set[str]
        space = context.space_data

        if hasattr(context, "node"):
            node = context.node
        else:
            node = getattr(context, "active_node", None)

        valid_node_groups = [
            "ShaderNodeHeroEngine",
            "CompositorNodeGroup",
            "ShaderNodeGroup",
            "TextureNodeGroup"
        ]

        if node and node.bl_idname in valid_node_groups and not self.exit:
            space.path.append(node_tree=node.node_tree, node=node)
        else:
            space.path.pop()

        return {'FINISHED'}
