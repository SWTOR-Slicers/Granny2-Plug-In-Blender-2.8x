# <pep8 compliant>

import bpy
from bpy.types import ShaderNodeTree


# Detect Blender version
major, minor, _ = bpy.app.version
blender_version = major + minor / 100


def add_output_socket_if_needed(node_tree):
    # type: (ShaderNodeTree) -> None
    '''
    Checks for the existence of node_tree outputs by different means
    depending on Blender version, and adds one if there is none
    '''
    if blender_version < 4.0:
        if len(node_tree.outputs) == 0:
            node_tree.outputs.new(type='NodeSocketShader', name='Shader')
    else:
        has_output_sockets = False
        for item in node_tree.interface.items_tree:
            if item.item_type == 'SOCKET':
                if item.in_out == 'OUTPUT':
                    has_output_sockets = True
                    break
        if has_output_sockets == False:
            node_tree.interface.new_socket('Shader', in_out='OUTPUT', socket_type='NodeSocketShader')


def creature(node_tree):
    # type: (ShaderNodeTree) -> None
    from .node_group import (
        get_flush_color,
        get_phong_specular,
        get_specular_lookup,
        normal_and_alpha_from_swizzled_texture,
    )

    # Add output socket to node tree
    add_output_socket_if_needed(node_tree)

    # Add and place nodes
    diffuseMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.label = "_d DiffuseMap"
    diffuseMap.location = (-460.0, 580.0)
    diffuseMap.name = '_d'

    gamma1 = node_tree.nodes.new(type='ShaderNodeGamma')
    gamma1.inputs['Gamma'].default_value = 2.1
    gamma1.location = (-120.0, 580.0)

    math1 = node_tree.nodes.new(type='ShaderNodeMath')
    math1.inputs[1].default_value = 0.5
    math1.location = (-120.0, 460.0)
    math1.operation = 'GREATER_THAN'

    math2 = node_tree.nodes.new(type='ShaderNodeMath')
    math2.location = (120.0, 460.0)
    math2.operation = 'MULTIPLY'

    math3 = node_tree.nodes.new(type='ShaderNodeMath')
    math3.inputs[1].default_value = 0.5
    math3.location = (360.0, 460.0)
    math3.operation = 'SUBTRACT'
    math3.use_clamp = True

    math4 = node_tree.nodes.new(type='ShaderNodeMath')
    math4.inputs[1].default_value = 2.0
    math4.location = (600.0, 460.0)
    math4.operation = 'MULTIPLY'

    rotationMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.label = "_n RotationMap"
    rotationMap.location = (-1900.0, 260.0)
    rotationMap.name = '_n'

    tangentN = node_tree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-1560.0, 260.0)
    tangentN.name = "tangentN"
    tangentN.node_tree = normal_and_alpha_from_swizzled_texture()
    tangentN.width = 400.0

    norMap = node_tree.nodes.new(type='ShaderNodeNormalMap')
    norMap.location = (-1060.0, 260.0)

    specLookup = node_tree.nodes.new(type='ShaderNodeGroup')
    specLookup.location = (-800.0, 260.0)
    specLookup.name = "hair"
    specLookup.node_tree = get_specular_lookup()
    specLookup.width = 240

    directionMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    directionMap.label = "DirectionMap"
    directionMap.location = (-460.0, 260.0)
    directionMap.name = 'directionMap'

    vMath1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-120.0, 260.0)
    vMath1.operation = 'MULTIPLY'

    mix1 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix1.location = (120.0, 260.0)

    vMath2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (360.0, 260.0)
    vMath2.operation = 'ADD'

    vMath3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (600.0, 260.0)
    vMath3.operation = 'ADD'

    diffuseBSDF = node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuseBSDF.inputs['Roughness'].default_value = 0.0
    diffuseBSDF.location = (840.0, 260.0)

    mixShader1 = node_tree.nodes.new(type='ShaderNodeMixShader')
    mixShader1.location = (1100.0, 260.0)

    addShader = node_tree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (1340.0, 260.0)

    mixShader2 = node_tree.nodes.new(type='ShaderNodeMixShader')
    mixShader2.location = (1580.0, 260.0)

    grpOut1 = node_tree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1820.0, 260.0)

    glossMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    glossMap.label = "_s GlossMap"
    glossMap.location = (-800.0, -80.0)
    glossMap.name = '_s'

    paletteMask = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMask.label = "_m PaletteMaskMap"
    paletteMask.location = (-800.0, -360.0)
    paletteMask.name = '_m'

    phongSpec = node_tree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (-460.0, -80.0)
    phongSpec.name = "GetPhongSpecular"
    phongSpec.node_tree = get_phong_specular()
    phongSpec.width = 220

    sepXYZ = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.location = (-120.0, -80.0)

    flushColor = node_tree.nodes.new(type='ShaderNodeGroup')
    flushColor.location = (-180.0, -360.0)
    flushColor.name = "GetFlushColor"
    flushColor.node_tree = get_flush_color()
    flushColor.width = 200

    vMath4 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (120.0, -80.0)
    vMath4.operation = 'MULTIPLY'

    glossyBSDF = node_tree.nodes.new(type='ShaderNodeBsdfGlossy')
    glossyBSDF.distribution = 'BECKMANN'
    glossyBSDF.inputs['Roughness'].default_value = 0.5
    glossyBSDF.location = (840.0, -80.0)

    emission = node_tree.nodes.new(type='ShaderNodeEmission')
    emission.location = (1100.0, -80.0)

    transparentBSDF = node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentBSDF.location = (1340.0, -80.0)

    # Add and place reroutes
    nr1 = node_tree.nodes.new(type='NodeReroute')
    nr1.location = (-120.0, 600.0)
    nr2 = node_tree.nodes.new(type='NodeReroute')
    nr2.location = (80.0, 600.0)
    nr3 = node_tree.nodes.new(type='NodeReroute')
    nr3.location = (80.0, 400.0)
    nr4 = node_tree.nodes.new(type='NodeReroute')
    nr4.location = (60.0, 500.0)
    nr5 = node_tree.nodes.new(type='NodeReroute')
    nr5.location = (60.0, 280.0)
    nr6 = node_tree.nodes.new(type='NodeReroute')
    nr6.location = (240.0, 280.0)
    nr7 = node_tree.nodes.new(type='NodeReroute')
    nr7.location = (-200.0, 280.0)
    nr8 = node_tree.nodes.new(type='NodeReroute')
    nr8.location = (-200.0, -420.0)
    nr9 = node_tree.nodes.new(type='NodeReroute')
    nr9.location = (780.0, 380.0)
    nr10 = node_tree.nodes.new(type='NodeReroute')
    nr10.location = (780.0, 280.0)
    nr11 = node_tree.nodes.new(type='NodeReroute')
    nr11.location = (980.0, 280.0)

    nr12 = node_tree.nodes.new(type='NodeReroute')
    nr12.location = (-1120.0, 160.0)
    nr13 = node_tree.nodes.new(type='NodeReroute')
    nr13.location = (-1120.0, 0.0)
    nr14 = node_tree.nodes.new(type='NodeReroute')
    nr14.location = (640.0, 0.0)
    nr15 = node_tree.nodes.new(type='NodeReroute')
    nr15.location = (840.0, 40.0)
    nr16 = node_tree.nodes.new(type='NodeReroute')
    nr16.location = (1400.0, 40.0)
    nr17 = node_tree.nodes.new(type='NodeReroute')
    nr17.location = (-1140.0, 160.0)
    nr18 = node_tree.nodes.new(type='NodeReroute')
    nr18.location = (-1140.0, -40.0)
    nr19 = node_tree.nodes.new(type='NodeReroute')
    nr19.location = (640.0, -40.0)
    nr20 = node_tree.nodes.new(type='NodeReroute')
    nr20.location = (840.0, -60.0)
    nr21 = node_tree.nodes.new(type='NodeReroute')
    nr21.location = (980.0, -60.0)
    nr22 = node_tree.nodes.new(type='NodeReroute')
    nr22.location = (-880.0, 180.0)
    nr23 = node_tree.nodes.new(type='NodeReroute')
    nr23.location = (-880.0, -20.0)
    nr24 = node_tree.nodes.new(type='NodeReroute')
    nr24.location = (-500.0, -20.0)
    nr25 = node_tree.nodes.new(type='NodeReroute')
    nr25.location = (-500.0, -160.0)
    nr26 = node_tree.nodes.new(type='NodeReroute')
    nr26.location = (-220.0, -20.0)
    nr27 = node_tree.nodes.new(type='NodeReroute')
    nr27.location = (-220.0, -460.0)
    nr28 = node_tree.nodes.new(type='NodeReroute')
    nr28.location = (640.0, -20.0)
    nr29 = node_tree.nodes.new(type='NodeReroute')
    nr29.location = (800.0, 160.0)
    nr30 = node_tree.nodes.new(type='NodeReroute')
    nr30.location = (800.0, -40.0)
    nr31 = node_tree.nodes.new(type='NodeReroute')
    nr31.location = (980.0, -40.0)
    nr32 = node_tree.nodes.new(type='NodeReroute')
    nr32.location = (800.0, -120.0)

    nr33 = node_tree.nodes.new(type='NodeReroute')
    nr33.location = (-460.0, -60.0)
    nr34 = node_tree.nodes.new(type='NodeReroute')
    nr34.location = (-180.0, -60.0)
    nr35 = node_tree.nodes.new(type='NodeReroute')
    nr35.location = (-180.0, 80.0)
    nr36 = node_tree.nodes.new(type='NodeReroute')
    nr36.location = (-460.0, -300.0)
    nr37 = node_tree.nodes.new(type='NodeReroute')
    nr37.location = (-260.0, -300.0)
    nr38 = node_tree.nodes.new(type='NodeReroute')
    nr38.location = (-120.0, -60.0)
    nr39 = node_tree.nodes.new(type='NodeReroute')
    nr39.location = (80.0, -60.0)
    nr40 = node_tree.nodes.new(type='NodeReroute')
    nr40.location = (80.0, 60.0)
    nr41 = node_tree.nodes.new(type='NodeReroute')
    nr41.location = (60.0, -80.0)
    nr42 = node_tree.nodes.new(type='NodeReroute')
    nr42.location = (60.0, 80.0)

    # Link nodes together
    node_tree.links.new(diffuseMap.outputs['Color'], gamma1.inputs['Color'])
    node_tree.links.new(diffuseMap.outputs['Alpha'], nr1.inputs[0])
    node_tree.links.new(diffuseMap.outputs['Alpha'], math1.inputs[0])
    node_tree.links.new(nr1.outputs[0], nr2.inputs[0])
    node_tree.links.new(gamma1.outputs['Color'], nr4.inputs[0])
    node_tree.links.new(math1.outputs['Value'], math2.inputs[1])
    node_tree.links.new(nr4.outputs[0], nr5.inputs[0])
    node_tree.links.new(nr2.outputs[0], nr3.inputs[0])
    node_tree.links.new(nr3.outputs[0], math2.inputs[0])
    node_tree.links.new(math2.outputs['Value'], math3.inputs[0])
    node_tree.links.new(math3.outputs['Value'], math4.inputs[0])
    node_tree.links.new(math4.outputs['Value'], nr9.inputs[0])
    node_tree.links.new(nr9.outputs[0], nr10.inputs[0])
    node_tree.links.new(nr10.outputs[0], nr11.inputs[0])
    node_tree.links.new(nr11.outputs[0], mixShader1.inputs['Fac'])

    node_tree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    node_tree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    node_tree.links.new(tangentN.outputs['Normal'], norMap.inputs['Color'])
    node_tree.links.new(tangentN.outputs['Alpha'], nr12.inputs[0])
    node_tree.links.new(tangentN.outputs['Emission Strength'], nr17.inputs[0])
    node_tree.links.new(nr12.outputs[0], nr13.inputs[0])
    node_tree.links.new(nr17.outputs[0], nr18.inputs[0])
    node_tree.links.new(nr13.outputs[0], nr14.inputs[0])
    node_tree.links.new(nr18.outputs[0], nr19.inputs[0])
    node_tree.links.new(norMap.outputs['Normal'], specLookup.inputs['Normal'])
    node_tree.links.new(norMap.outputs['Normal'], nr22.inputs[0])
    node_tree.links.new(nr22.outputs[0], nr23.inputs[0])
    node_tree.links.new(nr23.outputs[0], nr24.inputs[0])
    node_tree.links.new(specLookup.outputs['Vector'], directionMap.inputs['Vector'])
    node_tree.links.new(nr24.outputs[0], nr25.inputs[0])
    node_tree.links.new(nr24.outputs[0], nr26.inputs[0])
    node_tree.links.new(directionMap.outputs['Color'], vMath1.inputs[0])
    node_tree.links.new(nr26.outputs[0], nr27.inputs[0])
    node_tree.links.new(nr26.outputs[0], nr28.inputs[0])
    node_tree.links.new(nr7.outputs[0], nr8.inputs[0])
    node_tree.links.new(nr35.outputs[0], vMath1.inputs[1])
    node_tree.links.new(vMath1.outputs['Vector'], mix1.inputs['Color2'])
    node_tree.links.new(nr5.outputs[0], nr7.inputs[0])
    node_tree.links.new(nr5.outputs[0], nr6.inputs[0])
    node_tree.links.new(nr42.outputs[0], mix1.inputs['Fac'])
    node_tree.links.new(nr40.outputs[0], mix1.inputs['Color1'])
    node_tree.links.new(nr6.outputs[0], vMath2.inputs[0])
    node_tree.links.new(mix1.outputs['Color'], vMath2.inputs[1])
    node_tree.links.new(vMath2.outputs['Vector'], vMath3.inputs[0])
    node_tree.links.new(vMath3.outputs['Vector'], nr29.inputs[0])
    node_tree.links.new(nr14.outputs[0], nr15.inputs[0])
    node_tree.links.new(nr28.outputs[0], diffuseBSDF.inputs['Normal'])
    node_tree.links.new(nr28.outputs[0], glossyBSDF.inputs['Normal'])
    node_tree.links.new(nr19.outputs[0], nr20.inputs[0])
    node_tree.links.new(nr29.outputs[0], diffuseBSDF.inputs['Color'])
    node_tree.links.new(nr29.outputs[0], nr30.inputs[0])
    node_tree.links.new(nr30.outputs[0], nr31.inputs[0])
    node_tree.links.new(nr30.outputs[0], nr32.inputs[0])
    node_tree.links.new(nr32.outputs[0], glossyBSDF.inputs['Color'])
    node_tree.links.new(diffuseBSDF.outputs['BSDF'], mixShader1.inputs[1])
    node_tree.links.new(nr15.outputs[0], nr16.inputs[0])
    node_tree.links.new(nr20.outputs[0], nr21.inputs[0])
    node_tree.links.new(nr31.outputs[0], emission.inputs['Color'])
    node_tree.links.new(nr21.outputs[0], emission.inputs['Strength'])
    node_tree.links.new(mixShader1.outputs['Shader'], addShader.inputs[0])
    node_tree.links.new(addShader.outputs['Shader'], mixShader2.inputs[1])
    node_tree.links.new(nr16.outputs[0], mixShader2.inputs['Fac'])
    node_tree.links.new(mixShader2.outputs['Shader'], grpOut1.inputs['Shader'])

    node_tree.links.new(glossMap.outputs['Color'], nr33.inputs[0])
    node_tree.links.new(glossMap.outputs['Color'], phongSpec.inputs['Specular Color'])
    node_tree.links.new(glossMap.outputs['Alpha'], phongSpec.inputs['Specular Alpha'])
    node_tree.links.new(paletteMask.outputs['Color'], nr36.inputs[0])
    node_tree.links.new(nr25.outputs[0], phongSpec.inputs['Normal'])
    node_tree.links.new(nr25.outputs[0], phongSpec.inputs['-Normal'])
    node_tree.links.new(nr33.outputs[0], nr34.inputs[0])
    node_tree.links.new(phongSpec.outputs['Specular'], nr38.inputs[0])
    node_tree.links.new(nr36.outputs[0], nr37.inputs[0])
    node_tree.links.new(nr37.outputs[0], sepXYZ.inputs['Vector'])
    node_tree.links.new(nr27.outputs[0], flushColor.inputs['Normal'])
    node_tree.links.new(nr8.outputs[0], flushColor.inputs['Diffuse Color'])
    node_tree.links.new(nr34.outputs[0], nr35.inputs[0])
    node_tree.links.new(flushColor.outputs['Flush Color'], vMath4.inputs[1])
    node_tree.links.new(nr38.outputs[0], nr39.inputs[0])
    node_tree.links.new(sepXYZ.outputs['Y'], vMath4.inputs[0])
    node_tree.links.new(sepXYZ.outputs['Z'], nr41.inputs[0])
    node_tree.links.new(nr41.outputs[0], nr42.inputs[0])
    node_tree.links.new(nr39.outputs[0], nr40.inputs[0])
    node_tree.links.new(vMath4.outputs['Vector'], vMath3.inputs[1])
    node_tree.links.new(glossyBSDF.outputs['BSDF'], mixShader1.inputs[2])
    node_tree.links.new(emission.outputs['Emission'], addShader.inputs[1])
    node_tree.links.new(transparentBSDF.outputs['BSDF'], mixShader2.inputs[2])

    # Hide unlinked node sockets
    for node in node_tree.nodes:
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


