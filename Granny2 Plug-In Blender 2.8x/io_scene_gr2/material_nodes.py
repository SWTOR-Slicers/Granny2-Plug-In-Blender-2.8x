# <pep8 compliant>

"""
This script defines the material types used by Star Wars: The Old Republic models.
"""

import bpy


class HairShader():
    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.use_nodes = True
        self.material.blend_method = 'CLIP'
        self.material.alpha_threshold = 0.5
        self.material.node_tree.nodes['Principled BSDF'].inputs[7].default_value = 0.673

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-800, 520)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-802, 297)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-800, 80)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-522, -1)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-522, -243)

    def DiffuseMap(self):
        # Create the DiffuseMap node group
        NodeGroup = bpy.data.node_groups.new(name="DiffuseMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-838, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Hair Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m Color')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (301, 103)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Color')

        # Create the Separate RGB nodes
        SeparateRGB1 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB1.location = (-566, 107)
        SeparateRGB2 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB2.location = (-566, -260)

        # Create the Mix RGB nodes
        MixRGB1 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        MixRGB1.location = (-322, -115)
        MixRGB1.blend_type = 'MIX'

        # Create the HSV node
        HSV = NodeGroup.nodes.new(type='ShaderNodeHueSaturation')
        HSV.location = (86, 154)

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], MixRGB1.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[1], MixRGB1.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[2], SeparateRGB2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[3], HSV.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[4], SeparateRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB1.outputs[0], MixRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB2.outputs[0], HSV.inputs[0])
        NodeGroup.links.new(SeparateRGB2.outputs[1], HSV.inputs[1])
        NodeGroup.links.new(SeparateRGB2.outputs[2], HSV.inputs[2])
        NodeGroup.links.new(MixRGB1.outputs[0], HSV.inputs[4])
        NodeGroup.links.new(HSV.outputs[0], GroupOutput.inputs[0])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "DiffuseMap"
        link.width = 218
        link.location = (-277, 343)

    def GlossMap(self):
        pass

    def RotationMap(self):
        # Create the RotationMap node group
        NodeGroup = bpy.data.node_groups.new(name="RotationMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-460, -173.7)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (450, 0)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Emission')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Alpha')
        NodeGroup.outputs.new(type='NodeSocketVector', name='Normal')

        # Create the Separate RGB node
        SeparateRGB = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB.location = (-272, -90)

        # Create the Invert nodes
        Invert1 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert1.location = (-85.9, -54.13)
        Invert2 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert2.location = (-85.9, -176.7)

        # Create the Combine RGB node
        CombineRGB = NodeGroup.nodes.new(type='ShaderNodeCombineRGB')
        CombineRGB.location = (90, -10)
        CombineRGB.inputs[2].default_value = 1.0

        # Create the Normal Map node
        NormalMap = NodeGroup.nodes.new(type='ShaderNodeNormalMap')
        NormalMap.location = (250, 90)
        NormalMap.space = 'TANGENT'
        NormalMap.inputs[0].default_value = 2.0

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SeparateRGB.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], CombineRGB.inputs[0])
        NodeGroup.links.new(SeparateRGB.outputs[0], Invert2.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[1], Invert1.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[2], GroupOutput.inputs[0])
        NodeGroup.links.new(Invert1.outputs[0], CombineRGB.inputs[1])
        NodeGroup.links.new(Invert2.outputs[0], GroupOutput.inputs[1])
        NodeGroup.links.new(CombineRGB.outputs[0], NormalMap.inputs[1])
        NodeGroup.links.new(NormalMap.outputs[0], GroupOutput.inputs[2])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "RotationMap"
        link.location = (-200, -222)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Node Groups
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['DiffuseMap'].inputs[1])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['DiffuseMap'].inputs[2])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['DiffuseMap'].inputs[3])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['DiffuseMap'].inputs[4])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['Principled BSDF'].inputs[5])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['RotationMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['RotationMap'].inputs[1])

        # Link Node Groups to PBDSF node
        links.new(nodes['DiffuseMap'].outputs[0], nodes['Principled BSDF'].inputs[0])
        # links.new(nodes['GlossMap'].outputs[0], nodes['Principled BSDF'].inputs[5])
        links.new(nodes['RotationMap'].outputs[0], nodes['Principled BSDF'].inputs[17])
        links.new(nodes['RotationMap'].outputs[1], nodes['Principled BSDF'].inputs[18])
        links.new(nodes['RotationMap'].outputs[2], nodes['Principled BSDF'].inputs[19])

    def build(self):
        self.TextureNodes()
        self.DiffuseMap()
        self.GlossMap()
        self.RotationMap()
        self.LinkNodes()


class HeadMaterial():
    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.use_nodes = True
        self.material.node_tree.nodes['Principled BSDF'].inputs[7].default_value = 0.673

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-800, 520)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-802, 297)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-800, 80)

        # Complexion
        _x = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _x.name = _x.label = "ComplexionMap"
        _x.location = (-800, -140)

        # Make-up
        _u = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _u.name = _u.label = "Make-up"
        _u.location = (-800, -364)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-522, -144)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-522, -363)

    def DiffuseMap(self):
        # Create the DiffuseMap node group
        NodeGroup = bpy.data.node_groups.new(name="DiffuseMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-838, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Skin Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='ComplexionMap Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='Make-up Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Make-Up Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (546, -6)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Color')

        # Create the Separate RGB nodes
        SeparateRGB1 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB1.location = (-566, 107)
        SeparateRGB2 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB2.location = (-566, -260)

        # Create the Mix RGB nodes
        MixRGB1 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        MixRGB1.location = (-322, -115)
        MixRGB1.blend_type = 'COLOR'
        MixRGB2 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        MixRGB2.location = (109, 83)
        MixRGB2.blend_type = 'MULTIPLY'
        MixRGB2.inputs[0].default_value = 1.0
        MixRGB3 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        MixRGB3.location = (328, -45)
        MixRGB3.blend_type = 'MIX'

        # Create the HSV node
        HSV = NodeGroup.nodes.new(type='ShaderNodeHueSaturation')
        HSV.location = (-119, 127)

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], MixRGB1.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[1], MixRGB1.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[2], SeparateRGB1.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[3], HSV.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[4], SeparateRGB2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[5], MixRGB2.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[6], MixRGB3.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[7], MixRGB3.inputs[0])
        NodeGroup.links.new(SeparateRGB2.outputs[0], MixRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB1.outputs[0], HSV.inputs[0])
        NodeGroup.links.new(SeparateRGB1.outputs[1], HSV.inputs[1])
        NodeGroup.links.new(SeparateRGB1.outputs[2], HSV.inputs[2])
        NodeGroup.links.new(MixRGB1.outputs[0], HSV.inputs[4])
        NodeGroup.links.new(HSV.outputs[0], MixRGB2.inputs[1])
        NodeGroup.links.new(MixRGB2.outputs[0], MixRGB3.inputs[1])
        NodeGroup.links.new(MixRGB3.outputs[0], GroupOutput.inputs[0])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "DiffuseMap"
        link.width = 218
        link.location = (-277, 343)

    def GlossMap(self):
        # Create the GlossMap node group
        NodeGroup = bpy.data.node_groups.new(name="GlossMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-370, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_s Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (370, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Specular')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Roughness')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Clearcoat')

        # Create RGB to BW node
        RGBtoBW = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        RGBtoBW.location = (-194, 64)

        # Create Power node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.location = (-16.6, 132.5)
        Power.operation = 'POWER'
        Power.inputs[1].default_value = 2.0

        # Create Invert nodes
        Invert1 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert1.location = (170, 64)
        Invert2 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert2.location = (170, -49)

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], RGBtoBW.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[0], GroupOutput.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[1], Invert2.inputs[1])
        NodeGroup.links.new(RGBtoBW.outputs[0], Power.inputs[0])
        NodeGroup.links.new(Power.outputs[0], Invert1.inputs[1])
        NodeGroup.links.new(Invert1.outputs[0], GroupOutput.inputs[0])
        NodeGroup.links.new(Invert2.outputs[0], GroupOutput.inputs[1])

        # Link the GlossMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "GlossMap"
        link.location = (-201, -15.6)

    def RotationMap(self):
        # Create the RotationMap node group
        NodeGroup = bpy.data.node_groups.new(name="RotationMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-460, -173.7)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (450, 0)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Emission')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Alpha')
        NodeGroup.outputs.new(type='NodeSocketVector', name='Normal')

        # Create the Separate RGB node
        SeparateRGB = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB.location = (-272, -90)

        # Create the Invert nodes
        Invert1 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert1.location = (-85.9, -54.13)
        Invert2 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert2.location = (-85.9, -176.7)

        # Create the Combine RGB node
        CombineRGB = NodeGroup.nodes.new(type='ShaderNodeCombineRGB')
        CombineRGB.location = (90, -10)
        CombineRGB.inputs[2].default_value = 1.0

        # Create the Normal Map node
        NormalMap = NodeGroup.nodes.new(type='ShaderNodeNormalMap')
        NormalMap.location = (250, 90)
        NormalMap.space = 'TANGENT'
        NormalMap.inputs[0].default_value = 2.0

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SeparateRGB.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], CombineRGB.inputs[0])
        NodeGroup.links.new(SeparateRGB.outputs[0], Invert2.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[1], Invert1.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[2], GroupOutput.inputs[0])
        NodeGroup.links.new(Invert1.outputs[0], CombineRGB.inputs[1])
        NodeGroup.links.new(Invert2.outputs[0], GroupOutput.inputs[1])
        NodeGroup.links.new(CombineRGB.outputs[0], NormalMap.inputs[1])
        NodeGroup.links.new(NormalMap.outputs[0], GroupOutput.inputs[2])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "RotationMap"
        link.location = (-200, -222)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Node Groups
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['DiffuseMap'].inputs[1])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['DiffuseMap'].inputs[2])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['DiffuseMap'].inputs[3])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['DiffuseMap'].inputs[4])
        links.new(nodes['ComplexionMap'].outputs[0], nodes['DiffuseMap'].inputs[5])
        links.new(nodes['Make-up'].outputs[0], nodes['DiffuseMap'].inputs[6])
        links.new(nodes['Make-up'].outputs[1], nodes['DiffuseMap'].inputs[7])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['GlossMap'].inputs[0])
        links.new(nodes['_s GlossMap'].outputs[1], nodes['GlossMap'].inputs[1])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['RotationMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['RotationMap'].inputs[1])

        # Link Node Groups to PBDSF node
        links.new(nodes['DiffuseMap'].outputs[0], nodes['Principled BSDF'].inputs[0])
        links.new(nodes['GlossMap'].outputs[0], nodes['Principled BSDF'].inputs[5])
        links.new(nodes['GlossMap'].outputs[1], nodes['Principled BSDF'].inputs[7])
        links.new(nodes['GlossMap'].outputs[2], nodes['Principled BSDF'].inputs[12])
        links.new(nodes['RotationMap'].outputs[0], nodes['Principled BSDF'].inputs[17])
        links.new(nodes['RotationMap'].outputs[1], nodes['Principled BSDF'].inputs[18])
        links.new(nodes['RotationMap'].outputs[2], nodes['Principled BSDF'].inputs[19])

    def build(self):
        self.TextureNodes()
        self.DiffuseMap()
        self.GlossMap()
        self.RotationMap()
        self.LinkNodes()


class EyeShader():
    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.use_nodes = True
        self.material.node_tree.nodes['Principled BSDF'].inputs[7].default_value = 0.673

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-800, 520)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-802, 297)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-800, 80)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-522, -1)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-522, -243)

    def DiffuseMap(self):
        # Create the DiffuseMap node group
        NodeGroup = bpy.data.node_groups.new(name="DiffuseMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-838, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Eye Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m Color')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (301, 103)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Color')

        # Create the Separate RGB nodes
        SeparateRGB1 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB1.location = (-566, 107)
        SeparateRGB2 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB2.location = (-566, -260)

        # Create the Mix RGB nodes
        MixRGB1 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        MixRGB1.location = (-322, -115)
        MixRGB1.blend_type = 'MULTIPLY'

        # Create the Invert node
        Invert = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert.location = (-320, 7)

        # Create the HSV node
        HSV = NodeGroup.nodes.new(type='ShaderNodeHueSaturation')
        HSV.location = (86, 154)

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], MixRGB1.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[1], MixRGB1.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[2], SeparateRGB2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[3], HSV.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[4], SeparateRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB1.outputs[0], MixRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB2.outputs[0], HSV.inputs[0])
        NodeGroup.links.new(SeparateRGB2.outputs[1], HSV.inputs[1])
        NodeGroup.links.new(SeparateRGB2.outputs[2], Invert.inputs[1])
        NodeGroup.links.new(Invert.outputs[0], HSV.inputs[2])
        NodeGroup.links.new(MixRGB1.outputs[0], HSV.inputs[4])
        NodeGroup.links.new(HSV.outputs[0], GroupOutput.inputs[0])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "DiffuseMap"
        link.width = 218
        link.location = (-277, 343)

    def GlossMap(self):
        # Create the GlossMap node group
        NodeGroup = bpy.data.node_groups.new(name="GlossMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-370, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_s Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (370, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Specular')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Roughness')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Clearcoat')

        # Create RGB to BW node
        RGBtoBW = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        RGBtoBW.location = (-194, 64)

        # Create Power node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.location = (-16.6, 132.5)
        Power.operation = 'POWER'
        Power.inputs[1].default_value = 2.0

        # Create Invert nodes
        Invert1 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert1.location = (170, 64)
        Invert2 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert2.location = (170, -49)

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], RGBtoBW.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[0], GroupOutput.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[1], Invert2.inputs[1])
        NodeGroup.links.new(RGBtoBW.outputs[0], Power.inputs[0])
        NodeGroup.links.new(Power.outputs[0], Invert1.inputs[1])
        NodeGroup.links.new(Invert1.outputs[0], GroupOutput.inputs[0])
        NodeGroup.links.new(Invert2.outputs[0], GroupOutput.inputs[1])

        # Link the GlossMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "GlossMap"
        link.location = (-199, -41)

    def RotationMap(self):
        # Create the RotationMap node group
        NodeGroup = bpy.data.node_groups.new(name="RotationMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-460, -173.7)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (450, 0)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Emission')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Alpha')
        NodeGroup.outputs.new(type='NodeSocketVector', name='Normal')

        # Create the Separate RGB node
        SeparateRGB = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB.location = (-272, -90)

        # Create the Invert nodes
        Invert1 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert1.location = (-85.9, -54.13)
        Invert2 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert2.location = (-85.9, -176.7)

        # Create the Combine RGB node
        CombineRGB = NodeGroup.nodes.new(type='ShaderNodeCombineRGB')
        CombineRGB.location = (90, -10)
        CombineRGB.inputs[2].default_value = 1.0

        # Create the Normal Map node
        NormalMap = NodeGroup.nodes.new(type='ShaderNodeNormalMap')
        NormalMap.location = (250, 90)
        NormalMap.space = 'TANGENT'
        NormalMap.inputs[0].default_value = 2.0

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SeparateRGB.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], CombineRGB.inputs[0])
        NodeGroup.links.new(SeparateRGB.outputs[0], Invert2.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[1], Invert1.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[2], GroupOutput.inputs[0])
        NodeGroup.links.new(Invert1.outputs[0], CombineRGB.inputs[1])
        NodeGroup.links.new(Invert2.outputs[0], GroupOutput.inputs[1])
        NodeGroup.links.new(CombineRGB.outputs[0], NormalMap.inputs[1])
        NodeGroup.links.new(NormalMap.outputs[0], GroupOutput.inputs[2])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "RotationMap"
        link.location = (-200, -222)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Node Groups
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['DiffuseMap'].inputs[1])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['DiffuseMap'].inputs[2])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['DiffuseMap'].inputs[3])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['DiffuseMap'].inputs[4])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['GlossMap'].inputs[0])
        links.new(nodes['_s GlossMap'].outputs[1], nodes['GlossMap'].inputs[1])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['RotationMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['RotationMap'].inputs[1])

        # Link Node Groups to PBDSF node
        links.new(nodes['DiffuseMap'].outputs[0], nodes['Principled BSDF'].inputs[0])
        links.new(nodes['GlossMap'].outputs[0], nodes['Principled BSDF'].inputs[5])
        links.new(nodes['GlossMap'].outputs[1], nodes['Principled BSDF'].inputs[7])
        links.new(nodes['GlossMap'].outputs[2], nodes['Principled BSDF'].inputs[12])
        links.new(nodes['RotationMap'].outputs[0], nodes['Principled BSDF'].inputs[17])
        links.new(nodes['RotationMap'].outputs[1], nodes['Principled BSDF'].inputs[18])
        links.new(nodes['RotationMap'].outputs[2], nodes['Principled BSDF'].inputs[19])

    def build(self):
        self.TextureNodes()
        self.DiffuseMap()
        self.GlossMap()
        self.RotationMap()
        self.LinkNodes()


class SkinBShader():
    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.use_nodes = True
        self.material.blend_method = 'CLIP'
        self.material.alpha_threshold = 0.5
        self.material.node_tree.nodes['Principled BSDF'].inputs[7].default_value = 0.673

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-800, 520)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-802, 297)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-800, 80)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-522, -1)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-522, -243)

    def DiffuseMap(self):
        # Create the DiffuseMap node group
        NodeGroup = bpy.data.node_groups.new(name="DiffuseMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-838, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Skin Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m Color')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (301, 103)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Color')

        # Create the Separate RGB nodes
        SeparateRGB1 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB1.location = (-566, 107)
        SeparateRGB2 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB2.location = (-566, -260)

        # Create the Mix RGB nodes
        MixRGB1 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        MixRGB1.location = (-322, -115)
        MixRGB1.blend_type = 'MIX'

        # Create the HSV node
        HSV = NodeGroup.nodes.new(type='ShaderNodeHueSaturation')
        HSV.location = (86, 154)

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], MixRGB1.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[1], MixRGB1.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[2], SeparateRGB2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[3], HSV.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[4], SeparateRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB1.outputs[0], MixRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB2.outputs[0], HSV.inputs[0])
        NodeGroup.links.new(SeparateRGB2.outputs[1], HSV.inputs[1])
        NodeGroup.links.new(SeparateRGB2.outputs[2], HSV.inputs[2])
        NodeGroup.links.new(MixRGB1.outputs[0], HSV.inputs[4])
        NodeGroup.links.new(HSV.outputs[0], GroupOutput.inputs[0])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "DiffuseMap"
        link.width = 218
        link.location = (-277, 343)

    def GlossMap(self):
        # Create the GlossMap node group
        NodeGroup = bpy.data.node_groups.new(name="GlossMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-370, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s Color')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (370, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Specular')

        # Create RGB to BW node
        RGBtoBW = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        RGBtoBW.location = (-194, 64)

        # Create Power node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.location = (-16.6, 132.5)
        Power.operation = 'POWER'
        Power.inputs[1].default_value = 2.0

        # Create Invert nodes
        Invert = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert.location = (170, 64)

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], RGBtoBW.inputs[0])
        NodeGroup.links.new(RGBtoBW.outputs[0], Power.inputs[0])
        NodeGroup.links.new(Power.outputs[0], Invert.inputs[1])
        NodeGroup.links.new(Invert.outputs[0], GroupOutput.inputs[0])

        # Link the GlossMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "GlossMap"
        link.location = (-199, -41)

    def RotationMap(self):
        # Create the RotationMap node group
        NodeGroup = bpy.data.node_groups.new(name="RotationMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-460, -173.7)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (450, 0)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Emission')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Alpha')
        NodeGroup.outputs.new(type='NodeSocketVector', name='Normal')

        # Create the Separate RGB node
        SeparateRGB = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB.location = (-272, -90)

        # Create the Invert nodes
        Invert1 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert1.location = (-85.9, -54.13)
        Invert2 = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert2.location = (-85.9, -176.7)

        # Create the Combine RGB node
        CombineRGB = NodeGroup.nodes.new(type='ShaderNodeCombineRGB')
        CombineRGB.location = (90, -10)
        CombineRGB.inputs[2].default_value = 1.0

        # Create the Normal Map node
        NormalMap = NodeGroup.nodes.new(type='ShaderNodeNormalMap')
        NormalMap.location = (250, 90)
        NormalMap.space = 'TANGENT'
        NormalMap.inputs[0].default_value = 2.0

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SeparateRGB.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], CombineRGB.inputs[0])
        NodeGroup.links.new(SeparateRGB.outputs[0], Invert2.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[1], Invert1.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[2], GroupOutput.inputs[0])
        NodeGroup.links.new(Invert1.outputs[0], CombineRGB.inputs[1])
        NodeGroup.links.new(Invert2.outputs[0], GroupOutput.inputs[1])
        NodeGroup.links.new(CombineRGB.outputs[0], NormalMap.inputs[1])
        NodeGroup.links.new(NormalMap.outputs[0], GroupOutput.inputs[2])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "RotationMap"
        link.location = (-200, -222)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Node Groups
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['DiffuseMap'].inputs[1])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['DiffuseMap'].inputs[2])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['DiffuseMap'].inputs[3])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['DiffuseMap'].inputs[4])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['GlossMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['RotationMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['RotationMap'].inputs[1])

        # Link Node Groups to PBDSF node
        links.new(nodes['DiffuseMap'].outputs[0], nodes['Principled BSDF'].inputs[0])
        links.new(nodes['GlossMap'].outputs[0], nodes['Principled BSDF'].inputs[5])
        links.new(nodes['RotationMap'].outputs[0], nodes['Principled BSDF'].inputs[17])
        links.new(nodes['RotationMap'].outputs[1], nodes['Principled BSDF'].inputs[18])
        links.new(nodes['RotationMap'].outputs[2], nodes['Principled BSDF'].inputs[19])

    def build(self):
        self.TextureNodes()
        self.DiffuseMap()
        self.GlossMap()
        self.RotationMap()
        self.LinkNodes()


