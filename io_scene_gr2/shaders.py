# <pep8 compliant>

import bpy

from bpy.types import ShaderNodeTree

# ========================================= Function Trees ========================================


def _adjustLightness():
    if 'AdjustLightness' in bpy.data.node_groups:
        return bpy.data.node_groups['AdjustLightness']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='AdjustLightness', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketFloat', name='L')
    ngroup.inputs.new(type='NodeSocketFloat', name='Brightness')
    ngroup.inputs.new(type='NodeSocketFloat', name='Contrast')
    ngroup.outputs.new(type='NodeSocketFloat', name='L')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-720.0, 80.0)
    grpIn1.outputs['Brightness'].hide = True

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.location = (-520.0, 80.0)
    math1.operation = 'POWER'

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-520.0, -80.0)
    grpIn2.outputs['L'].hide = True
    grpIn2.outputs['Brightness'].hide = True

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.location = (-300.0, 80.0)
    math2.operation = 'MULTIPLY'

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-300.0, -80.0)
    grpIn3.outputs['L'].hide = True
    grpIn3.outputs['Contrast'].hide = True

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.inputs[0].default_value = 1.0
    math3.location = (-80.0, 80.0)
    math3.operation = 'SUBTRACT'

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (140.0, 160.0)
    grpIn4.outputs['L'].hide = True
    grpIn4.outputs['Contrast'].hide = True

    math4 = ngroup.nodes.new(type='ShaderNodeMath')
    math4.location = (140.0, 80.0)
    math4.operation = 'MULTIPLY'

    math5 = ngroup.nodes.new(type='ShaderNodeMath')
    math5.location = (360.0, 80.0)
    math5.operation = 'ADD'

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (580.0, 80.0)

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (-120.0, 0.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (-120.0, -100.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (60.0, -100.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['L'], math1.inputs[0])
    ngroup.links.new(grpIn1.outputs['Contrast'], math1.inputs[1])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[0])
    ngroup.links.new(grpIn2.outputs['Contrast'], math2.inputs[1])
    ngroup.links.new(math2.outputs['Value'], nr1.inputs[0])
    ngroup.links.new(grpIn3.outputs['Brightness'], math3.inputs[1])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(nr2.outputs[0], nr3.inputs[0])
    ngroup.links.new(math3.outputs['Value'], math4.inputs[0])
    ngroup.links.new(nr3.outputs[0], math4.inputs[1])
    ngroup.links.new(grpIn4.outputs['Brightness'], math5.inputs[0])
    ngroup.links.new(math4.outputs['Value'], math5.inputs[1])
    ngroup.links.new(math5.outputs['Value'], grpOut1.inputs['L'])

    return ngroup


def _chosenPalette():
    if 'ChosenPalette' in bpy.data.node_groups:
        return bpy.data.node_groups['ChosenPalette']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='ChosenPalette', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='Palette1 Hue')
    ngroup.inputs.new(type='NodeSocketFloat', name='Palette1 Saturation')
    ngroup.inputs.new(type='NodeSocketFloat', name='Palette1 Brightness')
    ngroup.inputs.new(type='NodeSocketFloat', name='Palette1 Contrast')
    ngroup.inputs.new(type='NodeSocketColor', name='Palette1 Specular')
    ngroup.inputs.new(type='NodeSocketColor', name='Palette1 Metallic Specular')
    ngroup.inputs.new(type='NodeSocketFloat', name='Palette2 Hue')
    ngroup.inputs.new(type='NodeSocketFloat', name='Palette2 Saturation')
    ngroup.inputs.new(type='NodeSocketFloat', name='Palette2 Brightness')
    ngroup.inputs.new(type='NodeSocketFloat', name='Palette2 Contrast')
    ngroup.inputs.new(type='NodeSocketColor', name='Palette2 Specular')
    ngroup.inputs.new(type='NodeSocketColor', name='Palette2 Metallic Specular')
    ngroup.outputs.new(type='NodeSocketFloat', name='Hue')
    ngroup.outputs.new(type='NodeSocketFloat', name='Saturation')
    ngroup.outputs.new(type='NodeSocketFloat', name='Brightness')
    ngroup.outputs.new(type='NodeSocketFloat', name='Contrast')
    ngroup.outputs.new(type='NodeSocketColor', name='Specular')
    ngroup.outputs.new(type='NodeSocketColor', name='Metallic Specular')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-480.0, 620.0)
    grpIn1.width = 200.0
    for socket in grpIn1.outputs:
        if socket.name != 'Palette2 Hue':
            socket.hide = True

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.location = (-200.0, 620.0)
    math1.operation = 'MULTIPLY'

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (20.0, 620.0)
    grpIn2.width = 200.0
    for socket in grpIn2.outputs:
        if socket.name != 'Palette1 Hue':
            socket.hide = True

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.location = (300.0, 620.0)
    math2.operation = 'MULTIPLY'

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.location = (520.0, 620.0)
    math3.operation = 'ADD'

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-480.0, 420.0)
    grpIn3.width = 200.0
    for socket in grpIn3.outputs:
        if socket.name != 'Palette2 Saturation':
            socket.hide = True

    math4 = ngroup.nodes.new(type='ShaderNodeMath')
    math4.location = (-200.0, 420.0)
    math4.operation = 'MULTIPLY'

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (20.0, 420.0)
    grpIn4.width = 200.0
    for socket in grpIn4.outputs:
        if socket.name != 'Palette1 Saturation':
            socket.hide = True

    math5 = ngroup.nodes.new(type='ShaderNodeMath')
    math5.location = (300.0, 420.0)
    math5.operation = 'MULTIPLY'

    math6 = ngroup.nodes.new(type='ShaderNodeMath')
    math6.location = (520.0, 420.0)
    math6.operation = 'ADD'

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (800.0, 420.0)

    grpIn5 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn5.location = (-480.0, 220.0)
    grpIn5.width = 200.0
    for socket in grpIn5.outputs:
        if socket.name != 'Palette2 Brightness':
            socket.hide = True

    math7 = ngroup.nodes.new(type='ShaderNodeMath')
    math7.location = (-200.0, 220.0)
    math7.operation = 'MULTIPLY'

    grpIn6 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn6.location = (20.0, 220.0)
    grpIn6.width = 200.0
    for socket in grpIn6.outputs:
        if socket.name != 'Palette1 Brightness':
            socket.hide = True

    math8 = ngroup.nodes.new(type='ShaderNodeMath')
    math8.location = (300.0, 220.0)
    math8.operation = 'MULTIPLY'

    math9 = ngroup.nodes.new(type='ShaderNodeMath')
    math9.location = (520.0, 220.0)
    math9.operation = 'ADD'

    grpIn7 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn7.location = (-480.0, 20.0)
    grpIn7.width = 200.0
    for socket in grpIn7.outputs:
        if socket.name != 'Palette2 Contrast':
            socket.hide = True

    math10 = ngroup.nodes.new(type='ShaderNodeMath')
    math10.location = (-200.0, 20.0)
    math10.operation = 'MULTIPLY'

    grpIn8 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn8.location = (20.0, 20.0)
    grpIn8.width = 200.0
    for socket in grpIn8.outputs:
        if socket.name != 'Palette1 Contrast':
            socket.hide = True

    math11 = ngroup.nodes.new(type='ShaderNodeMath')
    math11.location = (300.0, 20.0)
    math11.operation = 'MULTIPLY'

    math12 = ngroup.nodes.new(type='ShaderNodeMath')
    math12.location = (520.0, 20.0)
    math12.operation = 'ADD'

    grpIn9 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn9.location = (-480.0, -180.0)
    grpIn9.width = 200.0
    for socket in grpIn9.outputs:
        if socket.name != 'Palette2 Specular':
            socket.hide = True

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-200.0, -180.0)
    vMath1.operation = 'MULTIPLY'

    grpIn10 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn10.location = (20.0, -180.0)
    grpIn10.width = 200.0
    for socket in grpIn10.outputs:
        if socket.name != 'Palette1 Specular':
            socket.hide = True

    vMath2 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (300.0, -180.0)
    vMath2.operation = 'MULTIPLY'

    vMath3 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (520.0, -180.0)
    vMath3.operation = 'ADD'

    grpIn11 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn11.location = (-480.0, -360.0)
    grpIn11.width = 200.0
    for socket in grpIn11.outputs:
        if socket.name != 'Palette2 Metallic Specular':
            socket.hide = True

    vMath4 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (-200.0, -360.0)
    vMath4.operation = 'MULTIPLY'

    grpIn12 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn12.location = (20.0, -360.0)
    grpIn12.width = 200.0
    for socket in grpIn12.outputs:
        if socket.name != 'Palette1 Metallic Specular':
            socket.hide = True

    vMath5 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath5.location = (300.0, -360.0)
    vMath5.operation = 'MULTIPLY'

    vMath6 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath6.location = (520.0, -360.0)
    vMath6.operation = 'ADD'

    grpIn13 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn13.location = (-920.0, -500.0)
    grpIn13.width = 200
    for socket in grpIn13.outputs:
        if socket.name != '_m PaletteMaskMap Color':
            socket.hide = True

    sepXYZ = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.location = (-640.0, -500.0)
    sepXYZ.outputs['Z'].hide = True

    math13 = ngroup.nodes.new(type='ShaderNodeMath')
    math13.location = (-420.0, -500.0)
    math13.operation = 'LESS_THAN'

    math14 = ngroup.nodes.new(type='ShaderNodeMath')
    math14.inputs[1].default_value = 1.0
    math14.location = (-200.0, -500.0)
    math14.operation = 'LESS_THAN'

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (-240.0, 440.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (260.0, 440.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (20.0, 640.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (480.0, 640.0)
    nr5 = ngroup.nodes.new(type='NodeReroute')
    nr5.location = (480.0, 560.0)

    nr6 = ngroup.nodes.new(type='NodeReroute')
    nr6.location = (-240.0, 260.0)
    nr7 = ngroup.nodes.new(type='NodeReroute')
    nr7.location = (260.0, 260.0)
    nr8 = ngroup.nodes.new(type='NodeReroute')
    nr8.location = (20.0, 440.0)
    nr9 = ngroup.nodes.new(type='NodeReroute')
    nr9.location = (480.0, 440.0)
    nr10 = ngroup.nodes.new(type='NodeReroute')
    nr10.location = (480.0, 360.0)

    nr11 = ngroup.nodes.new(type='NodeReroute')
    nr11.location = (-240.0, 60.0)
    nr12 = ngroup.nodes.new(type='NodeReroute')
    nr12.location = (260.0, 60.0)
    nr13 = ngroup.nodes.new(type='NodeReroute')
    nr13.location = (20.0, 240.0)
    nr14 = ngroup.nodes.new(type='NodeReroute')
    nr14.location = (480.0, 240.0)
    nr15 = ngroup.nodes.new(type='NodeReroute')
    nr15.location = (480.0, 160.0)
    nr16 = ngroup.nodes.new(type='NodeReroute')
    nr16.location = (720.0, 180.0)
    nr17 = ngroup.nodes.new(type='NodeReroute')
    nr17.location = (740.0, 180.0)
    nr18 = ngroup.nodes.new(type='NodeReroute')
    nr18.location = (760.0, 180.0)

    nr19 = ngroup.nodes.new(type='NodeReroute')
    nr19.location = (-240.0, -140.0)
    nr20 = ngroup.nodes.new(type='NodeReroute')
    nr20.location = (260.0, -140.0)
    nr21 = ngroup.nodes.new(type='NodeReroute')
    nr21.location = (20.0, 40.0)
    nr22 = ngroup.nodes.new(type='NodeReroute')
    nr22.location = (480.0, 40.0)
    nr23 = ngroup.nodes.new(type='NodeReroute')
    nr23.location = (480.0, -40.0)
    nr24 = ngroup.nodes.new(type='NodeReroute')
    nr24.location = (720.0, 60.0)

    nr25 = ngroup.nodes.new(type='NodeReroute')
    nr25.location = (-240.0, -320.0)
    nr26 = ngroup.nodes.new(type='NodeReroute')
    nr26.location = (260.0, -320.0)
    nr27 = ngroup.nodes.new(type='NodeReroute')
    nr27.location = (20.0, -160.0)
    nr28 = ngroup.nodes.new(type='NodeReroute')
    nr28.location = (480.0, -160.0)
    nr29 = ngroup.nodes.new(type='NodeReroute')
    nr29.location = (480.0, -220.0)
    nr30 = ngroup.nodes.new(type='NodeReroute')
    nr30.location = (740.0, -120.0)

    nr31 = ngroup.nodes.new(type='NodeReroute')
    nr31.location = (-240.0, -480.0)
    nr32 = ngroup.nodes.new(type='NodeReroute')
    nr32.location = (0.0, -480.0)
    nr33 = ngroup.nodes.new(type='NodeReroute')
    nr33.location = (260.0, -480.0)
    nr34 = ngroup.nodes.new(type='NodeReroute')
    nr34.location = (20.0, -340.0)
    nr35 = ngroup.nodes.new(type='NodeReroute')
    nr35.location = (480.0, -340.0)
    nr36 = ngroup.nodes.new(type='NodeReroute')
    nr36.location = (480.0, -400.0)
    nr37 = ngroup.nodes.new(type='NodeReroute')
    nr37.location = (760.0, -280.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['Palette2 Hue'], math1.inputs[0])
    ngroup.links.new(nr1.outputs[0], math1.inputs[1])
    ngroup.links.new(math1.outputs['Value'], nr3.inputs[0])
    ngroup.links.new(nr3.outputs[0], nr4.inputs[0])
    ngroup.links.new(grpIn2.outputs['Palette1 Hue'], math2.inputs[0])
    ngroup.links.new(nr2.outputs[0], math2.inputs[1])
    ngroup.links.new(math2.outputs['Value'], math3.inputs[1])
    ngroup.links.new(nr4.outputs[0], nr5.inputs[0])
    ngroup.links.new(nr5.outputs[0], math3.inputs[0])
    ngroup.links.new(math3.outputs['Value'], grpOut1.inputs['Hue'])

    ngroup.links.new(grpIn3.outputs['Palette2 Saturation'], math4.inputs[0])
    ngroup.links.new(nr6.outputs[0], nr1.inputs[0])
    ngroup.links.new(nr6.outputs[0], math4.inputs[1])
    ngroup.links.new(math4.outputs['Value'], nr8.inputs[0])
    ngroup.links.new(nr8.outputs[0], nr9.inputs[0])
    ngroup.links.new(grpIn4.outputs['Palette1 Saturation'], math5.inputs[0])
    ngroup.links.new(nr7.outputs[0], nr2.inputs[0])
    ngroup.links.new(nr7.outputs[0], math5.inputs[1])
    ngroup.links.new(math5.outputs['Value'], math6.inputs[1])
    ngroup.links.new(nr9.outputs[0], nr10.inputs[0])
    ngroup.links.new(nr10.outputs[0], math6.inputs[0])
    ngroup.links.new(math6.outputs['Value'], grpOut1.inputs['Saturation'])

    ngroup.links.new(grpIn5.outputs['Palette2 Brightness'], math7.inputs[0])
    ngroup.links.new(nr11.outputs[0], nr6.inputs[0])
    ngroup.links.new(nr11.outputs[0], math7.inputs[1])
    ngroup.links.new(math7.outputs['Value'], nr13.inputs[0])
    ngroup.links.new(nr13.outputs[0], nr14.inputs[0])
    ngroup.links.new(grpIn6.outputs['Palette1 Brightness'], math8.inputs[0])
    ngroup.links.new(nr12.outputs[0], nr7.inputs[0])
    ngroup.links.new(nr12.outputs[0], math8.inputs[1])
    ngroup.links.new(math8.outputs['Value'], math9.inputs[1])
    ngroup.links.new(nr14.outputs[0], nr15.inputs[0])
    ngroup.links.new(nr15.outputs[0], math9.inputs[0])
    ngroup.links.new(math9.outputs['Value'], grpOut1.inputs['Brightness'])
    ngroup.links.new(nr16.outputs[0], grpOut1.inputs['Contrast'])
    ngroup.links.new(nr17.outputs[0], grpOut1.inputs['Specular'])
    ngroup.links.new(nr18.outputs[0], grpOut1.inputs['Metallic Specular'])

    ngroup.links.new(grpIn7.outputs['Palette2 Contrast'], math10.inputs[0])
    ngroup.links.new(nr19.outputs[0], nr11.inputs[0])
    ngroup.links.new(nr19.outputs[0], math10.inputs[1])
    ngroup.links.new(math10.outputs['Value'], nr21.inputs[0])
    ngroup.links.new(nr21.outputs[0], nr22.inputs[0])
    ngroup.links.new(grpIn8.outputs['Palette1 Contrast'], math11.inputs[0])
    ngroup.links.new(nr20.outputs[0], nr12.inputs[0])
    ngroup.links.new(nr20.outputs[0], math11.inputs[1])
    ngroup.links.new(math11.outputs['Value'], math12.inputs[1])
    ngroup.links.new(nr22.outputs[0], nr23.inputs[0])
    ngroup.links.new(nr23.outputs[0], math12.inputs[0])
    ngroup.links.new(math12.outputs['Value'], nr24.inputs[0])
    ngroup.links.new(nr24.outputs[0], nr16.inputs[0])

    ngroup.links.new(grpIn9.outputs['Palette2 Specular'], vMath1.inputs[0])
    ngroup.links.new(nr25.outputs[0], nr19.inputs[0])
    ngroup.links.new(nr25.outputs[0], vMath1.inputs[1])
    ngroup.links.new(vMath1.outputs['Vector'], nr27.inputs[0])
    ngroup.links.new(nr27.outputs[0], nr28.inputs[0])
    ngroup.links.new(grpIn10.outputs['Palette1 Specular'], vMath2.inputs[0])
    ngroup.links.new(nr26.outputs[0], nr20.inputs[0])
    ngroup.links.new(nr26.outputs[0], vMath2.inputs[1])
    ngroup.links.new(vMath2.outputs['Vector'], vMath3.inputs[1])
    ngroup.links.new(nr28.outputs[0], nr29.inputs[0])
    ngroup.links.new(nr29.outputs[0], vMath3.inputs[0])
    ngroup.links.new(vMath3.outputs['Vector'], nr30.inputs[0])
    ngroup.links.new(nr30.outputs[0], nr17.inputs[0])

    ngroup.links.new(grpIn11.outputs['Palette2 Metallic Specular'], vMath4.inputs[0])
    ngroup.links.new(nr31.outputs[0], nr25.inputs[0])
    ngroup.links.new(nr31.outputs[0], vMath4.inputs[1])
    ngroup.links.new(vMath4.outputs['Vector'], nr34.inputs[0])
    ngroup.links.new(nr32.outputs[0], nr33.inputs[0])
    ngroup.links.new(nr34.outputs[0], nr35.inputs[0])
    ngroup.links.new(grpIn12.outputs['Palette1 Metallic Specular'], vMath5.inputs[0])
    ngroup.links.new(nr33.outputs[0], nr26.inputs[0])
    ngroup.links.new(nr33.outputs[0], vMath5.inputs[1])
    ngroup.links.new(vMath5.outputs['Vector'], vMath6.inputs[1])
    ngroup.links.new(nr35.outputs[0], nr36.inputs[0])
    ngroup.links.new(nr36.outputs[0], vMath6.inputs[0])
    ngroup.links.new(vMath6.outputs['Vector'], nr37.inputs[0])
    ngroup.links.new(nr37.outputs[0], nr18.inputs[0])

    ngroup.links.new(grpIn13.outputs['_m PaletteMaskMap Color'], sepXYZ.inputs['Vector'])
    ngroup.links.new(sepXYZ.outputs['X'], math13.inputs[0])
    ngroup.links.new(sepXYZ.outputs['Y'], math13.inputs[1])
    ngroup.links.new(math13.outputs['Value'], nr31.inputs[0])
    ngroup.links.new(math13.outputs['Value'], math14.inputs[0])
    ngroup.links.new(math14.outputs['Value'], nr32.inputs[0])

    return ngroup


def _combineNormals():
    if 'CombineNormals' in bpy.data.node_groups:
        return bpy.data.node_groups['CombineNormals']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='CombineNormals', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketVector', name='TexNormal')
    ngroup.inputs.new(type='NodeSocketVector', name='AgeNormal')
    ngroup.inputs.new(type='NodeSocketFloat', name='Scar Strength')
    ngroup.inputs['Scar Strength'].default_value = 1.0
    ngroup.outputs.new(type='NodeSocketVector', name='Normal')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-320.0, 180.0)
    grpIn1.outputs['AgeNormal'].hide = True
    grpIn1.outputs['Scar Strength'].hide = True

    texNorMap = ngroup.nodes.new(type='ShaderNodeNormalMap')
    texNorMap.location = (-80.0, 180.0)

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (180.0, 180.0)
    vMath1.operation = 'ADD'

    vMath2 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (420.0, 180.0)
    vMath2.operation = 'NORMALIZE'

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (660.0, 180.0)

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-800.0, 20.0)
    grpIn2.outputs['TexNormal'].hide = True
    grpIn2.outputs['Scar Strength'].hide = True

    sepXYZ1 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ1.location = (-560.0, 20.0)
    sepXYZ1.outputs['Z'].hide = True

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-320.0, 20.0)
    grpIn3.outputs['TexNormal'].hide = True
    grpIn3.outputs['AgeNormal'].hide = True

    ageNorMap = ngroup.nodes.new(type='ShaderNodeNormalMap')
    ageNorMap.location = (-80.0, 20.0)

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (-800.0, -80.0)
    grpIn4.outputs['AgeNormal'].hide = True
    grpIn4.outputs['Scar Strength'].hide = True

    sepXYZ2 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ2.location = (-560.0, -80.0)
    sepXYZ2.outputs['X'].hide = True
    sepXYZ2.outputs['Y'].hide = True

    comXYZ = ngroup.nodes.new(type='ShaderNodeCombineXYZ')
    comXYZ.location = (-320.0, -60.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['TexNormal'], texNorMap.inputs['Color'])
    ngroup.links.new(texNorMap.outputs['Normal'], vMath1.inputs[0])
    ngroup.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    ngroup.links.new(vMath2.outputs['Vector'], grpOut1.inputs['Normal'])
    ngroup.links.new(grpIn2.outputs['AgeNormal'], sepXYZ1.inputs['Vector'])
    ngroup.links.new(sepXYZ1.outputs['X'], comXYZ.inputs['X'])
    ngroup.links.new(sepXYZ1.outputs['Y'], comXYZ.inputs['Y'])
    ngroup.links.new(grpIn3.outputs['Scar Strength'], ageNorMap.inputs['Strength'])
    ngroup.links.new(ageNorMap.outputs['Normal'], vMath1.inputs[1])
    ngroup.links.new(grpIn4.outputs['TexNormal'], sepXYZ2.inputs['Vector'])
    ngroup.links.new(sepXYZ2.outputs['Z'], comXYZ.inputs['Z'])
    ngroup.links.new(comXYZ.outputs['Vector'], ageNorMap.inputs['Color'])

    return ngroup