def eye(node_tree):
    # type: (ShaderNodeTree) -> None
    from .node_group import (
        get_phong_specular,
        hue_pixel,
        negative_normal,
        normal_and_alpha_from_swizzled_texture,
    )

    # Add output socket to node tree
    add_output_socket_if_needed(node_tree)

    # Add and place nodes
    diffuseMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.inputs['Vector'].hide = True
    diffuseMap.label = '_d DiffuseMap'
    diffuseMap.location = (-1780.0, 300.0)
    diffuseMap.name = '_d'
    diffuseMap.outputs['Alpha'].hide = True

    paletteMaskMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMaskMap.inputs['Vector'].hide = True
    paletteMaskMap.label = '_m PaletteMaskMap'
    paletteMaskMap.location = (-1440.0, 300.0)
    paletteMaskMap.name = '_m'
    paletteMaskMap.outputs['Alpha'].hide = True

    paletteMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMap.inputs['Vector'].hide = True
    paletteMap.label = '_h PaletteMap'
    paletteMap.location = (-1100.0, 300.0)
    paletteMap.name = '_h'

    huePixel = node_tree.nodes.new(type='ShaderNodeGroup')
    huePixel.location = (-760.0, 300.0)
    huePixel.name = 'HuePixel'
    huePixel.node_tree = hue_pixel()
    huePixel.width = 180.0

    vMath1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.inputs[1].default_value = [1.2, 1.2, 1.2]
    vMath1.location = (-480.0, 300.0)
    vMath1.operation = 'MULTIPLY'

    vMath2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (-240.0, 300.0)
    vMath2.operation = 'MULTIPLY'

    phongSpec = node_tree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (0.0, 300.0)
    phongSpec.node_tree = get_phong_specular()
    phongSpec.inputs['MaxSpecPower'].default_value = 8.0
    phongSpec.width = 180.0

    vMath3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (280.0, 300.0)
    vMath3.operation = 'ADD'

    principled = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    if blender_version < 4.0:
        principled.inputs['Clearcoat'].default_value = 1.0
        principled.inputs['IOR'].default_value = 1.41
        principled.inputs['Roughness'].default_value = 1.0
        principled.inputs['Specular'].default_value = 0.0
        principled.location = (520.0, 300.0)
        for socket in principled.inputs:
            if socket.name not in ['Base Color', 'Clearcoat', 'IOR', 'Normal', 'Clearcoat Normal']:
                socket.hide = True
    else:
        principled.inputs['Coat Weight'].default_value = 0.25 # Per Blender 3.6 to 4.0 conversions
        principled.inputs['IOR'].default_value = 1.41
        principled.inputs['Roughness'].default_value = 1.0
        principled.inputs['Specular IOR Level'].default_value = 0.0
        principled.location = (520.0, 300.0)
        for socket in principled.inputs:
            if socket.name not in ['Base Color', 'Coat Weight', 'IOR', 'Normal', 'Coat Normal']:
                socket.hide = True
    addShader = node_tree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (860.0, 300.0)

    mixShader1 = node_tree.nodes.new(type='ShaderNodeMixShader')
    mixShader1.location = (1100.0, 300.0)

    grpOut1 = node_tree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1340.0, 300.0)

    glossMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    glossMap.inputs['Vector'].hide = True
    glossMap.label = '_s GlossMap'
    glossMap.location = (-1780.0, -100.0)
    glossMap.name = '_s'

    rotationMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.inputs['Vector'].hide = True
    rotationMap.label = '_n RotationMap'
    rotationMap.location = (-1440.0, -100.0)
    rotationMap.name = '_n'

    tangentN = node_tree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-1100.0, -100.0)
    tangentN.node_tree = normal_and_alpha_from_swizzled_texture()
    tangentN.width = 240.0

    negativeN = node_tree.nodes.new(type='ShaderNodeGroup')
    negativeN.location = (-760.0, -100.0)
    negativeN.node_tree = negative_normal()
    negativeN.width = 180.0

    negN = node_tree.nodes.new(type='ShaderNodeNormalMap')
    negN.location = (-480.0, 60.0)
    negN.width = 140.0

    N = node_tree.nodes.new(type='ShaderNodeNormalMap')
    N.location = (-240.0, 60.0)
    N.width = 140.0

    emissionShader = node_tree.nodes.new(type='ShaderNodeEmission')
    emissionShader.location = (520.0, 40.0)
    emissionShader.width = 240.0

    transparentBSDF = node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentBSDF.location = (860.0, 40.0)

    # Add and place reroutes
    nr1 = node_tree.nodes.new(type='NodeReroute')
    nr1.location = (-1440.0, 320.0)
    nr2 = node_tree.nodes.new(type='NodeReroute')
    nr2.location = (-780.0, 320.0)
    nr3 = node_tree.nodes.new(type='NodeReroute')
    nr3.location = (-780.0, 220.0)
    nr4 = node_tree.nodes.new(type='NodeReroute')
    nr4.location = (-1160.0, 220.0)
    nr5 = node_tree.nodes.new(type='NodeReroute')
    nr5.location = (-1160.0, 20.0)
    nr6 = node_tree.nodes.new(type='NodeReroute')
    nr6.location = (-860.0, 20.0)
    nr7 = node_tree.nodes.new(type='NodeReroute')
    nr7.location = (-540.0, 220.0)
    nr8 = node_tree.nodes.new(type='NodeReroute')
    nr8.location = (-540.0, 80.0)
    nr9 = node_tree.nodes.new(type='NodeReroute')
    nr9.location = (240.0, 80.0)
    nr10 = node_tree.nodes.new(type='NodeReroute')
    nr10.location = (240.0, 160.0)
    nr11 = node_tree.nodes.new(type='NodeReroute')
    nr11.location = (-480.0, 320.0)
    nr12 = node_tree.nodes.new(type='NodeReroute')
    nr12.location = (-280.0, 320.0)
    nr13 = node_tree.nodes.new(type='NodeReroute')
    nr13.location = (-280.0, 240.0)
    nr14 = node_tree.nodes.new(type='NodeReroute')
    nr14.location = (-240.0, 120.0)
    nr15 = node_tree.nodes.new(type='NodeReroute')
    nr15.location = (-100.0, 120.0)
    nr16 = node_tree.nodes.new(type='NodeReroute')
    nr16.location = (-40.0, 60.0)
    nr17 = node_tree.nodes.new(type='NodeReroute')
    nr17.location = (-40.0, 120.0)
    nr18 = node_tree.nodes.new(type='NodeReroute')
    nr18.location = (420.0, 60.0)
    nr19 = node_tree.nodes.new(type='NodeReroute')
    nr19.location = (460.0, 220.0)
    nr20 = node_tree.nodes.new(type='NodeReroute')
    nr20.location = (460.0, 120.0)
    nr21 = node_tree.nodes.new(type='NodeReroute')
    nr21.location = (460.0, 40.0)

    nr22 = node_tree.nodes.new(type='NodeReroute')
    nr22.location = (-1440.0, -60.0)
    nr23 = node_tree.nodes.new(type='NodeReroute')
    nr23.location = (-800.0, -60.0)
    nr24 = node_tree.nodes.new(type='NodeReroute')
    nr24.location = (-800.0, 120.0)
    nr25 = node_tree.nodes.new(type='NodeReroute')
    nr25.location = (-1440.0, -80.0)
    nr26 = node_tree.nodes.new(type='NodeReroute')
    nr26.location = (-820.0, -80.0)
    nr27 = node_tree.nodes.new(type='NodeReroute')
    nr27.location = (-820.0, 340.0)
    nr28 = node_tree.nodes.new(type='NodeReroute')
    nr28.location = (-40.0, 340.0)
    nr29 = node_tree.nodes.new(type='NodeReroute')
    nr29.location = (-40.0, 240.0)
    nr30 = node_tree.nodes.new(type='NodeReroute')
    nr30.location = (-760.0, -220.0)
    nr31 = node_tree.nodes.new(type='NodeReroute')
    nr31.location = (-480.0, -220.0)
    nr32 = node_tree.nodes.new(type='NodeReroute')
    nr32.location = (-760.0, -240.0)
    nr33 = node_tree.nodes.new(type='NodeReroute')
    nr33.location = (-100.0, -240.0)
    nr34 = node_tree.nodes.new(type='NodeReroute')
    nr34.location = (520.0, 60.0)
    nr35 = node_tree.nodes.new(type='NodeReroute')
    nr35.location = (860.0, 60.0)
    nr36 = node_tree.nodes.new(type='NodeReroute')
    nr36.location = (-760.0, -260.0)
    nr37 = node_tree.nodes.new(type='NodeReroute')
    nr37.location = (-100.0, -260.0)

    # Link nodes together
    node_tree.links.new(diffuseMap.outputs['Color'], nr1.inputs[0])
    node_tree.links.new(nr1.outputs[0], nr2.inputs[0])
    node_tree.links.new(nr2.outputs[0], nr3.inputs[0])
    node_tree.links.new(nr3.outputs[0], huePixel.inputs['_d DiffuseMap Color'])
    node_tree.links.new(paletteMaskMap.outputs['Color'], nr4.inputs[0])
    node_tree.links.new(nr4.outputs[0], nr5.inputs[0])
    node_tree.links.new(nr5.outputs[0], nr6.inputs[0])
    node_tree.links.new(nr6.outputs[0], huePixel.inputs['_m PaletteMaskMap Color'])
    node_tree.links.new(paletteMap.outputs['Color'], huePixel.inputs['_h PaletteMap Color'])
    node_tree.links.new(paletteMap.outputs['Alpha'], huePixel.inputs['_h PaletteMap Alpha'])
    node_tree.links.new(huePixel.outputs['Diffuse Color'], vMath1.inputs[0])
    node_tree.links.new(huePixel.outputs['Diffuse Color'], nr7.inputs[0])
    node_tree.links.new(nr7.outputs[0], nr8.inputs[0])
    node_tree.links.new(nr8.outputs[0], nr9.inputs[0])
    node_tree.links.new(nr9.outputs[0], nr10.inputs[0])
    node_tree.links.new(nr10.outputs[0], vMath3.inputs[0])
    node_tree.links.new(huePixel.outputs['Specular Color'], nr11.inputs[0])
    node_tree.links.new(nr11.outputs[0], nr12.inputs[0])
    node_tree.links.new(nr12.outputs[0], nr13.inputs[0])
    node_tree.links.new(nr13.outputs[0], vMath2.inputs[1])
    node_tree.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    node_tree.links.new(vMath2.outputs['Vector'], phongSpec.inputs['Specular Color'])
    node_tree.links.new(phongSpec.outputs['Specular'], vMath3.inputs[1])
    node_tree.links.new(vMath3.outputs['Vector'], nr19.inputs[0])
    node_tree.links.new(nr19.outputs[0], nr20.inputs[0])
    node_tree.links.new(nr20.outputs[0], principled.inputs['Base Color'])
    node_tree.links.new(nr20.outputs[0], nr21.inputs[0])
    node_tree.links.new(nr21.outputs[0], emissionShader.inputs['Color'])
    node_tree.links.new(principled.outputs['BSDF'], addShader.inputs[0])
    node_tree.links.new(addShader.outputs['Shader'], mixShader1.inputs[1])
    node_tree.links.new(mixShader1.outputs['Shader'], grpOut1.inputs['Shader'])

    node_tree.links.new(glossMap.outputs['Color'], nr22.inputs[0])
    node_tree.links.new(nr22.outputs[0], nr23.inputs[0])
    node_tree.links.new(nr23.outputs[0], nr24.inputs[0])
    node_tree.links.new(nr24.outputs[0], huePixel.inputs['_s GlossMap Color'])
    node_tree.links.new(glossMap.outputs['Alpha'], nr25.inputs[0])
    node_tree.links.new(nr25.outputs[0], nr26.inputs[0])
    node_tree.links.new(nr26.outputs[0], nr27.inputs[0])
    node_tree.links.new(nr27.outputs[0], nr28.inputs[0])
    node_tree.links.new(nr28.outputs[0], nr29.inputs[0])
    node_tree.links.new(nr29.outputs[0], phongSpec.inputs['Specular Alpha'])
    node_tree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    node_tree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    node_tree.links.new(tangentN.outputs['Normal'], negativeN.inputs['Normal'])
    node_tree.links.new(negativeN.outputs['-Normal'], negN.inputs['Color'])
    node_tree.links.new(negN.outputs['Normal'], nr14.inputs[0])
    node_tree.links.new(nr14.outputs[0], nr15.inputs[0])
    node_tree.links.new(nr15.outputs[0], phongSpec.inputs['-Normal'])
    node_tree.links.new(tangentN.outputs['Normal'], nr30.inputs[0])
    node_tree.links.new(nr30.outputs[0], nr31.inputs[0])
    node_tree.links.new(nr31.outputs[0], N.inputs['Color'])
    node_tree.links.new(N.outputs['Normal'], nr16.inputs[0])
    node_tree.links.new(nr16.outputs[0], nr17.inputs[0])
    node_tree.links.new(nr17.outputs[0], phongSpec.inputs['Normal'])
    node_tree.links.new(nr16.outputs[0], nr18.inputs[0])
    node_tree.links.new(nr18.outputs[0], principled.inputs['Normal'])
    if blender_version < 4.0:
        node_tree.links.new(nr18.outputs[0], principled.inputs['Clearcoat Normal'])
    else:
        node_tree.links.new(nr18.outputs[0], principled.inputs['Coat Normal'])
    node_tree.links.new(tangentN.outputs['Alpha'], nr32.inputs[0])
    node_tree.links.new(nr32.outputs[0], nr33.inputs[0])
    node_tree.links.new(nr33.outputs[0], nr34.inputs[0])
    node_tree.links.new(nr34.outputs[0], nr35.inputs[0])
    node_tree.links.new(nr35.outputs[0], mixShader1.inputs['Fac'])
    node_tree.links.new(tangentN.outputs['Emission Strength'], nr36.inputs[0])
    node_tree.links.new(nr36.outputs[0], nr37.inputs[0])
    node_tree.links.new(nr37.outputs[0], emissionShader.inputs['Strength'])
    node_tree.links.new(emissionShader.outputs['Emission'], addShader.inputs[1])
    node_tree.links.new(transparentBSDF.outputs['BSDF'], mixShader1.inputs[2])


