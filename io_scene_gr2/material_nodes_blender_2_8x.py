# <pep8 compliant>

"""
This script defines the shader types used by Star Wars: The Old Republic models.
"""

import bpy


class CommonGroups():

    def AdjustLightness():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='AdjustLightness', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-827, 200)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='L')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='AO')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.Z')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.W')

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (-619, 153)
        Power.operation = 'POWER'

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (-429, 153)
        Mul1.operation = 'MULTIPLY'

        # Add a Subtract math node
        Sub1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub1.name = "Subtract.001"
        Sub1.location = (-30, 153)
        Sub1.operation = 'SUBTRACT'
        Sub1.inputs[0].default_value = 1.0

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (160, 153)
        Mul2.operation = 'MULTIPLY'

        # Add a Add math node
        Add1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add1.name = "Add.001"
        Add1.location = (350, 153)
        Add1.operation = 'ADD'

        # Add a Add math node
        Add2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add2.name = "Add.002"
        Add2.location = (-429, -113)
        Add2.operation = 'ADD'
        Add2.inputs[1].default_value = 1.0

        # Add a Subtract math node
        Sub2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub2.name = "Subtract.002"
        Sub2.location = (-239, -113)
        Sub2.operation = 'SUBTRACT'
        Sub2.inputs[0].default_value = 1.0

        # Add a Multiply math node
        Mul3 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul3.name = "Multiply.003"
        Mul3.location = (-49, -113)
        Mul3.operation = 'MULTIPLY'

        # Add a Add math node
        Add3 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add3.name = "Add.003"
        Add3.location = (141, -113)
        Add3.operation = 'ADD'

        # Add a Multiply math node
        Mul4 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul4.name = "Multiply.004"
        Mul4.location = (331, -113)
        Mul4.operation = 'MULTIPLY'

        # Add a Clamp node
        Clamp = NodeGroup.nodes.new(type='ShaderNodeClamp')
        Clamp.name = "Clamp"
        Clamp.location = (545, -113)
        Clamp.clamp_type = 'RANGE'
        Clamp.inputs[1].default_value = 0.0
        Clamp.inputs[2].default_value = 1.0

        # Add a Multiply math node
        Mul5 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul5.name = "Multiply.005"
        Mul5.location = (726, 53)
        Mul5.operation = 'MULTIPLY'

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (923, 10)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='L')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Power.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Mul3.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[1], Mul4.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Sub1.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[2], Add1.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Add2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[3], Power.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[3], Mul1.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul1.inputs[0])
        NodeGroup.links.new(Mul1.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Sub1.outputs[0], Mul2.inputs[0])
        NodeGroup.links.new(Mul2.outputs[0], Add1.inputs[1])
        NodeGroup.links.new(Add1.outputs[0], Mul5.inputs[0])
        NodeGroup.links.new(Add2.outputs[0], Sub2.inputs[1])
        NodeGroup.links.new(Add2.outputs[0], Add3.inputs[0])
        NodeGroup.links.new(Sub2.outputs[0], Mul3.inputs[0])
        NodeGroup.links.new(Mul3.outputs[0], Add3.inputs[1])
        NodeGroup.links.new(Add3.outputs[0], Mul4.inputs[1])
        NodeGroup.links.new(Mul4.outputs[0], Clamp.inputs[0])
        NodeGroup.links.new(Clamp.outputs[0], Mul5.inputs[1])
        NodeGroup.links.new(Mul5.outputs[0], GroupOutput.inputs[0])

    def AdjustSkinLightness():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='AdjustSkinLightness', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-827, 200)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='L')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.Z')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.W')

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (-619, 153)
        Power.operation = 'POWER'

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (-429, 153)
        Mul1.operation = 'MULTIPLY'

        # Add a Subtract math node
        Sub = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub.name = "Subtract"
        Sub.location = (-30, 153)
        Sub.operation = 'SUBTRACT'
        Sub.inputs[0].default_value = 1.0

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (160, 153)
        Mul2.operation = 'MULTIPLY'

        # Add a Add math node
        Add = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add.name = "Add"
        Add.location = (350, 153)
        Add.operation = 'ADD'

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (923, 10)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='L')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Power.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Sub.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[1], Add.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Power.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[2], Mul1.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul1.inputs[0])
        NodeGroup.links.new(Mul1.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Sub.outputs[0], Mul2.inputs[0])
        NodeGroup.links.new(Mul2.outputs[0], Add.inputs[1])
        NodeGroup.links.new(Add.outputs[0], GroupOutput.inputs[0])

    def DoublePaletteLerp():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='DoublePaletteLerp', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-540, 8)
        NodeGroup.inputs.new(type='NodeSocketColor', name='DiffuseMap Color')
        NodeGroup.inputs.new(type='NodeSocketVector', name='PaletteMask')
        NodeGroup.inputs.new(type='NodeSocketVector', name='Palette2')
        NodeGroup.inputs.new(type='NodeSocketVector', name='Palette1')

        # Add a Separate XYZ node
        SepXYZ = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ.name = "Separate XYZ"
        SepXYZ.location = (-358, 8)

        # Add a Less Than math node
        LThan1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        LThan1.name = "Less Than.001"
        LThan1.location = (-169, 45)
        LThan1.operation = 'LESS_THAN'

        # Add a Multiply vector math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (17, 147)
        Mul1.operation = 'MULTIPLY'

        # Add a Less Than math node
        LThan2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        LThan2.name = "Less Than.002"
        LThan2.location = (17, -13)
        LThan2.operation = 'LESS_THAN'
        LThan2.inputs[1].default_value = 1.0

        # Add a Multiply vector math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (197, -12)
        Mul2.operation = 'MULTIPLY'

        # Add a Add math node
        Add1 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Add1.name = "Add.001"
        Add1.location = (379, 92)
        Add1.operation = 'ADD'

        # Add a Add math node
        Add2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add2.name = "Add.002"
        Add2.location = (379, -85)
        Add2.operation = 'ADD'

        # Add a RGB Mix node
        Mix = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        Mix.name = "Mix RGB"
        Mix.location = (624, 61)
        Mix.blend_type = 'MIX'

        # Add a Gamma node
        Gamma = NodeGroup.nodes.new(type='ShaderNodeGamma')
        Gamma.name = "Gamma"
        Gamma.location = (818, 23)
        Gamma.inputs[1].default_value = 2.1

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (1004, -5)
        NodeGroup.outputs.new(type='NodeSocketColor', name='RGB')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Mix.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[1], SepXYZ.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Mul1.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[3], Mul2.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[0], LThan1.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[0], Add2.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[1], LThan1.inputs[1])
        NodeGroup.links.new(SepXYZ.outputs[1], Add2.inputs[1])
        NodeGroup.links.new(LThan1.outputs[0], Mul1.inputs[1])
        NodeGroup.links.new(LThan1.outputs[0], LThan2.inputs[0])
        NodeGroup.links.new(Mul1.outputs[0], Add1.inputs[0])
        NodeGroup.links.new(LThan2.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Mul2.outputs[0], Add1.inputs[1])
        NodeGroup.links.new(Add1.outputs[0], Mix.inputs[2])
        NodeGroup.links.new(Add2.outputs[0], Mix.inputs[0])
        NodeGroup.links.new(Mix.outputs[0], Gamma.inputs[0])
        NodeGroup.links.new(Gamma.outputs[0], GroupOutput.inputs[0])

    def ExpandHSL():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='ExpandHSL', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-686, -29)
        NodeGroup.inputs.new(type='NodeSocketColor', name='PaletteMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='PaletteMap Alpha')

        # Add a Separate XYZ node
        SepXYZ = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ.name = "Separate XYZ"
        SepXYZ.location = (-494, 68)

        # Add a Multiply Add math node
        MulAdd = NodeGroup.nodes.new(type='ShaderNodeMath')
        MulAdd.name = "Multiply Add"
        MulAdd.location = (-283, 200)
        MulAdd.operation = 'MULTIPLY_ADD'
        MulAdd.inputs[1].default_value = 0.706 - 0.3137
        MulAdd.inputs[2].default_value = 0.3137

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (-283, 11)
        Mul1.operation = 'MULTIPLY'
        Mul1.inputs[1].default_value = 0.5882

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (-283, -154)
        Mul2.operation = 'MULTIPLY'
        Mul2.inputs[1].default_value = 0.70588

        # Add a Subtract math node
        Sub = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub.name = "Subtract"
        Sub.location = (-98, 200)
        Sub.operation = 'SUBTRACT'
        Sub.inputs[1].default_value = 0.41176

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (233, 46)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='H')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='S')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='L')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='AO')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SepXYZ.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Mul2.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[0], GroupOutput.inputs[3])
        NodeGroup.links.new(SepXYZ.outputs[1], MulAdd.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[2], Mul1.inputs[0])
        NodeGroup.links.new(MulAdd.outputs[0], Sub.inputs[0])
        NodeGroup.links.new(Mul1.outputs[0], GroupOutput.inputs[1])
        NodeGroup.links.new(Mul2.outputs[0], GroupOutput.inputs[2])
        NodeGroup.links.new(Sub.outputs[0], GroupOutput.inputs[0])

    def HSLtoRGB():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='HSLtoRGB', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-1258, 0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='H')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='S')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='L')

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (-880, -278)
        Mul1.operation = 'MULTIPLY'
        Mul1.inputs[0].default_value = 2.0

        # Add a Subtract math node
        Sub1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub1.name = "Subtract.001"
        Sub1.location = (-690, -278)
        Sub1.operation = 'SUBTRACT'
        Sub1.inputs[1].default_value = 1.0

        # Add a Absolute math node
        Abs = NodeGroup.nodes.new(type='ShaderNodeMath')
        Abs.name = "Absolute"
        Abs.location = (-500, -278)
        Abs.operation = 'ABSOLUTE'

        # Add a Subtract math node
        Sub2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub2.name = "Subtract.002"
        Sub2.location = (-310, -278)
        Sub2.operation = 'SUBTRACT'
        Sub2.inputs[0].default_value = 1.0

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (-82, -114)
        Mul2.operation = 'MULTIPLY'

        # Add a Divide math node
        Div1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Div1.name = "Divide.001"
        Div1.location = (108, -114)
        Div1.operation = 'DIVIDE'
        Div1.inputs[1].default_value = 2.0

        # Add a Add math node
        Add = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add.name = "Add"
        Add.location = (302, 51)
        Add.operation = 'ADD'

        # Add a Subtract math node
        Sub3 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub3.name = "Subtract.003"
        Sub3.location = (618, 288)
        Sub3.operation = 'SUBTRACT'

        # Add a Multiply math node
        Mul3 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul3.name = "Multiply.003"
        Mul3.location = (808, 288)
        Mul3.operation = 'MULTIPLY'
        Mul3.inputs[0].default_value = 2.0

        # Add a Divide math node
        Div2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Div2.name = "Divide.002"
        Div2.location = (998, 288)
        Div2.operation = 'DIVIDE'

        # Add a Combine HSV node
        ComHSV = NodeGroup.nodes.new(type='ShaderNodeCombineHSV')
        ComHSV.name = "Combine HSV"
        ComHSV.location = (1258, -8)

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (1490, -56)
        NodeGroup.outputs.new(type='NodeSocketColor', name='RGB')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], ComHSV.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Mul2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Mul1.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[2], Add.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Sub3.inputs[1])
        NodeGroup.links.new(Mul1.outputs[0], Sub1.inputs[0])
        NodeGroup.links.new(Sub1.outputs[0], Abs.inputs[0])
        NodeGroup.links.new(Abs.outputs[0], Sub2.inputs[1])
        NodeGroup.links.new(Sub2.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Mul2.outputs[0], Div1.inputs[0])
        NodeGroup.links.new(Div1.outputs[0], Add.inputs[1])
        NodeGroup.links.new(Add.outputs[0], Sub3.inputs[0])
        NodeGroup.links.new(Add.outputs[0], Div2.inputs[1])
        NodeGroup.links.new(Add.outputs[0], ComHSV.inputs[2])
        NodeGroup.links.new(Sub3.outputs[0], Mul3.inputs[1])
        NodeGroup.links.new(Mul3.outputs[0], Div2.inputs[0])
        NodeGroup.links.new(Div2.outputs[0], ComHSV.inputs[1])
        NodeGroup.links.new(ComHSV.outputs[0], GroupOutput.inputs[0])

    def NdotL():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='NdotL', type='ShaderNodeTree')

        # Add a Geometry input node
        Geom = NodeGroup.nodes.new(type='ShaderNodeNewGeometry')
        Geom.name = "Geometry"
        Geom.location = (-94, 21)

        # Add a Dot Product vector math node
        DotProd = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        DotProd.name = "Dot Product"
        DotProd.location = (94, -21)
        DotProd.operation = 'DOT_PRODUCT'

        # Add node group's Ouput node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (294, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='NdotL')

        # Link nodes together
        NodeGroup.links.new(Geom.outputs[1], DotProd.inputs[0])
        NodeGroup.links.new(Geom.outputs[4], DotProd.inputs[1])
        NodeGroup.links.new(DotProd.outputs[1], GroupOutput.inputs[0])

    def OffsetHue():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='OffsetHue', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-287, 0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='H')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.X')

        # Add a Add math node
        Add = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add.name = "Add"
        Add.location = (-87, -0.6)
        Add.operation = 'ADD'

        # Add a Fraction math node
        Frac = NodeGroup.nodes.new(type='ShaderNodeMath')
        Frac.name = "Fraction"
        Frac.location = (87, -0.6)
        Frac.operation = 'FRACT'
        Frac.use_clamp = True

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (287, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='H')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Add.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Add.inputs[1])
        NodeGroup.links.new(Add.outputs[0], Frac.inputs[0])
        NodeGroup.links.new(Frac.outputs[0], GroupOutput.inputs[0])

    def OffsetSaturation():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='OffsetSaturation', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-369, 0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='S')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.Y')

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (-169, 80)
        Power.operation = 'POWER'

        # Add a Subtract math node
        Sub = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub.name = "Subtract"
        Sub.location = (-169, -82)
        Sub.operation = 'SUBTRACT'
        Sub.inputs[0].default_value = 1.0

        # Add a Multiply math node
        Mul = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul.name = "Multiply"
        Mul.location = (3, 82)
        Mul.operation = 'MULTIPLY'

        # Add a Clamp node
        Clamp = NodeGroup.nodes.new(type='ShaderNodeClamp')
        Clamp.name = "Clamp"
        Clamp.location = (169, 80)
        Clamp.clamp_type = 'RANGE'
        Clamp.inputs[1].default_value = 0.0
        Clamp.inputs[2].default_value = 1.0

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (369, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='S')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Power.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Power.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[1], Sub.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul.inputs[0])
        NodeGroup.links.new(Sub.outputs[0], Mul.inputs[1])
        NodeGroup.links.new(Mul.outputs[0], Clamp.inputs[0])
        NodeGroup.links.new(Clamp.outputs[0], GroupOutput.inputs[0])

    def OffsetSkinSaturation():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='OffsetSkinSaturation', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-369, 0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='S')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.Y')

        # Add a Subtract math node
        Sub = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub.name = "Subtract"
        Sub.location = (-169, -82)
        Sub.operation = 'SUBTRACT'
        Sub.inputs[0].default_value = 0.5

        # Add a Multiply math node
        Add = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add.name = "Add"
        Add.location = (3, 82)
        Add.operation = 'ADD'

        # Add a Clamp node
        Clamp = NodeGroup.nodes.new(type='ShaderNodeClamp')
        Clamp.name = "Clamp"
        Clamp.location = (169, 80)
        Clamp.clamp_type = 'RANGE'
        Clamp.inputs[1].default_value = 0.0
        Clamp.inputs[2].default_value = 1.0

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (369, 0)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='S')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Add.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Sub.inputs[1])
        NodeGroup.links.new(Sub.outputs[0], Add.inputs[1])
        NodeGroup.links.new(Add.outputs[0], Clamp.inputs[0])
        NodeGroup.links.new(Clamp.outputs[0], GroupOutput.inputs[0])

    def Palette():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='Palette', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-429, 0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='H')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='S')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='L')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='AO')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.X')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.Y')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.Z')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.W')

        # Add OffsetHue node group
        if 'OffsetHue' not in bpy.data.node_groups:
            CommonGroups.OffsetHue()
        Hue = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Hue.name = "Offset Hue"
        Hue.location = (-113, 134)
        Hue.node_tree = bpy.data.node_groups['OffsetHue']

        # Add OffsetSaturation node group
        if 'OffsetSaturation' not in bpy.data.node_groups:
            CommonGroups.OffsetSaturation()
        Sat = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Sat.name = "Offset Saturation"
        Sat.location = (-113, -0.5)
        Sat.node_tree = bpy.data.node_groups['OffsetSaturation']

        # Add AdjustLightness node group
        if 'AdjustLightness' not in bpy.data.node_groups:
            CommonGroups.AdjustLightness()
        Lit = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Lit.name = "Adjust Lightness"
        Lit.location = (-113, -134)
        Lit.node_tree = bpy.data.node_groups['AdjustLightness']

        # Add HSLtoRGB node group
        if 'HSLtoRGB' not in bpy.data.node_groups:
            CommonGroups.HSLtoRGB()
        Con = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Con.name = "HSL to RGB"
        Con.location = (114, 110)
        Con.node_tree = bpy.data.node_groups['HSLtoRGB']

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (350, -0.9)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Palette RGB')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Hue.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Sat.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Lit.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[3], Lit.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[4], Hue.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[5], Sat.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[6], Lit.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[7], Lit.inputs[3])
        NodeGroup.links.new(Hue.outputs[0], Con.inputs[0])
        NodeGroup.links.new(Sat.outputs[0], Con.inputs[1])
        NodeGroup.links.new(Lit.outputs[0], Con.inputs[2])
        NodeGroup.links.new(Con.outputs[0], GroupOutput.inputs[0])

    def PaletteLogic():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='PaletteLogic', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-643, 47)
        NodeGroup.inputs.new(type='NodeSocketColor', name='PaletteMask Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1')
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette2')

        # Add a Separate XYZ node
        SepXYZ = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ.name = "Separate XYZ"
        SepXYZ.location = (-449, 47)

        # Add a Less Than math node
        Less1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Less1.name = "Less Than.001"
        Less1.location = (-242, 51)
        Less1.operation = 'LESS_THAN'

        # Add a Multiply vector math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (-60, 216)
        Mul1.operation = 'MULTIPLY'

        # Add a Less Than math node
        Less2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Less2.name = "Less Than.002"
        Less2.location = (-60, 48)
        Less2.operation = 'LESS_THAN'
        Less2.inputs[1].default_value = 1.0

        # Add a Multiply vecror math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (136, 48)
        Mul2.operation = 'MULTIPLY'

        # Add a Add vector math node
        Add = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Add.name = "Add"
        Add.location = (357, 117)
        Add.operation = 'ADD'

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (611, 49)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Chosen Palette')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SepXYZ.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Mul2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Mul1.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[0], Less1.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[1], Less1.inputs[1])
        NodeGroup.links.new(Less1.outputs[0], Mul1.inputs[1])
        NodeGroup.links.new(Less1.outputs[0], Less2.inputs[0])
        NodeGroup.links.new(Mul1.outputs[0], Add.inputs[0])
        NodeGroup.links.new(Less2.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Mul2.outputs[0], Add.inputs[1])
        NodeGroup.links.new(Add.outputs[0], GroupOutput.inputs[0])

    def RotationMap():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='RotationMap', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-400, -120)
        NodeGroup.inputs.new(type='NodeSocketColor', name='RotationMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='RotationMap Alpha')

        # Add a Separate XYZ node
        SepXYZ = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ.name = "Separate XYZ"
        SepXYZ.location = (-220, 0)

        # Add a Subtract math node
        Sub = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub.name = "Subtract"
        Sub.location = (100, 140)
        Sub.operation = 'SUBTRACT'
        Sub.inputs[0].default_value = 1.0

        # Add a Subtract math node
        Sub2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub2.name = "Subtract"
        Sub2.location = (0, -100)
        Sub2.operation = 'SUBTRACT'
        Sub2.inputs[0].default_value = 1.0
        
        # Add a Combine XYZ node
        ComXYZ = NodeGroup.nodes.new(type='ShaderNodeCombineXYZ')
        ComXYZ.name = "Combine XYZ"
        ComXYZ.location = (200, -120)
        ComXYZ.inputs[2].default_value = 1.0

        # Add a Minimum math node
        Min = NodeGroup.nodes.new(type='ShaderNodeMath')
        Min.name = "Minimum"
        Min.location = (300, 140)
        Min.operation = 'MINIMUM'
        Min.inputs[0].default_value = 1.0

        # Add a Normal Map node
        Norm = NodeGroup.nodes.new(type='ShaderNodeNormalMap')
        Norm.name = "Normal Map"
        Norm.location = (400, -100)
        Norm.space = 'TANGENT'
        Norm.inputs[0].default_value = 1.0

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (600, 0)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Emission Strength')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Alpha')
        NodeGroup.outputs.new(type='NodeSocketVector', name='Normal')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SepXYZ.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], ComXYZ.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[0], Sub.inputs[1])
        NodeGroup.links.new(SepXYZ.outputs[1], Sub2.inputs[1])
        NodeGroup.links.new(Sub2.outputs[0], ComXYZ.inputs[1])
        NodeGroup.links.new(SepXYZ.outputs[2], GroupOutput.inputs[0])
        NodeGroup.links.new(Sub.outputs[0], Min.inputs[1])
        NodeGroup.links.new(ComXYZ.outputs[0], Norm.inputs[1])
        NodeGroup.links.new(Min.outputs[0], GroupOutput.inputs[1])
        NodeGroup.links.new(Norm.outputs[0], GroupOutput.inputs[2])

    def SinglePaletteLerp():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='SinglePaletteLerp', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (20, -198)
        NodeGroup.inputs.new(type='NodeSocketColor', name='DiffuseMap Color')
        NodeGroup.inputs.new(type='NodeSocketVector', name='PaletteMask')
        NodeGroup.inputs.new(type='NodeSocketVector', name='Palette1')

        # Add a Separate XYZ node
        SepXYZ = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ.name = "Separate XYZ"
        SepXYZ.location = (202, -198)

        # Add a Add math node
        Add = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add.name = "Add"
        Add.location = (381, -85)
        Add.operation = 'ADD'

        # Add a RGB Mix node
        Mix = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        Mix.name = "Mix RGB"
        Mix.location = (624, 61)
        Mix.blend_type = 'MIX'

        # Add a Gamma node
        Gamma = NodeGroup.nodes.new(type='ShaderNodeGamma')
        Gamma.name = "Gamma"
        Gamma.location = (818, 23)
        Gamma.inputs[1].default_value = 2.1

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (1004, -5)
        NodeGroup.outputs.new(type='NodeSocketColor', name='RGB')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Mix.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[1], SepXYZ.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Mix.inputs[2])
        NodeGroup.links.new(SepXYZ.outputs[0], Add.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[1], Add.inputs[1])
        NodeGroup.links.new(Add.outputs[0], Mix.inputs[0])
        NodeGroup.links.new(Mix.outputs[0], Gamma.inputs[0])
        NodeGroup.links.new(Gamma.outputs[0], GroupOutput.inputs[0])

    def SkinPalette():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='SkinPalette', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-538, 0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='H')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='S')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='L')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.X')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.Y')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.Z')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette.W')

        # Add a Subtract math node
        Sub = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub.name = "Subtract"
        Sub.location = (-330, 36)
        Sub.operation = 'SUBTRACT'
        Sub.inputs[1].default_value = 0.5

        # Add OffsetHue node group
        if 'OffsetHue' not in bpy.data.node_groups:
            CommonGroups.OffsetHue()
        Hue = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Hue.name = "Offset Hue"
        Hue.location = (-113, 134)
        Hue.node_tree = bpy.data.node_groups['OffsetHue']

        # Add OffsetSaturation node group
        if 'OffsetSkinSaturation' not in bpy.data.node_groups:
            CommonGroups.OffsetSaturation()
        Sat = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Sat.name = "Offset Saturation"
        Sat.location = (-113, -0.5)
        Sat.node_tree = bpy.data.node_groups['OffsetSaturation']

        # Add AdjustLightness node group
        if 'AdjustSkinLightness' not in bpy.data.node_groups:
            CommonGroups.AdjustSkinLightness()
        Lit = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Lit.name = "Adjust Skin Lightness"
        Lit.location = (-113, -134)
        Lit.node_tree = bpy.data.node_groups['AdjustSkinLightness']

        # Add HSLtoRGB node group
        if 'HSLtoRGB' not in bpy.data.node_groups:
            CommonGroups.HSLtoRGB()
        Con = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Con.name = "HSL to RGB"
        Con.location = (114, 110)
        Con.node_tree = bpy.data.node_groups['HSLtoRGB']

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (350, -0.9)
        NodeGroup.outputs.new(type='NodeSocketColor', name='Palette RGB')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Hue.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], Sat.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Lit.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[3], Sub.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[4], Sat.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[5], Lit.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[6], Lit.inputs[2])
        NodeGroup.links.new(Sub.outputs[0], Hue.inputs[1])
        NodeGroup.links.new(Hue.outputs[0], Con.inputs[0])
        NodeGroup.links.new(Sat.outputs[0], Con.inputs[1])
        NodeGroup.links.new(Lit.outputs[0], Con.inputs[2])
        NodeGroup.links.new(Con.outputs[0], GroupOutput.inputs[0])

    def Specular():
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='Specular', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-1201, 116)
        NodeGroup.inputs.new(type='NodeSocketColor', name='GlossMap Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='PaletteMask Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='Metallic Specular')
        NodeGroup.inputs.new(type='NodeSocketColor', name='Specular')

        # Add a Separate XYZ node
        SepXYZ1 = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ1.name = "Separate XYZ.001"
        SepXYZ1.location = (-1020, 41)

        # Add a Subtract math node
        Sub = NodeGroup.nodes.new(type='ShaderNodeMath')
        Sub.name = "Subtract"
        Sub.location = (-830, 225)
        Sub.operation = 'SUBTRACT'
        Sub.inputs[1].default_value = 0.5

        # Add a Separate XYZ node
        SepXYZ2 = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ2.name = "Separate XYZ.002"
        SepXYZ2.location = (-830, 41)

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (-644, 226)
        Mul1.operation = 'MULTIPLY'
        Mul1.inputs[1].default_value = 2.0

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (-644, 40)
        Mul2.operation = 'MULTIPLY'
        Mul2.inputs[1].default_value = 2.0

        # Add a Mix RGB node
        Mix1 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        Mix1.name = "Mix RGB.001"
        Mix1.location = (-451, 229)
        Mix1.blend_type = 'MIX'
        Mix1.inputs[1].default_value = (1.0, 1.0, 1.0, 1.0)

        # Add a Mix RGB node
        Mix2 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        Mix2.name = "Mix RGB.002"
        Mix2.location = (-451, 43)
        Mix2.blend_type = 'MIX'
        Mix2.inputs[2].default_value = (1.0, 1.0, 1.0, 1.0)

        # Add a Multiply vector math node
        Mul3 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul3.name = "Multiply.003"
        Mul3.location = (-258, 230)
        Mul3.operation = 'MULTIPLY'

        # Add a Add math node
        Add = NodeGroup.nodes.new(type='ShaderNodeMath')
        Add.name = "Add"
        Add.location = (-258, 45)
        Add.operation = 'ADD'

        # Add a Mix RGB node
        Mix3 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        Mix3.name = "Mix RGB.003"
        Mix3.location = (-71, 230)
        Mix3.blend_type = 'MIX'

        # Add a Multiply vector math node
        Mul4 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul4.name = "Multiply.004"
        Mul4.location = (-71, 47)
        Mul4.operation = 'MULTIPLY'

        # Add a RGB to BW node
        Mono1 = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        Mono1.name = "RGB to BW.001"
        Mono1.location = (121, 137)

        # Add a Mix RGB node
        Mix4 = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        Mix4.name = "Mix RGB.004"
        Mix4.location = (121, 48)
        Mix4.blend_type = 'MIX'

        # Add a RGB to BW node
        Mono2 = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        Mono2.name = "RGB to BW.002"
        Mono2.location = (297, 46)

        # Add a Greater Than math node
        GThan = NodeGroup.nodes.new(type='ShaderNodeMath')
        GThan.name = "Greater Than"
        GThan.location = (474, -43)
        GThan.operation = 'GREATER_THAN'
        GThan.inputs[1].default_value = 0.5

        # Add a Multiply math node
        Mul5 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul5.name = "Multiply.005"
        Mul5.location = (653, 101)
        Mul5.operation = 'MULTIPLY'

        # Add a Less Than math node
        LThan = NodeGroup.nodes.new(type='ShaderNodeMath')
        LThan.name = "Less Than"
        LThan.location = (653, -74)
        LThan.operation = 'LESS_THAN'
        LThan.inputs[1].default_value = 1.0

        # Add a Multiply math node
        Mul6 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul6.name = "Multiply.006"
        Mul6.location = (827, -74)
        Mul6.operation = 'MULTIPLY'

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (1068, -0.9)
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Metallic')
        NodeGroup.outputs.new(type='NodeSocketFloat', name='Specular')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], SepXYZ2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[0], Mix3.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[0], Mix4.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[1], SepXYZ1.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], Mix1.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[3], Mix2.inputs[1])
        NodeGroup.links.new(SepXYZ1.outputs[0], Add.inputs[0])
        NodeGroup.links.new(SepXYZ1.outputs[1], Add.inputs[1])
        NodeGroup.links.new(SepXYZ1.outputs[2], Sub.inputs[0])
        NodeGroup.links.new(SepXYZ1.outputs[2], Mul2.inputs[0])
        NodeGroup.links.new(SepXYZ1.outputs[2], GThan.inputs[0])
        NodeGroup.links.new(Sub.outputs[0], Mul1.inputs[0])
        NodeGroup.links.new(SepXYZ2.outputs[0], Mul3.inputs[1])
        NodeGroup.links.new(SepXYZ2.outputs[0], Mul4.inputs[1])
        NodeGroup.links.new(Mul1.outputs[0], Mix1.inputs[0])
        NodeGroup.links.new(Mul2.outputs[0], Mix2.inputs[0])
        NodeGroup.links.new(Mix1.outputs[0], Mul3.inputs[0])
        NodeGroup.links.new(Mix2.outputs[0], Mul4.inputs[0])
        NodeGroup.links.new(Mul3.outputs[0], Mix3.inputs[2])
        NodeGroup.links.new(Add.outputs[0], Mix3.inputs[0])
        NodeGroup.links.new(Add.outputs[0], Mix4.inputs[0])
        NodeGroup.links.new(Mix3.outputs[0], Mono1.inputs[0])
        NodeGroup.links.new(Mul4.outputs[0], Mix4.inputs[2])
        NodeGroup.links.new(Mono1.outputs[0], Mul5.inputs[0])
        NodeGroup.links.new(Mix4.outputs[0], Mono2.inputs[0])
        NodeGroup.links.new(Mono2.outputs[0], Mul6.inputs[0])
        NodeGroup.links.new(GThan.outputs[0], Mul5.inputs[1])
        NodeGroup.links.new(GThan.outputs[0], LThan.inputs[0])
        NodeGroup.links.new(Mul5.outputs[0], GroupOutput.inputs[0])
        NodeGroup.links.new(LThan.outputs[0], Mul6.inputs[1])
        NodeGroup.links.new(Mul6.outputs[0], GroupOutput.inputs[1])