def _convertHSLToRGB():
    if 'ConvertHSLToRGB' in bpy.data.node_groups:
        return bpy.data.node_groups['ConvertHSLToRGB']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='ConvertHSLToRGB', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketFloat', name='H')
    ngroup.inputs.new(type='NodeSocketFloat', name='S')
    ngroup.inputs.new(type='NodeSocketFloat', name='L')
    ngroup.outputs.new(type='NodeSocketColor', name='RGB')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-1420.0, 80.0)
    grpIn1.outputs['H'].hide = True
    grpIn1.outputs['S'].hide = True

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.inputs[0].default_value = 2.0
    math1.location = (-1180.0, 80.0)
    math1.operation = 'MULTIPLY'

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.inputs[1].default_value = 1.0
    math2.location = (-960.0, 80.0)
    math2.operation = 'SUBTRACT'

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.location = (-740.0, 80.0)
    math3.operation = 'ABSOLUTE'

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-520.0, 160.0)
    grpIn2.outputs['H'].hide = True
    grpIn2.outputs['L'].hide = True

    math4 = ngroup.nodes.new(type='ShaderNodeMath')
    math4.inputs[0].default_value = 1.0
    math4.location = (-520.0, 80.0)
    math4.operation = 'SUBTRACT'

    math5 = ngroup.nodes.new(type='ShaderNodeMath')
    math5.location = (-300.0, 80.0)
    math5.operation = 'MULTIPLY'

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-80.0, 160.0)
    grpIn3.outputs['H'].hide = True
    grpIn3.outputs['S'].hide = True

    math6 = ngroup.nodes.new(type='ShaderNodeMath')
    math6.inputs[1].default_value = 2.0
    math6.location = (-80.0, 80.0)
    math6.operation = 'DIVIDE'

    math7 = ngroup.nodes.new(type='ShaderNodeMath')
    math7.location = (140.0, 80.0)
    math7.operation = 'ADD'

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (140.0, -80.0)
    grpIn4.outputs['H'].hide = True
    grpIn4.outputs['S'].hide = True

    math8 = ngroup.nodes.new(type='ShaderNodeMath')
    math8.location = (360.0, 80.0)
    math8.operation = 'SUBTRACT'

    math9 = ngroup.nodes.new(type='ShaderNodeMath')
    math9.inputs[0].default_value = 2.0
    math9.location = (580.0, 80.0)
    math9.operation = 'MULTIPLY'

    grpIn5 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn5.location = (800.0, 160.0)
    grpIn5.outputs['S'].hide = True
    grpIn5.outputs['L'].hide = True

    math10 = ngroup.nodes.new(type='ShaderNodeMath')
    math10.location = (800.0, 80.0)
    math10.operation = 'DIVIDE'

    comHSV = ngroup.nodes.new(type='ShaderNodeCombineHSV')
    comHSV.location = (1020.0, 80.0)

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1240.0, 80.0)

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (320.0, 0.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (320.0, -100.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (720.0, -100.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (940.0, -100.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['L'], math1.inputs[1])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[0])
    ngroup.links.new(math2.outputs['Value'], math3.inputs[0])
    ngroup.links.new(math3.outputs['Value'], math4.inputs[1])
    ngroup.links.new(grpIn2.outputs['S'], math5.inputs[0])
    ngroup.links.new(math4.outputs['Value'], math5.inputs[1])
    ngroup.links.new(math5.outputs['Value'], math6.inputs[0])
    ngroup.links.new(grpIn3.outputs['L'], math7.inputs[0])
    ngroup.links.new(math6.outputs['Value'], math7.inputs[1])
    ngroup.links.new(math7.outputs['Value'], nr1.inputs[0])
    ngroup.links.new(grpIn4.outputs['L'], math8.inputs[1])
    ngroup.links.new(nr1.outputs[0], math8.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(nr2.outputs[0], nr3.inputs[0])
    ngroup.links.new(math8.outputs['Value'], math9.inputs[1])
    ngroup.links.new(math9.outputs['Value'], math10.inputs[0])
    ngroup.links.new(nr3.outputs[0], math10.inputs[1])
    ngroup.links.new(nr3.outputs[0], nr4.inputs[0])
    ngroup.links.new(grpIn5.outputs['H'], comHSV.inputs['H'])
    ngroup.links.new(math10.outputs['Value'], comHSV.inputs['S'])
    ngroup.links.new(nr4.outputs[0], comHSV.inputs['V'])
    ngroup.links.new(comHSV.outputs['Color'], grpOut1.inputs['RGB'])

    return ngroup


def _expandHSL():
    if 'ExpandHSL' in bpy.data.node_groups:
        return bpy.data.node_groups['ExpandHSL']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='ExpandHSL', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
    ngroup.outputs.new(type='NodeSocketFloat', name='H')
    ngroup.outputs.new(type='NodeSocketFloat', name='S')
    ngroup.outputs.new(type='NodeSocketFloat', name='L')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-500.0, 260.0)
    grpIn1.outputs['_h PaletteMap Alpha'].hide = True

    sepXYZ = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.location = (-280.0, 260.0)
    sepXYZ.outputs['X'].hide = True

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.inputs[0].default_value = 0.706
    math1.inputs[1].default_value = 0.3137
    math1.location = (-280.0, 80.0)
    math1.operation = 'SUBTRACT'

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-280.0, -80.0)
    grpIn2.outputs['_h PaletteMap Color'].hide = True

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.inputs[2].default_value = 0.3137
    math2.location = (-60.0, 260.0)
    math2.operation = 'MULTIPLY_ADD'

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.inputs[1].default_value = 0.5882
    math3.location = (-60.0, 80.0)
    math3.operation = 'MULTIPLY'

    math4 = ngroup.nodes.new(type='ShaderNodeMath')
    math4.inputs[1].default_value = 0.70588
    math4.location = (-60.0, -80.0)
    math4.operation = 'MULTIPLY'

    math5 = ngroup.nodes.new(type='ShaderNodeMath')
    math5.inputs[1].default_value = 0.41176
    math5.location = (160.0, 260.0)
    math5.operation = 'SUBTRACT'

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (380.0, 260.0)

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (-100.0, 160.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (-100.0, 20.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (120.0, 80.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (120.0, 60.0)
    nr5 = ngroup.nodes.new(type='NodeReroute')
    nr5.location = (120.0, -60.0)
    nr6 = ngroup.nodes.new(type='NodeReroute')
    nr6.location = (320.0, 140.0)
    nr7 = ngroup.nodes.new(type='NodeReroute')
    nr7.location = (320.0, 80.0)
    nr8 = ngroup.nodes.new(type='NodeReroute')
    nr8.location = (340.0, 140.0)
    nr9 = ngroup.nodes.new(type='NodeReroute')
    nr9.location = (340.0, 60.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['_h PaletteMap Color'], sepXYZ.inputs['Vector'])
    ngroup.links.new(sepXYZ.outputs['Y'], math2.inputs[0])
    ngroup.links.new(sepXYZ.outputs['Z'], nr1.inputs[0])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[1])
    ngroup.links.new(grpIn2.outputs['_h PaletteMap Alpha'], math4.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(nr2.outputs[0], math3.inputs[0])
    ngroup.links.new(math2.outputs['Value'], math5.inputs[0])
    ngroup.links.new(math3.outputs['Value'], nr3.inputs[0])
    ngroup.links.new(math4.outputs['Value'], nr5.inputs[0])
    ngroup.links.new(nr3.outputs[0], nr7.inputs[0])
    ngroup.links.new(nr4.outputs[0], nr9.inputs[0])
    ngroup.links.new(nr5.outputs[0], nr4.inputs[0])
    ngroup.links.new(math5.outputs['Value'], grpOut1.inputs['H'])
    ngroup.links.new(nr6.outputs[0], grpOut1.inputs['S'])
    ngroup.links.new(nr7.outputs[0], nr6.inputs[0])
    ngroup.links.new(nr8.outputs[0], grpOut1.inputs['L'])
    ngroup.links.new(nr9.outputs[0], nr8.inputs[0])

    return ngroup


def _extractAgeNormalAndScarFromSwizzledTexture():
    if 'ExtractAgeNormalAndScarFromSwizzledTexture' in bpy.data.node_groups:
        return bpy.data.node_groups['ExtractAgeNormalAndScarFromSwizzledTexture']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(
        name='ExtractAgeNormalAndScarFromSwizzledTexture',
        type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='AgeMap Color')
    ngroup.inputs['AgeMap Color'].default_value = [0.0, 0.5, 1.0, 1.0]
    ngroup.inputs.new(type='NodeSocketFloat', name='AgeMap Alpha')
    ngroup.inputs['AgeMap Alpha'].default_value = 0.5
    ngroup.outputs.new(type='NodeSocketVector', name='Normal')
    ngroup.outputs.new(type='NodeSocketFloat', name='Scar Mask')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-80.0, 180.0)
    grpIn1.outputs['AgeMap Color'].hide = True

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-560.0, 60.0)
    grpIn2.outputs['AgeMap Alpha'].hide = True

    sepXYZ = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.outputs['X'].hide = True
    sepXYZ.location = (-320.0, 60.0)

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.inputs[0].default_value = 1.0
    math1.location = (-80.0, 60.0)
    math1.operation = 'SUBTRACT'

    comXYZ = ngroup.nodes.new(type='ShaderNodeCombineXYZ')
    comXYZ.inputs['Z'].default_value = 0.0
    comXYZ.location = (160.0, 60.0)

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (400.0, 60.0)

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (-80.0, 80.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (300.0, 80.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['AgeMap Alpha'], comXYZ.inputs['X'])
    ngroup.links.new(grpIn2.outputs['AgeMap Color'], sepXYZ.inputs['Vector'])
    ngroup.links.new(sepXYZ.outputs['Y'], math1.inputs[1])
    ngroup.links.new(sepXYZ.outputs['Z'], nr1.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(math1.outputs['Value'], comXYZ.inputs['Y'])
    ngroup.links.new(nr2.outputs[0], grpOut1.inputs['Scar Mask'])
    ngroup.links.new(comXYZ.outputs['Vector'], grpOut1.inputs['Normal'])

    return ngroup


def _getFlushColor():
    if 'GetFlushColor' in bpy.data.node_groups:
        return bpy.data.node_groups['GetFlushColor']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='GetFlushColor', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='Diffuse Color')
    ngroup.inputs['Diffuse Color'].default_value = [0.0, 0.0, 0.0, 1.0]
    ngroup.inputs.new(type='NodeSocketFloat', name='Flesh Brightness')
    ngroup.inputs['Flesh Brightness'].default_value = 0.0
    ngroup.inputs['Flesh Brightness'].max_value = 1.0
    ngroup.inputs['Flesh Brightness'].min_value = 0.0
    ngroup.inputs.new(type='NodeSocketColor', name='Flush Tone')
    ngroup.inputs['Flush Tone'].default_value = [0.0, 0.0, 0.0, 1.0]
    ngroup.inputs.new(type='NodeSocketVector', name='Normal')
    ngroup.outputs.new(type='NodeSocketColor', name='Flush Color')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-960.0, 80.0)
    for socket in grpIn1.outputs:
        if socket.name != 'Normal':
            socket.hide = True

    geom1 = ngroup.nodes.new(type='ShaderNodeNewGeometry')
    geom1.location = (-960.0, 0.0)
    for socket in geom1.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-740.0, 80.0)
    vMath1.operation = 'DOT_PRODUCT'

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.inputs[1].default_value = 0.27
    math1.location = (-520.0, 80.0)
    math1.operation = 'SUBTRACT'

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.inputs[1].default_value = 3.0
    math2.location = (-300.0, 80.0)
    math2.operation = 'MULTIPLY'

    clamp1 = ngroup.nodes.new(type='ShaderNodeClamp')
    clamp1.inputs['Min'].default_value = 0.0
    clamp1.inputs['Max'].default_value = 1.0
    clamp1.location = (-80.0, 80.0)

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-80.0, -80.0)
    for socket in grpIn2.outputs:
        if socket.name != 'Flesh Brightness':
            socket.hide = True

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (140.0, 200.0)
    for socket in grpIn3.outputs:
        if socket.name != 'Flush Tone':
            socket.hide = True

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.location = (140.0, 80.0)
    math3.operation = 'MULTIPLY'

    vMath2 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (360.0, 80.0)
    vMath2.operation = 'MULTIPLY'

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (360.0, -80.0)
    for socket in grpIn4.outputs:
        if socket.name != 'Diffuse Color':
            socket.hide = True

    vMath3 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (580.0, 80.0)
    vMath3.operation = 'MULTIPLY'

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (800.0, 80.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['Normal'], vMath1.inputs[0])
    ngroup.links.new(geom1.outputs['Incoming'], vMath1.inputs[1])
    ngroup.links.new(vMath1.outputs['Value'], math1.inputs[0])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[0])
    ngroup.links.new(math2.outputs['Value'], clamp1.inputs['Value'])
    ngroup.links.new(clamp1.outputs['Result'], math3.inputs[0])
    ngroup.links.new(grpIn2.outputs['Flesh Brightness'], math3.inputs[1])
    ngroup.links.new(grpIn3.outputs['Flush Tone'], vMath2.inputs[0])
    ngroup.links.new(math3.outputs['Value'], vMath2.inputs[1])
    ngroup.links.new(vMath2.outputs['Vector'], vMath3.inputs[0])
    ngroup.links.new(grpIn4.outputs['Diffuse Color'], vMath3.inputs[1])
    ngroup.links.new(vMath3.outputs['Vector'], grpOut1.inputs['Flush Color'])

    return ngroup


def _getPhongSpecular():
    if 'GetPhongSpecular' in bpy.data.node_groups:
        return bpy.data.node_groups['GetPhongSpecular']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='GetPhongSpecular', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='Specular Color')
    ngroup.inputs['Specular Color'].default_value = [0.0, 0.0, 0.0, 1.0]
    ngroup.inputs.new(type='NodeSocketFloat', name='Specular Alpha')
    ngroup.inputs['Specular Alpha'].default_value = 0.0
    ngroup.inputs.new(type='NodeSocketVector', name='Normal')
    ngroup.inputs.new(type='NodeSocketVector', name='-Normal')
    ngroup.inputs.new(type='NodeSocketFloat', name='MaxSpecPower')
    ngroup.inputs['MaxSpecPower'].default_value = 64.0 * 0.5
    ngroup.outputs.new(type='NodeSocketColor', name='Specular')

    # Add and place nodes
    geom1 = ngroup.nodes.new(type='ShaderNodeNewGeometry')
    geom1.location = (-1240.0, 200.0)
    for socket in geom1.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.inputs[1].default_value = [-1.0, -1.0, -1.0]
    vMath1.location = (-1000.0, 200.0)
    vMath1.operation = 'MULTIPLY'

    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-1000.0, 0.0)
    for socket in grpIn1.outputs:
        if socket.name != '-Normal':
            socket.hide = True

    vMath2 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (-760, 200.0)
    vMath2.operation = 'REFLECT'

    geom2 = ngroup.nodes.new(type='ShaderNodeNewGeometry')
    geom2.location = (-760.0, 0.0)
    for socket in geom2.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vMath3 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (-520.0, 200.0)
    vMath3.operation = 'DOT_PRODUCT'

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-520.0, -100.0)
    for socket in grpIn2.outputs:
        if socket.name not in ['Specular Alpha', 'MaxSpecPower']:
            socket.hide = True

    clamp1 = ngroup.nodes.new(type='ShaderNodeClamp')
    clamp1.inputs['Min'].default_value = 0.0
    clamp1.inputs['Max'].default_value = 1.0
    clamp1.location = (-280.0, 200.0)

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.inputs[2].default_value = 1.0
    math1.location = (-280.0, -100.0)
    math1.operation = 'MULTIPLY_ADD'

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-60.0, 200.0)
    for socket in grpIn3.outputs:
        if socket.name != 'Specular Color':
            socket.hide = True

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.location = (-60.0, 80.0)
    math2.operation = 'POWER'

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (-60.0, -100.0)
    for socket in grpIn4.outputs:
        if socket.name != 'Normal':
            socket.hide = True

    geom3 = ngroup.nodes.new(type='ShaderNodeNewGeometry')
    geom3.location = (-60.0, -180.0)
    for socket in geom3.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vMath4 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (180.0, 80.0)
    vMath4.operation = 'MULTIPLY'

    vMath5 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath5.location = (180.0, -100.0)
    vMath5.operation = 'DOT_PRODUCT'

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.inputs[1].default_value = 8.0
    math3.location = (400.0, 80.0)
    math3.operation = 'MULTIPLY'

    clamp2 = ngroup.nodes.new(type='ShaderNodeClamp')
    clamp2.inputs['Min'].default_value = 0.0
    clamp2.inputs['Max'].default_value = 1.0
    clamp2.location = (620.0, 80.0)

    vMath6 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath6.location = (840.0, 80.0)
    vMath6.operation = 'MULTIPLY'

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1060.0, 80.0)

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (400.0, 100.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (800.0, 100.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (800.0, 40.0)

    # Link nodes together
    ngroup.links.new(geom1.outputs['Incoming'], vMath1.inputs[0])
    ngroup.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    ngroup.links.new(grpIn1.outputs['-Normal'], vMath2.inputs[1])
    ngroup.links.new(vMath2.outputs['Vector'], vMath3.inputs[0])
    ngroup.links.new(geom2.outputs['Incoming'], vMath3.inputs[1])
    ngroup.links.new(vMath3.outputs['Value'], clamp1.inputs['Value'])
    ngroup.links.new(clamp1.outputs['Result'], math2.inputs[0])
    ngroup.links.new(grpIn2.outputs['Specular Alpha'], math1.inputs[0])
    ngroup.links.new(grpIn2.outputs['MaxSpecPower'], math1.inputs[1])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[1])
    ngroup.links.new(grpIn3.outputs['Specular Color'], vMath4.inputs[0])
    ngroup.links.new(math2.outputs['Value'], vMath4.inputs[1])
    ngroup.links.new(grpIn4.outputs['Normal'], vMath5.inputs[0])
    ngroup.links.new(geom3.outputs['Incoming'], vMath5.inputs[1])
    ngroup.links.new(vMath4.outputs['Vector'], nr1.inputs[0])
    ngroup.links.new(vMath5.outputs['Value'], math3.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(math3.outputs['Value'], clamp2.inputs['Value'])
    ngroup.links.new(clamp2.outputs['Result'], vMath6.inputs[1])
    ngroup.links.new(nr2.outputs[0], nr3.inputs[0])
    ngroup.links.new(nr3.outputs[0], vMath6.inputs[0])
    ngroup.links.new(vMath6.outputs['Vector'], grpOut1.inputs['Specular'])

    return ngroup


def _getSpecularLookup():
    if 'GetSpecularLookup' in bpy.data.node_groups:
        return bpy.data.node_groups['GetSpecularLookup']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='GetSpecularLookup', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketVector', name='Normal')
    ngroup.outputs.new(type='NodeSocketVector', name='Vector')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-540.0, 0.0)

    geom1 = ngroup.nodes.new(type='ShaderNodeNewGeometry')
    geom1.location = (-540.0, -80.0)
    for socket in geom1.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-300.0, 0.0)
    vMath1.operation = 'DOT_PRODUCT'

    mapRange = ngroup.nodes.new(type='ShaderNodeMapRange')
    mapRange.clamp = True
    mapRange.inputs['From Min'].default_value = -1.0
    mapRange.inputs['From Max'].default_value = 1.0
    mapRange.inputs['To Min'].default_value = 0.0
    mapRange.inputs['To Max'].default_value = 1.0
    mapRange.interpolation_type = 'SMOOTHSTEP'
    mapRange.location = (-60.0, 0.0)

    comXYZ = ngroup.nodes.new(type='ShaderNodeCombineXYZ')
    comXYZ.inputs['Z'].default_value = 0.0
    comXYZ.inputs['Z'].hide = True
    comXYZ.location = (180.0, 0.0)

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (420.0, 0.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['Normal'], vMath1.inputs[0])
    ngroup.links.new(geom1.outputs['Incoming'], vMath1.inputs[1])
    ngroup.links.new(vMath1.outputs['Value'], mapRange.inputs['Value'])
    ngroup.links.new(mapRange.outputs['Result'], comXYZ.inputs['X'])
    ngroup.links.new(mapRange.outputs['Result'], comXYZ.inputs['Y'])
    ngroup.links.new(comXYZ.outputs['Vector'], grpOut1.inputs['Vector'])

    return ngroup