def garment(node_tree):
    # type: (ShaderNodeTree) -> None
    from .node_group import (
        chosen_palette,
        get_phong_specular,
        hue_pixel,
        normal_and_alpha_from_swizzled_texture,
    )

    # Add output socket to node tree
    add_output_socket_if_needed(node_tree)

    # Add and place nodes
    diffuseMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.inputs['Vector'].hide = True
    diffuseMap.location = (-1220.0, 540.0)
    diffuseMap.name = '_d'
    diffuseMap.outputs['Alpha'].hide = True

    glossMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    glossMap.inputs['Vector'].hide = True
    glossMap.location = (-880.0, 540.0)
    glossMap.name = '_s'

    huePixel = node_tree.nodes.new(type='ShaderNodeGroup')
    huePixel.location = (-500.0, 360.0)
    huePixel.name = 'HuePixel'
    huePixel.node_tree = hue_pixel()
    huePixel.width = 180.0

    phongSpec = node_tree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (-220.0, 360.0)
    phongSpec.name = 'GetPhongSpecular'
    phongSpec.node_tree = get_phong_specular()
    phongSpec.width = 220

    vMath1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (100.0, 360.0)
    vMath1.operation = 'ADD'

    diffuseBSDF = node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuseBSDF.inputs['Roughness'].default_value = 0.0
    # diffuseBSDF.inputs['Roughness'].hide = True
    diffuseBSDF.location = (340.0, 360.0)

    addShader = node_tree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (600.0, 360.0)

    mixShader = node_tree.nodes.new(type='ShaderNodeMixShader')
    mixShader.location = (840.0, 360.0)

    grpOut1 = node_tree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1080.0, 360.0)

    paletteMaskMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMaskMap.inputs['Vector'].hide = True
    paletteMaskMap.location = (-1220.0, 180.0)
    paletteMaskMap.name = '_m'
    paletteMaskMap.outputs['Alpha'].hide = True

    chosenPalette = node_tree.nodes.new(type='ShaderNodeGroup')
    chosenPalette.location = (-880.0, 180.0)
    chosenPalette.name = 'ChosenPalette'
    chosenPalette.node_tree = chosen_palette()
    chosenPalette.width = 240.0

    emissionShader = node_tree.nodes.new(type='ShaderNodeEmission')
    emissionShader.location = (340.0, 180.0)

    transparentShader = node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentShader.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentShader.location = (600.0, 180.0)

    paletteMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMap.inputs['Vector'].hide = True
    paletteMap.location = (-1220.0, -60.0)
    paletteMap.name = '_h'

    norMap = node_tree.nodes.new(type='ShaderNodeNormalMap')
    norMap.location = (-500.0, -60.0)
    norMap.width = 180

    rotationMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.inputs['Vector'].hide = True
    rotationMap.location = (-1220.0, -320.0)
    rotationMap.name = '_n'

    tangentN = node_tree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-880.0, -320.0)
    tangentN.node_tree = normal_and_alpha_from_swizzled_texture()
    tangentN.width = 280

    # Add and place reroutes
    nr1 = node_tree.nodes.new(type='NodeReroute')
    nr1.location = (-940.0, 460.0)
    nr2 = node_tree.nodes.new(type='NodeReroute')
    nr2.location = (-940.0, 260.0)
    nr3 = node_tree.nodes.new(type='NodeReroute')
    nr3.location = (-640.0, 260.0)
    nr4 = node_tree.nodes.new(type='NodeReroute')
    nr4.location = (-580.0, 420.0)
    nr5 = node_tree.nodes.new(type='NodeReroute')
    nr5.location = (-580.0, 380.0)
    nr6 = node_tree.nodes.new(type='NodeReroute')
    nr6.location = (-280.0, 380.0)
    nr7 = node_tree.nodes.new(type='NodeReroute')
    nr7.location = (-280.0, 320.0)
    nr8 = node_tree.nodes.new(type='NodeReroute')
    nr8.location = (-560.0, 420.0)
    nr9 = node_tree.nodes.new(type='NodeReroute')
    nr9.location = (-560.0, 300.0)
    nr10 = node_tree.nodes.new(type='NodeReroute')
    nr10.location = (-940.0, -40.0)
    nr11 = node_tree.nodes.new(type='NodeReroute')
    nr11.location = (-940.0, 240.0)
    nr12 = node_tree.nodes.new(type='NodeReroute')
    nr12.location = (-640.0, 240.0)
    nr13 = node_tree.nodes.new(type='NodeReroute')
    nr13.location = (-920.0, -40.0)
    nr14 = node_tree.nodes.new(type='NodeReroute')
    nr14.location = (-920.0, 220.0)
    nr15 = node_tree.nodes.new(type='NodeReroute')
    nr15.location = (-640.0, 220.0)
    nr16 = node_tree.nodes.new(type='NodeReroute')
    nr16.location = (-900.0, 200.0)
    nr17 = node_tree.nodes.new(type='NodeReroute')
    nr17.location = (-640.0, 200.0)
    nr18 = node_tree.nodes.new(type='NodeReroute')
    nr18.location = (-220.0, 380.0)
    nr19 = node_tree.nodes.new(type='NodeReroute')
    nr19.location = (60.0, 380.0)
    nr20 = node_tree.nodes.new(type='NodeReroute')
    nr20.location = (60.0, 320.0)
    nr21 = node_tree.nodes.new(type='NodeReroute')
    nr21.location = (300.0, 260.0)
    nr22 = node_tree.nodes.new(type='NodeReroute')
    nr22.location = (300.0, 160.0)
    nr23 = node_tree.nodes.new(type='NodeReroute')
    nr23.location = (-260.0, -20.0)
    nr24 = node_tree.nodes.new(type='NodeReroute')
    nr24.location = (-260.0, 160.0)
    nr25 = node_tree.nodes.new(type='NodeReroute')
    nr25.location = (240.0, 160.0)
    nr26 = node_tree.nodes.new(type='NodeReroute')
    nr26.location = (-500.0, -280.0)
    nr27 = node_tree.nodes.new(type='NodeReroute')
    nr27.location = (-240.0, -280.0)
    nr28 = node_tree.nodes.new(type='NodeReroute')
    nr28.location = (-240.0, 140.0)
    nr29 = node_tree.nodes.new(type='NodeReroute')
    nr29.location = (240.0, 140.0)
    nr30 = node_tree.nodes.new(type='NodeReroute')
    nr30.location = (340.0, 220.0)
    nr31 = node_tree.nodes.new(type='NodeReroute')
    nr31.location = (720.0, 220.0)
    nr32 = node_tree.nodes.new(type='NodeReroute')
    nr32.location = (-500.0, -300.0)
    nr33 = node_tree.nodes.new(type='NodeReroute')
    nr33.location = (-220.0, -300.0)
    nr34 = node_tree.nodes.new(type='NodeReroute')
    nr34.location = (-220.0, 120.0)
    nr35 = node_tree.nodes.new(type='NodeReroute')
    nr35.location = (240.0, 120.0)

    # Link nodes together
    node_tree.links.new(diffuseMap.outputs['Color'], nr1.inputs[0])
    node_tree.links.new(nr1.outputs[0], nr2.inputs[0])
    node_tree.links.new(nr2.outputs[0], nr3.inputs[0])
    node_tree.links.new(nr3.outputs[0], huePixel.inputs['_d DiffuseMap Color'])
    node_tree.links.new(glossMap.outputs['Color'], nr8.inputs[0])
    node_tree.links.new(nr8.outputs[0], nr9.inputs[0])
    node_tree.links.new(nr9.outputs[0], huePixel.inputs['_s GlossMap Color'])
    node_tree.links.new(glossMap.outputs['Alpha'], nr4.inputs[0])
    node_tree.links.new(nr4.outputs[0], nr5.inputs[0])
    node_tree.links.new(nr5.outputs[0], nr6.inputs[0])
    node_tree.links.new(nr6.outputs[0], nr7.inputs[0])
    node_tree.links.new(nr7.outputs[0], phongSpec.inputs['Specular Alpha'])
    node_tree.links.new(paletteMap.outputs['Color'], nr10.inputs[0])
    node_tree.links.new(nr10.outputs[0], nr11.inputs[0])
    node_tree.links.new(nr11.outputs[0], nr12.inputs[0])
    node_tree.links.new(nr12.outputs[0], huePixel.inputs['_h PaletteMap Color'])
    node_tree.links.new(paletteMap.outputs['Alpha'], nr13.inputs[0])
    node_tree.links.new(nr13.outputs[0], nr14.inputs[0])
    node_tree.links.new(nr14.outputs[0], nr15.inputs[0])
    node_tree.links.new(nr15.outputs[0], huePixel.inputs['_h PaletteMap Alpha'])
    node_tree.links.new(paletteMaskMap.outputs['Color'], nr16.inputs[0])
    node_tree.links.new(paletteMaskMap.outputs['Color'], chosenPalette.inputs['_m PaletteMaskMap Color'])
    node_tree.links.new(nr16.outputs[0], nr17.inputs[0])
    node_tree.links.new(nr17.outputs[0], huePixel.inputs['_m PaletteMaskMap Color'])
    node_tree.links.new(huePixel.outputs['Diffuse Color'], nr18.inputs[0])
    node_tree.links.new(huePixel.outputs['Specular Color'], phongSpec.inputs['Specular Color'])
    node_tree.links.new(nr18.outputs[0], nr19.inputs[0])
    node_tree.links.new(nr19.outputs[0], nr20.inputs[0])
    node_tree.links.new(nr20.outputs[0], vMath1.inputs[0])
    node_tree.links.new(phongSpec.outputs['Specular'], vMath1.inputs[1])
    node_tree.links.new(vMath1.outputs['Vector'], nr21.inputs[0])
    node_tree.links.new(nr21.outputs[0], diffuseBSDF.inputs['Color'])
    node_tree.links.new(nr21.outputs[0], nr22.inputs[0])
    node_tree.links.new(nr22.outputs[0], emissionShader.inputs['Color'])
    node_tree.links.new(diffuseBSDF.outputs['BSDF'], addShader.inputs[0])
    node_tree.links.new(addShader.outputs['Shader'], mixShader.inputs[1])
    node_tree.links.new(mixShader.outputs['Shader'], grpOut1.inputs['Shader'])
    node_tree.links.new(chosenPalette.outputs['Hue'], huePixel.inputs['Hue'])
    node_tree.links.new(chosenPalette.outputs['Saturation'], huePixel.inputs['Saturation'])
    node_tree.links.new(chosenPalette.outputs['Brightness'], huePixel.inputs['Brightness'])
    node_tree.links.new(chosenPalette.outputs['Contrast'], huePixel.inputs['Contrast'])
    node_tree.links.new(chosenPalette.outputs['Specular'], huePixel.inputs['Specular'])
    node_tree.links.new(chosenPalette.outputs['Metallic Specular'], huePixel.inputs['Metallic Specular'])
    node_tree.links.new(emissionShader.outputs['Emission'], addShader.inputs[1])
    node_tree.links.new(transparentShader.outputs['BSDF'], mixShader.inputs[2])
    node_tree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    node_tree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    node_tree.links.new(tangentN.outputs['Normal'], norMap.inputs['Color'])
    node_tree.links.new(norMap.outputs['Normal'], nr23.inputs[0])
    node_tree.links.new(nr23.outputs[0], nr24.inputs[0])
    node_tree.links.new(nr24.outputs[0], phongSpec.inputs['Normal'])
    node_tree.links.new(nr24.outputs[0], phongSpec.inputs['-Normal'])
    node_tree.links.new(nr24.outputs[0], nr25.inputs[0])
    node_tree.links.new(nr25.outputs[0], diffuseBSDF.inputs['Normal'])
    node_tree.links.new(tangentN.outputs['Alpha'], nr26.inputs[0])
    node_tree.links.new(nr26.outputs[0], nr27.inputs[0])
    node_tree.links.new(nr27.outputs[0], nr28.inputs[0])
    node_tree.links.new(nr28.outputs[0], nr29.inputs[0])
    node_tree.links.new(nr29.outputs[0], nr30.inputs[0])
    node_tree.links.new(nr30.outputs[0], nr31.inputs[0])
    node_tree.links.new(nr31.outputs[0], mixShader.inputs['Fac'])
    node_tree.links.new(tangentN.outputs['Emission Strength'], nr32.inputs[0])
    node_tree.links.new(nr32.outputs[0], nr33.inputs[0])
    node_tree.links.new(nr33.outputs[0], nr34.inputs[0])
    node_tree.links.new(nr34.outputs[0], nr35.inputs[0])
    node_tree.links.new(nr35.outputs[0], emissionShader.inputs['Strength'])