class CreatureShader():

    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.blend_method = 'CLIP'
        self.material.shadow_method = 'CLIP'
        self.material.alpha_threshold = 0.5
        self.material.use_nodes = True
        self.material.use_fake_user = True
        self.material.node_tree.nodes.remove(self.material.node_tree.nodes['Principled BSDF'])

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-578, 527)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-578, 260)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-578, -8)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-578, -277)

    def Creature(self):
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='Creature Shader', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-672, 193)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d DiffuseMap Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n RotationMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n RotationMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_s GlossMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')

        # Add a RGB to BW node
        Mono = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        Mono.name = "RGB to BW"
        Mono.location = (-412, 129)

        # Add a Separate XYZ node
        SepXYZ = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ.name = "Separate XYZ"
        SepXYZ.location = (-412, 46)

        # Add NdotL node group
        if 'NdotL' not in bpy.data.node_groups:
            CommonGroups.NdotL()
        NdotL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        NdotL.name = "NdotL"
        NdotL.location = (-239, 87)
        NdotL.node_tree = bpy.data.node_groups['NdotL']

        # Add a Multiply Add math node
        MulAdd = NodeGroup.nodes.new(type='ShaderNodeMath')
        MulAdd.name = "Multiply Add"
        MulAdd.location = (-238, -2)
        MulAdd.operation = 'MULTIPLY_ADD'
        MulAdd.inputs[1].default_value = 63.0
        MulAdd.inputs[2].default_value = 1.0

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (-66, -4)
        Power.operation = 'POWER'

        # Add a Gamma node
        Gamma = NodeGroup.nodes.new(type='ShaderNodeGamma')
        Gamma.name = "Gamma"
        Gamma.location = (105, 272)
        Gamma.inputs[1].default_value = 2.1

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (107, 164)
        Mul1.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = 'Multiply.002'
        Mul2.location = (103, -2)
        Mul2.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul3 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul3.name = 'Multiply.003'
        Mul3.location = (300, -60)
        Mul3.operation = 'MULTIPLY'

        # Add RotationMap node group
        if 'RotationMap' not in bpy.data.node_groups:
            CommonGroups.RotationMap()
        RotMap = NodeGroup.nodes.new(type='ShaderNodeGroup')
        RotMap.name = "RotationMap"
        RotMap.location = (103, -200)
        RotMap.node_tree = bpy.data.node_groups['RotationMap']

        # Add Principled BSDF shader node
        Principled = NodeGroup.nodes.new(type='ShaderNodeBsdfPrincipled')
        Principled.name = "Principled BSDF"
        Principled.location = (561, 264)
        Principled.inputs[7].default_value = 0.673

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (903, 178)
        NodeGroup.outputs.new(type='NodeSocketShader', name='BSDF')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Gamma.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], RotMap.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], RotMap.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[3], Mono.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[4], MulAdd.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[5], SepXYZ.inputs[0])
        NodeGroup.links.new(Mono.outputs[0], Mul2.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[2], Mul1.inputs[0])
        NodeGroup.links.new(NdotL.outputs[0], Power.inputs[0])
        NodeGroup.links.new(MulAdd.outputs[0], Power.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul1.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Principled.inputs[5])
        NodeGroup.links.new(Gamma.outputs[0], Principled.inputs[0])
        NodeGroup.links.new(Gamma.outputs[0], Mul3.inputs[0])
        NodeGroup.links.new(Mul1.outputs[0], Principled.inputs[4])
        NodeGroup.links.new(Mul2.outputs[0], Principled.inputs[6])
        NodeGroup.links.new(Mul3.outputs[0], Principled.inputs[17])
        NodeGroup.links.new(RotMap.outputs[0], Mul3.inputs[1])
        NodeGroup.links.new(RotMap.outputs[1], Principled.inputs[18])
        NodeGroup.links.new(RotMap.outputs[2], Principled.inputs[19])
        NodeGroup.links.new(Principled.outputs[0], GroupOutput.inputs[0])

        # Link the node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "Creature Shader"
        link.width = 178
        link.location = (-87, 107)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Creature Shader node group
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['Creature Shader'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['Creature Shader'].inputs[1])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['Creature Shader'].inputs[2])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['Creature Shader'].inputs[3])
        links.new(nodes['_s GlossMap'].outputs[1], nodes['Creature Shader'].inputs[4])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['Creature Shader'].inputs[5])

        # Link the Creature Shader node group to the Material Output node
        links.new(nodes['Creature Shader'].outputs[0], nodes['Material Output'].inputs[0])

    def build(self):
        self.TextureNodes()
        self.Creature()
        self.LinkNodes()