def _huePixel():
    if 'HuePixel' in bpy.data.node_groups:
        return bpy.data.node_groups['HuePixel']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='HuePixel', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='_d DiffuseMap Color')
    ngroup.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
    ngroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
    ngroup.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='Hue')
    ngroup.inputs.new(type='NodeSocketFloat', name='Saturation')
    ngroup.inputs.new(type='NodeSocketFloat', name='Brightness')
    ngroup.inputs.new(type='NodeSocketFloat', name='Contrast')
    ngroup.inputs.new(type='NodeSocketColor', name='Metallic Specular')
    ngroup.inputs.new(type='NodeSocketColor', name='Specular')
    ngroup.outputs.new(type='NodeSocketColor', name='Diffuse Color')
    ngroup.outputs.new(type='NodeSocketColor', name='Specular Color')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-1400.0, 440.0)
    for socket in grpIn1.outputs:
        if socket.name != '_m PaletteMaskMap Color':
            socket.hide = True

    sepXYZ1 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ1.location = (-1060.0, 440.0)

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.location = (-600.0, 440.0)
    math1.operation = 'ADD'

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-1400.0, 240.0)
    for socket in grpIn2.outputs:
        if socket.name not in [
            '_h PaletteMap Color',
            '_h PaletteMap Alpha',
            'Hue',
            'Saturation',
            'Brightness',
                'Contrast']:
            socket.hide = True

    manHSL = ngroup.nodes.new(type='ShaderNodeGroup')
    manHSL.location = (-1180.0, 240.0)
    manHSL.name = 'ManipulateHSL'
    manHSL.node_tree = _manipulateHSL()
    manHSL.width = 260.0

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.location = (-840.0, 140.0)
    math2.operation = 'MULTIPLY'

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-600.0, 240.0)
    for socket in grpIn3.outputs:
        if socket.name != '_d DiffuseMap Color':
            socket.hide = True

    toRGB = ngroup.nodes.new(type='ShaderNodeGroup')
    toRGB.location = (-600.0, 140.0)
    toRGB.name = 'ConvertHSLtoRGB'
    toRGB.node_tree = _convertHSLToRGB()

    mixRGB1 = ngroup.nodes.new(type='ShaderNodeMixRGB')
    mixRGB1.location = (-360.0, 140.0)

    gamma1 = ngroup.nodes.new(type='ShaderNodeGamma')
    gamma1.inputs['Gamma'].default_value = 2.1
    gamma1.location = (-120.0, 140.0)

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (160.0, 140.0)
    vMath1.operation = 'MULTIPLY'

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (-1400.0, -80.0)
    for socket in grpIn4.outputs:
        if socket.name not in ['_h PaletteMap Color', 'Brightness']:
            socket.hide = True

    manAO = ngroup.nodes.new(type='ShaderNodeGroup')
    manAO.location = (-1180.0, -80.0)
    manAO.name = 'ManipulateAO'
    manAO.node_tree = _manipulateAO()
    manAO.width = 260.0

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.inputs[1].default_value = 0.5
    math3.location = (-840.0, -80.0)
    math3.operation = 'SUBTRACT'

    math4 = ngroup.nodes.new(type='ShaderNodeMath')
    math4.inputs[1].default_value = 2.0
    math4.location = (-600.0, -80.0)
    math4.operation = 'MULTIPLY'

    mixRGB2 = ngroup.nodes.new(type='ShaderNodeMixRGB')
    mixRGB2.inputs['Color1'].default_value = [1.0, 1.0, 1.0, 1.0]
    mixRGB2.location = (-360.0, -80.0)

    math5 = ngroup.nodes.new(type='ShaderNodeMath')
    math5.inputs[1].default_value = 0.5
    math5.location = (-100.0, -80.0)
    math5.operation = 'GREATER_THAN'

    math6 = ngroup.nodes.new(type='ShaderNodeMath')
    math6.inputs[1].default_value = 1.0
    math6.location = (160.0, -80.0)
    math6.operation = 'LESS_THAN'

    vMath2 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (400.0, -80.0)
    vMath2.operation = 'MULTIPLY'

    vMath3 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (640.0, -80.0)
    vMath3.operation = 'ADD'

    vMath4 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (880.0, -80.0)
    vMath4.operation = 'MULTIPLY'

    mixRGB3 = ngroup.nodes.new(type='ShaderNodeMixRGB')
    mixRGB3.location = (1120.0, -80.0)

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1360.0, -80.0)

    math7 = ngroup.nodes.new(type='ShaderNodeMath')
    math7.inputs[1].default_value = 2.0
    math7.location = (-840.0, -280.0)
    math7.operation = 'MULTIPLY'

    grpIn5 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn5.location = (-600.0, -280.0)
    for socket in grpIn5.outputs:
        if socket.name not in ['Metallic Specular', 'Specular']:
            socket.hide = True

    mixRGB4 = ngroup.nodes.new(type='ShaderNodeMixRGB')
    mixRGB4.inputs['Color2'].default_value = [1.0, 1.0, 1.0, 1.0]
    mixRGB4.location = (-360.0, -280.0)

    grpIn6 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn6.location = (400.0, -280.0)
    for socket in grpIn6.outputs:
        if socket.name != '_s GlossMap Color':
            socket.hide = True

    sepXYZ2 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ2.location = (640.0, -280.0)
    sepXYZ2.outputs['Y'].hide = True
    sepXYZ2.outputs['Z'].hide = True

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (-880.0, 320.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (-380.0, 320.0)

    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (-840.0, 180.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (-620.0, 180.0)
    nr5 = ngroup.nodes.new(type='NodeReroute')
    nr5.location = (-620.0, 80.0)
    nr6 = ngroup.nodes.new(type='NodeReroute')
    nr6.location = (-840.0, 160.0)
    nr7 = ngroup.nodes.new(type='NodeReroute')
    nr7.location = (-640.0, 160.0)
    nr8 = ngroup.nodes.new(type='NodeReroute')
    nr8.location = (-640.0, 80.0)
    nr9 = ngroup.nodes.new(type='NodeReroute')
    nr9.location = (-380.0, 160.0)
    nr10 = ngroup.nodes.new(type='NodeReroute')
    nr10.location = (-380.0, 60.0)
    nr11 = ngroup.nodes.new(type='NodeReroute')
    nr11.location = (300.0, 160.0)

    nr12 = ngroup.nodes.new(type='NodeReroute')
    nr12.location = (-880.0, -60.0)
    nr13 = ngroup.nodes.new(type='NodeReroute')
    nr13.location = (-880.0, -140.0)
    nr14 = ngroup.nodes.new(type='NodeReroute')
    nr14.location = (-240.0, -60.0)
    nr15 = ngroup.nodes.new(type='NodeReroute')
    nr15.location = (-100.0, -60.0)
    nr16 = ngroup.nodes.new(type='NodeReroute')
    nr16.location = (40.0, -60.0)
    nr17 = ngroup.nodes.new(type='NodeReroute')
    nr17.location = (180.0, -40.0)
    nr18 = ngroup.nodes.new(type='NodeReroute')
    nr18.location = (500.0, -20.0)
    nr19 = ngroup.nodes.new(type='NodeReroute')
    nr19.location = (500.0, -60.0)
    nr20 = ngroup.nodes.new(type='NodeReroute')
    nr20.location = (600.0, -60.0)
    nr21 = ngroup.nodes.new(type='NodeReroute')
    nr21.location = (600.0, -120.0)
    nr22 = ngroup.nodes.new(type='NodeReroute')
    nr22.location = (1100.0, -20.0)
    nr23 = ngroup.nodes.new(type='NodeReroute')
    nr23.location = (1100.0, -160.0)
    nr24 = ngroup.nodes.new(type='NodeReroute')
    nr24.location = (1260.0, -40.0)

    nr25 = ngroup.nodes.new(type='NodeReroute')
    nr25.location = (-880.0, -340.0)
    nr26 = ngroup.nodes.new(type='NodeReroute')
    nr26.location = (-600.0, -260.0)
    nr27 = ngroup.nodes.new(type='NodeReroute')
    nr27.location = (-380.0, -260.0)
    nr28 = ngroup.nodes.new(type='NodeReroute')
    nr28.location = (-380.0, -360.0)
    nr29 = ngroup.nodes.new(type='NodeReroute')
    nr29.location = (-100.0, -260.0)
    nr30 = ngroup.nodes.new(type='NodeReroute')
    nr30.location = (300.0, -260.0)
    nr31 = ngroup.nodes.new(type='NodeReroute')
    nr31.location = (640.0, -260.0)
    nr32 = ngroup.nodes.new(type='NodeReroute')
    nr32.location = (1020.0, -260.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['_m PaletteMaskMap Color'], sepXYZ1.inputs['Vector'])
    ngroup.links.new(sepXYZ1.outputs['X'], math1.inputs[0])
    ngroup.links.new(sepXYZ1.outputs['Y'], math1.inputs[1])
    ngroup.links.new(sepXYZ1.outputs['Z'], nr1.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr12.inputs[0])
    ngroup.links.new(math1.outputs['Value'], nr2.inputs[0])
    ngroup.links.new(nr2.outputs[0], nr9.inputs[0])

    ngroup.links.new(grpIn2.outputs['_h PaletteMap Color'], manHSL.inputs['_h PaletteMap Color'])
    ngroup.links.new(grpIn2.outputs['_h PaletteMap Alpha'], manHSL.inputs['_h PaletteMap Alpha'])
    ngroup.links.new(grpIn2.outputs['Hue'], manHSL.inputs['Hue'])
    ngroup.links.new(grpIn2.outputs['Saturation'], manHSL.inputs['Saturation'])
    ngroup.links.new(grpIn2.outputs['Brightness'], manHSL.inputs['Brightness'])
    ngroup.links.new(grpIn2.outputs['Contrast'], manHSL.inputs['Contrast'])
    ngroup.links.new(manHSL.outputs['H'], nr3.inputs[0])
    ngroup.links.new(manHSL.outputs['S'], nr6.inputs[0])
    ngroup.links.new(manHSL.outputs['L'], math2.inputs[0])
    ngroup.links.new(nr3.outputs[0], nr4.inputs[0])
    ngroup.links.new(nr6.outputs[0], nr7.inputs[0])
    ngroup.links.new(math2.outputs['Value'], toRGB.inputs['L'])
    ngroup.links.new(nr4.outputs[0], nr5.inputs[0])
    ngroup.links.new(nr7.outputs[0], nr8.inputs[0])
    ngroup.links.new(nr8.outputs[0], toRGB.inputs['S'])
    ngroup.links.new(nr5.outputs[0], toRGB.inputs['H'])
    ngroup.links.new(grpIn3.outputs['_d DiffuseMap Color'], mixRGB1.inputs['Color1'])
    ngroup.links.new(toRGB.outputs['RGB'], mixRGB1.inputs['Color2'])
    ngroup.links.new(nr9.outputs[0], nr10.inputs[0])
    ngroup.links.new(nr9.outputs[0], nr11.inputs[0])
    ngroup.links.new(nr10.outputs[0], mixRGB1.inputs['Fac'])
    ngroup.links.new(mixRGB1.outputs['Color'], gamma1.inputs['Color'])
    ngroup.links.new(gamma1.outputs['Color'], nr17.inputs[0])
    ngroup.links.new(vMath1.outputs['Vector'], nr19.inputs[0])
    ngroup.links.new(nr17.outputs[0], nr24.inputs[0])
    ngroup.links.new(nr11.outputs[0], nr18.inputs[0])

    ngroup.links.new(grpIn4.outputs['_h PaletteMap Color'], manAO.inputs['_h PaletteMap Color'])
    ngroup.links.new(grpIn4.outputs['Brightness'], manAO.inputs['Brightness'])
    ngroup.links.new(manAO.outputs['AO'], math2.inputs[1])
    ngroup.links.new(nr12.outputs[0], nr13.inputs[0])
    ngroup.links.new(nr12.outputs[0], nr14.inputs[0])
    ngroup.links.new(nr13.outputs[0], math3.inputs[0])
    ngroup.links.new(nr13.outputs[0], nr25.inputs[0])
    ngroup.links.new(math3.outputs['Value'], math4.inputs[0])
    ngroup.links.new(math4.outputs['Value'], mixRGB2.inputs['Fac'])
    ngroup.links.new(mixRGB2.outputs['Color'], nr15.inputs[0])
    ngroup.links.new(nr14.outputs[0], math5.inputs[0])
    ngroup.links.new(nr15.outputs[0], nr16.inputs[0])
    ngroup.links.new(math5.outputs['Value'], vMath1.inputs[1])
    ngroup.links.new(math5.outputs['Value'], math6.inputs[0])
    ngroup.links.new(nr16.outputs[0], vMath1.inputs[0])
    ngroup.links.new(math6.outputs['Value'], vMath2.inputs[1])
    ngroup.links.new(vMath2.outputs['Vector'], vMath3.inputs[1])
    ngroup.links.new(nr18.outputs[0], nr22.inputs[0])
    ngroup.links.new(nr19.outputs[0], nr20.inputs[0])
    ngroup.links.new(nr20.outputs[0], nr21.inputs[0])
    ngroup.links.new(nr21.outputs[0], vMath3.inputs[0])
    ngroup.links.new(vMath3.outputs['Vector'], vMath4.inputs[0])
    ngroup.links.new(vMath4.outputs['Vector'], mixRGB3.inputs['Color2'])
    ngroup.links.new(nr22.outputs[0], nr23.inputs[0])
    ngroup.links.new(nr23.outputs[0], mixRGB3.inputs['Fac'])
    ngroup.links.new(mixRGB3.outputs['Color'], grpOut1.inputs['Specular Color'])
    ngroup.links.new(nr24.outputs[0], grpOut1.inputs['Diffuse Color'])

    ngroup.links.new(nr25.outputs[0], math7.inputs[0])
    ngroup.links.new(math7.outputs['Value'], nr26.inputs[0])
    ngroup.links.new(nr26.outputs[0], nr27.inputs[0])
    ngroup.links.new(grpIn5.outputs['Metallic Specular'], mixRGB2.inputs['Color2'])
    ngroup.links.new(grpIn5.outputs['Specular'], mixRGB4.inputs['Color1'])
    ngroup.links.new(nr27.outputs[0], nr28.inputs[0])
    ngroup.links.new(nr28.outputs[0], mixRGB4.inputs['Fac'])
    ngroup.links.new(mixRGB4.outputs['Color'], nr29.inputs[0])
    ngroup.links.new(nr29.outputs[0], nr30.inputs[0])
    ngroup.links.new(nr30.outputs[0], vMath2.inputs[0])
    ngroup.links.new(grpIn6.outputs['_s GlossMap Color'], nr31.inputs[0])
    ngroup.links.new(grpIn6.outputs['_s GlossMap Color'], sepXYZ2.inputs['Vector'])
    ngroup.links.new(nr31.outputs[0], nr32.inputs[0])
    ngroup.links.new(sepXYZ2.outputs['X'], vMath4.inputs[1])
    ngroup.links.new(nr32.outputs[0], mixRGB3.inputs['Color1'])

    return ngroup


def _hueSkinPixel():
    if 'HueSkinPixel' in bpy.data.node_groups:
        return bpy.data.node_groups['HueSkinPixel']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='HueSkinPixel', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='_d DiffuseMap Color')
    ngroup.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
    ngroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
    ngroup.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='Hue')
    ngroup.inputs.new(type='NodeSocketFloat', name='Saturation')
    ngroup.inputs.new(type='NodeSocketFloat', name='Brightness')
    ngroup.inputs.new(type='NodeSocketFloat', name='Contrast')
    ngroup.inputs.new(type='NodeSocketColor', name='Specular')
    ngroup.inputs.new(type='NodeSocketColor', name='Metallic Specular')
    ngroup.outputs.new(type='NodeSocketColor', name='Diffuse Color')
    ngroup.outputs.new(type='NodeSocketColor', name='Specular Color')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-1160.0, 460.0)
    for socket in grpIn1.outputs:
        if socket.name != '_m PaletteMaskMap Color':
            socket.hide = True

    sepXYZ1 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ1.location = (-940.0, 460.0)
    sepXYZ1.outputs['Z'].hide = True

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.location = (-720.0, 460.0)
    math1.operation = 'ADD'

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-1500.0, 260.0)
    for socket in grpIn2.outputs:
        if socket.name not in ['_h PaletteMap Color',
                               '_h PaletteMap Alpha',
                               'Hue',
                               'Saturation',
                               'Brightness',
                               'Contrast']:
            socket.hide = True

    manHSL = ngroup.nodes.new(type='ShaderNodeGroup')
    manHSL.location = (-1280.0, 260.0)
    manHSL.node_tree = _manipulateSkinHSL()
    manHSL.width = 260.0

    conHSL = ngroup.nodes.new(type='ShaderNodeGroup')
    conHSL.location = (-940.0, 260.0)
    conHSL.node_tree = _convertHSLToRGB()

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-720.0, 260.0)
    vMath1.operation = 'MULTIPLY'

    mixRGB1 = ngroup.nodes.new(type='ShaderNodeMixRGB')
    mixRGB1.location = (-500.0, 260.0)

    gamma1 = ngroup.nodes.new(type='ShaderNodeGamma')
    gamma1.inputs['Gamma'].default_value = 2.1
    gamma1.location = (-280.0, 260.0)

    sepXYZ2 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ2.location = (-940.0, 80.0)
    sepXYZ2.outputs['Y'].hide = True
    sepXYZ2.outputs['Z'].hide = True

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-720.0, 80.0)
    for socket in grpIn3.outputs:
        if socket.name != '_d DiffuseMap Color':
            socket.hide = True

    vMath2 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (420.0, 80.0)
    vMath2.operation = 'MULTIPLY'

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (-1160.0, -100.0)
    for socket in grpIn4.outputs:
        if socket.name != '_h PaletteMap Color':
            socket.hide = True

    grpIn5 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn5.location = (-940.0, -100.0)
    for socket in grpIn5.outputs:
        if socket.name != '_m PaletteMaskMap Color':
            socket.hide = True

    sepXYZ3 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ3.location = (-720.0, -100.0)
    sepXYZ3.outputs['X'].hide = True
    sepXYZ3.outputs['Y'].hide = True

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.inputs[1].default_value = 0.5
    math2.location = (-500.0, -100.0)
    math2.operation = 'SUBTRACT'

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.inputs[1].default_value = 2.0
    math3.location = (-280.0, -100.0)
    math3.operation = 'MULTIPLY'

    mixRGB2 = ngroup.nodes.new(type='ShaderNodeMixRGB')
    mixRGB2.inputs['Color1'].default_value = [1.0, 1.0, 1.0, 1.0]
    mixRGB2.location = (-60.0, -100.0)

    math4 = ngroup.nodes.new(type='ShaderNodeMath')
    math4.inputs[1].default_value = 0.5
    math4.location = (180.0, -100.0)
    math4.operation = 'GREATER_THAN'

    math5 = ngroup.nodes.new(type='ShaderNodeMath')
    math5.inputs[1].default_value = 1.0
    math5.location = (420.0, -100.0)
    math5.operation = 'LESS_THAN'

    vMath3 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (640.0, -100.0)
    vMath3.operation = 'MULTIPLY'

    vMath4 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (860.0, -100.0)
    vMath4.operation = 'ADD'

    vMath5 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath5.location = (1080.0, -100.0)
    vMath5.operation = 'MULTIPLY'

    mixRGB3 = ngroup.nodes.new(type='ShaderNodeMixRGB')
    mixRGB3.location = (1300.0, -100.0)

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1520.0, -100.0)

    math6 = ngroup.nodes.new(type='ShaderNodeMath')
    math6.inputs[1].default_value = 2.0
    math6.location = (-500.0, -320.0)
    math6.operation = 'MULTIPLY'

    grpIn6 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn6.location = (-280.0, -320.0)
    for socket in grpIn6.outputs:
        if socket.name != 'Metallic Specular':
            socket.hide = True

    grpIn7 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn7.location = (-280.0, -440.0)
    for socket in grpIn7.outputs:
        if socket.name != 'Specular':
            socket.hide = True

    mixRGB4 = ngroup.nodes.new(type='ShaderNodeMixRGB')
    mixRGB4.inputs['Color2'].default_value = [1.0, 1.0, 1.0, 1.0]
    mixRGB4.location = (-60.0, -320.0)

    grpIn8 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn8.location = (640.0, -320.0)
    for socket in grpIn8.outputs:
        if socket.name != '_s GlossMap Color':
            socket.hide = True

    sepXYZ4 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ4.location = (860.0, -320.0)
    sepXYZ4.outputs['Y'].hide = True
    sepXYZ4.outputs['Z'].hide = True

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (-540.0, 380.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (-540.0, 280.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (-540.0, 200.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (-100.0, 280.0)
    nr5 = ngroup.nodes.new(type='NodeReroute')
    nr5.location = (-100.0, 180.0)
    nr6 = ngroup.nodes.new(type='NodeReroute')
    nr6.location = (1280.0, 180.0)
    nr7 = ngroup.nodes.new(type='NodeReroute')
    nr7.location = (1280.0, -180.0)

    nr8 = ngroup.nodes.new(type='NodeReroute')
    nr8.location = (-60.0, 200.0)
    nr9 = ngroup.nodes.new(type='NodeReroute')
    nr9.location = (1300.0, 200.0)
    nr10 = ngroup.nodes.new(type='NodeReroute')
    nr10.location = (1300.0, -80.0)
    nr11 = ngroup.nodes.new(type='NodeReroute')
    nr11.location = (1440.0, -80.0)

    nr12 = ngroup.nodes.new(type='NodeReroute')
    nr12.location = (-540.0, -180.0)
    nr13 = ngroup.nodes.new(type='NodeReroute')
    nr13.location = (-540.0, -300.0)
    nr14 = ngroup.nodes.new(type='NodeReroute')
    nr14.location = (-540.0, -380.0)
    nr15 = ngroup.nodes.new(type='NodeReroute')
    nr15.location = (80.0, -300.0)

    nr16 = ngroup.nodes.new(type='NodeReroute')
    nr16.location = (180.0, -80.0)
    nr17 = ngroup.nodes.new(type='NodeReroute')
    nr17.location = (320.0, -80.0)

    nr18 = ngroup.nodes.new(type='NodeReroute')
    nr18.location = (700.0, -80.0)
    nr19 = ngroup.nodes.new(type='NodeReroute')
    nr19.location = (820.0, -80.0)
    nr20 = ngroup.nodes.new(type='NodeReroute')
    nr20.location = (820.0, -140.0)

    nr21 = ngroup.nodes.new(type='NodeReroute')
    nr21.location = (-280.0, -420.0)
    nr22 = ngroup.nodes.new(type='NodeReroute')
    nr22.location = (-140.0, -420.0)

    nr23 = ngroup.nodes.new(type='NodeReroute')
    nr23.location = (180.0, -300.0)
    nr24 = ngroup.nodes.new(type='NodeReroute')
    nr24.location = (520.0, -300.0)

    nr25 = ngroup.nodes.new(type='NodeReroute')
    nr25.location = (860.0, -300.0)
    nr26 = ngroup.nodes.new(type='NodeReroute')
    nr26.location = (1220.0, -300.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['_m PaletteMaskMap Color'], sepXYZ1.inputs['Vector'])
    ngroup.links.new(sepXYZ1.outputs['X'], math1.inputs[0])
    ngroup.links.new(sepXYZ1.outputs['Y'], math1.inputs[1])
    ngroup.links.new(math1.outputs['Value'], nr1.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(nr2.outputs[0], nr3.inputs[0])
    ngroup.links.new(nr2.outputs[0], nr4.inputs[0])
    ngroup.links.new(nr3.outputs[0], mixRGB1.inputs['Fac'])
    ngroup.links.new(nr4.outputs[0], nr5.inputs[0])
    ngroup.links.new(nr5.outputs[0], nr6.inputs[0])
    ngroup.links.new(nr6.outputs[0], nr7.inputs[0])
    ngroup.links.new(nr7.outputs[0], mixRGB3.inputs['Fac'])

    ngroup.links.new(grpIn2.outputs['_h PaletteMap Color'], manHSL.inputs['_h PaletteMap Color'])
    ngroup.links.new(grpIn2.outputs['_h PaletteMap Alpha'], manHSL.inputs['_h PaletteMap Alpha'])
    ngroup.links.new(grpIn2.outputs['Hue'], manHSL.inputs['Hue'])
    ngroup.links.new(grpIn2.outputs['Saturation'], manHSL.inputs['Saturation'])
    ngroup.links.new(grpIn2.outputs['Brightness'], manHSL.inputs['Brightness'])
    ngroup.links.new(grpIn2.outputs['Contrast'], manHSL.inputs['Contrast'])
    ngroup.links.new(manHSL.outputs['H'], conHSL.inputs['H'])
    ngroup.links.new(manHSL.outputs['S'], conHSL.inputs['S'])
    ngroup.links.new(manHSL.outputs['L'], conHSL.inputs['L'])
    ngroup.links.new(conHSL.outputs['RGB'], vMath1.inputs[0])
    ngroup.links.new(vMath1.outputs['Vector'], mixRGB1.inputs['Color2'])
    ngroup.links.new(mixRGB1.outputs['Color'], gamma1.inputs['Color'])
    ngroup.links.new(gamma1.outputs['Color'], nr8.inputs[0])
    ngroup.links.new(nr8.outputs[0], nr9.inputs[0])
    ngroup.links.new(nr9.outputs[0], nr10.inputs[0])
    ngroup.links.new(nr10.outputs[0], nr11.inputs[0])
    ngroup.links.new(nr11.outputs[0], grpOut1.inputs['Diffuse Color'])

    ngroup.links.new(sepXYZ2.outputs['X'], vMath1.inputs[1])
    ngroup.links.new(grpIn3.outputs['_d DiffuseMap Color'], mixRGB1.inputs['Color1'])
    ngroup.links.new(vMath2.outputs['Vector'], nr18.inputs[0])
    ngroup.links.new(nr18.outputs[0], nr19.inputs[0])
    ngroup.links.new(nr19.outputs[0], nr20.inputs[0])
    ngroup.links.new(nr20.outputs[0], vMath4.inputs[0])

    ngroup.links.new(grpIn4.outputs['_h PaletteMap Color'], sepXYZ2.inputs['Vector'])
    ngroup.links.new(grpIn5.outputs['_m PaletteMaskMap Color'], sepXYZ3.inputs['Vector'])
    ngroup.links.new(sepXYZ3.outputs['Z'], nr12.inputs[0])
    ngroup.links.new(nr12.outputs[0], nr13.inputs[0])
    ngroup.links.new(nr12.outputs[0], math2.inputs[0])
    ngroup.links.new(nr13.outputs[0], nr14.inputs[0])
    ngroup.links.new(nr13.outputs[0], nr15.inputs[0])
    ngroup.links.new(nr14.outputs[0], math6.inputs[0])
    ngroup.links.new(nr15.outputs[0], math4.inputs[0])
    ngroup.links.new(math2.outputs['Value'], math3.inputs[0])
    ngroup.links.new(math3.outputs['Value'], mixRGB2.inputs['Fac'])
    ngroup.links.new(mixRGB2.outputs['Color'], nr16.inputs[0])
    ngroup.links.new(nr16.outputs[0], nr17.inputs[0])
    ngroup.links.new(nr17.outputs[0], vMath2.inputs[0])
    ngroup.links.new(math4.outputs['Value'], vMath2.inputs[1])
    ngroup.links.new(math4.outputs['Value'], math5.inputs[0])
    ngroup.links.new(math5.outputs['Value'], vMath3.inputs[1])
    ngroup.links.new(vMath3.outputs['Vector'], vMath4.inputs[1])
    ngroup.links.new(vMath4.outputs['Vector'], vMath5.inputs[0])
    ngroup.links.new(vMath5.outputs['Vector'], mixRGB3.inputs['Color2'])
    ngroup.links.new(mixRGB3.outputs['Color'], grpOut1.inputs['Specular Color'])

    ngroup.links.new(math6.outputs['Value'], nr21.inputs[0])
    ngroup.links.new(nr21.outputs[0], nr22.inputs[0])
    ngroup.links.new(nr22.outputs[0], mixRGB4.inputs['Fac'])
    ngroup.links.new(grpIn6.outputs['Metallic Specular'], mixRGB2.inputs['Color2'])
    ngroup.links.new(grpIn7.outputs['Specular'], mixRGB4.inputs['Color1'])
    ngroup.links.new(mixRGB4.outputs['Color'], nr23.inputs[0])
    ngroup.links.new(nr23.outputs[0], nr24.inputs[0])
    ngroup.links.new(nr24.outputs[0], vMath3.inputs[0])
    ngroup.links.new(grpIn8.outputs['_s GlossMap Color'], nr25.inputs[0])
    ngroup.links.new(nr25.outputs[0], nr26.inputs[0])
    ngroup.links.new(nr26.outputs[0], mixRGB3.inputs['Color1'])
    ngroup.links.new(grpIn8.outputs['_s GlossMap Color'], sepXYZ4.inputs['Vector'])
    ngroup.links.new(sepXYZ4.outputs['X'], vMath5.inputs[1])

    return ngroup


def _negativeNormal():
    if 'NegativeNormal' in bpy.data.node_groups:
        return bpy.data.node_groups['NegativeNormal']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='NegativeNormal', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketVector', name='Normal')
    ngroup.outputs.new(type='NodeSocketVector', name='-Normal')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-720.0, 0.0)

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.inputs[1].default_value = [2.0, 2.0, 2.0]
    vMath1.location = (-480.0, 0.0)
    vMath1.operation = 'MULTIPLY'

    vMath2 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath2.inputs[1].default_value = [1.0, 1.0, 1.0]
    vMath2.location = (-240.0, 0.0)
    vMath2.operation = 'SUBTRACT'

    vMath3 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath3.inputs[1].default_value = [-1.0, -1.0, 1.0]
    vMath3.location = (0.0, 0.0)
    vMath3.operation = 'MULTIPLY'

    vMath4 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath4.inputs[1].default_value = [1.0, 1.0, 1.0]
    vMath4.location = (240.0, 0.0)
    vMath4.operation = 'ADD'

    vMath5 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath5.inputs[1].default_value = [2.0, 2.0, 2.0]
    vMath5.location = (480.0, 0.0)
    vMath5.operation = 'DIVIDE'

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (720.0, 0.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['Normal'], vMath1.inputs[0])
    ngroup.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    ngroup.links.new(vMath2.outputs['Vector'], vMath3.inputs[0])
    ngroup.links.new(vMath3.outputs['Vector'], vMath4.inputs[0])
    ngroup.links.new(vMath4.outputs['Vector'], vMath5.inputs[0])
    ngroup.links.new(vMath5.outputs['Vector'], grpOut1.inputs['-Normal'])

    return ngroup


def _manipulateAO():
    if 'ManipulateAO' in bpy.data.node_groups:
        return bpy.data.node_groups['ManipulateAO']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='ManipulateAO', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='Brightness')
    ngroup.outputs.new(type='NodeSocketFloat', name='AO')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-840.0, 120.0)
    grpIn1.outputs['_h PaletteMap Color'].hide = True

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-840.0, -60.0)
    grpIn2.outputs['Brightness'].hide = True

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.inputs[1].default_value = 1.0
    math1.location = (-620.0, 120.0)
    math1.operation = 'ADD'

    sepXYZ = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.location = (-620.0, -60.0)
    sepXYZ.outputs['Y'].hide = True
    sepXYZ.outputs['Z'].hide = True

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.inputs[0].default_value = 1.0
    math2.location = (-400.0, 120.0)
    math2.operation = 'SUBTRACT'

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.location = (-180.0, 120.0)
    math3.operation = 'MULTIPLY'

    math4 = ngroup.nodes.new(type='ShaderNodeMath')
    math4.location = (40.0, 120.0)
    math4.operation = 'ADD'

    math5 = ngroup.nodes.new(type='ShaderNodeMath')
    math5.location = (260.0, 120.0)
    math5.operation = 'MULTIPLY'

    clamp1 = ngroup.nodes.new(type='ShaderNodeClamp')
    clamp1.inputs['Min'].default_value = 0.0
    clamp1.inputs['Max'].default_value = 1.0
    clamp1.location = (480.0, 120.0)

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (700.0, 120.0)

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (-400.0, 140.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (-400.0, -60.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (-260.0, -60.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (20.0, 140.0)
    nr5 = ngroup.nodes.new(type='NodeReroute')
    nr5.location = (20.0, 40.0)
    nr6 = ngroup.nodes.new(type='NodeReroute')
    nr6.location = (180.0, -60.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['Brightness'], math1.inputs[0])
    ngroup.links.new(grpIn2.outputs['_h PaletteMap Color'], sepXYZ.inputs['Vector'])
    ngroup.links.new(math1.outputs['Value'], nr1.inputs[0])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[1])
    ngroup.links.new(sepXYZ.outputs['X'], nr2.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr4.inputs[0])
    ngroup.links.new(math2.outputs['Value'], math3.inputs[0])
    ngroup.links.new(nr2.outputs[0], nr3.inputs[0])
    ngroup.links.new(nr3.outputs[0], math3.inputs[1])
    ngroup.links.new(nr3.outputs[0], nr6.inputs[0])
    ngroup.links.new(math3.outputs['Value'], math4.inputs[1])
    ngroup.links.new(nr4.outputs[0], nr5.inputs[0])
    ngroup.links.new(nr5.outputs[0], math4.inputs[0])
    ngroup.links.new(math4.outputs['Value'], math5.inputs[1])
    ngroup.links.new(nr6.outputs[0], math5.inputs[0])
    ngroup.links.new(math5.outputs['Value'], clamp1.inputs['Value'])
    ngroup.links.new(clamp1.outputs['Result'], grpOut1.inputs['AO'])

    return ngroup


def _manipulateHSL():
    if 'ManipulateHSL' in bpy.data.node_groups:
        return bpy.data.node_groups['ManipulateHSL']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='ManipulateHSL', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
    ngroup.inputs.new(type='NodeSocketFloat', name='Hue')
    ngroup.inputs.new(type='NodeSocketFloat', name='Saturation')
    ngroup.inputs.new(type='NodeSocketFloat', name='Brightness')
    ngroup.inputs.new(type='NodeSocketFloat', name='Contrast')
    ngroup.outputs.new(type='NodeSocketFloat', name='H')
    ngroup.outputs.new(type='NodeSocketFloat', name='S')
    ngroup.outputs.new(type='NodeSocketFloat', name='L')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-400.0, 200.0)
    for socket in grpIn1.outputs:
        if socket.name not in ['_h PaletteMap Color', '_h PaletteMap Alpha']:
            socket.hide = True

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-180.0, 280.0)
    for socket in grpIn2.outputs:
        if socket.name != 'Hue':
            socket.hide = True

    expHSL = ngroup.nodes.new(type='ShaderNodeGroup')
    expHSL.location = (-180.0, 200.0)
    expHSL.name = 'ExpandHSL'
    expHSL.node_tree = _expandHSL()

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-180.0, 20.0)
    for socket in grpIn3.outputs:
        if socket.name != 'Saturation':
            socket.hide = True

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (-180.0, -120.0)
    for socket in grpIn4.outputs:
        if socket.name not in ['Brightness', 'Contrast']:
            socket.hide = True

    offHue = ngroup.nodes.new(type='ShaderNodeGroup')
    offHue.location = (40.0, 280.0)
    offHue.name = 'OffsetHue'
    offHue.node_tree = _offsetHue()

    offSat = ngroup.nodes.new(type='ShaderNodeGroup')
    offSat.location = (40.0, 20.0)
    offSat.name = 'OffsetSaturation'
    offSat.node_tree = _offsetSaturation()

    adjLig = ngroup.nodes.new(type='ShaderNodeGroup')
    adjLig.location = (40.0, -120.0)
    adjLig.name = 'AdjustLightness'
    adjLig.node_tree = _adjustLightness()

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (260.0, 280.0)

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (0.0, 80.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (0.0, -160.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (20.0, 80.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (20.0, -40.0)
    nr5 = ngroup.nodes.new(type='NodeReroute')
    nr5.location = (200.0, 160.0)
    nr6 = ngroup.nodes.new(type='NodeReroute')
    nr6.location = (200.0, 20.0)
    nr7 = ngroup.nodes.new(type='NodeReroute')
    nr7.location = (220.0, 160.0)
    nr8 = ngroup.nodes.new(type='NodeReroute')
    nr8.location = (220.0, -100.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['_h PaletteMap Color'], expHSL.inputs['_h PaletteMap Color'])
    ngroup.links.new(grpIn1.outputs['_h PaletteMap Alpha'], expHSL.inputs['_h PaletteMap Alpha'])
    ngroup.links.new(grpIn2.outputs['Hue'], offHue.inputs['Hue'])
    ngroup.links.new(expHSL.outputs['H'], offHue.inputs['H'])
    ngroup.links.new(expHSL.outputs['S'], nr3.inputs[0])
    ngroup.links.new(expHSL.outputs['L'], nr1.inputs[0])
    ngroup.links.new(grpIn3.outputs['Saturation'], offSat.inputs['Saturation'])
    ngroup.links.new(grpIn4.outputs['Brightness'], adjLig.inputs['Brightness'])
    ngroup.links.new(grpIn4.outputs['Contrast'], adjLig.inputs['Contrast'])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(nr2.outputs[0], adjLig.inputs['L'])
    ngroup.links.new(nr3.outputs[0], nr4.inputs[0])
    ngroup.links.new(nr4.outputs[0], offSat.inputs['S'])
    ngroup.links.new(offHue.outputs['H'], grpOut1.inputs['H'])
    ngroup.links.new(offSat.outputs['S'], nr6.inputs[0])
    ngroup.links.new(adjLig.outputs['L'], nr8.inputs[0])
    ngroup.links.new(nr5.outputs[0], grpOut1.inputs['S'])
    ngroup.links.new(nr6.outputs[0], nr5.inputs[0])
    ngroup.links.new(nr7.outputs[0], grpOut1.inputs['L'])
    ngroup.links.new(nr8.outputs[0], nr7.inputs[0])

    return ngroup


def _manipulateSkinHSL():
    if 'ManipulateSkinHSL' in bpy.data.node_groups:
        return bpy.data.node_groups['ManipulateSkinHSL']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='ManipulateSkinHSL', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
    ngroup.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
    ngroup.inputs.new(type='NodeSocketFloat', name='Hue')
    ngroup.inputs.new(type='NodeSocketFloat', name='Saturation')
    ngroup.inputs.new(type='NodeSocketFloat', name='Brightness')
    ngroup.inputs.new(type='NodeSocketFloat', name='Contrast')
    ngroup.outputs.new(type='NodeSocketFloat', name='H')
    ngroup.outputs.new(type='NodeSocketFloat', name='S')
    ngroup.outputs.new(type='NodeSocketFloat', name='L')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-400.0, 360.0)
    for socket in grpIn1.outputs:
        if socket.name != 'Hue':
            socket.hide = True

    math = ngroup.nodes.new(type='ShaderNodeMath')
    math.inputs[1].default_value = 0.5
    math.location = (-180.0, 360.0)
    math.operation = 'SUBTRACT'

    offHue = ngroup.nodes.new(type='ShaderNodeGroup')
    offHue.location = (40.0, 360.0)
    offHue.name = 'OffsetHue'
    offHue.node_tree = _offsetHue()

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (260.0, 360.0)

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-400.0, 200.0)
    for socket in grpIn2.outputs:
        if socket.name != '_h PaletteMap Color':
            socket.hide = True

    sepXYZ = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.location = (-180.0, 200.0)
    sepXYZ.outputs['X'].hide = True

    offSat = ngroup.nodes.new(type='ShaderNodeGroup')
    offSat.location = (40.0, 200.0)
    offSat.name = 'OffsetSkinSaturation'
    offSat.node_tree = _offsetSkinSaturation()

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-180.0, 100.0)
    for socket in grpIn3.outputs:
        if socket.name != 'Saturation':
            socket.hide = True

    grpIn4 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn4.location = (-180.0, 20.0)
    for socket in grpIn4.outputs:
        if socket.name not in ['_h PaletteMask Alpha', 'Brightness', 'Contrast']:
            socket.hide = True

    adjLit = ngroup.nodes.new(type='ShaderNodeGroup')
    adjLit.location = (40.0, 20.0)
    adjLit.name = 'AdjustLightness'
    adjLit.node_tree = _adjustLightness()

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (200.0, 200.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (200.0, 240.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (220.0, 40.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (220.0, 240.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['Hue'], math.inputs[0])
    ngroup.links.new(math.outputs['Value'], offHue.inputs['Hue'])
    ngroup.links.new(offHue.outputs['H'], grpOut1.inputs['H'])
    ngroup.links.new(grpIn2.outputs['_h PaletteMap Color'], sepXYZ.inputs['Vector'])
    ngroup.links.new(sepXYZ.outputs['Y'], offHue.inputs['H'])
    ngroup.links.new(sepXYZ.outputs['Z'], offSat.inputs['S'])
    ngroup.links.new(offSat.outputs['S'], nr1.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(nr2.outputs[0], grpOut1.inputs['S'])
    ngroup.links.new(grpIn3.outputs['Saturation'], offSat.inputs['Saturation'])
    ngroup.links.new(grpIn4.outputs['_h PaletteMap Alpha'], adjLit.inputs['L'])
    ngroup.links.new(grpIn4.outputs['Brightness'], adjLit.inputs['Brightness'])
    ngroup.links.new(grpIn4.outputs['Contrast'], adjLit.inputs['Contrast'])
    ngroup.links.new(adjLit.outputs['L'], nr3.inputs[0])
    ngroup.links.new(nr3.outputs[0], nr4.inputs[0])
    ngroup.links.new(nr4.outputs[0], grpOut1.inputs['L'])

    return ngroup


def _normalAndAlphaFromSwizzledTexture():
    if 'NormalAndAlphaFromSwizzledTexture' in bpy.data.node_groups:
        return bpy.data.node_groups['NormalAndAlphaFromSwizzledTexture']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(
        name='NormalAndAlphaFromSwizzledTexture',
        type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketColor', name='_n RotationMap Color')
    ngroup.inputs['_n RotationMap Color'].default_value = [0.0, 0.5, 0.0, 1.0]
    ngroup.inputs.new(type='NodeSocketFloat', name='_n RotationMap Alpha')
    ngroup.inputs['_n RotationMap Alpha'].default_value = 0.5
    ngroup.outputs.new(type='NodeSocketVector', name='Normal')
    ngroup.outputs.new(type='NodeSocketFloat', name='Alpha')
    ngroup.outputs.new(type='NodeSocketFloat', name='Emission Strength')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-1060.0, 200.0)

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.inputs[1].default_value = 2.0
    math1.location = (-840.0, 200.0)
    math1.operation = 'MULTIPLY'

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.inputs[1].default_value = 1.0
    math2.location = (-620.0, 200.0)
    math2.operation = 'SUBTRACT'

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.location = (-400.0, 200.0)
    math3.operation = 'MULTIPLY'

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (700.0, 200.0)

    math4 = ngroup.nodes.new(type='ShaderNodeMath')
    math4.inputs[0].default_value = 1.0
    math4.location = (920.0, 200.0)
    math4.operation = 'SUBTRACT'

    math5 = ngroup.nodes.new(type='ShaderNodeMath')
    math5.inputs[0].default_value = 1.0
    math5.location = (1140.0, 200.0)
    math5.operation = 'MINIMUM'

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1360.0, 200.0)

    grpIn3 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn3.location = (-1500.0, 0.0)

    vMath1 = ngroup.nodes.new(type='ShaderNodeVectorMath')
    vMath1.inputs[0].default_value = [1.0, 1.0, 1.0]
    vMath1.location = (-1280.0, 0.0)
    vMath1.operation = 'SUBTRACT'

    sepXYZ1 = ngroup.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ1.location = (-1060.0, 0.0)

    math6 = ngroup.nodes.new(type='ShaderNodeMath')
    math6.inputs[1].default_value = 2.0
    math6.location = (-840.0, 0.0)
    math6.operation = 'MULTIPLY'

    math7 = ngroup.nodes.new(type='ShaderNodeMath')
    math7.inputs[1].default_value = 1.0
    math7.location = (-620.0, 0.0)
    math7.operation = 'SUBTRACT'

    math8 = ngroup.nodes.new(type='ShaderNodeMath')
    math8.location = (-400.0, 0.0)
    math8.operation = 'MULTIPLY'

    math9 = ngroup.nodes.new(type='ShaderNodeMath')
    math9.location = (-180.0, 0.0)
    math9.operation = 'ADD'

    math10 = ngroup.nodes.new(type='ShaderNodeMath')
    math10.inputs[0].default_value = 1.0
    math10.location = (40.0, 0.0)
    math10.operation = 'SUBTRACT'

    math11 = ngroup.nodes.new(type='ShaderNodeMath')
    math11.location = (260.0, 0.0)
    math11.operation = 'SQRT'

    math12 = ngroup.nodes.new(type='ShaderNodeMath')
    math12.inputs[1].default_value = 1.0
    math12.location = (480.0, 0.0)
    math12.operation = 'ADD'

    math13 = ngroup.nodes.new(type='ShaderNodeMath')
    math13.inputs[1].default_value = 2.0
    math13.location = (700.0, 0.0)
    math13.operation = 'DIVIDE'

    comXYZ = ngroup.nodes.new(type='ShaderNodeCombineXYZ')
    comXYZ.location = (920.0, 0.0)

    math14 = ngroup.nodes.new(type='ShaderNodeMath')
    math14.inputs[0].default_value = 1.0
    math14.location = (1140.0, 0.0)
    math14.operation = 'SUBTRACT'

    # Add and place reroutes
    nr1 = ngroup.nodes.new(type='NodeReroute')
    nr1.location = (-840.0, 20.0)
    nr2 = ngroup.nodes.new(type='NodeReroute')
    nr2.location = (840.0, 20.0)
    nr3 = ngroup.nodes.new(type='NodeReroute')
    nr3.location = (-880.0, -100.0)
    nr4 = ngroup.nodes.new(type='NodeReroute')
    nr4.location = (-880.0, -180.0)
    nr5 = ngroup.nodes.new(type='NodeReroute')
    nr5.location = (820.0, -180.0)
    nr6 = ngroup.nodes.new(type='NodeReroute')
    nr6.location = (-900.0, -120.0)
    nr7 = ngroup.nodes.new(type='NodeReroute')
    nr7.location = (-900.0, -200.0)
    nr8 = ngroup.nodes.new(type='NodeReroute')
    nr8.location = (1000.0, -200.0)
    nr9 = ngroup.nodes.new(type='NodeReroute')
    nr9.location = (1120.0, 20.0)
    nr10 = ngroup.nodes.new(type='NodeReroute')
    nr10.location = (1340.0, 20.0)
    nr11 = ngroup.nodes.new(type='NodeReroute')
    nr11.location = (1340.0, 140.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['_n RotationMap Alpha'], math1.inputs[0])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[0])
    ngroup.links.new(math2.outputs['Value'], math3.inputs[0])
    ngroup.links.new(math2.outputs['Value'], math3.inputs[1])
    ngroup.links.new(math3.outputs['Value'], math9.inputs[0])
    ngroup.links.new(grpIn2.outputs['_n RotationMap Alpha'], comXYZ.inputs['X'])

    ngroup.links.new(grpIn3.outputs['_n RotationMap Color'], vMath1.inputs[1])
    ngroup.links.new(vMath1.outputs['Vector'], sepXYZ1.inputs['Vector'])
    ngroup.links.new(sepXYZ1.outputs['X'], nr1.inputs[0])
    ngroup.links.new(nr1.outputs[0], nr2.inputs[0])
    ngroup.links.new(nr2.outputs[0], math4.inputs[1])
    ngroup.links.new(math4.outputs['Value'], math5.inputs[1])
    ngroup.links.new(math5.outputs['Value'], grpOut1.inputs['Alpha'])

    ngroup.links.new(sepXYZ1.outputs['Y'], nr3.inputs[0])
    ngroup.links.new(nr3.outputs[0], math6.inputs[0])
    ngroup.links.new(math6.outputs['Value'], math7.inputs[0])
    ngroup.links.new(math7.outputs['Value'], math8.inputs[0])
    ngroup.links.new(math7.outputs['Value'], math8.inputs[1])
    ngroup.links.new(math8.outputs['Value'], math9.inputs[1])
    ngroup.links.new(math9.outputs['Value'], math10.inputs[1])
    ngroup.links.new(math10.outputs['Value'], math11.inputs[0])
    ngroup.links.new(math11.outputs['Value'], math12.inputs[0])
    ngroup.links.new(math12.outputs['Value'], math13.inputs[0])
    ngroup.links.new(math13.outputs['Value'], comXYZ.inputs['Z'])
    ngroup.links.new(nr3.outputs[0], nr4.inputs[0])
    ngroup.links.new(nr4.outputs[0], nr5.inputs[0])
    ngroup.links.new(nr5.outputs[0], comXYZ.inputs['Y'])

    ngroup.links.new(sepXYZ1.outputs['Z'], nr6.inputs[0])
    ngroup.links.new(nr6.outputs[0], nr7.inputs[0])
    ngroup.links.new(nr7.outputs[0], nr8.inputs[0])
    ngroup.links.new(nr8.outputs[0], math14.inputs[1])
    ngroup.links.new(math14.outputs['Value'], grpOut1.inputs['Emission Strength'])

    ngroup.links.new(comXYZ.outputs['Vector'], nr9.inputs[0])
    ngroup.links.new(nr9.outputs[0], nr10.inputs[0])
    ngroup.links.new(nr10.outputs[0], nr11.inputs[0])
    ngroup.links.new(nr11.outputs[0], grpOut1.inputs['Normal'])

    return ngroup


def _offsetHue():
    if 'OffsetHue' in bpy.data.node_groups:
        return bpy.data.node_groups['OffsetHue']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='OffsetHue', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketFloat', name='H')
    ngroup.inputs.new(type='NodeSocketFloat', name='Hue')
    ngroup.outputs.new(type='NodeSocketFloat', name='H')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-440.0, 80.0)

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.location = (-200.0, 80.0)
    math1.operation = 'ADD'

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.location = (40.0, 80.0)
    math2.operation = 'FRACT'
    math2.use_clamp = True

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (280.0, 80.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['H'], math1.inputs[0])
    ngroup.links.new(grpIn1.outputs['Hue'], math1.inputs[1])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[0])
    ngroup.links.new(math2.outputs['Value'], grpOut1.inputs['H'])

    return ngroup