def hairc(node_tree):
    # type: (ShaderNodeTree) -> None
    from .node_group import (
        get_phong_specular,
        get_specular_lookup,
        hue_pixel,
        normal_and_alpha_from_swizzled_texture,
    )

    # Add output socket to node tree
    add_output_socket_if_needed(node_tree)

    # Add and place nodes
    diffuseMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.inputs['Vector'].hide = True
    diffuseMap.label = '_d DiffuseMap'
    diffuseMap.location = (-1520.0, 380.0)
    diffuseMap.name = '_d'
    diffuseMap.outputs['Alpha'].hide = True

    paletteMaskMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMaskMap.inputs['Vector'].hide = True
    paletteMaskMap.label = '_m PaletteMaskMap'
    paletteMaskMap.location = (-1180.0, 380.0)
    paletteMaskMap.name = '_m'
    paletteMaskMap.outputs['Alpha'].hide = True

    paletteMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMap.inputs['Vector'].hide = True
    paletteMap.label = '_h PaletteMap'
    paletteMap.location = (-840.0, 380.0)
    paletteMap.name = '_h'

    sepXYZ = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    sepXYZ.location = (-440.0, 500.0)
    sepXYZ.outputs['X'].hide = True
    sepXYZ.outputs['Y'].hide = True
    sepXYZ.width = 180.0

    huePixel = node_tree.nodes.new(type='ShaderNodeGroup')
    huePixel.location = (-440.0, 380.0)
    huePixel.name = 'HuePixel'
    huePixel.node_tree = hue_pixel()
    huePixel.width = 180.0

    phongSpec = node_tree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (-160.0, 380.0)
    phongSpec.node_tree = get_phong_specular()
    phongSpec.width = 180.0

    mixRGB = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mixRGB.location = (160.0, 380.0)

    vMath1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (400.0, 380.0)
    vMath1.operation = 'ADD'

    diffuseBSDF = node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuseBSDF.location = (640.0, 380.0)

    addShader = node_tree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (900.0, 380.0)

    mixShader = node_tree.nodes.new(type='ShaderNodeMixShader')
    mixShader.location = (1140.0, 380.0)

    grpOut1 = node_tree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1380.0, 380.0)

    rotationMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.inputs['Vector'].hide = True
    rotationMap.label = '_n RotationMap'
    rotationMap.location = (-1520.0, 0.0)
    rotationMap.name = '_n'

    tangentN = node_tree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-1180.0, 0.0)
    tangentN.node_tree = normal_and_alpha_from_swizzled_texture()

    norMap = node_tree.nodes.new(type='ShaderNodeNormalMap')
    norMap.location = (-940.0, -320.0)

    specLookup = node_tree.nodes.new(type='ShaderNodeGroup')
    specLookup.location = (-740.0, -320.0)
    specLookup.node_tree = get_specular_lookup()

    glossMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    glossMap.inputs['Vector'].hide = True
    glossMap.label = '_s GlossMap'
    glossMap.location = (-840.0, 0.0)
    glossMap.name = '_s'

    directionMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    directionMap.label = 'DirectionMap'
    directionMap.location = (-500.0, 0.0)
    directionMap.name = 'directionMap'
    directionMap.outputs['Alpha'].hide = True

    vMath2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (-160.0, 180.0)
    vMath2.operation = 'MULTIPLY'

    emission = node_tree.nodes.new(type='ShaderNodeEmission')
    emission.location = (640.0, 160.0)

    transparentBSDF = node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.location = (900.0, 160.0)

    # Add and place reroutes
    nr1 = node_tree.nodes.new(type='NodeReroute')
    nr1.location = (-1240.0, 300.0)
    nr2 = node_tree.nodes.new(type='NodeReroute')
    nr2.location = (-1240.0, 100.0)
    nr3 = node_tree.nodes.new(type='NodeReroute')
    nr3.location = (-480.0, 100.0)
    nr4 = node_tree.nodes.new(type='NodeReroute')
    nr4.location = (-480.0, 220.0)
    nr5 = node_tree.nodes.new(type='NodeReroute')
    nr5.location = (-840.0, 400.0)
    nr6 = node_tree.nodes.new(type='NodeReroute')
    nr6.location = (-500.0, 400.0)
    nr7 = node_tree.nodes.new(type='NodeReroute')
    nr7.location = (-500.0, 260.0)
    nr8 = node_tree.nodes.new(type='NodeReroute')
    nr8.location = (-160.0, 420.0)
    nr9 = node_tree.nodes.new(type='NodeReroute')
    nr9.location = (120.0, 420.0)
    nr10 = node_tree.nodes.new(type='NodeReroute')
    nr10.location = (120.0, 320.0)
    nr11 = node_tree.nodes.new(type='NodeReroute')
    nr11.location = (-160.0, 400.0)
    nr12 = node_tree.nodes.new(type='NodeReroute')
    nr12.location = (360.0, 400.0)
    nr13 = node_tree.nodes.new(type='NodeReroute')
    nr13.location = (360.0, 340.0)
    nr14 = node_tree.nodes.new(type='NodeReroute')
    nr14.location = (-180.0, 260.0)
    nr15 = node_tree.nodes.new(type='NodeReroute')
    nr15.location = (-180.0, 120.0)
    nr16 = node_tree.nodes.new(type='NodeReroute')
    nr16.location = (600.0, 280.0)
    nr17 = node_tree.nodes.new(type='NodeReroute')
    nr17.location = (600.0, 140.0)

    nr18 = node_tree.nodes.new(type='NodeReroute')
    nr18.location = (-1020.0, -100.0)
    nr19 = node_tree.nodes.new(type='NodeReroute')
    nr19.location = (-1020.0, -300.0)
    nr20 = node_tree.nodes.new(type='NodeReroute')
    nr20.location = (-200.0, -300.0)
    nr21 = node_tree.nodes.new(type='NodeReroute')
    nr21.location = (540.0, 160.0)
    nr22 = node_tree.nodes.new(type='NodeReroute')
    nr22.location = (-1000.0, -100.0)
    nr23 = node_tree.nodes.new(type='NodeReroute')
    nr23.location = (-1000.0, -280.0)
    nr24 = node_tree.nodes.new(type='NodeReroute')
    nr24.location = (-200.0, -280.0)
    nr25 = node_tree.nodes.new(type='NodeReroute')
    nr25.location = (540.0, 180.0)
    nr26 = node_tree.nodes.new(type='NodeReroute')
    nr26.location = (660.0, 200.0)
    nr27 = node_tree.nodes.new(type='NodeReroute')
    nr27.location = (1000.0, 200.0)
    nr28 = node_tree.nodes.new(type='NodeReroute')
    nr28.location = (-980.0, -100.0)
    nr29 = node_tree.nodes.new(type='NodeReroute')
    nr29.location = (-980.0, -400.0)
    nr30 = node_tree.nodes.new(type='NodeReroute')
    nr30.location = (-680.0, -260.0)
    nr31 = node_tree.nodes.new(type='NodeReroute')
    nr31.location = (-200.0, -260.0)
    nr32 = node_tree.nodes.new(type='NodeReroute')
    nr32.location = (-200.0, 200.0)
    nr33 = node_tree.nodes.new(type='NodeReroute')
    nr33.location = (540.0, 200.0)
    nr34 = node_tree.nodes.new(type='NodeReroute')
    nr34.location = (-560.0, 20.0)
    nr35 = node_tree.nodes.new(type='NodeReroute')
    nr35.location = (-560.0, 120.0)
    nr36 = node_tree.nodes.new(type='NodeReroute')
    nr36.location = (-500.0, 20.0)
    nr37 = node_tree.nodes.new(type='NodeReroute')
    nr37.location = (-220.0, 20.0)
    nr38 = node_tree.nodes.new(type='NodeReroute')
    nr38.location = (-220.0, 200.0)

    # Link nodes together
    node_tree.links.new(diffuseMap.outputs['Color'], nr1.inputs[0])
    node_tree.links.new(nr1.outputs[0], nr2.inputs[0])
    node_tree.links.new(nr2.outputs[0], nr3.inputs[0])
    node_tree.links.new(nr3.outputs[0], nr4.inputs[0])
    node_tree.links.new(nr4.outputs[0], huePixel.inputs['_d DiffuseMap Color'])
    node_tree.links.new(paletteMaskMap.outputs['Color'], nr5.inputs[0])
    node_tree.links.new(nr5.outputs[0], nr6.inputs[0])
    node_tree.links.new(nr6.outputs[0], sepXYZ.inputs['Vector'])
    node_tree.links.new(nr6.outputs[0], nr7.inputs[0])
    node_tree.links.new(nr7.outputs[0], huePixel.inputs['_m PaletteMaskMap Color'])
    node_tree.links.new(paletteMap.outputs['Color'], huePixel.inputs['_h PaletteMap Color'])
    node_tree.links.new(paletteMap.outputs['Alpha'], huePixel.inputs['_h PaletteMap Alpha'])
    node_tree.links.new(sepXYZ.outputs['Z'], nr8.inputs[0])
    node_tree.links.new(nr8.outputs[0], nr9.inputs[0])
    node_tree.links.new(nr9.outputs[0], nr10.inputs[0])
    node_tree.links.new(nr10.outputs[0], mixRGB.inputs['Fac'])
    node_tree.links.new(huePixel.outputs['Diffuse Color'], nr11.inputs[0])
    node_tree.links.new(nr11.outputs[0], nr12.inputs[0])
    node_tree.links.new(nr12.outputs[0], nr13.inputs[0])
    node_tree.links.new(nr13.outputs[0], vMath1.inputs[0])
    node_tree.links.new(huePixel.outputs['Specular Color'], nr14.inputs[0])
    node_tree.links.new(nr14.outputs[0], phongSpec.inputs['Specular Color'])
    node_tree.links.new(nr14.outputs[0], nr15.inputs[0])
    node_tree.links.new(nr15.outputs[0], vMath2.inputs[0])
    node_tree.links.new(phongSpec.outputs['Specular'], mixRGB.inputs['Color1'])
    node_tree.links.new(mixRGB.outputs['Color'], vMath1.inputs[1])
    node_tree.links.new(vMath1.outputs['Vector'], nr16.inputs[0])
    node_tree.links.new(nr16.outputs[0], diffuseBSDF.inputs['Color'])
    node_tree.links.new(nr16.outputs[0], nr17.inputs[0])
    node_tree.links.new(nr17.outputs[0], emission.inputs['Color'])
    node_tree.links.new(diffuseBSDF.outputs['BSDF'], addShader.inputs[0])
    node_tree.links.new(addShader.outputs['Shader'], mixShader.inputs[1])
    node_tree.links.new(mixShader.outputs['Shader'], grpOut1.inputs['Shader'])

    node_tree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    node_tree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    node_tree.links.new(tangentN.outputs['Emission Strength'], nr18.inputs[0])
    node_tree.links.new(nr18.outputs[0], nr19.inputs[0])
    node_tree.links.new(nr19.outputs[0], nr20.inputs[0])
    node_tree.links.new(nr20.outputs[0], nr21.inputs[0])
    node_tree.links.new(nr21.outputs[0], emission.inputs['Strength'])
    node_tree.links.new(tangentN.outputs['Alpha'], nr22.inputs[0])
    node_tree.links.new(nr22.outputs[0], nr23.inputs[0])
    node_tree.links.new(nr23.outputs[0], nr24.inputs[0])
    node_tree.links.new(nr24.outputs[0], nr25.inputs[0])
    node_tree.links.new(nr25.outputs[0], nr26.inputs[0])
    node_tree.links.new(nr26.outputs[0], nr27.inputs[0])
    node_tree.links.new(nr27.outputs[0], mixShader.inputs['Fac'])
    node_tree.links.new(tangentN.outputs['Normal'], nr28.inputs[0])
    node_tree.links.new(nr28.outputs[0], nr29.inputs[0])
    node_tree.links.new(nr29.outputs[0], norMap.inputs['Color'])
    node_tree.links.new(norMap.outputs['Normal'], nr30.inputs[0])
    node_tree.links.new(nr30.outputs[0], nr31.inputs[0])
    node_tree.links.new(nr31.outputs[0], nr32.inputs[0])
    node_tree.links.new(nr32.outputs[0], phongSpec.inputs['Normal'])
    node_tree.links.new(nr32.outputs[0], phongSpec.inputs['-Normal'])
    node_tree.links.new(nr31.outputs[0], nr33.inputs[0])
    node_tree.links.new(nr33.outputs[0], diffuseBSDF.inputs['Normal'])
    node_tree.links.new(norMap.outputs['Normal'], specLookup.inputs['Normal'])
    node_tree.links.new(specLookup.outputs['Vector'], directionMap.inputs['Vector'])
    node_tree.links.new(directionMap.outputs['Color'], vMath2.inputs[1])
    node_tree.links.new(vMath2.outputs['Vector'], mixRGB.inputs['Color2'])
    node_tree.links.new(glossMap.outputs['Color'], nr34.inputs[0])
    node_tree.links.new(nr34.outputs[0], nr35.inputs[0])
    node_tree.links.new(nr35.outputs[0], huePixel.inputs['_s GlossMap Color'])
    node_tree.links.new(glossMap.outputs['Alpha'], nr36.inputs[0])
    node_tree.links.new(nr36.outputs[0], nr37.inputs[0])
    node_tree.links.new(nr37.outputs[0], nr38.inputs[0])
    node_tree.links.new(nr38.outputs[0], phongSpec.inputs['Specular Alpha'])
    node_tree.links.new(emission.outputs['Emission'], addShader.inputs[1])
    node_tree.links.new(transparentBSDF.outputs['BSDF'], mixShader.inputs[2])