class EyeShader():

    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.blend_method = 'CLIP'
        self.material.shadow_method = 'CLIP'
        self.material.alpha_threshold = 0.5
        self.material.use_nodes = True
        self.material.use_fake_user = True
        self.material.node_tree.nodes.remove(self.material.node_tree.nodes['Principled BSDF'])

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-578, 658)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-578, 390)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-578, 123)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-578, -144)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-578, -409)

    def Eye(self):
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='Eye Shader', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-674, 593)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d DiffuseMap')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n RotationMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n RotationMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_s GlossMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.X')
        NodeGroup.inputs[5].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.Y')
        NodeGroup.inputs[6].default_value = 0.5
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.Z')
        NodeGroup.inputs[7].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.W')
        NodeGroup.inputs[8].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1 Specular')
        NodeGroup.inputs[9].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1 Metallic Specular')
        NodeGroup.inputs[10].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        NodeGroup.inputs[11].default_value = (0.0, 0.0, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        NodeGroup.inputs[12].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
        NodeGroup.inputs[13].default_value = (0.0, 0.0, 0.0, 1.0)

        # Add ExpandHSL node group
        if 'ExpandHSL' not in bpy.data.node_groups:
            CommonGroups.ExpandHSL()
        ExpHSL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        ExpHSL.name = "Expand HSL"
        ExpHSL.location = (-412, 558)
        ExpHSL.node_tree = bpy.data.node_groups['ExpandHSL']

        # Add Palette node group
        if 'Palette' not in bpy.data.node_groups:
            CommonGroups.Palette()
        Palette = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Palette.name = "Palette1"
        Palette.location = (-163, 562)
        Palette.node_tree = bpy.data.node_groups['Palette']

        # Add Lerp node group
        if 'SinglePaletteLerp' not in bpy.data.node_groups:
            CommonGroups.SinglePaletteLerp()
        Lerp = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Lerp.name = "Lerp"
        Lerp.location = (37, 564)
        Lerp.node_tree = bpy.data.node_groups['SinglePaletteLerp']

        # Add Specular node group
        if 'Specular' not in bpy.data.node_groups:
            CommonGroups.Specular()
        Spec = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Spec.name = "Specular"
        Spec.location = (-414, 163)
        Spec.node_tree = bpy.data.node_groups['Specular']

        # Add NdotL node group
        if 'NdotL' not in bpy.data.node_groups:
            CommonGroups.NdotL()
        NdotL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        NdotL.name = "NdotL"
        NdotL.location = (-212, 166)
        NdotL.node_tree = bpy.data.node_groups['NdotL']

        # Add a Multiply Add math node
        MulAdd = NodeGroup.nodes.new(type='ShaderNodeMath')
        MulAdd.name = "Multiply Add"
        MulAdd.location = (-212, 77)
        MulAdd.operation = 'MULTIPLY_ADD'
        MulAdd.inputs[1].default_value = 63.0
        MulAdd.inputs[2].default_value = 1.0

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (-22, 101)
        Power.operation = 'POWER'

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = 'Multiply.001'
        Mul1.location = (186, 164)
        Mul1.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (186, -2)
        Mul2.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul3 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul3.name = 'Multiply.003'
        Mul3.location = (375, -95)
        Mul3.operation = 'MULTIPLY'

        # Add RotationMap node group
        if 'RotationMap' not in bpy.data.node_groups:
            CommonGroups.RotationMap()
        RotMap = NodeGroup.nodes.new(type='ShaderNodeGroup')
        RotMap.name = "RotationMap"
        RotMap.location = (182, -219)
        RotMap.node_tree = bpy.data.node_groups['RotationMap']

        # Add Principled BSDF shader node
        Principled = NodeGroup.nodes.new(type='ShaderNodeBsdfPrincipled')
        Principled.name = "Principled BSDF"
        Principled.location = (582, 181)
        Principled.inputs[7].default_value = 0.673

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (894, 119)
        NodeGroup.outputs.new(type='NodeSocketShader', name='BSDF')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Lerp.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], RotMap.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], RotMap.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[3], Spec.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[4], MulAdd.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[5], Palette.inputs[4])
        NodeGroup.links.new(GroupInput.outputs[6], Palette.inputs[5])
        NodeGroup.links.new(GroupInput.outputs[7], Palette.inputs[6])
        NodeGroup.links.new(GroupInput.outputs[8], Palette.inputs[7])
        NodeGroup.links.new(GroupInput.outputs[9], Spec.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[10], Spec.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[11], ExpHSL.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[12], ExpHSL.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[13], Lerp.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[13], Spec.inputs[1])
        NodeGroup.links.new(ExpHSL.outputs[0], Palette.inputs[0])
        NodeGroup.links.new(ExpHSL.outputs[1], Palette.inputs[1])
        NodeGroup.links.new(ExpHSL.outputs[2], Palette.inputs[2])
        NodeGroup.links.new(ExpHSL.outputs[3], Palette.inputs[3])
        NodeGroup.links.new(Palette.outputs[0], Lerp.inputs[2])
        NodeGroup.links.new(Lerp.outputs[0], Principled.inputs[0])
        NodeGroup.links.new(Lerp.outputs[0], Mul3.inputs[0])
        NodeGroup.links.new(Spec.outputs[0], Mul1.inputs[0])
        NodeGroup.links.new(Spec.outputs[1], Mul2.inputs[0])
        NodeGroup.links.new(NdotL.outputs[0], Power.inputs[0])
        NodeGroup.links.new(MulAdd.outputs[0], Power.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul1.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Principled.inputs[5])
        NodeGroup.links.new(Mul1.outputs[0], Principled.inputs[4])
        NodeGroup.links.new(Mul2.outputs[0], Principled.inputs[6])
        NodeGroup.links.new(Mul3.outputs[0], Principled.inputs[17])
        NodeGroup.links.new(RotMap.outputs[0], Mul3.inputs[1])
        NodeGroup.links.new(RotMap.outputs[1], Principled.inputs[18])
        NodeGroup.links.new(RotMap.outputs[2], Principled.inputs[19])
        NodeGroup.links.new(Principled.outputs[0], GroupOutput.inputs[0])

        # Link the node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "Eye Shader"
        link.width = 326
        link.location = (-162, 192)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Eye Shader node group
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['Eye Shader'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['Eye Shader'].inputs[1])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['Eye Shader'].inputs[2])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['Eye Shader'].inputs[3])
        links.new(nodes['_s GlossMap'].outputs[1], nodes['Eye Shader'].inputs[4])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['Eye Shader'].inputs[11])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['Eye Shader'].inputs[12])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['Eye Shader'].inputs[13])

        # Link the Eye Shader node group to the Material Output node
        links.new(nodes['Eye Shader'].outputs[0], nodes['Material Output'].inputs[0])

    def build(self):
        self.TextureNodes()
        self.Eye()
        self.LinkNodes()