def _offsetSaturation():
    if 'OffsetSaturation' in bpy.data.node_groups:
        return bpy.data.node_groups['OffsetSaturation']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='OffsetSaturation', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketFloat', name='S')
    ngroup.inputs.new(type='NodeSocketFloat', name='Saturation')
    ngroup.outputs.new(type='NodeSocketFloat', name='S')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-560.0, 180.0)

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-560.0, -20.0)
    grpIn2.outputs['S'].hide = True

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.location = (-320.0, 180.0)
    math1.operation = 'POWER'

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.inputs[0].default_value = 1.0
    math2.location = (-320.0, -20.0)
    math2.operation = 'SUBTRACT'

    math3 = ngroup.nodes.new(type='ShaderNodeMath')
    math3.location = (-80.0, 180.0)
    math3.operation = 'MULTIPLY'

    clamp1 = ngroup.nodes.new(type='ShaderNodeClamp')
    clamp1.inputs['Min'].default_value = 0.0
    clamp1.inputs['Max'].default_value = 1.0
    clamp1.location = (160.0, 180.0)

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (400.0, 180.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['S'], math1.inputs[0])
    ngroup.links.new(grpIn1.outputs['Saturation'], math1.inputs[1])
    ngroup.links.new(grpIn2.outputs['Saturation'], math2.inputs[1])
    ngroup.links.new(math1.outputs['Value'], math3.inputs[0])
    ngroup.links.new(math2.outputs['Value'], math3.inputs[1])
    ngroup.links.new(math3.outputs['Value'], clamp1.inputs['Value'])
    ngroup.links.new(clamp1.outputs['Result'], grpOut1.inputs['S'])

    return ngroup