def skinb(node_tree):
    # type: (ShaderNodeTree) -> None
    from .node_group import (
        combine_normals,
        extract_age_normal_and_scar_from_swizzled_texture,
        get_flush_color,
        get_phong_specular,
        hue_skin_pixel,
        normal_and_alpha_from_swizzled_texture,
    )

    # Add output socket to node tree
    add_output_socket_if_needed(node_tree)

    # Add and place nodes
    glossMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    glossMap.inputs['Vector'].hide = True
    glossMap.label = '_s GlossMap'
    glossMap.location = (-1940.0, 460.0)
    glossMap.name = '_s'

    paletteMaskMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMaskMap.inputs['Vector'].hide = True
    paletteMaskMap.label = '_m PaletteMaskMap'
    paletteMaskMap.location = (-1600.0, 460.0)
    paletteMaskMap.name = '_m'
    paletteMaskMap.outputs['Alpha'].hide = True

    paletteMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    paletteMap.inputs['Vector'].hide = True
    paletteMap.label = '_h PaletteMap'
    paletteMap.location = (-1260.0, 460.0)
    paletteMap.name = '_h'

    huePixel = node_tree.nodes.new(type='ShaderNodeGroup')
    huePixel.location = (-920.0, 460.0)
    huePixel.name = 'HueSkinPixel'
    huePixel.node_tree = hue_skin_pixel()
    huePixel.width = 240.0

    phongSpec = node_tree.nodes.new(type='ShaderNodeGroup')
    phongSpec.location = (-580.0, 460.0)
    phongSpec.node_tree = get_phong_specular()

    vMath1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-340.0, 460.0)
    vMath1.operation = 'MULTIPLY'

    vMath2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.location = (-100.0, 460.0)
    vMath2.operation = 'MULTIPLY'

    mixRGB = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mixRGB.inputs['Fac'].default_value = 0.0
    mixRGB.location = (140.0, 460.0)

    vMath3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (380.0, 460.0)
    vMath3.operation = 'ADD'

    vMath4 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (620.0, 460.0)
    vMath4.operation = 'ADD'

    diffuseBSDF = node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuseBSDF.inputs['Roughness'].default_value = 0.0
    diffuseBSDF.location = (860.0, 460.0)

    addShader = node_tree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (1120.0, 460.0)

    mixShader = node_tree.nodes.new(type='ShaderNodeMixShader')
    mixShader.location = (1360.0, 460.0)

    grpOut1 = node_tree.nodes.new(type='NodeGroupOutput')
    grpOut1.location = (1600.0, 460.0)

    gamma1 = node_tree.nodes.new(type='ShaderNodeGamma')
    gamma1.inputs['Gamma'].default_value = 2.1
    gamma1.location = (-580.0, 240.0)

    vMath5 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath5.location = (-100.0, 240.0)
    vMath5.operation = 'MULTIPLY'

    flushColor = node_tree.nodes.new(type='ShaderNodeGroup')
    flushColor.label = 'GetFlushColor'
    flushColor.location = (380.0, 240.0)
    flushColor.name = 'GetFlushColor'
    flushColor.node_tree = get_flush_color()

    emission = node_tree.nodes.new(type='ShaderNodeEmission')
    emission.location = (860.0, 240.0)

    transparentBSDF = node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentBSDF.location = (1120.0, 240.0)

    diffuseMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.inputs['Vector'].hide = True
    diffuseMap.label = '_d DiffuseMap'
    diffuseMap.location = (-1940.0, 0.0)
    diffuseMap.name = '_d'
    diffuseMap.outputs['Alpha'].hide = True

    rotationMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.inputs['Vector'].hide = True
    rotationMap.label = '_n RotationMap'
    rotationMap.location = (-1600.0, 0.0)
    rotationMap.name = '_n'

    tangentN = node_tree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-1260.0, 0.0)
    tangentN.node_tree = normal_and_alpha_from_swizzled_texture()
    tangentN.width = 240.0

    comNor = node_tree.nodes.new(type='ShaderNodeGroup')
    comNor.location = (-920.0, 0.0)
    comNor.node_tree = combine_normals()
    comNor.width = 180.0

    ageDarkening = node_tree.nodes.new(type='ShaderNodeMixRGB')
    ageDarkening.inputs['Color1'].default_value = [0.0, 0.0, 0.0, 1.0]
    ageDarkening.inputs['Color2'].default_value = [1.0, 1.0, 1.0, 1.0]
    ageDarkening.label = 'AgeDarkening'
    ageDarkening.location = (-580.0, 0.0)
    ageDarkening.name = 'ageDarkening'

    complexionMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    complexionMap.inputs['Vector'].hide = True
    complexionMap.label = 'ComplexionMap'
    complexionMap.location = (-1940.0, -280.0)
    complexionMap.name = 'complexionMap'
    complexionMap.outputs['Alpha'].hide = True

    ageMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    ageMap.inputs['Vector'].hide = True
    ageMap.label = 'AgeMap'
    ageMap.location = (-1600.0, -280.0)
    ageMap.name = 'ageMap'

    ageNormal = node_tree.nodes.new(type='ShaderNodeGroup')
    ageNormal.location = (-1260.0, -280.0)
    ageNormal.node_tree = extract_age_normal_and_scar_from_swizzled_texture()
    ageNormal.width = 240.0

    facepaintMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    facepaintMap.inputs['Vector'].hide = True
    facepaintMap.label = 'FacepaintMap'
    facepaintMap.location = (-920.0, -280.0)
    facepaintMap.name = 'facepaintMap'

    # Add and place reroutes
    nr1 = node_tree.nodes.new(type='NodeReroute')
    nr1.location = (-1600.0, 500.0)
    nr2 = node_tree.nodes.new(type='NodeReroute')
    nr2.location = (-940.0, 500.0)
    nr3 = node_tree.nodes.new(type='NodeReroute')
    nr3.location = (-940.0, 360.0)

    nr4 = node_tree.nodes.new(type='NodeReroute')
    nr4.location = (-1600.0, 480.0)
    nr5 = node_tree.nodes.new(type='NodeReroute')
    nr5.location = (-640.0, 480.0)
    nr6 = node_tree.nodes.new(type='NodeReroute')
    nr6.location = (-640.0, 420.0)

    nr7 = node_tree.nodes.new(type='NodeReroute')
    nr7.location = (-1320.0, 380.0)
    nr8 = node_tree.nodes.new(type='NodeReroute')
    nr8.location = (-1320.0, 200.0)
    nr9 = node_tree.nodes.new(type='NodeReroute')
    nr9.location = (-1020.0, 200.0)

    nr10 = node_tree.nodes.new(type='NodeReroute')
    nr10.location = (-580.0, 480.0)
    nr11 = node_tree.nodes.new(type='NodeReroute')
    nr11.location = (-360.0, 480.0)
    nr12 = node_tree.nodes.new(type='NodeReroute')
    nr12.location = (-360.0, 400.0)
    nr13 = node_tree.nodes.new(type='NodeReroute')
    nr13.location = (340.0, 480.0)
    nr14 = node_tree.nodes.new(type='NodeReroute')
    nr14.location = (340.0, 200.0)

    nr15 = node_tree.nodes.new(type='NodeReroute')
    nr15.location = (-420.0, 400.0)
    nr16 = node_tree.nodes.new(type='NodeReroute')
    nr16.location = (-420.0, 240.0)
    nr17 = node_tree.nodes.new(type='NodeReroute')
    nr17.location = (-200.0, 240.0)

    nr18 = node_tree.nodes.new(type='NodeReroute')
    nr18.location = (820.0, 360.0)
    nr19 = node_tree.nodes.new(type='NodeReroute')
    nr19.location = (820.0, 220.0)

    nr20 = node_tree.nodes.new(type='NodeReroute')
    nr20.location = (-1620.0, 40.0)
    nr21 = node_tree.nodes.new(type='NodeReroute')
    nr21.location = (-1000.0, 40.0)
    nr22 = node_tree.nodes.new(type='NodeReroute')
    nr22.location = (-1000.0, 260.0)

    nr23 = node_tree.nodes.new(type='NodeReroute')
    nr23.location = (-920.0, 40.0)
    nr24 = node_tree.nodes.new(type='NodeReroute')
    nr24.location = (520.0, 40.0)
    nr25 = node_tree.nodes.new(type='NodeReroute')
    nr25.location = (860.0, 320.0)
    nr26 = node_tree.nodes.new(type='NodeReroute')
    nr26.location = (1260.0, 320.0)

    nr27 = node_tree.nodes.new(type='NodeReroute')
    nr27.location = (-920.0, 20.0)
    nr28 = node_tree.nodes.new(type='NodeReroute')
    nr28.location = (520.0, 20.0)

    nr29 = node_tree.nodes.new(type='NodeReroute')
    nr29.location = (-660.0, 60.0)
    nr30 = node_tree.nodes.new(type='NodeReroute')
    nr30.location = (-660.0, 220.0)
    nr31 = node_tree.nodes.new(type='NodeReroute')
    nr31.location = (280.0, 60.0)
    nr32 = node_tree.nodes.new(type='NodeReroute')
    nr32.location = (520.0, 60.0)

    nr33 = node_tree.nodes.new(type='NodeReroute')
    nr33.location = (-340.0, 260.0)
    nr34 = node_tree.nodes.new(type='NodeReroute')
    nr34.location = (40.0, 260.0)

    nr35 = node_tree.nodes.new(type='NodeReroute')
    nr35.location = (-300.0, 100.0)
    nr36 = node_tree.nodes.new(type='NodeReroute')
    nr36.location = (-140.0, 100.0)
    nr37 = node_tree.nodes.new(type='NodeReroute')
    nr37.location = (-140.0, 300.0)

    nr38 = node_tree.nodes.new(type='NodeReroute')
    nr38.location = (140.0, 260.0)
    nr39 = node_tree.nodes.new(type='NodeReroute')
    nr39.location = (280.0, 260.0)

    nr40 = node_tree.nodes.new(type='NodeReroute')
    nr40.location = (-1620.0, -220.0)
    nr41 = node_tree.nodes.new(type='NodeReroute')
    nr41.location = (-1620.0, 20.0)
    nr42 = node_tree.nodes.new(type='NodeReroute')
    nr42.location = (-1020.0, 20.0)
    nr43 = node_tree.nodes.new(type='NodeReroute')
    nr43.location = (-920.0, 80.0)
    nr44 = node_tree.nodes.new(type='NodeReroute')
    nr44.location = (-380.0, 80.0)
    nr45 = node_tree.nodes.new(type='NodeReroute')
    nr45.location = (-380.0, 300.0)

    nr46 = node_tree.nodes.new(type='NodeReroute')
    nr46.location = (-980.0, -260.0)
    nr47 = node_tree.nodes.new(type='NodeReroute')
    nr47.location = (-980.0, -180.0)

    nr48 = node_tree.nodes.new(type='NodeReroute')
    nr48.location = (-960.0, -260.0)
    nr49 = node_tree.nodes.new(type='NodeReroute')
    nr49.location = (-960.0, -180.0)
    nr50 = node_tree.nodes.new(type='NodeReroute')
    nr50.location = (-680.0, -180.0)

    nr51 = node_tree.nodes.new(type='NodeReroute')
    nr51.location = (-640.0, -260.0)
    nr52 = node_tree.nodes.new(type='NodeReroute')
    nr52.location = (-640.0, 120.0)

    nr53 = node_tree.nodes.new(type='NodeReroute')
    nr53.location = (-620.0, -260.0)
    nr54 = node_tree.nodes.new(type='NodeReroute')
    nr54.location = (-620.0, 120.0)
    nr55 = node_tree.nodes.new(type='NodeReroute')
    nr55.location = (-440.0, 120.0)
    nr56 = node_tree.nodes.new(type='NodeReroute')
    nr56.location = (-200.0, 280.0)
    nr57 = node_tree.nodes.new(type='NodeReroute')
    nr57.location = (40.0, 280.0)

    # Link nodes together
    node_tree.links.new(glossMap.outputs['Color'], nr1.inputs[0])
    node_tree.links.new(nr1.outputs[0], nr2.inputs[0])
    node_tree.links.new(nr2.outputs[0], nr3.inputs[0])
    node_tree.links.new(nr3.outputs[0], huePixel.inputs['_s GlossMap Color'])
    node_tree.links.new(glossMap.outputs['Alpha'], nr4.inputs[0])
    node_tree.links.new(nr4.outputs[0], nr5.inputs[0])
    node_tree.links.new(nr5.outputs[0], nr6.inputs[0])
    node_tree.links.new(nr6.outputs[0], phongSpec.inputs['Specular Alpha'])
    node_tree.links.new(paletteMaskMap.outputs['Color'], nr7.inputs[0])
    node_tree.links.new(nr7.outputs[0], nr8.inputs[0])
    node_tree.links.new(nr8.outputs[0], nr9.inputs[0])
    node_tree.links.new(nr9.outputs[0], huePixel.inputs['_m PaletteMaskMap Color'])
    node_tree.links.new(paletteMap.outputs['Color'], huePixel.inputs['_h PaletteMap Color'])
    node_tree.links.new(paletteMap.outputs['Alpha'], huePixel.inputs['_h PaletteMap Alpha'])
    node_tree.links.new(huePixel.outputs['Diffuse Color'], nr10.inputs[0])
    node_tree.links.new(nr10.outputs[0], nr11.inputs[0])
    node_tree.links.new(nr11.outputs[0], nr12.inputs[0])
    node_tree.links.new(nr11.outputs[0], nr13.inputs[0])
    node_tree.links.new(nr12.outputs[0], vMath1.inputs[0])
    node_tree.links.new(nr13.outputs[0], nr14.inputs[0])
    node_tree.links.new(nr14.outputs[0], flushColor.inputs['Diffuse Color'])
    node_tree.links.new(huePixel.outputs['Specular Color'], phongSpec.inputs['Specular Color'])
    node_tree.links.new(phongSpec.outputs['Specular'], nr15.inputs[0])
    node_tree.links.new(nr15.outputs[0], nr16.inputs[0])
    node_tree.links.new(nr16.outputs[0], nr17.inputs[0])
    node_tree.links.new(nr17.outputs[0], vMath5.inputs[0])
    node_tree.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    node_tree.links.new(vMath2.outputs['Vector'], mixRGB.inputs['Color1'])
    node_tree.links.new(mixRGB.outputs['Color'], vMath3.inputs[0])
    node_tree.links.new(vMath3.outputs['Vector'], vMath4.inputs[0])
    node_tree.links.new(vMath4.outputs['Vector'], nr18.inputs[0])
    node_tree.links.new(nr18.outputs[0], diffuseBSDF.inputs['Color'])
    node_tree.links.new(nr18.outputs[0], nr19.inputs[0])
    node_tree.links.new(nr19.outputs[0], emission.inputs['Color'])
    node_tree.links.new(diffuseBSDF.outputs['BSDF'], addShader.inputs[0])
    node_tree.links.new(addShader.outputs['Shader'], mixShader.inputs[1])
    node_tree.links.new(mixShader.outputs['Shader'], grpOut1.inputs['Shader'])

    node_tree.links.new(gamma1.outputs['Color'], nr33.inputs[0])
    node_tree.links.new(nr33.outputs[0], nr34.inputs[0])
    node_tree.links.new(nr34.outputs[0], mixRGB.inputs['Color2'])
    node_tree.links.new(vMath5.outputs['Vector'], nr38.inputs[0])
    node_tree.links.new(nr38.outputs[0], nr39.inputs[0])
    node_tree.links.new(nr39.outputs[0], vMath3.inputs[1])
    node_tree.links.new(flushColor.outputs['Flush Color'], vMath4.inputs[1])
    node_tree.links.new(emission.outputs['Emission'], addShader.inputs[1])
    node_tree.links.new(transparentBSDF.outputs['BSDF'], mixShader.inputs[2])

    node_tree.links.new(diffuseMap.outputs['Color'], nr20.inputs[0])
    node_tree.links.new(nr20.outputs[0], nr21.inputs[0])
    node_tree.links.new(nr21.outputs[0], nr22.inputs[0])
    node_tree.links.new(nr22.outputs[0], huePixel.inputs['_d DiffuseMap Color'])
    node_tree.links.new(rotationMap.outputs['Color'], tangentN.inputs['_n RotationMap Color'])
    node_tree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs['_n RotationMap Alpha'])
    node_tree.links.new(tangentN.outputs['Normal'], comNor.inputs['TexNormal'])
    node_tree.links.new(tangentN.outputs['Alpha'], nr23.inputs[0])
    node_tree.links.new(nr23.outputs[0], nr24.inputs[0])
    node_tree.links.new(nr24.outputs[0], nr25.inputs[0])
    node_tree.links.new(nr25.outputs[0], nr26.inputs[0])
    node_tree.links.new(nr26.outputs[0], mixShader.inputs['Fac'])
    node_tree.links.new(tangentN.outputs['Emission Strength'], nr27.inputs[0])
    node_tree.links.new(nr27.outputs[0], nr28.inputs[0])
    node_tree.links.new(nr28.outputs[0], emission.inputs['Strength'])
    node_tree.links.new(comNor.outputs['Normal'], nr29.inputs[0])
    node_tree.links.new(nr29.outputs[0], nr30.inputs[0])
    node_tree.links.new(nr30.outputs[0], phongSpec.inputs['Normal'])
    node_tree.links.new(nr30.outputs[0], phongSpec.inputs['-Normal'])
    node_tree.links.new(nr29.outputs[0], nr31.inputs[0])
    node_tree.links.new(nr31.outputs[0], flushColor.inputs['Normal'])
    node_tree.links.new(nr31.outputs[0], nr32.inputs[0])
    node_tree.links.new(nr32.outputs[0], diffuseBSDF.inputs['Normal'])
    node_tree.links.new(ageDarkening.outputs['Color'], nr35.inputs[0])
    node_tree.links.new(nr35.outputs[0], nr36.inputs[0])
    node_tree.links.new(nr36.outputs[0], vMath5.inputs[1])
    node_tree.links.new(nr36.outputs[0], nr37.inputs[0])
    node_tree.links.new(nr37.outputs[0], vMath2.inputs[1])

    node_tree.links.new(complexionMap.outputs['Color'], nr40.inputs[0])
    node_tree.links.new(nr40.outputs[0], nr41.inputs[0])
    node_tree.links.new(nr41.outputs[0], nr42.inputs[0])
    node_tree.links.new(nr42.outputs[0], nr43.inputs[0])
    node_tree.links.new(nr43.outputs[0], nr44.inputs[0])
    node_tree.links.new(nr44.outputs[0], nr45.inputs[0])
    node_tree.links.new(nr45.outputs[0], vMath1.inputs[1])
    node_tree.links.new(ageMap.outputs['Color'], ageNormal.inputs['AgeMap Color'])
    node_tree.links.new(ageMap.outputs['Alpha'], ageNormal.inputs['AgeMap Alpha'])
    node_tree.links.new(ageNormal.outputs['Normal'], nr46.inputs[0])
    node_tree.links.new(nr46.outputs[0], nr47.inputs[0])
    node_tree.links.new(nr47.outputs[0], comNor.inputs['AgeNormal'])
    node_tree.links.new(ageNormal.outputs['Scar Mask'], nr48.inputs[0])
    node_tree.links.new(nr48.outputs[0], nr49.inputs[0])
    node_tree.links.new(nr49.outputs[0], nr50.inputs[0])
    node_tree.links.new(nr50.outputs[0], ageDarkening.inputs['Fac'])
    node_tree.links.new(facepaintMap.outputs['Color'], nr51.inputs[0])
    node_tree.links.new(nr51.outputs[0], nr52.inputs[0])
    node_tree.links.new(nr52.outputs[0], gamma1.inputs['Color'])
    node_tree.links.new(facepaintMap.outputs['Alpha'], nr53.inputs[0])
    node_tree.links.new(nr53.outputs[0], nr54.inputs[0])
    node_tree.links.new(nr54.outputs[0], nr55.inputs[0])
    node_tree.links.new(nr55.outputs[0], nr56.inputs[0])
    node_tree.links.new(nr56.outputs[0], nr57.inputs[0])
    node_tree.links.new(nr57.outputs[0], mixRGB.inputs['Fac'])