class GarmentShader():
    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.use_nodes = True
        self.material.node_tree.nodes['Principled BSDF'].inputs[7].default_value = 0.673

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-800, 520)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-802, 297)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-800, 80)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-522, -1)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-522, -243)

    def DiffuseMap(self):
        # Create the DiffuseMap node group
        NodeGroup = bpy.data.node_groups.new(name="DiffuseMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-838, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Primary Dye')
        NodeGroup.inputs.new(type='NodeSocketColor', name='Secondary Dye')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m Color')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (301, 103)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Color')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Metallic')

        # Create the Separate RGB nodes
        SeparateRGB1 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB1.location = (-566, 107)
        SeparateRGB2 = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB2.location = (-566, -260)

        # Create the Mix RGB nodes
        MixRGB1 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        MixRGB1.location = (-322, -115)
        MixRGB1.blend_type = 'MIX'
        MixRGB2 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        MixRGB2.location = (-112, 21)
        MixRGB2.blend_type = 'MIX'

        # Create the HSV node
        HSV = NodeGroup.nodes.new(type='ShaderNodeHueSaturation')
        HSV.location = (86, 154)

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], MixRGB1.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[1], MixRGB2.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[2], MixRGB1.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[3], SeparateRGB2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[4], HSV.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[5], SeparateRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB1.outputs[0], MixRGB1.inputs[0])
        NodeGroup.links.new(SeparateRGB1.outputs[1], MixRGB2.inputs[0])
        NodeGroup.links.new(SeparateRGB1.outputs[2], GroupOutput.inputs[1])
        NodeGroup.links.new(SeparateRGB2.outputs[0], HSV.inputs[0])
        NodeGroup.links.new(SeparateRGB2.outputs[1], HSV.inputs[1])
        NodeGroup.links.new(SeparateRGB2.outputs[2], HSV.inputs[2])
        NodeGroup.links.new(MixRGB1.outputs[0], MixRGB2.inputs[1])
        NodeGroup.links.new(MixRGB2.outputs[0], HSV.inputs[4])
        NodeGroup.links.new(HSV.outputs[0], GroupOutput.inputs[0])

        # Link the DiffuseMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "DiffuseMap"
        link.width = 218
        link.location = (-277, 343)

    def GlossMap(self):
        # Create the GlossMap node group
        NodeGroup = bpy.data.node_groups.new(name="GlossMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-370, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s Color')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (370, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Specular')

        # Create RGB to BW node
        RGBtoBW = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        RGBtoBW.location = (-194, 64)

        # Create Power node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.location = (-16.6, 132.5)
        Power.operation = 'POWER'
        Power.inputs[1].default_value = 2.0

        # Create Invert nodes
        Invert = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert.location = (170, 64)

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], RGBtoBW.inputs[0])
        NodeGroup.links.new(RGBtoBW.outputs[0], Power.inputs[0])
        NodeGroup.links.new(Power.outputs[0], Invert.inputs[1])
        NodeGroup.links.new(Invert.outputs[0], GroupOutput.inputs[0])

        # Link the GlossMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "GlossMap"
        link.location = (-199, -41)

    def RotationMap(self):
        # Create the RotationMap node group
        NodeGroup = bpy.data.node_groups.new(name="RotationMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-460, -173.7)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (450, 0)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Emission')
        NodeGroup.outputs.new(type='NodeSocketVector', name='Normal')

        # Create the Separate RGB node
        SeparateRGB = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB.location = (-272, -90)

        # Create the Invert node
        Invert = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert.location = (-85.9, -54.13)

        # Create the Combine RGB node
        CombineRGB = NodeGroup.nodes.new(type='ShaderNodeCombineRGB')
        CombineRGB.location = (90, -10)
        CombineRGB.inputs[2].default_value = 1.0

        # Create the Normal Map node
        NormalMap = NodeGroup.nodes.new(type='ShaderNodeNormalMap')
        NormalMap.location = (250, 90)
        NormalMap.space = 'TANGENT'
        NormalMap.inputs[0].default_value = 2.0

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SeparateRGB.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], CombineRGB.inputs[0])
        NodeGroup.links.new(SeparateRGB.outputs[1], Invert.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[2], GroupOutput.inputs[0])
        NodeGroup.links.new(Invert.outputs[0], CombineRGB.inputs[1])
        NodeGroup.links.new(CombineRGB.outputs[0], NormalMap.inputs[1])
        NodeGroup.links.new(NormalMap.outputs[0], GroupOutput.inputs[1])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "RotationMap"
        link.location = (-200, -222)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Node Groups
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['DiffuseMap'].inputs[2])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['DiffuseMap'].inputs[3])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['DiffuseMap'].inputs[4])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['DiffuseMap'].inputs[5])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['GlossMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['RotationMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['RotationMap'].inputs[1])

        # Link Node Groups to PBDSF node
        links.new(nodes['DiffuseMap'].outputs[0], nodes['Principled BSDF'].inputs[0])
        links.new(nodes['DiffuseMap'].outputs[1], nodes['Principled BSDF'].inputs[4])
        links.new(nodes['GlossMap'].outputs[0], nodes['Principled BSDF'].inputs[5])
        links.new(nodes['RotationMap'].outputs[0], nodes['Principled BSDF'].inputs[17])
        links.new(nodes['RotationMap'].outputs[1], nodes['Principled BSDF'].inputs[19])

    def build(self):
        self.TextureNodes()
        self.DiffuseMap()
        self.GlossMap()
        self.RotationMap()
        self.LinkNodes()