def _offsetSkinSaturation():
    if 'OffsetSkinSaturation' in bpy.data.node_groups:
        return bpy.data.node_groups['OffsetSkinSaturation']

    # Make new node tree and add input/output sockets
    ngroup = bpy.data.node_groups.new(name='OffsetSkinSaturation', type='ShaderNodeTree')
    ngroup.inputs.new(type='NodeSocketFloat', name='S')
    ngroup.inputs.new(type='NodeSocketFloat', name='Saturation')
    ngroup.outputs.new(type='NodeSocketFloat', name='S')

    # Add and place nodes
    grpIn1 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn1.location = (-520.0, 40.0)
    grpIn1.outputs['S'].hide = True

    grpIn2 = ngroup.nodes.new(type='NodeGroupInput')
    grpIn2.location = (-300.0, 120.0)
    grpIn2.outputs['Saturation'].hide = True

    math1 = ngroup.nodes.new(type='ShaderNodeMath')
    math1.inputs[0].default_value = 0.5
    math1.location = (-300.0, 40.0)
    math1.operation = 'SUBTRACT'

    math2 = ngroup.nodes.new(type='ShaderNodeMath')
    math2.location = (-80.0, 40.0)
    math2.operation = 'ADD'

    clamp1 = ngroup.nodes.new(type='ShaderNodeClamp')
    clamp1.inputs['Min'].default_value = 0.0
    clamp1.inputs['Max'].default_value = 1.0
    clamp1.location = (140.0, 40.0)

    grpOut1 = ngroup.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (360.0, 40.0)

    # Link nodes together
    ngroup.links.new(grpIn1.outputs['Saturation'], math1.inputs[1])
    ngroup.links.new(grpIn2.outputs['S'], math2.inputs[0])
    ngroup.links.new(math1.outputs['Value'], math2.inputs[1])
    ngroup.links.new(math2.outputs['Value'], clamp1.inputs['Value'])
    ngroup.links.new(clamp1.outputs['Result'], grpOut1.inputs['S'])

    return ngroup


# ========================================= Shader Trees ==========================================


def Creature(ntree: ShaderNodeTree):
    # Add output socket to node tree
    if len(ntree.outputs) < 1:
        ntree.outputs.new(type='NodeSocketShader', name='Shader')

    # Add and place nodes
    diffuseMap = ntree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.label = "_d DiffuseMap"
    diffuseMap.location = (-460.0, 580.0)
    diffuseMap.name = '_d'

    gamma1 = ntree.nodes.new(type='ShaderNodeGamma')
    gamma1.inputs['Gamma'].default_value = 2.1
    gamma1.location = (-120.0, 580.0)

    math1 = ntree.nodes.new(type='ShaderNodeMath')
    math1.inputs[1].default_value = 0.5
    math1.location = (-120.0, 460.0)
    math1.operation = 'GREATER_THAN'

    math2 = ntree.nodes.new(type='ShaderNodeMath')
    math2.location = (120.0, 460.0)
    math2.operation = 'MULTIPLY'

    math3 = ntree.nodes.new(type='ShaderNodeMath')
    math3.inputs[1].default_value = 0.5
    math3.location = (360.0, 460.0)
    math3.operation = 'SUBTRACT'
    math3.use_clamp = True

    math4 = ntree.nodes.new(type='ShaderNodeMath')
    math4.inputs[1].default_value = 2.0
    math4.location = (600.0, 460.0)
    math4.operation = 'MULTIPLY'

    rotationMap = ntree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.label = "_n RotationMap"
    rotationMap.location = (-1900.0, 260.0)
    rotationMap.name = '_n'

    tangentN = ntree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-1560.0, 260.0)
    tangentN.name = "tangentN"
    tangentN.node_tree = _normalAndAlphaFromSwizzledTexture()
    tangentN.width = 400.0

    norMap = ntree.nodes.new(type='ShaderNodeNormalMap')
    norMap.location = (-1060.0, 260.0)

    specLookup = ntree.nodes.new(type='ShaderNodeGroup')
    specLookup.location = (-800.0, 260.0)
    specLookup.name = "hair"
    specLookup.node_tree = _getSpecularLookup()
    specLookup.width = 240

    directionMap = ntree.nodes.new(type='ShaderNodeTexImage')
    directionMap.label = "DirectionMap"
    directionMap.location = (-460.0, 260.0)
    directionMap.name = 'directionMap'

    vMath1 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-120.0, 260.0)
    vMath1.operation = 'MULTIPLY'

    mix1 = ntree.nodes.new(type='ShaderNodeMixRGB')
    mix1.location = (120.0, 260.0)

    vMath2 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (360.0, 260.0)
    vMath2.operation = 'ADD'

    vMath3 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (600.0, 260.0)
    vMath3.operation = 'ADD'

    diffuseBSDF = ntree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuseBSDF.inputs['Roughness'].default_value = 0.0
    diffuseBSDF.location = (840.0, 260.0)

    mixShader1 = ntree.nodes.new(type='ShaderNodeMixShader')
    mixShader1.location = (1100.0, 260.0)

    addShader = ntree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (1340.0, 260.0)

    mixShader2 = ntree.nodes.new(type='ShaderNodeMixShader')
    mixShader2.location = (1580.0, 260.0)

    grpOut1 = ntree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1820.0, 260.0)

    glossMap = ntree.nodes.new(type='ShaderNodeTexImage')
    glossMap.label = "_s GlossMap"
    glossMap.location = (-800.0, -80.0)
    glossMap.name = '_s'

    paletteMask = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMask.label = "_m PaletteMaskMap"
    paletteMask.location = (-800.0, -360.0)
    paletteMask.name = '_m'

    phongSpec = ntree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (-460.0, -80.0)
    phongSpec.name = "GetPhongSpecular"
    phongSpec.node_tree = _getPhongSpecular()
    phongSpec.width = 220

    sepXYZ = ntree.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.location = (-120.0, -80.0)

    flushColor = ntree.nodes.new(type='ShaderNodeGroup')
    flushColor.location = (-180.0, -360.0)
    flushColor.name = "GetFlushColor"
    flushColor.node_tree = _getFlushColor()
    flushColor.width = 200

    vMath4 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (120.0, -80.0)
    vMath4.operation = 'MULTIPLY'

    glossyBSDF = ntree.nodes.new(type='ShaderNodeBsdfGlossy')
    glossyBSDF.distribution = 'BECKMANN'
    glossyBSDF.inputs['Roughness'].default_value = 0.5
    glossyBSDF.location = (840.0, -80.0)

    emission = ntree.nodes.new(type='ShaderNodeEmission')
    emission.location = (1100.0, -80.0)

    transparentBSDF = ntree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentBSDF.location = (1340.0, -80.0)

    # Add and place reroutes
    nr1 = ntree.nodes.new(type='NodeReroute')
    nr1.location = (-120.0, 600.0)
    nr2 = ntree.nodes.new(type='NodeReroute')
    nr2.location = (80.0, 600.0)
    nr3 = ntree.nodes.new(type='NodeReroute')
    nr3.location = (80.0, 400.0)
    nr4 = ntree.nodes.new(type='NodeReroute')
    nr4.location = (60.0, 500.0)
    nr5 = ntree.nodes.new(type='NodeReroute')
    nr5.location = (60.0, 280.0)
    nr6 = ntree.nodes.new(type='NodeReroute')
    nr6.location = (240.0, 280.0)
    nr7 = ntree.nodes.new(type='NodeReroute')
    nr7.location = (-200.0, 280.0)
    nr8 = ntree.nodes.new(type='NodeReroute')
    nr8.location = (-200.0, -420.0)
    nr9 = ntree.nodes.new(type='NodeReroute')
    nr9.location = (780.0, 380.0)
    nr10 = ntree.nodes.new(type='NodeReroute')
    nr10.location = (780.0, 280.0)
    nr11 = ntree.nodes.new(type='NodeReroute')
    nr11.location = (980.0, 280.0)

    nr12 = ntree.nodes.new(type='NodeReroute')
    nr12.location = (-1120.0, 160.0)
    nr13 = ntree.nodes.new(type='NodeReroute')
    nr13.location = (-1120.0, 0.0)
    nr14 = ntree.nodes.new(type='NodeReroute')
    nr14.location = (640.0, 0.0)
    nr15 = ntree.nodes.new(type='NodeReroute')
    nr15.location = (840.0, 40.0)
    nr16 = ntree.nodes.new(type='NodeReroute')
    nr16.location = (1400.0, 40.0)
    nr17 = ntree.nodes.new(type='NodeReroute')
    nr17.location = (-1140.0, 160.0)
    nr18 = ntree.nodes.new(type='NodeReroute')
    nr18.location = (-1140.0, -40.0)
    nr19 = ntree.nodes.new(type='NodeReroute')
    nr19.location = (640.0, -40.0)
    nr20 = ntree.nodes.new(type='NodeReroute')
    nr20.location = (840.0, -60.0)
    nr21 = ntree.nodes.new(type='NodeReroute')
    nr21.location = (980.0, -60.0)
    nr22 = ntree.nodes.new(type='NodeReroute')
    nr22.location = (-880.0, 180.0)
    nr23 = ntree.nodes.new(type='NodeReroute')
    nr23.location = (-880.0, -20.0)
    nr24 = ntree.nodes.new(type='NodeReroute')
    nr24.location = (-500.0, -20.0)
    nr25 = ntree.nodes.new(type='NodeReroute')
    nr25.location = (-500.0, -160.0)
    nr26 = ntree.nodes.new(type='NodeReroute')
    nr26.location = (-220.0, -20.0)
    nr27 = ntree.nodes.new(type='NodeReroute')
    nr27.location = (-220.0, -460.0)
    nr28 = ntree.nodes.new(type='NodeReroute')
    nr28.location = (640.0, -20.0)
    nr29 = ntree.nodes.new(type='NodeReroute')
    nr29.location = (800.0, 160.0)
    nr30 = ntree.nodes.new(type='NodeReroute')
    nr30.location = (800.0, -40.0)
    nr31 = ntree.nodes.new(type='NodeReroute')
    nr31.location = (980.0, -40.0)
    nr32 = ntree.nodes.new(type='NodeReroute')
    nr32.location = (800.0, -120.0)

    nr33 = ntree.nodes.new(type='NodeReroute')
    nr33.location = (-460.0, -60.0)
    nr34 = ntree.nodes.new(type='NodeReroute')
    nr34.location = (-180.0, -60.0)
    nr35 = ntree.nodes.new(type='NodeReroute')
    nr35.location = (-180.0, 80.0)
    nr36 = ntree.nodes.new(type='NodeReroute')
    nr36.location = (-460.0, -300.0)
    nr37 = ntree.nodes.new(type='NodeReroute')
    nr37.location = (-260.0, -300.0)
    nr38 = ntree.nodes.new(type='NodeReroute')
    nr38.location = (-120.0, -60.0)
    nr39 = ntree.nodes.new(type='NodeReroute')
    nr39.location = (80.0, -60.0)
    nr40 = ntree.nodes.new(type='NodeReroute')
    nr40.location = (80.0, 60.0)
    nr41 = ntree.nodes.new(type='NodeReroute')
    nr41.location = (60.0, -80.0)
    nr42 = ntree.nodes.new(type='NodeReroute')
    nr42.location = (60.0, 80.0)

    # Link nodes together
    ntree.links.new(diffuseMap.outputs['Color'], gamma1.inputs['Color'])
    ntree.links.new(diffuseMap.outputs['Alpha'], nr1.inputs[0])
    ntree.links.new(diffuseMap.outputs['Alpha'], math1.inputs[0])
    ntree.links.new(nr1.outputs[0], nr2.inputs[0])
    ntree.links.new(gamma1.outputs['Color'], nr4.inputs[0])
    ntree.links.new(math1.outputs['Value'], math2.inputs[1])
    ntree.links.new(nr4.outputs[0], nr5.inputs[0])
    ntree.links.new(nr2.outputs[0], nr3.inputs[0])
    ntree.links.new(nr3.outputs[0], math2.inputs[0])
    ntree.links.new(math2.outputs['Value'], math3.inputs[0])
    ntree.links.new(math3.outputs['Value'], math4.inputs[0])
    ntree.links.new(math4.outputs['Value'], nr9.inputs[0])
    ntree.links.new(nr9.outputs[0], nr10.inputs[0])
    ntree.links.new(nr10.outputs[0], nr11.inputs[0])
    ntree.links.new(nr11.outputs[0], mixShader1.inputs['Fac'])

    ntree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    ntree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    ntree.links.new(tangentN.outputs['Normal'], norMap.inputs['Color'])
    ntree.links.new(tangentN.outputs['Alpha'], nr12.inputs[0])
    ntree.links.new(tangentN.outputs['Emission Strength'], nr17.inputs[0])
    ntree.links.new(nr12.outputs[0], nr13.inputs[0])
    ntree.links.new(nr17.outputs[0], nr18.inputs[0])
    ntree.links.new(nr13.outputs[0], nr14.inputs[0])
    ntree.links.new(nr18.outputs[0], nr19.inputs[0])
    ntree.links.new(norMap.outputs['Normal'], specLookup.inputs['Normal'])
    ntree.links.new(norMap.outputs['Normal'], nr22.inputs[0])
    ntree.links.new(nr22.outputs[0], nr23.inputs[0])
    ntree.links.new(nr23.outputs[0], nr24.inputs[0])
    ntree.links.new(specLookup.outputs['Vector'], directionMap.inputs['Vector'])
    ntree.links.new(nr24.outputs[0], nr25.inputs[0])
    ntree.links.new(nr24.outputs[0], nr26.inputs[0])
    ntree.links.new(directionMap.outputs['Color'], vMath1.inputs[0])
    ntree.links.new(nr26.outputs[0], nr27.inputs[0])
    ntree.links.new(nr26.outputs[0], nr28.inputs[0])
    ntree.links.new(nr7.outputs[0], nr8.inputs[0])
    ntree.links.new(nr35.outputs[0], vMath1.inputs[1])
    ntree.links.new(vMath1.outputs['Vector'], mix1.inputs['Color2'])
    ntree.links.new(nr5.outputs[0], nr7.inputs[0])
    ntree.links.new(nr5.outputs[0], nr6.inputs[0])
    ntree.links.new(nr42.outputs[0], mix1.inputs['Fac'])
    ntree.links.new(nr40.outputs[0], mix1.inputs['Color1'])
    ntree.links.new(nr6.outputs[0], vMath2.inputs[0])
    ntree.links.new(mix1.outputs['Color'], vMath2.inputs[1])
    ntree.links.new(vMath2.outputs['Vector'], vMath3.inputs[0])
    ntree.links.new(vMath3.outputs['Vector'], nr29.inputs[0])
    ntree.links.new(nr14.outputs[0], nr15.inputs[0])
    ntree.links.new(nr28.outputs[0], diffuseBSDF.inputs['Normal'])
    ntree.links.new(nr28.outputs[0], glossyBSDF.inputs['Normal'])
    ntree.links.new(nr19.outputs[0], nr20.inputs[0])
    ntree.links.new(nr29.outputs[0], diffuseBSDF.inputs['Color'])
    ntree.links.new(nr29.outputs[0], nr30.inputs[0])
    ntree.links.new(nr30.outputs[0], nr31.inputs[0])
    ntree.links.new(nr30.outputs[0], nr32.inputs[0])
    ntree.links.new(nr32.outputs[0], glossyBSDF.inputs['Color'])
    ntree.links.new(diffuseBSDF.outputs['BSDF'], mixShader1.inputs[1])
    ntree.links.new(nr15.outputs[0], nr16.inputs[0])
    ntree.links.new(nr20.outputs[0], nr21.inputs[0])
    ntree.links.new(nr31.outputs[0], emission.inputs['Color'])
    ntree.links.new(nr21.outputs[0], emission.inputs['Strength'])
    ntree.links.new(mixShader1.outputs['Shader'], addShader.inputs[0])
    ntree.links.new(addShader.outputs['Shader'], mixShader2.inputs[1])
    ntree.links.new(nr16.outputs[0], mixShader2.inputs['Fac'])
    ntree.links.new(mixShader2.outputs['Shader'], grpOut1.inputs['Shader'])

    ntree.links.new(glossMap.outputs['Color'], nr33.inputs[0])
    ntree.links.new(glossMap.outputs['Color'], phongSpec.inputs['Specular Color'])
    ntree.links.new(glossMap.outputs['Alpha'], phongSpec.inputs['Specular Alpha'])
    ntree.links.new(paletteMask.outputs['Color'], nr36.inputs[0])
    ntree.links.new(nr25.outputs[0], phongSpec.inputs['Normal'])
    ntree.links.new(nr25.outputs[0], phongSpec.inputs['-Normal'])
    ntree.links.new(nr33.outputs[0], nr34.inputs[0])
    ntree.links.new(phongSpec.outputs['Specular'], nr38.inputs[0])
    ntree.links.new(nr36.outputs[0], nr37.inputs[0])
    ntree.links.new(nr37.outputs[0], sepXYZ.inputs['Vector'])
    ntree.links.new(nr27.outputs[0], flushColor.inputs['Normal'])
    ntree.links.new(nr8.outputs[0], flushColor.inputs['Diffuse Color'])
    ntree.links.new(nr34.outputs[0], nr35.inputs[0])
    ntree.links.new(flushColor.outputs['Flush Color'], vMath4.inputs[1])
    ntree.links.new(nr38.outputs[0], nr39.inputs[0])
    ntree.links.new(sepXYZ.outputs['Y'], vMath4.inputs[0])
    ntree.links.new(sepXYZ.outputs['Z'], nr41.inputs[0])
    ntree.links.new(nr41.outputs[0], nr42.inputs[0])
    ntree.links.new(nr39.outputs[0], nr40.inputs[0])
    ntree.links.new(vMath4.outputs['Vector'], vMath3.inputs[1])
    ntree.links.new(glossyBSDF.outputs['BSDF'], mixShader1.inputs[2])
    ntree.links.new(emission.outputs['Emission'], addShader.inputs[1])
    ntree.links.new(transparentBSDF.outputs['BSDF'], mixShader2.inputs[2])

    # Hide unlinked node sockets
    for node in ntree.nodes:
        if node.select:
            for socket in node.inputs:
                socket.hide = True
            for socket in node.outputs:
                socket.hide = True

    # Unhide select unlinked node sockets
    gamma1.inputs[1].hide = False
    math1.inputs[1].hide = False
    math3.inputs[1].hide = False
    math4.inputs[1].hide = False
    norMap.inputs['Strength'].hide = False
    phongSpec.inputs['MaxSpecPower'].hide = False
    transparentBSDF.inputs['Color'].hide = False
    flushColor.inputs['Flesh Brightness'].hide = False
    flushColor.inputs['Flush Tone'].hide = False