def uber(node_tree):
    # type: (ShaderNodeTree) -> None
    from .node_group import normal_and_alpha_from_swizzled_texture

    # Add output socket to node tree
    add_output_socket_if_needed(node_tree)

    # Add and place nodes
    geom1 = node_tree.nodes.new(type='ShaderNodeNewGeometry')
    geom1.location = (-1400.0, 280.0)

    vMath1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath1.location = (-1160.0, 280.0)
    vMath1.operation = 'REFLECT'

    vMath2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath2.inputs[1].default_value = [-1.0, -1.0, -1.0]
    vMath2.location = (-920.0, 280.0)
    vMath2.operation = 'MULTIPLY'

    geom2 = node_tree.nodes.new(type='ShaderNodeNewGeometry')
    geom2.location = (-920.0, 80.0)

    vMath3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath3.location = (-680.0, 280.0)
    vMath3.operation = 'DOT_PRODUCT'

    clamp1 = node_tree.nodes.new(type='ShaderNodeClamp')
    clamp1.inputs['Min'].default_value = 0.0
    clamp1.inputs['Max'].default_value = 1.0
    clamp1.location = (-440.0, 280.0)

    math1 = node_tree.nodes.new(type='ShaderNodeMath')
    math1.location = (-200, 280.0)
    math1.operation = 'POWER'

    vMath4 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath4.location = (40.0, 280.0)
    vMath4.operation = 'MULTIPLY'

    vMath5 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vMath5.location = (280.0, 280.0)
    vMath5.operation = 'ADD'

    diffBSDF = node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
    diffBSDF.inputs['Roughness'].default_value = 0.0
    diffBSDF.location = (520.0, 280.0)

    addShader = node_tree.nodes.new(type='ShaderNodeAddShader')
    addShader.location = (780.0, 280.0)

    mixShader = node_tree.nodes.new(type='ShaderNodeMixShader')
    mixShader.location = (1020.0, 280.0)

    grpOut = node_tree.nodes.new(type='NodeGroupOutput')
    grpOut.location = (1260.0, 280.0)

    glossMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    glossMap.label = "_s GlossMap"
    glossMap.location = (-1260.0, 0.0)
    glossMap.name = '_s'

    math2 = node_tree.nodes.new('ShaderNodeMath')
    math2.inputs[0].default_value = 64.0
    math2.inputs[1].default_value = 1.0
    math2.location = (-920.0, -100.0)
    math2.operation = 'SUBTRACT'

    math3 = node_tree.nodes.new(type='ShaderNodeMath')
    math3.location = (-680.0, 0.0)
    math3.operation = 'MULTIPLY'

    math4 = node_tree.nodes.new(type='ShaderNodeMath')
    math4.inputs[1].default_value = 1.0
    math4.location = (-440.0, 0.0)
    math4.operation = 'ADD'

    diffuseMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    diffuseMap.label = "_d DiffuseMap"
    diffuseMap.location = (-260.0, 0.0)
    diffuseMap.name = '_d'

    gamma1 = node_tree.nodes.new(type='ShaderNodeGamma')
    gamma1.inputs['Gamma'].default_value = 2.1
    gamma1.location = (40.0, 0.0)

    emission = node_tree.nodes.new(type='ShaderNodeEmission')
    emission.location = (520.0, 0.0)

    transparentBSDF = node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
    transparentBSDF.inputs['Color'].default_value = [1.0, 1.0, 1.0, 1.0]
    transparentBSDF.location = (780.0, 0.0)

    rotationMap = node_tree.nodes.new(type='ShaderNodeTexImage')
    rotationMap.label = "_n RotationMap"
    rotationMap.location = (-1040.0, -280.0)
    rotationMap.name = '_n'

    tangentN = node_tree.nodes.new(type='ShaderNodeGroup')
    tangentN.location = (-680.0, -280.0)
    tangentN.node_tree = normal_and_alpha_from_swizzled_texture()
    tangentN.width = 380.0

    norMap = node_tree.nodes.new(type='ShaderNodeNormalMap')
    norMap.location = (-180.0, -280.0)

    # Add and place reroutes
    nr1 = node_tree.nodes.new(type='NodeReroute')
    nr1.location = (-1200.0, 240.0)
    nr2 = node_tree.nodes.new(type='NodeReroute')
    nr2.location = (-1200.0, 300.0)
    nr3 = node_tree.nodes.new(type='NodeReroute')
    nr3.location = (0.0, 300.0)
    nr4 = node_tree.nodes.new(type='NodeReroute')
    nr4.location = (480.0, 180.0)
    nr5 = node_tree.nodes.new(type='NodeReroute')
    nr5.location = (-920.0, -80.0)
    nr6 = node_tree.nodes.new(type='NodeReroute')
    nr6.location = (-780.0, -80.0)
    nr7 = node_tree.nodes.new(type='NodeReroute')
    nr7.location = (-920.0, -60.0)
    nr8 = node_tree.nodes.new(type='NodeReroute')
    nr8.location = (-780.0, -60.0)
    nr9 = node_tree.nodes.new(type='NodeReroute')
    nr9.location = (-680.0, 20.0)
    nr10 = node_tree.nodes.new(type='NodeReroute')
    nr10.location = (-200.0, 20.0)
    nr11 = node_tree.nodes.new(type='NodeReroute')
    nr11.location = (480.0, -20.0)
    nr12 = node_tree.nodes.new(type='NodeReroute')
    nr12.location = (540.0, 80.0)
    nr13 = node_tree.nodes.new(type='NodeReroute')
    nr13.location = (860.0, 80.0)
    nr14 = node_tree.nodes.new(type='NodeReroute')
    nr14.location = (-180.0, -240.0)
    nr15 = node_tree.nodes.new(type='NodeReroute')
    nr15.location = (100.0, -240.0)
    nr16 = node_tree.nodes.new(type='NodeReroute')
    nr16.location = (-180.0, -260.0)
    nr17 = node_tree.nodes.new(type='NodeReroute')
    nr17.location = (100.0, -260.0)
    nr18 = node_tree.nodes.new(type='NodeReroute')
    nr18.location = (0.0, -280.0)
    nr19 = node_tree.nodes.new(type='NodeReroute')
    nr19.location = (0.0, -220.0)
    nr20 = node_tree.nodes.new(type='NodeReroute')
    nr20.location = (100.0, -220.0)

    # Link nodes together
    node_tree.links.new(geom1.outputs['Incoming'], vMath1.inputs[1])
    node_tree.links.new(nr1.outputs[0], vMath1.inputs[0])
    node_tree.links.new(nr2.outputs[0], nr1.inputs[0])
    node_tree.links.new(vMath1.outputs['Vector'], vMath2.inputs[0])
    node_tree.links.new(vMath2.outputs['Vector'], vMath3.inputs[0])
    node_tree.links.new(geom2.outputs['Incoming'], vMath3.inputs[1])
    node_tree.links.new(vMath3.outputs['Value'], clamp1.inputs['Value'])
    node_tree.links.new(clamp1.outputs['Result'], math1.inputs[0])
    node_tree.links.new(nr3.outputs[0], nr2.inputs[0])
    node_tree.links.new(math1.outputs['Value'], vMath4.inputs[1])
    node_tree.links.new(vMath4.outputs['Vector'], vMath5.inputs[1])
    node_tree.links.new(vMath5.outputs['Vector'], nr4.inputs[0])
    node_tree.links.new(nr4.outputs[0], diffBSDF.inputs['Color'])
    node_tree.links.new(diffBSDF.outputs['BSDF'], addShader.inputs[0])
    node_tree.links.new(addShader.outputs['Shader'], mixShader.inputs[1])
    node_tree.links.new(mixShader.outputs['Shader'], grpOut.inputs[0])

    node_tree.links.new(input=glossMap.outputs['Color'], output=nr7.inputs[0])
    node_tree.links.new(input=nr7.outputs[0], output=nr8.inputs[0])
    node_tree.links.new(input=nr8.outputs[0], output=nr9.inputs[0])
    node_tree.links.new(input=nr9.outputs[0], output=nr10.inputs[0])
    node_tree.links.new(input=nr10.outputs[0], output=vMath4.inputs[0])
    node_tree.links.new(input=glossMap.outputs['Alpha'], output=nr5.inputs[0])
    node_tree.links.new(input=nr5.outputs[0], output=nr6.inputs[0])
    node_tree.links.new(input=nr6.outputs[0], output=math3.inputs[0])
    node_tree.links.new(input=math2.outputs['Value'], output=math3.inputs[1])
    node_tree.links.new(input=math3.outputs['Value'], output=math4.inputs[0])
    node_tree.links.new(input=math4.outputs['Value'], output=math1.inputs[1])
    node_tree.links.new(input=diffuseMap.outputs['Color'], output=gamma1.inputs['Color'])
    node_tree.links.new(input=gamma1.outputs['Color'], output=vMath5.inputs[0])
    node_tree.links.new(input=nr4.outputs[0], output=nr11.inputs[0])
    node_tree.links.new(input=nr11.outputs[0], output=emission.inputs['Color'])
    node_tree.links.new(input=emission.outputs['Emission'], output=addShader.inputs[1])
    node_tree.links.new(input=transparentBSDF.outputs['BSDF'], output=mixShader.inputs[2])

    node_tree.links.new(rotationMap.outputs['Color'], tangentN.inputs[0])
    node_tree.links.new(rotationMap.outputs['Alpha'], tangentN.inputs[1])
    node_tree.links.new(tangentN.outputs['Normal'], norMap.inputs['Color'])
    node_tree.links.new(norMap.outputs['Normal'], nr18.inputs[0])
    node_tree.links.new(nr18.outputs[0], nr19.inputs[0])
    node_tree.links.new(nr19.outputs[0], nr3.inputs[0])
    node_tree.links.new(nr19.outputs[0], nr20.inputs[0])
    node_tree.links.new(nr20.outputs[0], diffBSDF.inputs['Normal'])
    node_tree.links.new(tangentN.outputs['Alpha'], nr14.inputs[0])
    node_tree.links.new(nr14.outputs[0], nr15.inputs[0])
    node_tree.links.new(nr15.outputs[0], nr12.inputs[0])
    node_tree.links.new(nr12.outputs[0], nr13.inputs[0])
    node_tree.links.new(nr13.outputs[0], mixShader.inputs['Fac'])
    node_tree.links.new(tangentN.outputs['Emission Strength'], nr16.inputs[0])
    node_tree.links.new(nr16.outputs[0], nr17.inputs[0])
    node_tree.links.new(nr17.outputs[0], emission.inputs['Strength'])

    # Hide unlinked node sockets
    for node in node_tree.nodes:
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