class GarmentShader():

    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.blend_method = 'CLIP'
        self.material.shadow_method = 'CLIP'
        self.material.alpha_threshold = 0.5
        self.material.use_nodes = True
        self.material.use_fake_user = True
        self.material.node_tree.nodes.remove(self.material.node_tree.nodes['Principled BSDF'])

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-578, 658)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-578, 390)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-578, 123)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-578, -144)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-578, -409)

    def Garment(self):
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='Garment Shader', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-944, 798)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d DiffuseMap')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n RotationMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n RotationMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_s GlossMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.X')
        NodeGroup.inputs[5].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.Y')
        NodeGroup.inputs[6].default_value = 0.5
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.Z')
        NodeGroup.inputs[7].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.W')
        NodeGroup.inputs[8].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1 Specular')
        NodeGroup.inputs[9].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1 Metallic Specular')
        NodeGroup.inputs[10].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette2.X')
        NodeGroup.inputs[11].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette2.Y')
        NodeGroup.inputs[12].default_value = 0.5
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette2.Z')
        NodeGroup.inputs[13].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette2.W')
        NodeGroup.inputs[14].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette2 Specular')
        NodeGroup.inputs[15].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette2 Metallic Specular')
        NodeGroup.inputs[16].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        NodeGroup.inputs[17].default_value = (0.0, 0.0, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        NodeGroup.inputs[18].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
        NodeGroup.inputs[19].default_value = (0.0, 0.0, 0.0, 1.0)

        # Add ExpandHSL node group
        if 'ExpandHSL' not in bpy.data.node_groups:
            CommonGroups.ExpandHSL()
        ExpHSL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        ExpHSL.name = "Expand HSL"
        ExpHSL.location = (-521, 645)
        ExpHSL.node_tree = bpy.data.node_groups['ExpandHSL']

        # Add Palette node group
        if 'Palette' not in bpy.data.node_groups:
            CommonGroups.Palette()
        P1 = NodeGroup.nodes.new(type='ShaderNodeGroup')
        P1.name = "Palette1"
        P1.location = (-249, 555)
        P1.node_tree = bpy.data.node_groups['Palette']

        # Add Palette node group
        P2 = NodeGroup.nodes.new(type='ShaderNodeGroup')
        P2.name = "Palette2"
        P2.location = (-249, 835)
        P2.node_tree = bpy.data.node_groups['Palette']

        # Add Lerp node group
        if 'DoublePaletteLerp' not in bpy.data.node_groups:
            CommonGroups.DoublePaletteLerp()
        Lerp = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Lerp.name = "Lerp"
        Lerp.location = (-12, 654)
        Lerp.node_tree = bpy.data.node_groups['DoublePaletteLerp']

        # Add PaletteLogic node group
        if 'PaletteLogic' not in bpy.data.node_groups:
            CommonGroups.PaletteLogic()
        Logic1 = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Logic1.name = "Palette Logic.001"
        Logic1.location = (-598, 13)
        Logic1.node_tree = bpy.data.node_groups['PaletteLogic']

        # Add PlaetteLogic node group
        Logic2 = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Logic2.name = "Palette Logic.002"
        Logic2.location = (-598, 173)
        Logic2.node_tree = bpy.data.node_groups['PaletteLogic']

        # Add Specular node group
        if 'Specular' not in bpy.data.node_groups:
            CommonGroups.Specular()
        Spec = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Spec.name = "Specular"
        Spec.location = (-378, 171)
        Spec.node_tree = bpy.data.node_groups['Specular']

        # Add NdotL node group
        if 'NdotL' not in bpy.data.node_groups:
            CommonGroups.NdotL()
        NdotL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        NdotL.name = "NdotL"
        NdotL.location = (-181, 181)
        NdotL.node_tree = bpy.data.node_groups['NdotL']

        # Add a Multiply Add math node
        MulAdd = NodeGroup.nodes.new(type='ShaderNodeMath')
        MulAdd.name = "Multiply Add"
        MulAdd.location = (-181, 91)
        MulAdd.operation = 'MULTIPLY_ADD'
        MulAdd.inputs[1].default_value = 63.0
        MulAdd.inputs[2].default_value = 1.0

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (18, 115)
        Power.operation = 'POWER'

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = 'Multiply.001'
        Mul1.location = (217, 179)
        Mul1.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (217, 12)
        Mul2.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul3 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul3.name = 'Multiply.003'
        Mul3.location = (410, -65)
        Mul3.operation = 'MULTIPLY'

        # Add RotationMap node group
        if 'RotationMap' not in bpy.data.node_groups:
            CommonGroups.RotationMap()
        RotMap = NodeGroup.nodes.new(type='ShaderNodeGroup')
        RotMap.name = "RotationMap"
        RotMap.location = (234, -243)
        RotMap.node_tree = bpy.data.node_groups['RotationMap']

        # Add Principled BSDF shader node
        Principled = NodeGroup.nodes.new(type='ShaderNodeBsdfPrincipled')
        Principled.name = "Principled BSDF"
        Principled.location = (692, 289)
        Principled.inputs[7].default_value = 0.673

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (1030, 260)
        NodeGroup.outputs.new(type='NodeSocketShader', name='BSDF')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Lerp.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], RotMap.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], RotMap.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[3], Spec.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[4], MulAdd.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[5], P1.inputs[4])
        NodeGroup.links.new(GroupInput.outputs[6], P1.inputs[5])
        NodeGroup.links.new(GroupInput.outputs[7], P1.inputs[6])
        NodeGroup.links.new(GroupInput.outputs[8], P1.inputs[7])
        NodeGroup.links.new(GroupInput.outputs[9], Logic1.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[10], Logic2.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[11], P2.inputs[4])
        NodeGroup.links.new(GroupInput.outputs[12], P2.inputs[5])
        NodeGroup.links.new(GroupInput.outputs[13], P2.inputs[6])
        NodeGroup.links.new(GroupInput.outputs[14], P2.inputs[7])
        NodeGroup.links.new(GroupInput.outputs[15], Logic1.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[16], Logic2.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[17], ExpHSL.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[18], ExpHSL.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[19], Lerp.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[19], Logic1.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[19], Logic2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[19], Spec.inputs[1])
        NodeGroup.links.new(ExpHSL.outputs[0], P1.inputs[0])
        NodeGroup.links.new(ExpHSL.outputs[0], P2.inputs[0])
        NodeGroup.links.new(ExpHSL.outputs[1], P1.inputs[1])
        NodeGroup.links.new(ExpHSL.outputs[1], P2.inputs[1])
        NodeGroup.links.new(ExpHSL.outputs[2], P1.inputs[2])
        NodeGroup.links.new(ExpHSL.outputs[2], P2.inputs[2])
        NodeGroup.links.new(ExpHSL.outputs[3], P1.inputs[3])
        NodeGroup.links.new(ExpHSL.outputs[3], P2.inputs[3])
        NodeGroup.links.new(P1.outputs[0], Lerp.inputs[3])
        NodeGroup.links.new(P2.outputs[0], Lerp.inputs[2])
        NodeGroup.links.new(Lerp.outputs[0], Principled.inputs[0])
        NodeGroup.links.new(Lerp.outputs[0], Mul3.inputs[0])
        NodeGroup.links.new(Logic1.outputs[0], Spec.inputs[3])
        NodeGroup.links.new(Logic2.outputs[0], Spec.inputs[2])
        NodeGroup.links.new(Spec.outputs[0], Mul1.inputs[0])
        NodeGroup.links.new(Spec.outputs[1], Mul2.inputs[0])
        NodeGroup.links.new(NdotL.outputs[0], Power.inputs[0])
        NodeGroup.links.new(MulAdd.outputs[0], Power.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul1.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Principled.inputs[5])
        NodeGroup.links.new(Mul1.outputs[0], Principled.inputs[4])
        NodeGroup.links.new(Mul2.outputs[0], Principled.inputs[6])
        NodeGroup.links.new(Mul3.outputs[0], Principled.inputs[17])
        NodeGroup.links.new(RotMap.outputs[0], Mul3.inputs[1])
        NodeGroup.links.new(RotMap.outputs[1], Principled.inputs[18])
        NodeGroup.links.new(RotMap.outputs[2], Principled.inputs[19])
        NodeGroup.links.new(Principled.outputs[0], GroupOutput.inputs[0])

        # Link the node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "Garment Shader"
        link.width = 326
        link.location = (-162, 255)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to Garment Shader node group
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['Garment Shader'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['Garment Shader'].inputs[1])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['Garment Shader'].inputs[2])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['Garment Shader'].inputs[3])
        links.new(nodes['_s GlossMap'].outputs[1], nodes['Garment Shader'].inputs[4])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['Garment Shader'].inputs[17])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['Garment Shader'].inputs[18])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['Garment Shader'].inputs[19])

        # Link the Garment Shader node group to the Material Output node
        links.new(nodes['Garment Shader'].outputs[0], nodes['Material Output'].inputs[0])

    def build(self):
        self.TextureNodes()
        self.Garment()
        self.LinkNodes()