def Eye(ntree: ShaderNodeTree):
    # Add output socket to node tree
    if len(ntree.outputs) < 1:
        ntree.outputs.new(type='NodeSocketShader', name='Shader')

    # Add and place nodes
    diffuseMap = ntree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.inputs['Vector'].hide = True
    diffuseMap.label = '_d DiffuseMap'
    diffuseMap.location = (-1780.0, 300.0)
    diffuseMap.name = '_d'
    diffuseMap.outputs['Alpha'].hide = True

    paletteMaskMap = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMaskMap.inputs['Vector'].hide = True
    paletteMaskMap.label = '_m PaletteMaskMap'
    paletteMaskMap.location = (-1440.0, 300.0)
    paletteMaskMap.name = '_m'
    paletteMaskMap.outputs['Alpha'].hide = True

    paletteMap = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMap.inputs['Vector'].hide = True
    paletteMap.label = '_h PaletteMap'
    paletteMap.location = (-1100.0, 300.0)
    paletteMap.name = '_h'

    huePixel = ntree.nodes.new(type='ShaderNodeGroup')
    huePixel.location = (-760.0, 300.0)
    huePixel.name = 'HuePixel'
    huePixel.node_tree = _huePixel()
    huePixel.width = 180.0

    vMath1 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.inputs[1].default_value = [1.2, 1.2, 1.2]
    vMath1.location = (-480.0, 300.0)
    vMath1.operation = 'MULTIPLY'

    vMath2 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (-240.0, 300.0)
    vMath2.operation = 'MULTIPLY'

    phongSpec = ntree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (0.0, 300.0)
    phongSpec.node_tree = _getPhongSpecular()
    phongSpec.inputs['MaxSpecPower'].default_value = 8.0
    phongSpec.width = 180.0

    vMath3 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (280.0, 300.0)
    vMath3.operation = 'ADD'

    principled = ntree.nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Clearcoat'].default_value = 1.0
    principled.inputs['IOR'].default_value = 1.41
    principled.inputs['Roughness'].default_value = 1.0
    principled.inputs['Specular'].default_value = 0.0
    principled.location = (520.0, 300.0)
    for socket in principled.inputs:
        if socket.name not in ['Base Color', 'Clearcoat', 'IOR', 'Normal', 'Clearcoat Normal']:
            socket.hide = True

    addShader = ntree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (860.0, 300.0)

    mixShader1 = ntree.nodes.new(type='ShaderNodeMixShader')
    mixShader1.location = (1100.0, 300.0)

    grpOut1 = ntree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1340.0, 300.0)

    glossMap = ntree.nodes.new(type='ShaderNodeTexImage')
    glossMap.inputs['Vector'].hide = True
    glossMap.label = '_s GlossMap'
    glossMap.location = (-1780.0, -100.0)
    glossMap.name = '_s'

    rotationMap = ntree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.inputs['Vector'].hide = True
    rotationMap.label = '_n RotationMap'
    rotationMap.location = (-1440.0, -100.0)
    rotationMap.name = '_n'

    tangentN = ntree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-1100.0, -100.0)
    tangentN.node_tree = _normalAndAlphaFromSwizzledTexture()
    tangentN.width = 240.0

    negativeN = ntree.nodes.new(type='ShaderNodeGroup')
    negativeN.location = (-760.0, -100.0)
    negativeN.node_tree = _negativeNormal()
    negativeN.width = 180.0

    negN = ntree.nodes.new(type='ShaderNodeNormalMap')
    negN.location = (-480.0, 60.0)
    negN.width = 140.0

    N = ntree.nodes.new(type='ShaderNodeNormalMap')
    N.location = (-240.0, 60.0)
    N.width = 140.0

    emissionShader = ntree.nodes.new(type='ShaderNodeEmission')
    emissionShader.location = (520.0, 40.0)
    emissionShader.width = 240.0

    transparentBSDF = ntree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentBSDF.location = (860.0, 40.0)

    # Add and place reroutes
    nr1 = ntree.nodes.new(type='NodeReroute')
    nr1.location = (-1440.0, 320.0)
    nr2 = ntree.nodes.new(type='NodeReroute')
    nr2.location = (-780.0, 320.0)
    nr3 = ntree.nodes.new(type='NodeReroute')
    nr3.location = (-780.0, 220.0)
    nr4 = ntree.nodes.new(type='NodeReroute')
    nr4.location = (-1160.0, 220.0)
    nr5 = ntree.nodes.new(type='NodeReroute')
    nr5.location = (-1160.0, 20.0)
    nr6 = ntree.nodes.new(type='NodeReroute')
    nr6.location = (-860.0, 20.0)
    nr7 = ntree.nodes.new(type='NodeReroute')
    nr7.location = (-540.0, 220.0)
    nr8 = ntree.nodes.new(type='NodeReroute')
    nr8.location = (-540.0, 80.0)
    nr9 = ntree.nodes.new(type='NodeReroute')
    nr9.location = (240.0, 80.0)
    nr10 = ntree.nodes.new(type='NodeReroute')
    nr10.location = (240.0, 160.0)
    nr11 = ntree.nodes.new(type='NodeReroute')
    nr11.location = (-480.0, 320.0)
    nr12 = ntree.nodes.new(type='NodeReroute')
    nr12.location = (-280.0, 320.0)
    nr13 = ntree.nodes.new(type='NodeReroute')
    nr13.location = (-280.0, 240.0)
    nr14 = ntree.nodes.new(type='NodeReroute')
    nr14.location = (-240.0, 120.0)
    nr15 = ntree.nodes.new(type='NodeReroute')
    nr15.location = (-100.0, 120.0)
    nr16 = ntree.nodes.new(type='NodeReroute')
    nr16.location = (-40.0, 60.0)
    nr17 = ntree.nodes.new(type='NodeReroute')
    nr17.location = (-40.0, 120.0)
    nr18 = ntree.nodes.new(type='NodeReroute')
    nr18.location = (420.0, 60.0)
    nr19 = ntree.nodes.new(type='NodeReroute')
    nr19.location = (460.0, 220.0)
    nr20 = ntree.nodes.new(type='NodeReroute')
    nr20.location = (460.0, 120.0)
    nr21 = ntree.nodes.new(type='NodeReroute')
    nr21.location = (460.0, 40.0)

    nr22 = ntree.nodes.new(type='NodeReroute')
    nr22.location = (-1440.0, -60.0)
    nr23 = ntree.nodes.new(type='NodeReroute')
    nr23.location = (-800.0, -60.0)
    nr24 = ntree.nodes.new(type='NodeReroute')
    nr24.location = (-800.0, 120.0)
    nr25 = ntree.nodes.new(type='NodeReroute')
    nr25.location = (-1440.0, -80.0)
    nr26 = ntree.nodes.new(type='NodeReroute')
    nr26.location = (-820.0, -80.0)
    nr27 = ntree.nodes.new(type='NodeReroute')
    nr27.location = (-820.0, 340.0)
    nr28 = ntree.nodes.new(type='NodeReroute')
    nr28.location = (-40.0, 340.0)
    nr29 = ntree.nodes.new(type='NodeReroute')
    nr29.location = (-40.0, 240.0)
    nr30 = ntree.nodes.new(type='NodeReroute')
    nr30.location = (-760.0, -220.0)
    nr31 = ntree.nodes.new(type='NodeReroute')
    nr31.location = (-480.0, -220.0)
    nr32 = ntree.nodes.new(type='NodeReroute')
    nr32.location = (-760.0, -240.0)
    nr33 = ntree.nodes.new(type='NodeReroute')
    nr33.location = (-100.0, -240.0)
    nr34 = ntree.nodes.new(type='NodeReroute')
    nr34.location = (520.0, 60.0)
    nr35 = ntree.nodes.new(type='NodeReroute')
    nr35.location = (860.0, 60.0)
    nr36 = ntree.nodes.new(type='NodeReroute')
    nr36.location = (-760.0, -260.0)
    nr37 = ntree.nodes.new(type='NodeReroute')
    nr37.location = (-100.0, -260.0)

    # Link nodes together
    ntree.links.new(diffuseMap.outputs['Color'], nr1.inputs[0])
    ntree.links.new(nr1.outputs[0], nr2.inputs[0])
    ntree.links.new(nr2.outputs[0], nr3.inputs[0])
    ntree.links.new(nr3.outputs[0], huePixel.inputs['_d DiffuseMap Color'])
    ntree.links.new(paletteMaskMap.outputs['Color'], nr4.inputs[0])
    ntree.links.new(nr4.outputs[0], nr5.inputs[0])
    ntree.links.new(nr5.outputs[0], nr6.inputs[0])
    ntree.links.new(nr6.outputs[0], huePixel.inputs['_m PaletteMaskMap Color'])
    ntree.links.new(paletteMap.outputs['Color'], huePixel.inputs['_h PaletteMap Color'])
    ntree.links.new(paletteMap.outputs['Alpha'], huePixel.inputs['_h PaletteMap Alpha'])
    ntree.links.new(huePixel.outputs['Diffuse Color'], vMath1.inputs[0])
    ntree.links.new(huePixel.outputs['Diffuse Color'], nr7.inputs[0])
    ntree.links.new(nr7.outputs[0], nr8.inputs[0])
    ntree.links.new(nr8.outputs[0], nr9.inputs[0])
    ntree.links.new(nr9.outputs[0], nr10.inputs[0])
    ntree.links.new(nr10.outputs[0], vMath3.inputs[0])
    ntree.links.new(huePixel.outputs['Specular Color'], nr11.inputs[0])
    ntree.links.new(nr11.outputs[0], nr12.inputs[0])
    ntree.links.new(nr12.outputs[0], nr13.inputs[0])
    ntree.links.new(nr13.outputs[0], vMath2.inputs[1])
    ntree.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    ntree.links.new(vMath2.outputs['Vector'], phongSpec.inputs['Specular Color'])
    ntree.links.new(phongSpec.outputs['Specular'], vMath3.inputs[1])
    ntree.links.new(vMath3.outputs['Vector'], nr19.inputs[0])
    ntree.links.new(nr19.outputs[0], nr20.inputs[0])
    ntree.links.new(nr20.outputs[0], principled.inputs['Base Color'])
    ntree.links.new(nr20.outputs[0], nr21.inputs[0])
    ntree.links.new(nr21.outputs[0], emissionShader.inputs['Color'])
    ntree.links.new(principled.outputs['BSDF'], addShader.inputs[0])
    ntree.links.new(addShader.outputs['Shader'], mixShader1.inputs[1])
    ntree.links.new(mixShader1.outputs['Shader'], grpOut1.inputs['Shader'])

    ntree.links.new(glossMap.outputs['Color'], nr22.inputs[0])
    ntree.links.new(nr22.outputs[0], nr23.inputs[0])
    ntree.links.new(nr23.outputs[0], nr24.inputs[0])
    ntree.links.new(nr24.outputs[0], huePixel.inputs['_s GlossMap Color'])
    ntree.links.new(glossMap.outputs['Alpha'], nr25.inputs[0])
    ntree.links.new(nr25.outputs[0], nr26.inputs[0])
    ntree.links.new(nr26.outputs[0], nr27.inputs[0])
    ntree.links.new(nr27.outputs[0], nr28.inputs[0])
    ntree.links.new(nr28.outputs[0], nr29.inputs[0])
    ntree.links.new(nr29.outputs[0], phongSpec.inputs['Specular Alpha'])
    ntree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    ntree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    ntree.links.new(tangentN.outputs['Normal'], negativeN.inputs['Normal'])
    ntree.links.new(negativeN.outputs['-Normal'], negN.inputs['Color'])
    ntree.links.new(negN.outputs['Normal'], nr14.inputs[0])
    ntree.links.new(nr14.outputs[0], nr15.inputs[0])
    ntree.links.new(nr15.outputs[0], phongSpec.inputs['-Normal'])
    ntree.links.new(tangentN.outputs['Normal'], nr30.inputs[0])
    ntree.links.new(nr30.outputs[0], nr31.inputs[0])
    ntree.links.new(nr31.outputs[0], N.inputs['Color'])
    ntree.links.new(N.outputs['Normal'], nr16.inputs[0])
    ntree.links.new(nr16.outputs[0], nr17.inputs[0])
    ntree.links.new(nr17.outputs[0], phongSpec.inputs['Normal'])
    ntree.links.new(nr16.outputs[0], nr18.inputs[0])
    ntree.links.new(nr18.outputs[0], principled.inputs['Normal'])
    ntree.links.new(nr18.outputs[0], principled.inputs['Clearcoat Normal'])
    ntree.links.new(tangentN.outputs['Alpha'], nr32.inputs[0])
    ntree.links.new(nr32.outputs[0], nr33.inputs[0])
    ntree.links.new(nr33.outputs[0], nr34.inputs[0])
    ntree.links.new(nr34.outputs[0], nr35.inputs[0])
    ntree.links.new(nr35.outputs[0], mixShader1.inputs['Fac'])
    ntree.links.new(tangentN.outputs['Emission Strength'], nr36.inputs[0])
    ntree.links.new(nr36.outputs[0], nr37.inputs[0])
    ntree.links.new(nr37.outputs[0], emissionShader.inputs['Strength'])
    ntree.links.new(emissionShader.outputs['Emission'], addShader.inputs[1])
    ntree.links.new(transparentBSDF.outputs['BSDF'], mixShader1.inputs[2])


def Garment(ntree: ShaderNodeTree):
    # Add output socket to node tree
    if len(ntree.outputs) < 1:
        ntree.outputs.new(type='NodeSocketShader', name='Shader')

    # Add and place nodes
    diffuseMap = ntree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.inputs['Vector'].hide = True
    diffuseMap.location = (-1220.0, 540.0)
    diffuseMap.name = '_d'
    diffuseMap.outputs['Alpha'].hide = True

    glossMap = ntree.nodes.new(type='ShaderNodeTexImage')
    glossMap.inputs['Vector'].hide = True
    glossMap.location = (-880.0, 540.0)
    glossMap.name = '_s'

    huePixel = ntree.nodes.new(type='ShaderNodeGroup')
    huePixel.location = (-500.0, 360.0)
    huePixel.name = 'HuePixel'
    huePixel.node_tree = _huePixel()
    huePixel.width = 180.0

    phongSpec = ntree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (-220.0, 360.0)
    phongSpec.name = 'GetPhongSpecular'
    phongSpec.node_tree = _getPhongSpecular()
    phongSpec.width = 220

    vMath1 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (100.0, 360.0)
    vMath1.operation = 'ADD'

    diffuseBSDF = ntree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuseBSDF.inputs['Roughness'].default_value = 0.0
    # diffuseBSDF.inputs['Roughness'].hide = True
    diffuseBSDF.location = (340.0, 360.0)

    addShader = ntree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (600.0, 360.0)

    mixShader = ntree.nodes.new(type='ShaderNodeMixShader')
    mixShader.location = (840.0, 360.0)

    grpOut1 = ntree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1080.0, 360.0)

    paletteMaskMap = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMaskMap.inputs['Vector'].hide = True
    paletteMaskMap.location = (-1220.0, 180.0)
    paletteMaskMap.name = '_m'
    paletteMaskMap.outputs['Alpha'].hide = True

    chosenPalette = ntree.nodes.new(type='ShaderNodeGroup')
    chosenPalette.location = (-880.0, 180.0)
    chosenPalette.name = 'ChosenPalette'
    chosenPalette.node_tree = _chosenPalette()
    chosenPalette.width = 240.0

    emissionShader = ntree.nodes.new(type='ShaderNodeEmission')
    emissionShader.location = (340.0, 180.0)

    transparentShader = ntree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentShader.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentShader.location = (600.0, 180.0)

    paletteMap = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMap.inputs['Vector'].hide = True
    paletteMap.location = (-1220.0, -60.0)
    paletteMap.name = '_h'

    norMap = ntree.nodes.new(type='ShaderNodeNormalMap')
    norMap.location = (-500.0, -60.0)
    norMap.width = 180

    rotationMap = ntree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.inputs['Vector'].hide = True
    rotationMap.location = (-1220.0, -320.0)
    rotationMap.name = '_n'

    tangentN = ntree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-880.0, -320.0)
    tangentN.node_tree = _normalAndAlphaFromSwizzledTexture()
    tangentN.width = 280

    # Add and place reroutes
    nr1 = ntree.nodes.new(type='NodeReroute')
    nr1.location = (-940.0, 460.0)
    nr2 = ntree.nodes.new(type='NodeReroute')
    nr2.location = (-940.0, 260.0)
    nr3 = ntree.nodes.new(type='NodeReroute')
    nr3.location = (-640.0, 260.0)
    nr4 = ntree.nodes.new(type='NodeReroute')
    nr4.location = (-580.0, 420.0)
    nr5 = ntree.nodes.new(type='NodeReroute')
    nr5.location = (-580.0, 380.0)
    nr6 = ntree.nodes.new(type='NodeReroute')
    nr6.location = (-280.0, 380.0)
    nr7 = ntree.nodes.new(type='NodeReroute')
    nr7.location = (-280.0, 320.0)
    nr8 = ntree.nodes.new(type='NodeReroute')
    nr8.location = (-560.0, 420.0)
    nr9 = ntree.nodes.new(type='NodeReroute')
    nr9.location = (-560.0, 300.0)
    nr10 = ntree.nodes.new(type='NodeReroute')
    nr10.location = (-940.0, -40.0)
    nr11 = ntree.nodes.new(type='NodeReroute')
    nr11.location = (-940.0, 240.0)
    nr12 = ntree.nodes.new(type='NodeReroute')
    nr12.location = (-640.0, 240.0)
    nr13 = ntree.nodes.new(type='NodeReroute')
    nr13.location = (-920.0, -40.0)
    nr14 = ntree.nodes.new(type='NodeReroute')
    nr14.location = (-920.0, 220.0)
    nr15 = ntree.nodes.new(type='NodeReroute')
    nr15.location = (-640.0, 220.0)
    nr16 = ntree.nodes.new(type='NodeReroute')
    nr16.location = (-900.0, 200.0)
    nr17 = ntree.nodes.new(type='NodeReroute')
    nr17.location = (-640.0, 200.0)
    nr18 = ntree.nodes.new(type='NodeReroute')
    nr18.location = (-220.0, 380.0)
    nr19 = ntree.nodes.new(type='NodeReroute')
    nr19.location = (60.0, 380.0)
    nr20 = ntree.nodes.new(type='NodeReroute')
    nr20.location = (60.0, 320.0)
    nr21 = ntree.nodes.new(type='NodeReroute')
    nr21.location = (300.0, 260.0)
    nr22 = ntree.nodes.new(type='NodeReroute')
    nr22.location = (300.0, 160.0)
    nr23 = ntree.nodes.new(type='NodeReroute')
    nr23.location = (-260.0, -20.0)
    nr24 = ntree.nodes.new(type='NodeReroute')
    nr24.location = (-260.0, 160.0)
    nr25 = ntree.nodes.new(type='NodeReroute')
    nr25.location = (240.0, 160.0)
    nr26 = ntree.nodes.new(type='NodeReroute')
    nr26.location = (-500.0, -280.0)
    nr27 = ntree.nodes.new(type='NodeReroute')
    nr27.location = (-240.0, -280.0)
    nr28 = ntree.nodes.new(type='NodeReroute')
    nr28.location = (-240.0, 140.0)
    nr29 = ntree.nodes.new(type='NodeReroute')
    nr29.location = (240.0, 140.0)
    nr30 = ntree.nodes.new(type='NodeReroute')
    nr30.location = (340.0, 220.0)
    nr31 = ntree.nodes.new(type='NodeReroute')
    nr31.location = (720.0, 220.0)
    nr32 = ntree.nodes.new(type='NodeReroute')
    nr32.location = (-500.0, -300.0)
    nr33 = ntree.nodes.new(type='NodeReroute')
    nr33.location = (-220.0, -300.0)
    nr34 = ntree.nodes.new(type='NodeReroute')
    nr34.location = (-220.0, 120.0)
    nr35 = ntree.nodes.new(type='NodeReroute')
    nr35.location = (240.0, 120.0)

    # Link nodes together
    ntree.links.new(diffuseMap.outputs['Color'], nr1.inputs[0])
    ntree.links.new(nr1.outputs[0], nr2.inputs[0])
    ntree.links.new(nr2.outputs[0], nr3.inputs[0])
    ntree.links.new(nr3.outputs[0], huePixel.inputs['_d DiffuseMap Color'])
    ntree.links.new(glossMap.outputs['Color'], nr8.inputs[0])
    ntree.links.new(nr8.outputs[0], nr9.inputs[0])
    ntree.links.new(nr9.outputs[0], huePixel.inputs['_s GlossMap Color'])
    ntree.links.new(glossMap.outputs['Alpha'], nr4.inputs[0])
    ntree.links.new(nr4.outputs[0], nr5.inputs[0])
    ntree.links.new(nr5.outputs[0], nr6.inputs[0])
    ntree.links.new(nr6.outputs[0], nr7.inputs[0])
    ntree.links.new(nr7.outputs[0], phongSpec.inputs['Specular Alpha'])
    ntree.links.new(paletteMap.outputs['Color'], nr10.inputs[0])
    ntree.links.new(nr10.outputs[0], nr11.inputs[0])
    ntree.links.new(nr11.outputs[0], nr12.inputs[0])
    ntree.links.new(nr12.outputs[0], huePixel.inputs['_h PaletteMap Color'])
    ntree.links.new(paletteMap.outputs['Alpha'], nr13.inputs[0])
    ntree.links.new(nr13.outputs[0], nr14.inputs[0])
    ntree.links.new(nr14.outputs[0], nr15.inputs[0])
    ntree.links.new(nr15.outputs[0], huePixel.inputs['_h PaletteMap Alpha'])
    ntree.links.new(paletteMaskMap.outputs['Color'], nr16.inputs[0])
    ntree.links.new(paletteMaskMap.outputs['Color'], chosenPalette.inputs['_m PaletteMaskMap Color'])
    ntree.links.new(nr16.outputs[0], nr17.inputs[0])
    ntree.links.new(nr17.outputs[0], huePixel.inputs['_m PaletteMaskMap Color'])
    ntree.links.new(huePixel.outputs['Diffuse Color'], nr18.inputs[0])
    ntree.links.new(huePixel.outputs['Specular Color'], phongSpec.inputs['Specular Color'])
    ntree.links.new(nr18.outputs[0], nr19.inputs[0])
    ntree.links.new(nr19.outputs[0], nr20.inputs[0])
    ntree.links.new(nr20.outputs[0], vMath1.inputs[0])
    ntree.links.new(phongSpec.outputs['Specular'], vMath1.inputs[1])
    ntree.links.new(vMath1.outputs['Vector'], nr21.inputs[0])
    ntree.links.new(nr21.outputs[0], diffuseBSDF.inputs['Color'])
    ntree.links.new(nr21.outputs[0], nr22.inputs[0])
    ntree.links.new(nr22.outputs[0], emissionShader.inputs['Color'])
    ntree.links.new(diffuseBSDF.outputs['BSDF'], addShader.inputs[0])
    ntree.links.new(addShader.outputs['Shader'], mixShader.inputs[1])
    ntree.links.new(mixShader.outputs['Shader'], grpOut1.inputs['Shader'])
    ntree.links.new(chosenPalette.outputs['Hue'], huePixel.inputs['Hue'])
    ntree.links.new(chosenPalette.outputs['Saturation'], huePixel.inputs['Saturation'])
    ntree.links.new(chosenPalette.outputs['Brightness'], huePixel.inputs['Brightness'])
    ntree.links.new(chosenPalette.outputs['Contrast'], huePixel.inputs['Contrast'])
    ntree.links.new(chosenPalette.outputs['Specular'], huePixel.inputs['Specular'])
    ntree.links.new(chosenPalette.outputs['Metallic Specular'], huePixel.inputs['Metallic Specular'])
    ntree.links.new(emissionShader.outputs['Emission'], addShader.inputs[1])
    ntree.links.new(transparentShader.outputs['BSDF'], mixShader.inputs[2])
    ntree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    ntree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    ntree.links.new(tangentN.outputs['Normal'], norMap.inputs['Color'])
    ntree.links.new(norMap.outputs['Normal'], nr23.inputs[0])
    ntree.links.new(nr23.outputs[0], nr24.inputs[0])
    ntree.links.new(nr24.outputs[0], phongSpec.inputs['Normal'])
    ntree.links.new(nr24.outputs[0], phongSpec.inputs['-Normal'])
    ntree.links.new(nr24.outputs[0], nr25.inputs[0])
    ntree.links.new(nr25.outputs[0], diffuseBSDF.inputs['Normal'])
    ntree.links.new(tangentN.outputs['Alpha'], nr26.inputs[0])
    ntree.links.new(nr26.outputs[0], nr27.inputs[0])
    ntree.links.new(nr27.outputs[0], nr28.inputs[0])
    ntree.links.new(nr28.outputs[0], nr29.inputs[0])
    ntree.links.new(nr29.outputs[0], nr30.inputs[0])
    ntree.links.new(nr30.outputs[0], nr31.inputs[0])
    ntree.links.new(nr31.outputs[0], mixShader.inputs['Fac'])
    ntree.links.new(tangentN.outputs['Emission Strength'], nr32.inputs[0])
    ntree.links.new(nr32.outputs[0], nr33.inputs[0])
    ntree.links.new(nr33.outputs[0], nr34.inputs[0])
    ntree.links.new(nr34.outputs[0], nr35.inputs[0])
    ntree.links.new(nr35.outputs[0], emissionShader.inputs['Strength'])