class UberShader():
    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.use_nodes = True
        self.material.node_tree.nodes['Principled BSDF'].inputs[7].default_value = 0.673

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-522, 299)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-522, 19)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-522, -261)

    def GlossMap(self):
        # Create the GlossMap node group
        NodeGroup = bpy.data.node_groups.new(name="GlossMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-370, 0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s Color')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (370, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Specular')

        # Create RGB to BW node
        RGBtoBW = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        RGBtoBW.location = (-194, 64)

        # Create Power node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.location = (-16.6, 132.5)
        Power.operation = 'POWER'
        Power.inputs[1].default_value = 2.0

        # Create Invert nodes
        Invert = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert.location = (170, 64)

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], RGBtoBW.inputs[0])
        NodeGroup.links.new(RGBtoBW.outputs[0], Power.inputs[0])
        NodeGroup.links.new(Power.outputs[0], Invert.inputs[1])
        NodeGroup.links.new(Invert.outputs[0], GroupOutput.inputs[0])

        # Link the GlossMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "GlossMap"
        link.location = (-200, -41)

    def RotationMap(self):
        # Create the RotationMap node group
        NodeGroup = bpy.data.node_groups.new(name="RotationMap", type='ShaderNodeTree')

        # Create the Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-460, -173.7)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n Alpha')

        # Create the Group Output node
        GroupOutput = NodeGroup.nodes.new('NodeGroupOutput')
        GroupOutput.location = (450, 0)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Emission')
        NodeGroup.outputs.new(type='NodeSocketVector', name='Normal')

        # Create the Separate RGB node
        SeparateRGB = NodeGroup.nodes.new(type='ShaderNodeSeparateRGB')
        SeparateRGB.location = (-272, -90)

        # Create the Invert node
        Invert = NodeGroup.nodes.new(type='ShaderNodeInvert')
        Invert.location = (-85.9, -54.13)

        # Create the Combine RGB node
        CombineRGB = NodeGroup.nodes.new(type='ShaderNodeCombineRGB')
        CombineRGB.location = (90, -10)
        CombineRGB.inputs[2].default_value = 1.0

        # Create the Normal Map node
        NormalMap = NodeGroup.nodes.new(type='ShaderNodeNormalMap')
        NormalMap.location = (250, 90)
        NormalMap.space = 'TANGENT'
        NormalMap.inputs[0].default_value = 2.0

        # Link the nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SeparateRGB.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], CombineRGB.inputs[0])
        NodeGroup.links.new(SeparateRGB.outputs[1], Invert.inputs[1])
        NodeGroup.links.new(SeparateRGB.outputs[2], GroupOutput.inputs[0])
        NodeGroup.links.new(Invert.outputs[0], CombineRGB.inputs[1])
        NodeGroup.links.new(CombineRGB.outputs[0], NormalMap.inputs[1])
        NodeGroup.links.new(NormalMap.outputs[0], GroupOutput.inputs[1])

        # Link the RotationMap node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "RotationMap"
        link.location = (-200, -222)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Node Groups
        links.new(nodes['_s GlossMap'].outputs[0], nodes['GlossMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['RotationMap'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['RotationMap'].inputs[1])

        # Link Node Groups to PBDSF node
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['Principled BSDF'].inputs[0])
        links.new(nodes['GlossMap'].outputs[0], nodes['Principled BSDF'].inputs[5])
        links.new(nodes['RotationMap'].outputs[0], nodes['Principled BSDF'].inputs[17])
        links.new(nodes['RotationMap'].outputs[1], nodes['Principled BSDF'].inputs[19])

    def build(self):
        self.TextureNodes()
        self.GlossMap()
        self.RotationMap()
        self.LinkNodes()