class HairCShader():

    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.blend_method = 'CLIP'
        self.material.shadow_method = 'CLIP'
        self.material.alpha_threshold = 0.5
        self.material.use_nodes = True
        self.material.use_fake_user = True
        self.material.node_tree.nodes.remove(self.material.node_tree.nodes['Principled BSDF'])

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-578, 658)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-578, 390)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-578, 123)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-578, -144)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-578, -409)

    def Hair(self):
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='HairC Shader', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-674, 593)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d DiffuseMap')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n RotationMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n RotationMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_s GlossMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.X')
        NodeGroup.inputs[5].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.Y')
        NodeGroup.inputs[6].default_value = 0.5
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.Z')
        NodeGroup.inputs[7].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.W')
        NodeGroup.inputs[8].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1 Specular')
        NodeGroup.inputs[9].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1 Metallic Specular')
        NodeGroup.inputs[10].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        NodeGroup.inputs[11].default_value = (0.0, 0.0, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        NodeGroup.inputs[12].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
        NodeGroup.inputs[13].default_value = (0.0, 0.0, 0.0, 1.0)

        # Add ExpandHSL node group
        if 'ExpandHSL' not in bpy.data.node_groups:
            CommonGroups.ExpandHSL()
        ExpHSL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        ExpHSL.name = "Expand HSL"
        ExpHSL.location = (-412, 558)
        ExpHSL.node_tree = bpy.data.node_groups['ExpandHSL']

        # Add Palette node group
        if 'Palette' not in bpy.data.node_groups:
            CommonGroups.Palette()
        Palette = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Palette.name = "Palette1"
        Palette.location = (-163, 562)
        Palette.node_tree = bpy.data.node_groups['Palette']

        # Add Lerp node group
        if 'SinglePaletteLerp' not in bpy.data.node_groups:
            CommonGroups.SinglePaletteLerp()
        Lerp = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Lerp.name = "Lerp"
        Lerp.location = (37, 564)
        Lerp.node_tree = bpy.data.node_groups['SinglePaletteLerp']

        # Add Specular node group
        if 'Specular' not in bpy.data.node_groups:
            CommonGroups.Specular()
        Spec = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Spec.name = "Specular"
        Spec.location = (-414, 163)
        Spec.node_tree = bpy.data.node_groups['Specular']

        # Add NdotL node group
        if 'NdotL' not in bpy.data.node_groups:
            CommonGroups.NdotL()
        NdotL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        NdotL.name = "NdotL"
        NdotL.location = (-212, 166)
        NdotL.node_tree = bpy.data.node_groups['NdotL']

        # Add a Multiply Add math node
        MulAdd = NodeGroup.nodes.new(type='ShaderNodeMath')
        MulAdd.name = "Multiply Add"
        MulAdd.location = (-212, 77)
        MulAdd.operation = 'MULTIPLY_ADD'
        MulAdd.inputs[1].default_value = 63.0
        MulAdd.inputs[2].default_value = 1.0

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (-22, 101)
        Power.operation = 'POWER'

        # Add a Multiply math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul1.name = 'Multiply.001'
        Mul1.location = (186, 164)
        Mul1.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (186, -2)
        Mul2.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul3 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul3.name = 'Multiply.003'
        Mul3.location = (390, -90)
        Mul3.operation = 'MULTIPLY'


        # Add RotationMap node group
        if 'RotationMap' not in bpy.data.node_groups:
            CommonGroups.RotationMap()
        RotMap = NodeGroup.nodes.new(type='ShaderNodeGroup')
        RotMap.name = "RotationMap"
        RotMap.location = (182, -219)
        RotMap.node_tree = bpy.data.node_groups['RotationMap']

        # Add Principled BSDF shader node
        Principled = NodeGroup.nodes.new(type='ShaderNodeBsdfPrincipled')
        Principled.name = "Principled BSDF"
        Principled.location = (582, 181)
        Principled.inputs[7].default_value = 0.673

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (894, 119)
        NodeGroup.outputs.new(type='NodeSocketShader', name='BSDF')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Lerp.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], RotMap.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], RotMap.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[3], Spec.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[4], MulAdd.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[5], Palette.inputs[4])
        NodeGroup.links.new(GroupInput.outputs[6], Palette.inputs[5])
        NodeGroup.links.new(GroupInput.outputs[7], Palette.inputs[6])
        NodeGroup.links.new(GroupInput.outputs[8], Palette.inputs[7])
        NodeGroup.links.new(GroupInput.outputs[9], Spec.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[10], Spec.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[11], ExpHSL.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[12], ExpHSL.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[13], Lerp.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[13], Spec.inputs[1])
        NodeGroup.links.new(ExpHSL.outputs[0], Palette.inputs[0])
        NodeGroup.links.new(ExpHSL.outputs[1], Palette.inputs[1])
        NodeGroup.links.new(ExpHSL.outputs[2], Palette.inputs[2])
        NodeGroup.links.new(ExpHSL.outputs[3], Palette.inputs[3])
        NodeGroup.links.new(Palette.outputs[0], Lerp.inputs[2])
        NodeGroup.links.new(Lerp.outputs[0], Principled.inputs[0])
        NodeGroup.links.new(Lerp.outputs[0], Mul3.inputs[0])
        NodeGroup.links.new(Spec.outputs[0], Mul1.inputs[0])
        NodeGroup.links.new(Spec.outputs[1], Mul2.inputs[0])
        NodeGroup.links.new(NdotL.outputs[0], Power.inputs[0])
        NodeGroup.links.new(MulAdd.outputs[0], Power.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul1.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul2.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Principled.inputs[5])
        NodeGroup.links.new(Mul1.outputs[0], Principled.inputs[4])
        NodeGroup.links.new(Mul2.outputs[0], Principled.inputs[6])
        NodeGroup.links.new(Mul3.outputs[0], Principled.inputs[17])
        NodeGroup.links.new(RotMap.outputs[0], Mul3.inputs[1])
        NodeGroup.links.new(RotMap.outputs[0], Mul3.inputs[1])
        NodeGroup.links.new(RotMap.outputs[1], Principled.inputs[18])
        NodeGroup.links.new(RotMap.outputs[2], Principled.inputs[19])
        NodeGroup.links.new(Principled.outputs[0], GroupOutput.inputs[0])

        # Link the node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "HairC Shader"
        link.width = 326
        link.location = (-162, 192)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to HairC Shader node group
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['HairC Shader'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['HairC Shader'].inputs[1])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['HairC Shader'].inputs[2])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['HairC Shader'].inputs[3])
        links.new(nodes['_s GlossMap'].outputs[1], nodes['HairC Shader'].inputs[4])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['HairC Shader'].inputs[11])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['HairC Shader'].inputs[12])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['HairC Shader'].inputs[13])

        # Link the HairC Shader node group to the Material Output node
        links.new(nodes['HairC Shader'].outputs[0], nodes['Material Output'].inputs[0])

    def build(self):
        self.TextureNodes()
        self.Hair()
        self.LinkNodes()