def HairC(ntree: ShaderNodeTree):
    # Add output socket to node tree
    if len(ntree.outputs) < 1:
        ntree.outputs.new(type='NodeSocketShader', name='Shader')

    # Add and place nodes
    diffuseMap = ntree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.inputs['Vector'].hide = True
    diffuseMap.label = '_d DiffuseMap'
    diffuseMap.location = (-1520.0, 380.0)
    diffuseMap.name = '_d'
    diffuseMap.outputs['Alpha'].hide = True

    paletteMaskMap = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMaskMap.inputs['Vector'].hide = True
    paletteMaskMap.label = '_m PaletteMaskMap'
    paletteMaskMap.location = (-1180.0, 380.0)
    paletteMaskMap.name = '_m'
    paletteMaskMap.outputs['Alpha'].hide = True

    paletteMap = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMap.inputs['Vector'].hide = True
    paletteMap.label = '_h PaletteMap'
    paletteMap.location = (-840.0, 380.0)
    paletteMap.name = '_h'

    sepXYZ = ntree.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.location = (-440.0, 500.0)
    sepXYZ.outputs['X'].hide = True
    sepXYZ.outputs['Y'].hide = True
    sepXYZ.width = 180.0

    huePixel = ntree.nodes.new(type='ShaderNodeGroup')
    huePixel.location = (-440.0, 380.0)
    huePixel.name = 'HuePixel'
    huePixel.node_tree = _huePixel()
    huePixel.width = 180.0

    phongSpec = ntree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (-160.0, 380.0)
    phongSpec.node_tree = _getPhongSpecular()
    phongSpec.width = 180.0

    mixRGB = ntree.nodes.new(type='ShaderNodeMixRGB')
    mixRGB.location = (160.0, 380.0)

    vMath1 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (400.0, 380.0)
    vMath1.operation = 'ADD'

    diffuseBSDF = ntree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuseBSDF.location = (640.0, 380.0)

    addShader = ntree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (900.0, 380.0)

    mixShader = ntree.nodes.new(type='ShaderNodeMixShader')
    mixShader.location = (1140.0, 380.0)

    grpOut1 = ntree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1380.0, 380.0)

    rotationMap = ntree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.inputs['Vector'].hide = True
    rotationMap.label = '_n RotationMap'
    rotationMap.location = (-1520.0, 0.0)
    rotationMap.name = '_n'

    tangentN = ntree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-1180.0, 0.0)
    tangentN.node_tree = _normalAndAlphaFromSwizzledTexture()

    norMap = ntree.nodes.new(type='ShaderNodeNormalMap')
    norMap.location = (-940.0, -320.0)

    specLookup = ntree.nodes.new(type='ShaderNodeGroup')
    specLookup.location = (-740.0, -320.0)
    specLookup.node_tree = _getSpecularLookup()

    glossMap = ntree.nodes.new(type='ShaderNodeTexImage')
    glossMap.inputs['Vector'].hide = True
    glossMap.label = '_s GlossMap'
    glossMap.location = (-840.0, 0.0)
    glossMap.name = '_s'

    directionMap = ntree.nodes.new(type='ShaderNodeTexImage')
    directionMap.label = 'DirectionMap'
    directionMap.location = (-500.0, 0.0)
    directionMap.name = 'directionMap'
    directionMap.outputs['Alpha'].hide = True

    vMath2 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (-160.0, 180.0)
    vMath2.operation = 'MULTIPLY'

    emission = ntree.nodes.new(type='ShaderNodeEmission')
    emission.location = (640.0, 160.0)

    transparentBSDF = ntree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.location = (900.0, 160.0)

    # Add and place reroutes
    nr1 = ntree.nodes.new(type='NodeReroute')
    nr1.location = (-1240.0, 300.0)
    nr2 = ntree.nodes.new(type='NodeReroute')
    nr2.location = (-1240.0, 100.0)
    nr3 = ntree.nodes.new(type='NodeReroute')
    nr3.location = (-480.0, 100.0)
    nr4 = ntree.nodes.new(type='NodeReroute')
    nr4.location = (-480.0, 220.0)
    nr5 = ntree.nodes.new(type='NodeReroute')
    nr5.location = (-840.0, 400.0)
    nr6 = ntree.nodes.new(type='NodeReroute')
    nr6.location = (-500.0, 400.0)
    nr7 = ntree.nodes.new(type='NodeReroute')
    nr7.location = (-500.0, 260.0)
    nr8 = ntree.nodes.new(type='NodeReroute')
    nr8.location = (-160.0, 420.0)
    nr9 = ntree.nodes.new(type='NodeReroute')
    nr9.location = (120.0, 420.0)
    nr10 = ntree.nodes.new(type='NodeReroute')
    nr10.location = (120.0, 320.0)
    nr11 = ntree.nodes.new(type='NodeReroute')
    nr11.location = (-160.0, 400.0)
    nr12 = ntree.nodes.new(type='NodeReroute')
    nr12.location = (360.0, 400.0)
    nr13 = ntree.nodes.new(type='NodeReroute')
    nr13.location = (360.0, 340.0)
    nr14 = ntree.nodes.new(type='NodeReroute')
    nr14.location = (-180.0, 260.0)
    nr15 = ntree.nodes.new(type='NodeReroute')
    nr15.location = (-180.0, 120.0)
    nr16 = ntree.nodes.new(type='NodeReroute')
    nr16.location = (600.0, 280.0)
    nr17 = ntree.nodes.new(type='NodeReroute')
    nr17.location = (600.0, 140.0)

    nr18 = ntree.nodes.new(type='NodeReroute')
    nr18.location = (-1020.0, -100.0)
    nr19 = ntree.nodes.new(type='NodeReroute')
    nr19.location = (-1020.0, -300.0)
    nr20 = ntree.nodes.new(type='NodeReroute')
    nr20.location = (-200.0, -300.0)
    nr21 = ntree.nodes.new(type='NodeReroute')
    nr21.location = (540.0, 160.0)
    nr22 = ntree.nodes.new(type='NodeReroute')
    nr22.location = (-1000.0, -100.0)
    nr23 = ntree.nodes.new(type='NodeReroute')
    nr23.location = (-1000.0, -280.0)
    nr24 = ntree.nodes.new(type='NodeReroute')
    nr24.location = (-200.0, -280.0)
    nr25 = ntree.nodes.new(type='NodeReroute')
    nr25.location = (540.0, 180.0)
    nr26 = ntree.nodes.new(type='NodeReroute')
    nr26.location = (660.0, 200.0)
    nr27 = ntree.nodes.new(type='NodeReroute')
    nr27.location = (1000.0, 200.0)
    nr28 = ntree.nodes.new(type='NodeReroute')
    nr28.location = (-980.0, -100.0)
    nr29 = ntree.nodes.new(type='NodeReroute')
    nr29.location = (-980.0, -400.0)
    nr30 = ntree.nodes.new(type='NodeReroute')
    nr30.location = (-680.0, -260.0)
    nr31 = ntree.nodes.new(type='NodeReroute')
    nr31.location = (-200.0, -260.0)
    nr32 = ntree.nodes.new(type='NodeReroute')
    nr32.location = (-200.0, 200.0)
    nr33 = ntree.nodes.new(type='NodeReroute')
    nr33.location = (540.0, 200.0)
    nr34 = ntree.nodes.new(type='NodeReroute')
    nr34.location = (-560.0, 20.0)
    nr35 = ntree.nodes.new(type='NodeReroute')
    nr35.location = (-560.0, 120.0)
    nr36 = ntree.nodes.new(type='NodeReroute')
    nr36.location = (-500.0, 20.0)
    nr37 = ntree.nodes.new(type='NodeReroute')
    nr37.location = (-220.0, 20.0)
    nr38 = ntree.nodes.new(type='NodeReroute')
    nr38.location = (-220.0, 200.0)

    # Link nodes together
    ntree.links.new(diffuseMap.outputs['Color'], nr1.inputs[0])
    ntree.links.new(nr1.outputs[0], nr2.inputs[0])
    ntree.links.new(nr2.outputs[0], nr3.inputs[0])
    ntree.links.new(nr3.outputs[0], nr4.inputs[0])
    ntree.links.new(nr4.outputs[0], huePixel.inputs['_d DiffuseMap Color'])
    ntree.links.new(paletteMaskMap.outputs['Color'], nr5.inputs[0])
    ntree.links.new(nr5.outputs[0], nr6.inputs[0])
    ntree.links.new(nr6.outputs[0], sepXYZ.inputs['Vector'])
    ntree.links.new(nr6.outputs[0], nr7.inputs[0])
    ntree.links.new(nr7.outputs[0], huePixel.inputs['_m PaletteMaskMap Color'])
    ntree.links.new(paletteMap.outputs['Color'], huePixel.inputs['_h PaletteMap Color'])
    ntree.links.new(paletteMap.outputs['Alpha'], huePixel.inputs['_h PaletteMap Alpha'])
    ntree.links.new(sepXYZ.outputs['Z'], nr8.inputs[0])
    ntree.links.new(nr8.outputs[0], nr9.inputs[0])
    ntree.links.new(nr9.outputs[0], nr10.inputs[0])
    ntree.links.new(nr10.outputs[0], mixRGB.inputs['Fac'])
    ntree.links.new(huePixel.outputs['Diffuse Color'], nr11.inputs[0])
    ntree.links.new(nr11.outputs[0], nr12.inputs[0])
    ntree.links.new(nr12.outputs[0], nr13.inputs[0])
    ntree.links.new(nr13.outputs[0], vMath1.inputs[0])
    ntree.links.new(huePixel.outputs['Specular Color'], nr14.inputs[0])
    ntree.links.new(nr14.outputs[0], phongSpec.inputs['Specular Color'])
    ntree.links.new(nr14.outputs[0], nr15.inputs[0])
    ntree.links.new(nr15.outputs[0], vMath2.inputs[0])
    ntree.links.new(phongSpec.outputs['Specular'], mixRGB.inputs['Color1'])
    ntree.links.new(mixRGB.outputs['Color'], vMath1.inputs[1])
    ntree.links.new(vMath1.outputs['Vector'], nr16.inputs[0])
    ntree.links.new(nr16.outputs[0], diffuseBSDF.inputs['Color'])
    ntree.links.new(nr16.outputs[0], nr17.inputs[0])
    ntree.links.new(nr17.outputs[0], emission.inputs['Color'])
    ntree.links.new(diffuseBSDF.outputs['BSDF'], addShader.inputs[0])
    ntree.links.new(addShader.outputs['Shader'], mixShader.inputs[1])
    ntree.links.new(mixShader.outputs['Shader'], grpOut1.inputs['Shader'])

    ntree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    ntree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    ntree.links.new(tangentN.outputs['Emission Strength'], nr18.inputs[0])
    ntree.links.new(nr18.outputs[0], nr19.inputs[0])
    ntree.links.new(nr19.outputs[0], nr20.inputs[0])
    ntree.links.new(nr20.outputs[0], nr21.inputs[0])
    ntree.links.new(nr21.outputs[0], emission.inputs['Strength'])
    ntree.links.new(tangentN.outputs['Alpha'], nr22.inputs[0])
    ntree.links.new(nr22.outputs[0], nr23.inputs[0])
    ntree.links.new(nr23.outputs[0], nr24.inputs[0])
    ntree.links.new(nr24.outputs[0], nr25.inputs[0])
    ntree.links.new(nr25.outputs[0], nr26.inputs[0])
    ntree.links.new(nr26.outputs[0], nr27.inputs[0])
    ntree.links.new(nr27.outputs[0], mixShader.inputs['Fac'])
    ntree.links.new(tangentN.outputs['Normal'], nr28.inputs[0])
    ntree.links.new(nr28.outputs[0], nr29.inputs[0])
    ntree.links.new(nr29.outputs[0], norMap.inputs['Color'])
    ntree.links.new(norMap.outputs['Normal'], nr30.inputs[0])
    ntree.links.new(nr30.outputs[0], nr31.inputs[0])
    ntree.links.new(nr31.outputs[0], nr32.inputs[0])
    ntree.links.new(nr32.outputs[0], phongSpec.inputs['Normal'])
    ntree.links.new(nr32.outputs[0], phongSpec.inputs['-Normal'])
    ntree.links.new(nr31.outputs[0], nr33.inputs[0])
    ntree.links.new(nr33.outputs[0], diffuseBSDF.inputs['Normal'])
    ntree.links.new(norMap.outputs['Normal'], specLookup.inputs['Normal'])
    ntree.links.new(specLookup.outputs['Vector'], directionMap.inputs['Vector'])
    ntree.links.new(directionMap.outputs['Color'], vMath2.inputs[1])
    ntree.links.new(vMath2.outputs['Vector'], mixRGB.inputs['Color2'])
    ntree.links.new(glossMap.outputs['Color'], nr34.inputs[0])
    ntree.links.new(nr34.outputs[0], nr35.inputs[0])
    ntree.links.new(nr35.outputs[0], huePixel.inputs['_s GlossMap Color'])
    ntree.links.new(glossMap.outputs['Alpha'], nr36.inputs[0])
    ntree.links.new(nr36.outputs[0], nr37.inputs[0])
    ntree.links.new(nr37.outputs[0], nr38.inputs[0])
    ntree.links.new(nr38.outputs[0], phongSpec.inputs['Specular Alpha'])
    ntree.links.new(emission.outputs['Emission'], addShader.inputs[1])
    ntree.links.new(transparentBSDF.outputs['BSDF'], mixShader.inputs[2])