class SkinBShader():

    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.blend_method = 'CLIP'
        self.material.shadow_method = 'CLIP'
        self.material.alpha_threshold = 0.5
        self.material.use_nodes = True
        self.material.use_fake_user = True
        self.material.node_tree.nodes.remove(self.material.node_tree.nodes['Principled BSDF'])

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-578, 658)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-578, 390)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-578, 123)

        # Palette
        _h = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _h.name = _h.label = "_h PaletteMap"
        _h.location = (-578, -144)

        # PaletteMask
        _m = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _m.name = _m.label = "_m PaletteMaskMap"
        _m.location = (-578, -409)

        # Complexion
        _c = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _c.name = _c.label = "ComplexionMap"
        _c.location = (-858, 123)

        # Facepaint
        _f = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _f.name = _f.label = "FacepaintMap"
        _f.location = (-858, -144)

    def SkinB(self):
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name='SkinB Shader', type='ShaderNodeTree')

        # Add node group's Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-1209, 594)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_d DiffuseMap')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_n RotationMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_n RotationMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_s GlossMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.X')
        NodeGroup.inputs[5].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.Y')
        NodeGroup.inputs[6].default_value = 0.5
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.Z')
        NodeGroup.inputs[7].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='Palette1.W')
        NodeGroup.inputs[8].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1 Specular')
        NodeGroup.inputs[9].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='Palette1 Metallic Specular')
        NodeGroup.inputs[10].default_value = (0.0, 0.5, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        NodeGroup.inputs[11].default_value = (0.0, 0.0, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        NodeGroup.inputs[12].default_value = 1.0
        NodeGroup.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
        NodeGroup.inputs[13].default_value = (0.0, 0.0, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='ComplexionMap Color')
        NodeGroup.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketColor', name='FacepaintMap Color')
        NodeGroup.inputs[15].default_value = (0.0, 0.0, 0.0, 1.0)
        NodeGroup.inputs.new(type='NodeSocketFloat', name='FacepaintMap Alpha')
        NodeGroup.inputs[16].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='FleshBrightness')
        NodeGroup.inputs[17].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='FlushTone.X')
        NodeGroup.inputs[18].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='FlushTone.Y')
        NodeGroup.inputs[19].default_value = 0.0
        NodeGroup.inputs.new(type='NodeSocketFloat', name='FlushTone.Z')
        NodeGroup.inputs[20].default_value = 0.0

        # Add a Separate XYZ node
        SepXYZ = NodeGroup.nodes.new(type='ShaderNodeSeparateXYZ')
        SepXYZ.name = "Separate XYZ"
        SepXYZ.location = (-784, 441)

        # Add Palette node group
        if 'SkinPalette' not in bpy.data.node_groups:
            CommonGroups.SkinPalette()
        Palette = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Palette.name = "Palette1"
        Palette.location = (-608, 441)
        Palette.node_tree = bpy.data.node_groups['SkinPalette']

        # Add a Multiply vector math node
        Mul1 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul1.name = "Multiply.001"
        Mul1.location = (-438, 336)
        Mul1.operation = 'MULTIPLY'

        # Add Lerp node group
        if 'SinglePaletteLerp' not in bpy.data.node_groups:
            CommonGroups.SinglePaletteLerp()
        Lerp = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Lerp.name = "Lerp"
        Lerp.location = (-273, 441)
        Lerp.node_tree = bpy.data.node_groups['SinglePaletteLerp']

        # Add a Multiply vector math node
        Mul2 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul2.name = "Multiply.002"
        Mul2.location = (-108, 441)
        Mul2.operation = 'MULTIPLY'

        # Add a Combine XYZ node
        ComXYZ = NodeGroup.nodes.new(type='ShaderNodeCombineXYZ')
        ComXYZ.name = "Combine XYZ"
        ComXYZ.location = (-111, 295)

        # Add a Mix RGB node
        Mix = NodeGroup.nodes.new(type='ShaderNodeMixRGB')
        Mix.name = "Mix RGB"
        Mix.location = (65, 441)
        Mix.blend_type = 'MIX'

        # Add a Multiply vector math node
        Mul3 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul3.name = "Multiply.003"
        Mul3.location = (244, 441)
        Mul3.operation = 'MULTIPLY'

        # Add a Multiply vector math node
        Mul4 = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Mul4.name = "Multiply.004"
        Mul4.location = (420, 441)
        Mul4.operation = 'MULTIPLY'

        # Add a Add vector math node
        Add = NodeGroup.nodes.new(type='ShaderNodeVectorMath')
        Add.name = "Add"
        Add.location = (592, 441)
        Add.operation = 'ADD'

        # Add Specular node group
        if 'Specular' not in bpy.data.node_groups:
            CommonGroups.Specular()
        Spec = NodeGroup.nodes.new(type='ShaderNodeGroup')
        Spec.name = "Specular"
        Spec.location = (-7, 30)
        Spec.node_tree = bpy.data.node_groups['Specular']

        # Add NdotL node group
        if 'NdotL' not in bpy.data.node_groups:
            CommonGroups.NdotL()
        NdotL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        NdotL.name = "NdotL"
        NdotL.location = (196, 32)
        NdotL.node_tree = bpy.data.node_groups['NdotL']

        # Add a Multiply Add math node
        MulAdd = NodeGroup.nodes.new(type='ShaderNodeMath')
        MulAdd.name = "Multiply Add"
        MulAdd.location = (196, -57)
        MulAdd.operation = 'MULTIPLY_ADD'
        MulAdd.inputs[1].default_value = 63.0
        MulAdd.inputs[2].default_value = 1.0

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (393, -26)
        Power.operation = 'POWER'

        # Add a Multiply math node
        Mul5 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul5.name = 'Multiply.005'
        Mul5.location = (591, 30)
        Mul5.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul6 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul6.name = "Multiply.006"
        Mul6.location = (591, -136)
        Mul6.operation = 'MULTIPLY'

        # Add a Multiply math node
        Mul7 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Mul7.name = 'Multiply.007'
        Mul7.location = (850, -200)
        Mul7.operation = 'MULTIPLY'

        # Add RotationMap node group
        if 'RotationMap' not in bpy.data.node_groups:
            CommonGroups.RotationMap()
        RotMap = NodeGroup.nodes.new(type='ShaderNodeGroup')
        RotMap.name = "RotationMap"
        RotMap.location = (590, -377)
        RotMap.node_tree = bpy.data.node_groups['RotationMap']

        # Add Principled BSDF shader node
        Principled = NodeGroup.nodes.new(type='ShaderNodeBsdfPrincipled')
        Principled.name = "Principled BSDF"
        Principled.location = (1030, 139)
        Principled.inputs[7].default_value = 0.673

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (1368, 110)
        NodeGroup.outputs.new(type='NodeSocketShader', name='BSDF')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Lerp.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], RotMap.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], RotMap.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[3], Spec.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[4], MulAdd.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[5], Palette.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[6], Palette.inputs[4])
        NodeGroup.links.new(GroupInput.outputs[7], Palette.inputs[5])
        NodeGroup.links.new(GroupInput.outputs[8], Palette.inputs[6])
        NodeGroup.links.new(GroupInput.outputs[9], Spec.inputs[3])
        NodeGroup.links.new(GroupInput.outputs[10], Spec.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[11], SepXYZ.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[12], Palette.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[13], Lerp.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[13], Spec.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[14], Mul2.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[15], Mix.inputs[2])
        NodeGroup.links.new(GroupInput.outputs[16], Mix.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[17], Mul3.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[18], ComXYZ.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[19], ComXYZ.inputs[1])
        NodeGroup.links.new(GroupInput.outputs[20], ComXYZ.inputs[2])
        NodeGroup.links.new(SepXYZ.outputs[0], Mul1.inputs[1])
        NodeGroup.links.new(SepXYZ.outputs[1], Palette.inputs[0])
        NodeGroup.links.new(SepXYZ.outputs[2], Palette.inputs[1])
        NodeGroup.links.new(Palette.outputs[0], Mul1.inputs[0])
        NodeGroup.links.new(Mul1.outputs[0], Lerp.inputs[2])
        NodeGroup.links.new(Lerp.outputs[0], Mul2.inputs[0])
        NodeGroup.links.new(Lerp.outputs[0], Mul4.inputs[1])
        NodeGroup.links.new(Mul2.outputs[0], Mix.inputs[1])
        NodeGroup.links.new(ComXYZ.outputs[0], Mul3.inputs[0])
        NodeGroup.links.new(Mix.outputs[0], Add.inputs[0])
        NodeGroup.links.new(Mul3.outputs[0], Mul4.inputs[0])
        NodeGroup.links.new(Mul4.outputs[0], Add.inputs[1])
        NodeGroup.links.new(Add.outputs[0], Principled.inputs[0])
        NodeGroup.links.new(Add.outputs[0], Mul7.inputs[0])
        NodeGroup.links.new(Spec.outputs[0], Mul5.inputs[0])
        NodeGroup.links.new(Spec.outputs[1], Mul6.inputs[0])
        NodeGroup.links.new(NdotL.outputs[0], Power.inputs[0])
        NodeGroup.links.new(MulAdd.outputs[0], Power.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul5.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Mul6.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Principled.inputs[5])
        NodeGroup.links.new(Mul5.outputs[0], Principled.inputs[4])
        NodeGroup.links.new(Mul6.outputs[0], Principled.inputs[6])
        NodeGroup.links.new(Mul7.outputs[0], Principled.inputs[17])
        NodeGroup.links.new(RotMap.outputs[0], Mul7.inputs[1])
        NodeGroup.links.new(RotMap.outputs[1], Principled.inputs[18])
        NodeGroup.links.new(RotMap.outputs[2], Principled.inputs[19])
        NodeGroup.links.new(Principled.outputs[0], GroupOutput.inputs[0])

        # Link the node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "SkinB Shader"
        link.width = 326
        link.location = (-162, 192)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to SkinB Shader node group
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['SkinB Shader'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['SkinB Shader'].inputs[1])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['SkinB Shader'].inputs[2])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['SkinB Shader'].inputs[3])
        links.new(nodes['_s GlossMap'].outputs[1], nodes['SkinB Shader'].inputs[4])
        links.new(nodes['_h PaletteMap'].outputs[0], nodes['SkinB Shader'].inputs[11])
        links.new(nodes['_h PaletteMap'].outputs[1], nodes['SkinB Shader'].inputs[12])
        links.new(nodes['_m PaletteMaskMap'].outputs[0], nodes['SkinB Shader'].inputs[13])
        links.new(nodes['ComplexionMap'].outputs[0], nodes['SkinB Shader'].inputs[14])
        links.new(nodes['FacepaintMap'].outputs[0], nodes['SkinB Shader'].inputs[15])
        links.new(nodes['FacepaintMap'].outputs[1], nodes['SkinB Shader'].inputs[16])

        # Link the SkinB Shader node group to the Material Output node
        links.new(nodes['SkinB Shader'].outputs[0], nodes['Material Output'].inputs[0])

    def build(self):
        self.TextureNodes()
        self.SkinB()
        self.LinkNodes()