def SkinB(ntree: ShaderNodeTree):
    # Add output socket to node tree
    if len(ntree.outputs) < 1:
        ntree.outputs.new(type='NodeSocketShader', name='Shader')

    # Add and place nodes
    glossMap = ntree.nodes.new(type='ShaderNodeTexImage')
    glossMap.inputs['Vector'].hide = True
    glossMap.label = '_s GlossMap'
    glossMap.location = (-1940.0, 460.0)
    glossMap.name = '_s'

    paletteMaskMap = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMaskMap.inputs['Vector'].hide = True
    paletteMaskMap.label = '_m PaletteMaskMap'
    paletteMaskMap.location = (-1600.0, 460.0)
    paletteMaskMap.name = '_m'
    paletteMaskMap.outputs['Alpha'].hide = True

    paletteMap = ntree.nodes.new(type='ShaderNodeTexImage')
    paletteMap.inputs['Vector'].hide = True
    paletteMap.label = '_h PaletteMap'
    paletteMap.location = (-1260.0, 460.0)
    paletteMap.name = '_h'

    huePixel = ntree.nodes.new(type='ShaderNodeGroup')
    huePixel.location = (-920.0, 460.0)
    huePixel.name = 'HueSkinPixel'
    huePixel.node_tree = _hueSkinPixel()
    huePixel.width = 240.0

    phongSpec = ntree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (-580.0, 460.0)
    phongSpec.node_tree = _getPhongSpecular()

    vMath1 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-340.0, 460.0)
    vMath1.operation = 'MULTIPLY'

    vMath2 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (-100.0, 460.0)
    vMath2.operation = 'MULTIPLY'

    mixRGB = ntree.nodes.new(type='ShaderNodeMixRGB')
    mixRGB.inputs['Fac'].default_value = 0.0
    mixRGB.location = (140.0, 460.0)

    vMath3 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (380.0, 460.0)
    vMath3.operation = 'ADD'

    vMath4 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (620.0, 460.0)
    vMath4.operation = 'ADD'

    diffuseBSDF = ntree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuseBSDF.inputs['Roughness'].default_value = 0.0
    diffuseBSDF.location = (860.0, 460.0)

    addShader = ntree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (1120.0, 460.0)

    mixShader = ntree.nodes.new(type='ShaderNodeMixShader')
    mixShader.location = (1360.0, 460.0)

    grpOut1 = ntree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1600.0, 460.0)

    gamma1 = ntree.nodes.new(type='ShaderNodeGamma')
    gamma1.inputs['Gamma'].default_value = 2.1
    gamma1.location = (-580.0, 240.0)

    vMath5 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath5.location = (-100.0, 240.0)
    vMath5.operation = 'MULTIPLY'

    flushColor = ntree.nodes.new(type='ShaderNodeGroup')
    flushColor.label = 'GetFlushColor'
    flushColor.location = (380.0, 240.0)
    flushColor.name = 'GetFlushColor'
    flushColor.node_tree = _getFlushColor()

    emission = ntree.nodes.new(type='ShaderNodeEmission')
    emission.location = (860.0, 240.0)

    transparentBSDF = ntree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentBSDF.location = (1120.0, 240.0)

    diffuseMap = ntree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.inputs['Vector'].hide = True
    diffuseMap.label = '_d DiffuseMap'
    diffuseMap.location = (-1940.0, 0.0)
    diffuseMap.name = '_d'
    diffuseMap.outputs['Alpha'].hide = True

    rotationMap = ntree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.inputs['Vector'].hide = True
    rotationMap.label = '_n RotationMap'
    rotationMap.location = (-1600.0, 0.0)
    rotationMap.name = '_n'

    tangentN = ntree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-1260.0, 0.0)
    tangentN.node_tree = _normalAndAlphaFromSwizzledTexture()
    tangentN.width = 240.0

    comNor = ntree.nodes.new(type='ShaderNodeGroup')
    comNor.location = (-920.0, 0.0)
    comNor.node_tree = _combineNormals()
    comNor.width = 180.0

    ageDarkening = ntree.nodes.new(type='ShaderNodeMixRGB')
    ageDarkening.inputs['Color1'].default_value = [0.0, 0.0, 0.0, 1.0]
    ageDarkening.inputs['Color2'].default_value = [1.0, 1.0, 1.0, 1.0]
    ageDarkening.label = 'AgeDarkening'
    ageDarkening.location = (-580.0, 0.0)
    ageDarkening.name = 'ageDarkening'

    complexionMap = ntree.nodes.new(type='ShaderNodeTexImage')
    complexionMap.inputs['Vector'].hide = True
    complexionMap.label = 'ComplexionMap'
    complexionMap.location = (-1940.0, -280.0)
    complexionMap.name = 'complexionMap'
    complexionMap.outputs['Alpha'].hide = True

    ageMap = ntree.nodes.new(type='ShaderNodeTexImage')
    ageMap.inputs['Vector'].hide = True
    ageMap.label = 'AgeMap'
    ageMap.location = (-1600.0, -280.0)
    ageMap.name = 'ageMap'

    ageNormal = ntree.nodes.new(type='ShaderNodeGroup')
    ageNormal.location = (-1260.0, -280.0)
    ageNormal.node_tree = _extractAgeNormalAndScarFromSwizzledTexture()
    ageNormal.width = 240.0

    facepaintMap = ntree.nodes.new(type='ShaderNodeTexImage')
    facepaintMap.inputs['Vector'].hide = True
    facepaintMap.label = 'FacepaintMap'
    facepaintMap.location = (-920.0, -280.0)
    facepaintMap.name = 'facepaintMap'

    # Add and place reroutes
    nr1 = ntree.nodes.new(type='NodeReroute')
    nr1.location = (-1600.0, 500.0)
    nr2 = ntree.nodes.new(type='NodeReroute')
    nr2.location = (-940.0, 500.0)
    nr3 = ntree.nodes.new(type='NodeReroute')
    nr3.location = (-940.0, 360.0)

    nr4 = ntree.nodes.new(type='NodeReroute')
    nr4.location = (-1600.0, 480.0)
    nr5 = ntree.nodes.new(type='NodeReroute')
    nr5.location = (-640.0, 480.0)
    nr6 = ntree.nodes.new(type='NodeReroute')
    nr6.location = (-640.0, 420.0)

    nr7 = ntree.nodes.new(type='NodeReroute')
    nr7.location = (-1320.0, 380.0)
    nr8 = ntree.nodes.new(type='NodeReroute')
    nr8.location = (-1320.0, 200.0)
    nr9 = ntree.nodes.new(type='NodeReroute')
    nr9.location = (-1020.0, 200.0)

    nr10 = ntree.nodes.new(type='NodeReroute')
    nr10.location = (-580.0, 480.0)
    nr11 = ntree.nodes.new(type='NodeReroute')
    nr11.location = (-360.0, 480.0)
    nr12 = ntree.nodes.new(type='NodeReroute')
    nr12.location = (-360.0, 400.0)
    nr13 = ntree.nodes.new(type='NodeReroute')
    nr13.location = (340.0, 480.0)
    nr14 = ntree.nodes.new(type='NodeReroute')
    nr14.location = (340.0, 200.0)

    nr15 = ntree.nodes.new(type='NodeReroute')
    nr15.location = (-420.0, 400.0)
    nr16 = ntree.nodes.new(type='NodeReroute')
    nr16.location = (-420.0, 240.0)
    nr17 = ntree.nodes.new(type='NodeReroute')
    nr17.location = (-200.0, 240.0)

    nr18 = ntree.nodes.new(type='NodeReroute')
    nr18.location = (820.0, 360.0)
    nr19 = ntree.nodes.new(type='NodeReroute')
    nr19.location = (820.0, 220.0)

    nr20 = ntree.nodes.new(type='NodeReroute')
    nr20.location = (-1620.0, 40.0)
    nr21 = ntree.nodes.new(type='NodeReroute')
    nr21.location = (-1000.0, 40.0)
    nr22 = ntree.nodes.new(type='NodeReroute')
    nr22.location = (-1000.0, 260.0)

    nr23 = ntree.nodes.new(type='NodeReroute')
    nr23.location = (-920.0, 40.0)
    nr24 = ntree.nodes.new(type='NodeReroute')
    nr24.location = (520.0, 40.0)
    nr25 = ntree.nodes.new(type='NodeReroute')
    nr25.location = (860.0, 320.0)
    nr26 = ntree.nodes.new(type='NodeReroute')
    nr26.location = (1260.0, 320.0)

    nr27 = ntree.nodes.new(type='NodeReroute')
    nr27.location = (-920.0, 20.0)
    nr28 = ntree.nodes.new(type='NodeReroute')
    nr28.location = (520.0, 20.0)

    nr29 = ntree.nodes.new(type='NodeReroute')
    nr29.location = (-660.0, 60.0)
    nr30 = ntree.nodes.new(type='NodeReroute')
    nr30.location = (-660.0, 220.0)
    nr31 = ntree.nodes.new(type='NodeReroute')
    nr31.location = (280.0, 60.0)
    nr32 = ntree.nodes.new(type='NodeReroute')
    nr32.location = (520.0, 60.0)

    nr33 = ntree.nodes.new(type='NodeReroute')
    nr33.location = (-340.0, 260.0)
    nr34 = ntree.nodes.new(type='NodeReroute')
    nr34.location = (40.0, 260.0)

    nr35 = ntree.nodes.new(type='NodeReroute')
    nr35.location = (-300.0, 100.0)
    nr36 = ntree.nodes.new(type='NodeReroute')
    nr36.location = (-140.0, 100.0)
    nr37 = ntree.nodes.new(type='NodeReroute')
    nr37.location = (-140.0, 300.0)

    nr38 = ntree.nodes.new(type='NodeReroute')
    nr38.location = (140.0, 260.0)
    nr39 = ntree.nodes.new(type='NodeReroute')
    nr39.location = (280.0, 260.0)

    nr40 = ntree.nodes.new(type='NodeReroute')
    nr40.location = (-1620.0, -220.0)
    nr41 = ntree.nodes.new(type='NodeReroute')
    nr41.location = (-1620.0, 20.0)
    nr42 = ntree.nodes.new(type='NodeReroute')
    nr42.location = (-1020.0, 20.0)
    nr43 = ntree.nodes.new(type='NodeReroute')
    nr43.location = (-920.0, 80.0)
    nr44 = ntree.nodes.new(type='NodeReroute')
    nr44.location = (-380.0, 80.0)
    nr45 = ntree.nodes.new(type='NodeReroute')
    nr45.location = (-380.0, 300.0)

    nr46 = ntree.nodes.new(type='NodeReroute')
    nr46.location = (-980.0, -260.0)
    nr47 = ntree.nodes.new(type='NodeReroute')
    nr47.location = (-980.0, -180.0)

    nr48 = ntree.nodes.new(type='NodeReroute')
    nr48.location = (-960.0, -260.0)
    nr49 = ntree.nodes.new(type='NodeReroute')
    nr49.location = (-960.0, -180.0)
    nr50 = ntree.nodes.new(type='NodeReroute')
    nr50.location = (-680.0, -180.0)

    nr51 = ntree.nodes.new(type='NodeReroute')
    nr51.location = (-640.0, -260.0)
    nr52 = ntree.nodes.new(type='NodeReroute')
    nr52.location = (-640.0, 120.0)

    nr53 = ntree.nodes.new(type='NodeReroute')
    nr53.location = (-620.0, -260.0)
    nr54 = ntree.nodes.new(type='NodeReroute')
    nr54.location = (-620.0, 120.0)
    nr55 = ntree.nodes.new(type='NodeReroute')
    nr55.location = (-440.0, 120.0)
    nr56 = ntree.nodes.new(type='NodeReroute')
    nr56.location = (-200.0, 280.0)
    nr57 = ntree.nodes.new(type='NodeReroute')
    nr57.location = (40.0, 280.0)

    # Link nodes together
    ntree.links.new(glossMap.outputs['Color'], nr1.inputs[0])
    ntree.links.new(nr1.outputs[0], nr2.inputs[0])
    ntree.links.new(nr2.outputs[0], nr3.inputs[0])
    ntree.links.new(nr3.outputs[0], huePixel.inputs['_s GlossMap Color'])
    ntree.links.new(glossMap.outputs['Alpha'], nr4.inputs[0])
    ntree.links.new(nr4.outputs[0], nr5.inputs[0])
    ntree.links.new(nr5.outputs[0], nr6.inputs[0])
    ntree.links.new(nr6.outputs[0], phongSpec.inputs['Specular Alpha'])
    ntree.links.new(paletteMaskMap.outputs['Color'], nr7.inputs[0])
    ntree.links.new(nr7.outputs[0], nr8.inputs[0])
    ntree.links.new(nr8.outputs[0], nr9.inputs[0])
    ntree.links.new(nr9.outputs[0], huePixel.inputs['_m PaletteMaskMap Color'])
    ntree.links.new(paletteMap.outputs['Color'], huePixel.inputs['_h PaletteMap Color'])
    ntree.links.new(paletteMap.outputs['Alpha'], huePixel.inputs['_h PaletteMap Alpha'])
    ntree.links.new(huePixel.outputs['Diffuse Color'], nr10.inputs[0])
    ntree.links.new(nr10.outputs[0], nr11.inputs[0])
    ntree.links.new(nr11.outputs[0], nr12.inputs[0])
    ntree.links.new(nr11.outputs[0], nr13.inputs[0])
    ntree.links.new(nr12.outputs[0], vMath1.inputs[0])
    ntree.links.new(nr13.outputs[0], nr14.inputs[0])
    ntree.links.new(nr14.outputs[0], flushColor.inputs['Diffuse Color'])
    ntree.links.new(huePixel.outputs['Specular Color'], phongSpec.inputs['Specular Color'])
    ntree.links.new(phongSpec.outputs['Specular'], nr15.inputs[0])
    ntree.links.new(nr15.outputs[0], nr16.inputs[0])
    ntree.links.new(nr16.outputs[0], nr17.inputs[0])
    ntree.links.new(nr17.outputs[0], vMath5.inputs[0])
    ntree.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    ntree.links.new(vMath2.outputs['Vector'], mixRGB.inputs['Color1'])
    ntree.links.new(mixRGB.outputs['Color'], vMath3.inputs[0])
    ntree.links.new(vMath3.outputs['Vector'], vMath4.inputs[0])
    ntree.links.new(vMath4.outputs['Vector'], nr18.inputs[0])
    ntree.links.new(nr18.outputs[0], diffuseBSDF.inputs['Color'])
    ntree.links.new(nr18.outputs[0], nr19.inputs[0])
    ntree.links.new(nr19.outputs[0], emission.inputs['Color'])
    ntree.links.new(diffuseBSDF.outputs['BSDF'], addShader.inputs[0])
    ntree.links.new(addShader.outputs['Shader'], mixShader.inputs[1])
    ntree.links.new(mixShader.outputs['Shader'], grpOut1.inputs['Shader'])

    ntree.links.new(gamma1.outputs['Color'], nr33.inputs[0])
    ntree.links.new(nr33.outputs[0], nr34.inputs[0])
    ntree.links.new(nr34.outputs[0], mixRGB.inputs['Color2'])
    ntree.links.new(vMath5.outputs['Vector'], nr38.inputs[0])
    ntree.links.new(nr38.outputs[0], nr39.inputs[0])
    ntree.links.new(nr39.outputs[0], vMath3.inputs[1])
    ntree.links.new(flushColor.outputs['Flush Color'], vMath4.inputs[1])
    ntree.links.new(emission.outputs['Emission'], addShader.inputs[1])
    ntree.links.new(transparentBSDF.outputs['BSDF'], mixShader.inputs[2])

    ntree.links.new(diffuseMap.outputs['Color'], nr20.inputs[0])
    ntree.links.new(nr20.outputs[0], nr21.inputs[0])
    ntree.links.new(nr21.outputs[0], nr22.inputs[0])
    ntree.links.new(nr22.outputs[0], huePixel.inputs['_d DiffuseMap Color'])
    ntree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    ntree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    ntree.links.new(tangentN.outputs['Normal'], comNor.inputs['TexNormal'])
    ntree.links.new(tangentN.outputs['Alpha'], nr23.inputs[0])
    ntree.links.new(nr23.outputs[0], nr24.inputs[0])
    ntree.links.new(nr24.outputs[0], nr25.inputs[0])
    ntree.links.new(nr25.outputs[0], nr26.inputs[0])
    ntree.links.new(nr26.outputs[0], mixShader.inputs['Fac'])
    ntree.links.new(tangentN.outputs['Emission Strength'], nr27.inputs[0])
    ntree.links.new(nr27.outputs[0], nr28.inputs[0])
    ntree.links.new(nr28.outputs[0], emission.inputs['Strength'])
    ntree.links.new(comNor.outputs['Normal'], nr29.inputs[0])
    ntree.links.new(nr29.outputs[0], nr30.inputs[0])
    ntree.links.new(nr30.outputs[0], phongSpec.inputs['Normal'])
    ntree.links.new(nr30.outputs[0], phongSpec.inputs['-Normal'])
    ntree.links.new(nr29.outputs[0], nr31.inputs[0])
    ntree.links.new(nr31.outputs[0], flushColor.inputs['Normal'])
    ntree.links.new(nr31.outputs[0], nr32.inputs[0])
    ntree.links.new(nr32.outputs[0], diffuseBSDF.inputs['Normal'])
    ntree.links.new(ageDarkening.outputs['Color'], nr35.inputs[0])
    ntree.links.new(nr35.outputs[0], nr36.inputs[0])
    ntree.links.new(nr36.outputs[0], vMath5.inputs[1])
    ntree.links.new(nr36.outputs[0], nr37.inputs[0])
    ntree.links.new(nr37.outputs[0], vMath2.inputs[1])

    ntree.links.new(complexionMap.outputs['Color'], nr40.inputs[0])
    ntree.links.new(nr40.outputs[0], nr41.inputs[0])
    ntree.links.new(nr41.outputs[0], nr42.inputs[0])
    ntree.links.new(nr42.outputs[0], nr43.inputs[0])
    ntree.links.new(nr43.outputs[0], nr44.inputs[0])
    ntree.links.new(nr44.outputs[0], nr45.inputs[0])
    ntree.links.new(nr45.outputs[0], vMath1.inputs[1])
    ntree.links.new(ageMap.outputs['Color'], ageNormal.inputs['AgeMap Color'])
    ntree.links.new(ageMap.outputs['Alpha'], ageNormal.inputs['AgeMap Alpha'])
    ntree.links.new(ageNormal.outputs['Normal'], nr46.inputs[0])
    ntree.links.new(nr46.outputs[0], nr47.inputs[0])
    ntree.links.new(nr47.outputs[0], comNor.inputs['AgeNormal'])
    ntree.links.new(ageNormal.outputs['Scar Mask'], nr48.inputs[0])
    ntree.links.new(nr48.outputs[0], nr49.inputs[0])
    ntree.links.new(nr49.outputs[0], nr50.inputs[0])
    ntree.links.new(nr50.outputs[0], ageDarkening.inputs['Fac'])
    ntree.links.new(facepaintMap.outputs['Color'], nr51.inputs[0])
    ntree.links.new(nr51.outputs[0], nr52.inputs[0])
    ntree.links.new(nr52.outputs[0], gamma1.inputs['Color'])
    ntree.links.new(facepaintMap.outputs['Alpha'], nr53.inputs[0])
    ntree.links.new(nr53.outputs[0], nr54.inputs[0])
    ntree.links.new(nr54.outputs[0], nr55.inputs[0])
    ntree.links.new(nr55.outputs[0], nr56.inputs[0])
    ntree.links.new(nr56.outputs[0], nr57.inputs[0])
    ntree.links.new(nr57.outputs[0], mixRGB.inputs['Fac'])


def Uber(ntree: ShaderNodeTree):
    # Add output socket to node tree
    if len(ntree.outputs) < 1:
        ntree.outputs.new(type='NodeSocketShader', name='Shader')

    # Add and place nodes
    geom1 = ntree.nodes.new(type='ShaderNodeNewGeometry')
    geom1.location = (-1400.0, 280.0)

    vMath1 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-1160.0, 280.0)
    vMath1.operation = 'REFLECT'

    vMath2 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.inputs[1].default_value = [-1.0, -1.0, -1.0]
    vMath2.location = (-920.0, 280.0)
    vMath2.operation = 'MULTIPLY'

    geom2 = ntree.nodes.new(type='ShaderNodeNewGeometry')
    geom2.location = (-920.0, 80.0)

    vMath3 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (-680.0, 280.0)
    vMath3.operation = 'DOT_PRODUCT'

    clamp1 = ntree.nodes.new(type='ShaderNodeClamp')
    clamp1.inputs['Min'].default_value = 0.0
    clamp1.inputs['Max'].default_value = 1.0
    clamp1.location = (-440.0, 280.0)

    math1 = ntree.nodes.new(type='ShaderNodeMath')
    math1.location = (-200, 280.0)
    math1.operation = 'POWER'

    vMath4 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (40.0, 280.0)
    vMath4.operation = 'MULTIPLY'

    vMath5 = ntree.nodes.new(type='ShaderNodeVectorMath')
    vMath5.location = (280.0, 280.0)
    vMath5.operation = 'ADD'

    diffBSDF = ntree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffBSDF.inputs['Roughness'].default_value = 0.0
    diffBSDF.location = (520.0, 280.0)

    addShader = ntree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (780.0, 280.0)

    mixShader = ntree.nodes.new(type='ShaderNodeMixShader')
    mixShader.location = (1020.0, 280.0)

    grpOut = ntree.nodes.new(type='NodeGroupOutput')
    grpOut.location = (1260.0, 280.0)

    glossMap = ntree.nodes.new(type='ShaderNodeTexImage')
    glossMap.label = "_s GlossMap"
    glossMap.location = (-1260.0, 0.0)
    glossMap.name = '_s'

    math2 = ntree.nodes.new('ShaderNodeMath')
    math2.inputs[0].default_value = 64.0
    math2.inputs[1].default_value = 1.0
    math2.location = (-920.0, -100.0)
    math2.operation = 'SUBTRACT'

    math3 = ntree.nodes.new(type='ShaderNodeMath')
    math3.location = (-680.0, 0.0)
    math3.operation = 'MULTIPLY'

    math4 = ntree.nodes.new(type='ShaderNodeMath')
    math4.inputs[1].default_value = 1.0
    math4.location = (-440.0, 0.0)
    math4.operation = 'ADD'

    diffuseMap = ntree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.label = "_d DiffuseMap"
    diffuseMap.location = (-260.0, 0.0)
    diffuseMap.name = '_d'

    gamma1 = ntree.nodes.new(type='ShaderNodeGamma')
    gamma1.inputs['Gamma'].default_value = 2.1
    gamma1.location = (40.0, 0.0)

    emission = ntree.nodes.new(type='ShaderNodeEmission')
    emission.location = (520.0, 0.0)

    transparentBSDF = ntree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentBSDF.location = (780.0, 0.0)

    rotationMap = ntree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.label = "_n RotationMap"
    rotationMap.location = (-1040.0, -280.0)
    rotationMap.name = '_n'

    tangentN = ntree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-680.0, -280.0)
    tangentN.node_tree = _normalAndAlphaFromSwizzledTexture()
    tangentN.width = 380.0

    norMap = ntree.nodes.new(type='ShaderNodeNormalMap')
    norMap.location = (-180.0, -280.0)

    # Add and place reroutes
    nr1 = ntree.nodes.new(type='NodeReroute')
    nr1.location = (-1200.0, 240.0)
    nr2 = ntree.nodes.new(type='NodeReroute')
    nr2.location = (-1200.0, 300.0)
    nr3 = ntree.nodes.new(type='NodeReroute')
    nr3.location = (0.0, 300.0)
    nr4 = ntree.nodes.new(type='NodeReroute')
    nr4.location = (480.0, 180.0)
    nr5 = ntree.nodes.new(type='NodeReroute')
    nr5.location = (-920.0, -80.0)
    nr6 = ntree.nodes.new(type='NodeReroute')
    nr6.location = (-780.0, -80.0)
    nr7 = ntree.nodes.new(type='NodeReroute')
    nr7.location = (-920.0, -60.0)
    nr8 = ntree.nodes.new(type='NodeReroute')
    nr8.location = (-780.0, -60.0)
    nr9 = ntree.nodes.new(type='NodeReroute')
    nr9.location = (-680.0, 20.0)
    nr10 = ntree.nodes.new(type='NodeReroute')
    nr10.location = (-200.0, 20.0)
    nr11 = ntree.nodes.new(type='NodeReroute')
    nr11.location = (480.0, -20.0)
    nr12 = ntree.nodes.new(type='NodeReroute')
    nr12.location = (540.0, 80.0)
    nr13 = ntree.nodes.new(type='NodeReroute')
    nr13.location = (860.0, 80.0)
    nr14 = ntree.nodes.new(type='NodeReroute')
    nr14.location = (-180.0, -240.0)
    nr15 = ntree.nodes.new(type='NodeReroute')
    nr15.location = (100.0, -240.0)
    nr16 = ntree.nodes.new(type='NodeReroute')
    nr16.location = (-180.0, -260.0)
    nr17 = ntree.nodes.new(type='NodeReroute')
    nr17.location = (100.0, -260.0)
    nr18 = ntree.nodes.new(type='NodeReroute')
    nr18.location = (0.0, -280.0)
    nr19 = ntree.nodes.new(type='NodeReroute')
    nr19.location = (0.0, -220.0)
    nr20 = ntree.nodes.new(type='NodeReroute')
    nr20.location = (100.0, -220.0)

    # Link nodes together
    ntree.links.new(geom1.outputs['Incoming'], vMath1.inputs[1])
    ntree.links.new(nr1.outputs[0], vMath1.inputs[0])
    ntree.links.new(nr2.outputs[0], nr1.inputs[0])
    ntree.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    ntree.links.new(vMath2.outputs['Vector'], vMath3.inputs[0])
    ntree.links.new(geom2.outputs['Incoming'], vMath3.inputs[1])
    ntree.links.new(vMath3.outputs['Value'], clamp1.inputs['Value'])
    ntree.links.new(clamp1.outputs['Result'], math1.inputs[0])
    ntree.links.new(nr3.outputs[0], nr2.inputs[0])
    ntree.links.new(math1.outputs['Value'], vMath4.inputs[1])
    ntree.links.new(vMath4.outputs['Vector'], vMath5.inputs[1])
    ntree.links.new(vMath5.outputs['Vector'], nr4.inputs[0])
    ntree.links.new(nr4.outputs[0], diffBSDF.inputs['Color'])
    ntree.links.new(diffBSDF.outputs['BSDF'], addShader.inputs[0])
    ntree.links.new(addShader.outputs['Shader'], mixShader.inputs[1])
    ntree.links.new(mixShader.outputs['Shader'], grpOut.inputs[0])

    ntree.links.new(input=glossMap.outputs['Color'], output=nr7.inputs[0])
    ntree.links.new(input=nr7.outputs[0], output=nr8.inputs[0])
    ntree.links.new(input=nr8.outputs[0], output=nr9.inputs[0])
    ntree.links.new(input=nr9.outputs[0], output=nr10.inputs[0])
    ntree.links.new(input=nr10.outputs[0], output=vMath4.inputs[0])
    ntree.links.new(input=glossMap.outputs['Alpha'], output=nr5.inputs[0])
    ntree.links.new(input=nr5.outputs[0], output=nr6.inputs[0])
    ntree.links.new(input=nr6.outputs[0], output=math3.inputs[0])
    ntree.links.new(input=math2.outputs['Value'], output=math3.inputs[1])
    ntree.links.new(input=math3.outputs['Value'], output=math4.inputs[0])
    ntree.links.new(input=math4.outputs['Value'], output=math1.inputs[1])
    ntree.links.new(input=diffuseMap.outputs['Color'], output=gamma1.inputs['Color'])
    ntree.links.new(input=gamma1.outputs['Color'], output=vMath5.inputs[0])
    ntree.links.new(input=nr4.outputs[0], output=nr11.inputs[0])
    ntree.links.new(input=nr11.outputs[0], output=emission.inputs['Color'])
    ntree.links.new(input=emission.outputs['Emission'], output=addShader.inputs[1])
    ntree.links.new(input=transparentBSDF.outputs['BSDF'], output=mixShader.inputs[2])

    ntree.links.new(rotationMap.outputs['Color'], tangentN.inputs[0])
    ntree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs[1])
    ntree.links.new(tangentN.outputs['Normal'], norMap.inputs['Color'])
    ntree.links.new(norMap.outputs['Normal'], nr18.inputs[0])
    ntree.links.new(nr18.outputs[0], nr19.inputs[0])
    ntree.links.new(nr19.outputs[0], nr3.inputs[0])
    ntree.links.new(nr19.outputs[0], nr20.inputs[0])
    ntree.links.new(nr20.outputs[0], diffBSDF.inputs['Normal'])
    ntree.links.new(tangentN.outputs['Alpha'], nr14.inputs[0])
    ntree.links.new(nr14.outputs[0], nr15.inputs[0])
    ntree.links.new(nr15.outputs[0], nr12.inputs[0])
    ntree.links.new(nr12.outputs[0], nr13.inputs[0])
    ntree.links.new(nr13.outputs[0], mixShader.inputs['Fac'])
    ntree.links.new(tangentN.outputs['Emission Strength'], nr16.inputs[0])
    ntree.links.new(nr16.outputs[0], nr17.inputs[0])
    ntree.links.new(nr17.outputs[0], emission.inputs['Strength'])

    # Hide unlinked node sockets
    for node in ntree.nodes:
        if node.select:
            for socket in node.inputs:
                socket.hide = True
            for socket in node.outputs:
                socket.hide = True

    # Unhide select unlinked node sockets
    vMath2.inputs[1].hide = False
    clamp1.inputs[1].hide = False
    clamp1.inputs[2].hide = False
    math2.inputs[0].hide = False
    math2.inputs[1].hide = False
    math4.inputs[1].hide = False
    gamma1.inputs[1].hide = False
    transparentBSDF.inputs['Color'].hide = False
    norMap.inputs['Strength'].hide = False