class UberShader():

    def __init__(self, material):
        self.material = bpy.data.materials.new(name=material)
        self.material.use_nodes = True
        self.material.blend_method = 'CLIP'
        self.material.shadow_method = 'CLIP'
        self.material.use_fake_user = True
        self.material.node_tree.nodes.remove(self.material.node_tree.nodes['Principled BSDF'])

    def TextureNodes(self):
        # Diffuse
        _d = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _d.name = _d.label = "_d DiffuseMap"
        _d.location = (-464, 379)

        # Rotation
        _n = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _n.name = _n.label = "_n RotationMap"
        _n.location = (-464, 117)

        # Gloss
        _s = self.material.node_tree.nodes.new(type='ShaderNodeTexImage')
        _s.name = _s.label = "_s GlossMap"
        _s.location = (-464, -146)

    def Uber(self):
        # Create the node group
        NodeGroup = bpy.data.node_groups.new(name="Uber Shader", type='ShaderNodeTree')

        # Add Group Input node
        GroupInput = NodeGroup.nodes.new(type='NodeGroupInput')
        GroupInput.location = (-550, 44)
        NodeGroup.inputs.new(type='NodeSocketColor', name='DiffuseMap Color')
        NodeGroup.inputs.new(type='NodeSocketColor', name='RotationMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='RotationMap Alpha')
        NodeGroup.inputs.new(type='NodeSocketColor', name='GlossMap Color')
        NodeGroup.inputs.new(type='NodeSocketFloat', name='GlossMap Alpha')

        # Add NdotL node group
        if 'NdotL' not in bpy.data.node_groups:
            CommonGroups.NdotL()
        NdotL = NodeGroup.nodes.new(type='ShaderNodeGroup')
        NdotL.name = "NdotL"
        NdotL.location = (-333, -113)
        NdotL.node_tree = bpy.data.node_groups['NdotL']

        # Add a Multiply Add math node
        MultiplyAdd = NodeGroup.nodes.new(type='ShaderNodeMath')
        MultiplyAdd.name = "MultiplyAdd"
        MultiplyAdd. location = (-333, -208)
        MultiplyAdd.operation = 'MULTIPLY_ADD'
        MultiplyAdd.inputs[1].default_value = 63.0
        MultiplyAdd.inputs[2].default_value = 1.0

        # Add a Power math node
        Power = NodeGroup.nodes.new(type='ShaderNodeMath')
        Power.name = "Power"
        Power.location = (-166, -112)
        Power.operation = 'POWER'

        # Add a RGB to BW node
        RGBtoBW = NodeGroup.nodes.new(type='ShaderNodeRGBToBW')
        RGBtoBW.name = "RGBtoBW"
        RGBtoBW.location = (-166, -279)

        # Add a Gamma node
        Gamma = NodeGroup.nodes.new(type='ShaderNodeGamma')
        Gamma.name = "Gamma"
        Gamma.location = (-2, 183)
        Gamma.inputs[1].default_value = 2.1

        # Add RotationMap node group
        if 'RotationMap' not in bpy.data.node_groups:
            CommonGroups.RotationMap()
        RotationMap = NodeGroup.nodes.new(type='ShaderNodeGroup')
        RotationMap.name = "RotationMap"
        RotationMap.location = (-2, 71)
        RotationMap.node_tree = bpy.data.node_groups['RotationMap']

        # Add a Multiply math node
        Multiply = NodeGroup.nodes.new(type='ShaderNodeMath')
        Multiply.name = "Multiply"
        Multiply.location = (-2, -111)
        Multiply.operation = 'MULTIPLY'

        # Add a Multiply math node
        Multiply2 = NodeGroup.nodes.new(type='ShaderNodeMath')
        Multiply2.name = "Multiply.002"
        Multiply2.location = (200, 200)
        Multiply2.operation = 'MULTIPLY'

        # Add a Principled BSDF shader node
        Principled = NodeGroup.nodes.new(type='ShaderNodeBsdfPrincipled')
        Principled.name = "Principled BSDF"
        Principled.location = (478, 334)
        Principled.inputs[7].default_value = 0.673

        # Add node group's Output node
        GroupOutput = NodeGroup.nodes.new(type='NodeGroupOutput')
        GroupOutput.location = (780, 290)
        NodeGroup.outputs.new(type='NodeSocketShader', name='BSDF')

        # Link nodes together
        NodeGroup.links.new(GroupInput.outputs[0], Gamma.inputs[0])
        NodeGroup.links.new(Gamma.outputs[0], Principled.inputs[0])
        NodeGroup.links.new(Gamma.outputs[0], Multiply2.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[1], RotationMap.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[2], RotationMap.inputs[1])
        NodeGroup.links.new(RotationMap.outputs[0], Multiply2.inputs[1])
        NodeGroup.links.new(RotationMap.outputs[1], Principled.inputs[18])
        NodeGroup.links.new(RotationMap.outputs[2], Principled.inputs[19])
        NodeGroup.links.new(GroupInput.outputs[3], RGBtoBW.inputs[0])
        NodeGroup.links.new(GroupInput.outputs[4], MultiplyAdd.inputs[0])
        NodeGroup.links.new(NdotL.outputs[0], Power.inputs[0])
        NodeGroup.links.new(MultiplyAdd.outputs[0], Power.inputs[1])
        NodeGroup.links.new(Power.outputs[0], Principled.inputs[5])
        NodeGroup.links.new(Power.outputs[0], Multiply.inputs[1])
        NodeGroup.links.new(RGBtoBW.outputs[0], Multiply.inputs[0])
        NodeGroup.links.new(Multiply.outputs[0], Principled.inputs[6])
        NodeGroup.links.new(Multiply2.outputs[0], Principled.inputs[17])
        NodeGroup.links.new(Principled.outputs[0], GroupOutput.inputs[0])

        # Link the node group to the material
        link = self.material.node_tree.nodes.new(type='ShaderNodeGroup')
        link.node_tree = NodeGroup
        link.name = link.label = "Uber Shader"
        link.location = (-53, 90)

    def LinkNodes(self):
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links

        # Link Texture nodes to the Uber Shader node group
        links.new(nodes['_d DiffuseMap'].outputs[0], nodes['Uber Shader'].inputs[0])
        links.new(nodes['_n RotationMap'].outputs[0], nodes['Uber Shader'].inputs[1])
        links.new(nodes['_n RotationMap'].outputs[1], nodes['Uber Shader'].inputs[2])
        links.new(nodes['_s GlossMap'].outputs[0], nodes['Uber Shader'].inputs[3])
        links.new(nodes['_s GlossMap'].outputs[1], nodes['Uber Shader'].inputs[4])

        # Link the Uber Shader node group to the Material Output node
        links.new(nodes['Uber Shader'].outputs[0], nodes['Material Output'].inputs[0])

    def build(self):
        self.TextureNodes()
        self.Uber()
        self.LinkNodes()
