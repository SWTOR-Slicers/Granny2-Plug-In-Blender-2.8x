# <pep8 compliant>

import bpy
from bpy.types import NodeTree


# Detect Blender version
major, minor, _ = bpy.app.version
blender_version = major + minor / 100


def adjust_lightness():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'AdjustLightness' in bpy.data.node_groups:
        return bpy.data.node_groups['AdjustLightness']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='AdjustLightness', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketFloat', name='L')
        node_tree.inputs.new(type='NodeSocketFloat', name='Brightness')
        node_tree.inputs.new(type='NodeSocketFloat', name='Contrast')
        node_tree.outputs.new(type='NodeSocketFloat', name='L')
    else:
        node_tree.interface.new_socket('L', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Contrast', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('L', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-720.0, 80.0)
    group_input_1.outputs['Brightness'].hide = True

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.location = (-520.0, 80.0)
    math_1.operation = 'POWER'

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-520.0, -80.0)
    group_input_2.outputs['L'].hide = True
    group_input_2.outputs['Brightness'].hide = True

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.location = (-300.0, 80.0)
    math_2.operation = 'MULTIPLY'

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-300.0, -80.0)
    group_input_3.outputs['L'].hide = True
    group_input_3.outputs['Contrast'].hide = True

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.inputs[0].default_value = 1.0
    math_3.location = (-80.0, 80.0)
    math_3.operation = 'SUBTRACT'

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (140.0, 160.0)
    group_input_4.outputs['L'].hide = True
    group_input_4.outputs['Contrast'].hide = True

    math_4 = node_tree.nodes.new(type='ShaderNodeMath')
    math_4.location = (140.0, 80.0)
    math_4.operation = 'MULTIPLY'

    math_5 = node_tree.nodes.new(type='ShaderNodeMath')
    math_5.location = (360.0, 80.0)
    math_5.operation = 'ADD'

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (580.0, 80.0)

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (-120.0, 0.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (-120.0, -100.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (60.0, -100.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['L'], math_1.inputs[0])
    node_tree.links.new(group_input_1.outputs['Contrast'], math_1.inputs[1])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[0])
    node_tree.links.new(group_input_2.outputs['Contrast'], math_2.inputs[1])
    node_tree.links.new(math_2.outputs['Value'], node_reroute_1.inputs[0])
    node_tree.links.new(group_input_3.outputs['Brightness'], math_3.inputs[1])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], node_reroute_3.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], math_4.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], math_4.inputs[1])
    node_tree.links.new(group_input_4.outputs['Brightness'], math_5.inputs[0])
    node_tree.links.new(math_4.outputs['Value'], math_5.inputs[1])
    node_tree.links.new(math_5.outputs['Value'], group_output.inputs['L'])

    return node_tree


def chosen_palette():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'ChosenPalette' in bpy.data.node_groups:
        return bpy.data.node_groups['ChosenPalette']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='ChosenPalette', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='Palette1 Hue')
        node_tree.inputs.new(type='NodeSocketFloat', name='Palette1 Saturation')
        node_tree.inputs.new(type='NodeSocketFloat', name='Palette1 Brightness')
        node_tree.inputs.new(type='NodeSocketFloat', name='Palette1 Contrast')
        node_tree.inputs.new(type='NodeSocketColor', name='Palette1 Specular')
        node_tree.inputs.new(type='NodeSocketColor', name='Palette1 Metallic Specular')
        node_tree.inputs.new(type='NodeSocketFloat', name='Palette2 Hue')
        node_tree.inputs.new(type='NodeSocketFloat', name='Palette2 Saturation')
        node_tree.inputs.new(type='NodeSocketFloat', name='Palette2 Brightness')
        node_tree.inputs.new(type='NodeSocketFloat', name='Palette2 Contrast')
        node_tree.inputs.new(type='NodeSocketColor', name='Palette2 Specular')
        node_tree.inputs.new(type='NodeSocketColor', name='Palette2 Metallic Specular')
        node_tree.outputs.new(type='NodeSocketFloat', name='Hue')
        node_tree.outputs.new(type='NodeSocketFloat', name='Saturation')
        node_tree.outputs.new(type='NodeSocketFloat', name='Brightness')
        node_tree.outputs.new(type='NodeSocketFloat', name='Contrast')
        node_tree.outputs.new(type='NodeSocketColor', name='Specular')
        node_tree.outputs.new(type='NodeSocketColor', name='Metallic Specular')
    else:
        node_tree.interface.new_socket('_m PaletteMaskMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Palette1 Hue', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Palette1 Saturation', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Palette1 Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Palette1 Contrast', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Palette1 Specular', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Palette1 Metallic Specular', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Palette2 Hue', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Palette2 Saturation', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Palette2 Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Palette2 Contrast', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Palette2 Specular', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Palette2 Metallic Specular', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Hue', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Saturation', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Brightness', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Contrast', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Specular', in_out='OUTPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Metallic Specular', in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-480.0, 620.0)
    group_input_1.width = 200.0
    for socket in group_input_1.outputs:
        if socket.name != 'Palette2 Hue':
            socket.hide = True

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.location = (-200.0, 620.0)
    math_1.operation = 'MULTIPLY'

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (20.0, 620.0)
    group_input_2.width = 200.0
    for socket in group_input_2.outputs:
        if socket.name != 'Palette1 Hue':
            socket.hide = True

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.location = (300.0, 620.0)
    math_2.operation = 'MULTIPLY'

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.location = (520.0, 620.0)
    math_3.operation = 'ADD'

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-480.0, 420.0)
    group_input_3.width = 200.0
    for socket in group_input_3.outputs:
        if socket.name != 'Palette2 Saturation':
            socket.hide = True

    math_4 = node_tree.nodes.new(type='ShaderNodeMath')
    math_4.location = (-200.0, 420.0)
    math_4.operation = 'MULTIPLY'

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (20.0, 420.0)
    group_input_4.width = 200.0
    for socket in group_input_4.outputs:
        if socket.name != 'Palette1 Saturation':
            socket.hide = True

    math_5 = node_tree.nodes.new(type='ShaderNodeMath')
    math_5.location = (300.0, 420.0)
    math_5.operation = 'MULTIPLY'

    math_6 = node_tree.nodes.new(type='ShaderNodeMath')
    math_6.location = (520.0, 420.0)
    math_6.operation = 'ADD'

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (800.0, 420.0)

    group_input_5 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_5.location = (-480.0, 220.0)
    group_input_5.width = 200.0
    for socket in group_input_5.outputs:
        if socket.name != 'Palette2 Brightness':
            socket.hide = True

    math_7 = node_tree.nodes.new(type='ShaderNodeMath')
    math_7.location = (-200.0, 220.0)
    math_7.operation = 'MULTIPLY'

    group_input_6 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_6.location = (20.0, 220.0)
    group_input_6.width = 200.0
    for socket in group_input_6.outputs:
        if socket.name != 'Palette1 Brightness':
            socket.hide = True

    math_8 = node_tree.nodes.new(type='ShaderNodeMath')
    math_8.location = (300.0, 220.0)
    math_8.operation = 'MULTIPLY'

    math_9 = node_tree.nodes.new(type='ShaderNodeMath')
    math_9.location = (520.0, 220.0)
    math_9.operation = 'ADD'

    group_input_7 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_7.location = (-480.0, 20.0)
    group_input_7.width = 200.0
    for socket in group_input_7.outputs:
        if socket.name != 'Palette2 Contrast':
            socket.hide = True

    math_10 = node_tree.nodes.new(type='ShaderNodeMath')
    math_10.location = (-200.0, 20.0)
    math_10.operation = 'MULTIPLY'

    group_input_8 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_8.location = (20.0, 20.0)
    group_input_8.width = 200.0
    for socket in group_input_8.outputs:
        if socket.name != 'Palette1 Contrast':
            socket.hide = True

    math_11 = node_tree.nodes.new(type='ShaderNodeMath')
    math_11.location = (300.0, 20.0)
    math_11.operation = 'MULTIPLY'

    math_12 = node_tree.nodes.new(type='ShaderNodeMath')
    math_12.location = (520.0, 20.0)
    math_12.operation = 'ADD'

    group_input_9 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_9.location = (-480.0, -180.0)
    group_input_9.width = 200.0
    for socket in group_input_9.outputs:
        if socket.name != 'Palette2 Specular':
            socket.hide = True

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.location = (-200.0, -180.0)
    vector_math_1.operation = 'MULTIPLY'

    group_input_10 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_10.location = (20.0, -180.0)
    group_input_10.width = 200.0
    for socket in group_input_10.outputs:
        if socket.name != 'Palette1 Specular':
            socket.hide = True

    vector_math_2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_2.location = (300.0, -180.0)
    vector_math_2.operation = 'MULTIPLY'

    vector_math_3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_3.location = (520.0, -180.0)
    vector_math_3.operation = 'ADD'

    group_input_11 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_11.location = (-480.0, -360.0)
    group_input_11.width = 200.0
    for socket in group_input_11.outputs:
        if socket.name != 'Palette2 Metallic Specular':
            socket.hide = True

    vector_math_4 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_4.location = (-200.0, -360.0)
    vector_math_4.operation = 'MULTIPLY'

    group_input_12 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_12.location = (20.0, -360.0)
    group_input_12.width = 200.0
    for socket in group_input_12.outputs:
        if socket.name != 'Palette1 Metallic Specular':
            socket.hide = True

    vector_math_5 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_5.location = (300.0, -360.0)
    vector_math_5.operation = 'MULTIPLY'

    vector_math_6 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_6.location = (520.0, -360.0)
    vector_math_6.operation = 'ADD'

    group_input_13 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_13.location = (-920.0, -500.0)
    group_input_13.width = 200
    for socket in group_input_13.outputs:
        if socket.name != '_m PaletteMaskMap Color':
            socket.hide = True

    separate_xyz = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz.location = (-640.0, -500.0)
    separate_xyz.outputs['Z'].hide = True

    math_13 = node_tree.nodes.new(type='ShaderNodeMath')
    math_13.location = (-420.0, -500.0)
    math_13.operation = 'LESS_THAN'

    math_14 = node_tree.nodes.new(type='ShaderNodeMath')
    math_14.inputs[1].default_value = 1.0
    math_14.location = (-200.0, -500.0)
    math_14.operation = 'LESS_THAN'

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (-240.0, 440.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (260.0, 440.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (20.0, 640.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (480.0, 640.0)
    node_reroute_5 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_5.location = (480.0, 560.0)

    node_reroute_6 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_6.location = (-240.0, 260.0)
    node_reroute_7 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_7.location = (260.0, 260.0)
    node_reroute_8 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_8.location = (20.0, 440.0)
    node_reroute_9 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_9.location = (480.0, 440.0)
    node_reroute_10 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_10.location = (480.0, 360.0)

    node_reroute_11 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_11.location = (-240.0, 60.0)
    node_reroute_12 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_12.location = (260.0, 60.0)
    node_reroute_13 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_13.location = (20.0, 240.0)
    node_reroute_14 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_14.location = (480.0, 240.0)
    node_reroute_15 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_15.location = (480.0, 160.0)
    node_reroute_16 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_16.location = (720.0, 180.0)
    node_reroute_17 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_17.location = (740.0, 180.0)
    node_reroute_18 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_18.location = (760.0, 180.0)

    node_reroute_19 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_19.location = (-240.0, -140.0)
    node_reroute_20 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_20.location = (260.0, -140.0)
    node_reroute_21 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_21.location = (20.0, 40.0)
    node_reroute_22 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_22.location = (480.0, 40.0)
    node_reroute_23 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_23.location = (480.0, -40.0)
    node_reroute_24 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_24.location = (720.0, 60.0)

    node_reroute_25 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_25.location = (-240.0, -320.0)
    node_reroute_26 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_26.location = (260.0, -320.0)
    node_reroute_27 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_27.location = (20.0, -160.0)
    node_reroute_28 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_28.location = (480.0, -160.0)
    node_reroute_29 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_29.location = (480.0, -220.0)
    node_reroute_30 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_30.location = (740.0, -120.0)

    node_reroute_31 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_31.location = (-240.0, -480.0)
    node_reroute_32 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_32.location = (0.0, -480.0)
    node_reroute_33 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_33.location = (260.0, -480.0)
    node_reroute_34 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_34.location = (20.0, -340.0)
    node_reroute_35 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_35.location = (480.0, -340.0)
    node_reroute_36 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_36.location = (480.0, -400.0)
    node_reroute_37 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_37.location = (760.0, -280.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['Palette2 Hue'], math_1.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], math_1.inputs[1])
    node_tree.links.new(math_1.outputs['Value'], node_reroute_3.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(group_input_2.outputs['Palette1 Hue'], math_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], math_2.inputs[1])
    node_tree.links.new(math_2.outputs['Value'], math_3.inputs[1])
    node_tree.links.new(node_reroute_4.outputs[0], node_reroute_5.inputs[0])
    node_tree.links.new(node_reroute_5.outputs[0], math_3.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], group_output.inputs['Hue'])

    node_tree.links.new(group_input_3.outputs['Palette2 Saturation'], math_4.inputs[0])
    node_tree.links.new(node_reroute_6.outputs[0], node_reroute_1.inputs[0])
    node_tree.links.new(node_reroute_6.outputs[0], math_4.inputs[1])
    node_tree.links.new(math_4.outputs['Value'], node_reroute_8.inputs[0])
    node_tree.links.new(node_reroute_8.outputs[0], node_reroute_9.inputs[0])
    node_tree.links.new(group_input_4.outputs['Palette1 Saturation'], math_5.inputs[0])
    node_tree.links.new(node_reroute_7.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_7.outputs[0], math_5.inputs[1])
    node_tree.links.new(math_5.outputs['Value'], math_6.inputs[1])
    node_tree.links.new(node_reroute_9.outputs[0], node_reroute_10.inputs[0])
    node_tree.links.new(node_reroute_10.outputs[0], math_6.inputs[0])
    node_tree.links.new(math_6.outputs['Value'], group_output.inputs['Saturation'])

    node_tree.links.new(group_input_5.outputs['Palette2 Brightness'], math_7.inputs[0])
    node_tree.links.new(node_reroute_11.outputs[0], node_reroute_6.inputs[0])
    node_tree.links.new(node_reroute_11.outputs[0], math_7.inputs[1])
    node_tree.links.new(math_7.outputs['Value'], node_reroute_13.inputs[0])
    node_tree.links.new(node_reroute_13.outputs[0], node_reroute_14.inputs[0])
    node_tree.links.new(group_input_6.outputs['Palette1 Brightness'], math_8.inputs[0])
    node_tree.links.new(node_reroute_12.outputs[0], node_reroute_7.inputs[0])
    node_tree.links.new(node_reroute_12.outputs[0], math_8.inputs[1])
    node_tree.links.new(math_8.outputs['Value'], math_9.inputs[1])
    node_tree.links.new(node_reroute_14.outputs[0], node_reroute_15.inputs[0])
    node_tree.links.new(node_reroute_15.outputs[0], math_9.inputs[0])
    node_tree.links.new(math_9.outputs['Value'], group_output.inputs['Brightness'])
    node_tree.links.new(node_reroute_16.outputs[0], group_output.inputs['Contrast'])
    node_tree.links.new(node_reroute_17.outputs[0], group_output.inputs['Specular'])
    node_tree.links.new(node_reroute_18.outputs[0], group_output.inputs['Metallic Specular'])

    node_tree.links.new(group_input_7.outputs['Palette2 Contrast'], math_10.inputs[0])
    node_tree.links.new(node_reroute_19.outputs[0], node_reroute_11.inputs[0])
    node_tree.links.new(node_reroute_19.outputs[0], math_10.inputs[1])
    node_tree.links.new(math_10.outputs['Value'], node_reroute_21.inputs[0])
    node_tree.links.new(node_reroute_21.outputs[0], node_reroute_22.inputs[0])
    node_tree.links.new(group_input_8.outputs['Palette1 Contrast'], math_11.inputs[0])
    node_tree.links.new(node_reroute_20.outputs[0], node_reroute_12.inputs[0])
    node_tree.links.new(node_reroute_20.outputs[0], math_11.inputs[1])
    node_tree.links.new(math_11.outputs['Value'], math_12.inputs[1])
    node_tree.links.new(node_reroute_22.outputs[0], node_reroute_23.inputs[0])
    node_tree.links.new(node_reroute_23.outputs[0], math_12.inputs[0])
    node_tree.links.new(math_12.outputs['Value'], node_reroute_24.inputs[0])
    node_tree.links.new(node_reroute_24.outputs[0], node_reroute_16.inputs[0])

    node_tree.links.new(group_input_9.outputs['Palette2 Specular'], vector_math_1.inputs[0])
    node_tree.links.new(node_reroute_25.outputs[0], node_reroute_19.inputs[0])
    node_tree.links.new(node_reroute_25.outputs[0], vector_math_1.inputs[1])
    node_tree.links.new(vector_math_1.outputs['Vector'], node_reroute_27.inputs[0])
    node_tree.links.new(node_reroute_27.outputs[0], node_reroute_28.inputs[0])
    node_tree.links.new(group_input_10.outputs['Palette1 Specular'], vector_math_2.inputs[0])
    node_tree.links.new(node_reroute_26.outputs[0], node_reroute_20.inputs[0])
    node_tree.links.new(node_reroute_26.outputs[0], vector_math_2.inputs[1])
    node_tree.links.new(vector_math_2.outputs['Vector'], vector_math_3.inputs[1])
    node_tree.links.new(node_reroute_28.outputs[0], node_reroute_29.inputs[0])
    node_tree.links.new(node_reroute_29.outputs[0], vector_math_3.inputs[0])
    node_tree.links.new(vector_math_3.outputs['Vector'], node_reroute_30.inputs[0])
    node_tree.links.new(node_reroute_30.outputs[0], node_reroute_17.inputs[0])

    node_tree.links.new(group_input_11.outputs['Palette2 Metallic Specular'], vector_math_4.inputs[0])
    node_tree.links.new(node_reroute_31.outputs[0], node_reroute_25.inputs[0])
    node_tree.links.new(node_reroute_31.outputs[0], vector_math_4.inputs[1])
    node_tree.links.new(vector_math_4.outputs['Vector'], node_reroute_34.inputs[0])
    node_tree.links.new(node_reroute_32.outputs[0], node_reroute_33.inputs[0])
    node_tree.links.new(node_reroute_34.outputs[0], node_reroute_35.inputs[0])
    node_tree.links.new(group_input_12.outputs['Palette1 Metallic Specular'], vector_math_5.inputs[0])
    node_tree.links.new(node_reroute_33.outputs[0], node_reroute_26.inputs[0])
    node_tree.links.new(node_reroute_33.outputs[0], vector_math_5.inputs[1])
    node_tree.links.new(vector_math_5.outputs['Vector'], vector_math_6.inputs[1])
    node_tree.links.new(node_reroute_35.outputs[0], node_reroute_36.inputs[0])
    node_tree.links.new(node_reroute_36.outputs[0], vector_math_6.inputs[0])
    node_tree.links.new(vector_math_6.outputs['Vector'], node_reroute_37.inputs[0])
    node_tree.links.new(node_reroute_37.outputs[0], node_reroute_18.inputs[0])

    node_tree.links.new(group_input_13.outputs['_m PaletteMaskMap Color'], separate_xyz.inputs['Vector'])
    node_tree.links.new(separate_xyz.outputs['X'], math_13.inputs[0])
    node_tree.links.new(separate_xyz.outputs['Y'], math_13.inputs[1])
    node_tree.links.new(math_13.outputs['Value'], node_reroute_31.inputs[0])
    node_tree.links.new(math_13.outputs['Value'], math_14.inputs[0])
    node_tree.links.new(math_14.outputs['Value'], node_reroute_32.inputs[0])

    return node_tree


def combine_normals():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'CombineNormals' in bpy.data.node_groups:
        return bpy.data.node_groups['CombineNormals']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='CombineNormals', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketVector', name='TexNormal')
        node_tree.inputs.new(type='NodeSocketVector', name='AgeNormal')
        node_tree.inputs.new(type='NodeSocketFloat', name='Scar Strength')
        node_tree.inputs['Scar Strength'].default_value = 1.0
        node_tree.outputs.new(type='NodeSocketVector', name='Normal')
    else:
        node_tree.interface.new_socket('TexNormal', in_out='INPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('AgeNormal', in_out='INPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('Scar Strength', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.items_tree['Scar Strength'].default_value = 1.0
        node_tree.interface.new_socket('Normal', in_out='OUTPUT', socket_type='NodeSocketVector')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-320.0, 180.0)
    group_input_1.outputs['AgeNormal'].hide = True
    group_input_1.outputs['Scar Strength'].hide = True

    normal_map_1 = node_tree.nodes.new(type='ShaderNodeNormalMap')
    normal_map_1.location = (-80.0, 180.0)

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.location = (180.0, 180.0)
    vector_math_1.operation = 'ADD'

    vector_math_2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_2.location = (420.0, 180.0)
    vector_math_2.operation = 'NORMALIZE'

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (660.0, 180.0)

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-800.0, 20.0)
    group_input_2.outputs['TexNormal'].hide = True
    group_input_2.outputs['Scar Strength'].hide = True

    separate_xyz_1 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz_1.location = (-560.0, 20.0)
    separate_xyz_1.outputs['Z'].hide = True

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-320.0, 20.0)
    group_input_3.outputs['TexNormal'].hide = True
    group_input_3.outputs['AgeNormal'].hide = True

    normal_map_2 = node_tree.nodes.new(type='ShaderNodeNormalMap')
    normal_map_2.location = (-80.0, 20.0)

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (-800.0, -80.0)
    group_input_4.outputs['AgeNormal'].hide = True
    group_input_4.outputs['Scar Strength'].hide = True

    separate_xyz_2 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz_2.location = (-560.0, -80.0)
    separate_xyz_2.outputs['X'].hide = True
    separate_xyz_2.outputs['Y'].hide = True

    combine_xyz = node_tree.nodes.new(type='ShaderNodeCombineXYZ')
    combine_xyz.location = (-320.0, -60.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['TexNormal'], normal_map_1.inputs['Color'])
    node_tree.links.new(normal_map_1.outputs['Normal'], vector_math_1.inputs[0])
    node_tree.links.new(vector_math_1.outputs['Vector'], vector_math_2.inputs[0])
    node_tree.links.new(vector_math_2.outputs['Vector'], group_output.inputs['Normal'])
    node_tree.links.new(group_input_2.outputs['AgeNormal'], separate_xyz_1.inputs['Vector'])
    node_tree.links.new(separate_xyz_1.outputs['X'], combine_xyz.inputs['X'])
    node_tree.links.new(separate_xyz_1.outputs['Y'], combine_xyz.inputs['Y'])
    node_tree.links.new(group_input_3.outputs['Scar Strength'], normal_map_2.inputs['Strength'])
    node_tree.links.new(normal_map_2.outputs['Normal'], vector_math_1.inputs[1])
    node_tree.links.new(group_input_4.outputs['TexNormal'], separate_xyz_2.inputs['Vector'])
    node_tree.links.new(separate_xyz_2.outputs['Z'], combine_xyz.inputs['Z'])
    node_tree.links.new(combine_xyz.outputs['Vector'], normal_map_2.inputs['Color'])

    return node_tree


def convert_hsl_to_rgb():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'ConvertHSLToRGB' in bpy.data.node_groups:
        return bpy.data.node_groups['ConvertHSLToRGB']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='ConvertHSLToRGB', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketFloat', name='H')
        node_tree.inputs.new(type='NodeSocketFloat', name='S')
        node_tree.inputs.new(type='NodeSocketFloat', name='L')
        node_tree.outputs.new(type='NodeSocketColor', name='RGB')
    else:
        node_tree.interface.new_socket('H', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('S', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('L', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('RGB', in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-1420.0, 80.0)
    group_input_1.outputs['H'].hide = True
    group_input_1.outputs['S'].hide = True

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.inputs[0].default_value = 2.0
    math_1.location = (-1180.0, 80.0)
    math_1.operation = 'MULTIPLY'

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.inputs[1].default_value = 1.0
    math_2.location = (-960.0, 80.0)
    math_2.operation = 'SUBTRACT'

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.location = (-740.0, 80.0)
    math_3.operation = 'ABSOLUTE'

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-520.0, 160.0)
    group_input_2.outputs['H'].hide = True
    group_input_2.outputs['L'].hide = True

    math_4 = node_tree.nodes.new(type='ShaderNodeMath')
    math_4.inputs[0].default_value = 1.0
    math_4.location = (-520.0, 80.0)
    math_4.operation = 'SUBTRACT'

    math_5 = node_tree.nodes.new(type='ShaderNodeMath')
    math_5.location = (-300.0, 80.0)
    math_5.operation = 'MULTIPLY'

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-80.0, 160.0)
    group_input_3.outputs['H'].hide = True
    group_input_3.outputs['S'].hide = True

    math_6 = node_tree.nodes.new(type='ShaderNodeMath')
    math_6.inputs[1].default_value = 2.0
    math_6.location = (-80.0, 80.0)
    math_6.operation = 'DIVIDE'

    math_7 = node_tree.nodes.new(type='ShaderNodeMath')
    math_7.location = (140.0, 80.0)
    math_7.operation = 'ADD'

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (140.0, -80.0)
    group_input_4.outputs['H'].hide = True
    group_input_4.outputs['S'].hide = True

    math_8 = node_tree.nodes.new(type='ShaderNodeMath')
    math_8.location = (360.0, 80.0)
    math_8.operation = 'SUBTRACT'

    math_9 = node_tree.nodes.new(type='ShaderNodeMath')
    math_9.inputs[0].default_value = 2.0
    math_9.location = (580.0, 80.0)
    math_9.operation = 'MULTIPLY'

    group_input_5 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_5.location = (800.0, 160.0)
    group_input_5.outputs['S'].hide = True
    group_input_5.outputs['L'].hide = True

    math_10 = node_tree.nodes.new(type='ShaderNodeMath')
    math_10.location = (800.0, 80.0)
    math_10.operation = 'DIVIDE'

    combine_hsv = node_tree.nodes.new(type='ShaderNodeCombineHSV')
    combine_hsv.location = (1020.0, 80.0)

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (1240.0, 80.0)

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (320.0, 0.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (320.0, -100.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (720.0, -100.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (940.0, -100.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['L'], math_1.inputs[1])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], math_3.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], math_4.inputs[1])
    node_tree.links.new(group_input_2.outputs['S'], math_5.inputs[0])
    node_tree.links.new(math_4.outputs['Value'], math_5.inputs[1])
    node_tree.links.new(math_5.outputs['Value'], math_6.inputs[0])
    node_tree.links.new(group_input_3.outputs['L'], math_7.inputs[0])
    node_tree.links.new(math_6.outputs['Value'], math_7.inputs[1])
    node_tree.links.new(math_7.outputs['Value'], node_reroute_1.inputs[0])
    node_tree.links.new(group_input_4.outputs['L'], math_8.inputs[1])
    node_tree.links.new(node_reroute_1.outputs[0], math_8.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], node_reroute_3.inputs[0])
    node_tree.links.new(math_8.outputs['Value'], math_9.inputs[1])
    node_tree.links.new(math_9.outputs['Value'], math_10.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], math_10.inputs[1])
    node_tree.links.new(node_reroute_3.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(group_input_5.outputs['H'], combine_hsv.inputs['H'])
    node_tree.links.new(math_10.outputs['Value'], combine_hsv.inputs['S'])
    node_tree.links.new(node_reroute_4.outputs[0], combine_hsv.inputs['V'])
    node_tree.links.new(combine_hsv.outputs['Color'], group_output.inputs['RGB'])

    return node_tree


def expand_hsl():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'ExpandHSL' in bpy.data.node_groups:
        return bpy.data.node_groups['ExpandHSL']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='ExpandHSL', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        node_tree.outputs.new(type='NodeSocketFloat', name='H')
        node_tree.outputs.new(type='NodeSocketFloat', name='S')
        node_tree.outputs.new(type='NodeSocketFloat', name='L')
    else:
        node_tree.interface.new_socket('_h PaletteMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_h PaletteMap Alpha', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('H', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('S', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('L', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-500.0, 260.0)
    group_input_1.outputs['_h PaletteMap Alpha'].hide = True

    separate_xyz = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz.location = (-280.0, 260.0)
    separate_xyz.outputs['X'].hide = True

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.inputs[0].default_value = 0.706
    math_1.inputs[1].default_value = 0.3137
    math_1.location = (-280.0, 80.0)
    math_1.operation = 'SUBTRACT'

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-280.0, -80.0)
    group_input_2.outputs['_h PaletteMap Color'].hide = True

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.inputs[2].default_value = 0.3137
    math_2.location = (-60.0, 260.0)
    math_2.operation = 'MULTIPLY_ADD'

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.inputs[1].default_value = 0.5882
    math_3.location = (-60.0, 80.0)
    math_3.operation = 'MULTIPLY'

    math_4 = node_tree.nodes.new(type='ShaderNodeMath')
    math_4.inputs[1].default_value = 0.70588
    math_4.location = (-60.0, -80.0)
    math_4.operation = 'MULTIPLY'

    math_5 = node_tree.nodes.new(type='ShaderNodeMath')
    math_5.inputs[1].default_value = 0.41176
    math_5.location = (160.0, 260.0)
    math_5.operation = 'SUBTRACT'

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (380.0, 260.0)

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (-100.0, 160.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (-100.0, 20.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (120.0, 80.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (120.0, 60.0)
    node_reroute_5 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_5.location = (120.0, -60.0)
    node_reroute_6 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_6.location = (320.0, 140.0)
    node_reroute_7 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_7.location = (320.0, 80.0)
    node_reroute_8 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_8.location = (340.0, 140.0)
    node_reroute_9 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_9.location = (340.0, 60.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['_h PaletteMap Color'], separate_xyz.inputs['Vector'])
    node_tree.links.new(separate_xyz.outputs['Y'], math_2.inputs[0])
    node_tree.links.new(separate_xyz.outputs['Z'], node_reroute_1.inputs[0])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[1])
    node_tree.links.new(group_input_2.outputs['_h PaletteMap Alpha'], math_4.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], math_3.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], math_5.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], node_reroute_3.inputs[0])
    node_tree.links.new(math_4.outputs['Value'], node_reroute_5.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], node_reroute_7.inputs[0])
    node_tree.links.new(node_reroute_4.outputs[0], node_reroute_9.inputs[0])
    node_tree.links.new(node_reroute_5.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(math_5.outputs['Value'], group_output.inputs['H'])
    node_tree.links.new(node_reroute_6.outputs[0], group_output.inputs['S'])
    node_tree.links.new(node_reroute_7.outputs[0], node_reroute_6.inputs[0])
    node_tree.links.new(node_reroute_8.outputs[0], group_output.inputs['L'])
    node_tree.links.new(node_reroute_9.outputs[0], node_reroute_8.inputs[0])

    return node_tree


def extract_age_normal_and_scar_from_swizzled_texture():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'ExtractAgeNormalAndScarFromSwizzledTexture' in bpy.data.node_groups:
        return bpy.data.node_groups['ExtractAgeNormalAndScarFromSwizzledTexture']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(
        name='ExtractAgeNormalAndScarFromSwizzledTexture',
        type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='AgeMap Color')
        node_tree.inputs['AgeMap Color'].default_value = [0.0, 0.5, 1.0, 1.0]
        node_tree.inputs.new(type='NodeSocketFloat', name='AgeMap Alpha')
        node_tree.inputs['AgeMap Alpha'].default_value = 0.5
        node_tree.outputs.new(type='NodeSocketVector', name='Normal')
        node_tree.outputs.new(type='NodeSocketFloat', name='Scar Mask')
    else:
        node_tree.interface.new_socket('AgeMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.items_tree['AgeMap Color'].default_value = [0.0, 0.5, 1.0, 1.0]
        node_tree.interface.new_socket('AgeMap Alpha', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.items_tree['AgeMap Alpha'].default_value = 0.5
        node_tree.interface.new_socket('Normal', in_out='OUTPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('Scar Mask', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-80.0, 180.0)
    group_input_1.outputs['AgeMap Color'].hide = True

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-560.0, 60.0)
    group_input_2.outputs['AgeMap Alpha'].hide = True

    separate_xyz = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz.outputs['X'].hide = True
    separate_xyz.location = (-320.0, 60.0)

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.inputs[0].default_value = 1.0
    math_1.location = (-80.0, 60.0)
    math_1.operation = 'SUBTRACT'

    combine_xyz = node_tree.nodes.new(type='ShaderNodeCombineXYZ')
    combine_xyz.inputs['Z'].default_value = 0.0
    combine_xyz.location = (160.0, 60.0)

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (400.0, 60.0)

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (-80.0, 80.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (300.0, 80.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['AgeMap Alpha'], combine_xyz.inputs['X'])
    node_tree.links.new(group_input_2.outputs['AgeMap Color'], separate_xyz.inputs['Vector'])
    node_tree.links.new(separate_xyz.outputs['Y'], math_1.inputs[1])
    node_tree.links.new(separate_xyz.outputs['Z'], node_reroute_1.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(math_1.outputs['Value'], combine_xyz.inputs['Y'])
    node_tree.links.new(node_reroute_2.outputs[0], group_output.inputs['Scar Mask'])
    node_tree.links.new(combine_xyz.outputs['Vector'], group_output.inputs['Normal'])

    return node_tree


def get_flush_color():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'GetFlushColor' in bpy.data.node_groups:
        return bpy.data.node_groups['GetFlushColor']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='GetFlushColor', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='Diffuse Color')
        node_tree.inputs['Diffuse Color'].default_value = [0.0, 0.0, 0.0, 1.0]
        node_tree.inputs.new(type='NodeSocketFloat', name='Flesh Brightness')
        node_tree.inputs['Flesh Brightness'].default_value = 0.0
        node_tree.inputs['Flesh Brightness'].max_value = 1.0
        node_tree.inputs['Flesh Brightness'].min_value = 0.0
        node_tree.inputs.new(type='NodeSocketColor', name='Flush Tone')
        node_tree.inputs['Flush Tone'].default_value = [0.0, 0.0, 0.0, 1.0]
        node_tree.inputs.new(type='NodeSocketVector', name='Normal')
        node_tree.outputs.new(type='NodeSocketColor', name='Flush Color')
    else:
        node_tree.interface.new_socket('Diffuse Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.items_tree['Diffuse Color'].default_value = [0.0, 0.0, 0.0, 1.0]
        node_tree.interface.new_socket('Flesh Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.items_tree['Flesh Brightness'].default_value = 0.0
        node_tree.interface.items_tree['Flesh Brightness'].max_value = 1.0
        node_tree.interface.items_tree['Flesh Brightness'].min_value = 0.0
        node_tree.interface.new_socket('Flush Tone', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.items_tree['Flush Tone'].default_value = [0.0, 0.0, 0.0, 1.0]
        node_tree.interface.new_socket('Normal', in_out='INPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('Flush Color', in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-960.0, 80.0)
    for socket in group_input_1.outputs:
        if socket.name != 'Normal':
            socket.hide = True

    geometry_1 = node_tree.nodes.new(type='ShaderNodeNewGeometry')
    geometry_1.location = (-960.0, 0.0)
    for socket in geometry_1.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.location = (-740.0, 80.0)
    vector_math_1.operation = 'DOT_PRODUCT'

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.inputs[1].default_value = 0.27
    math_1.location = (-520.0, 80.0)
    math_1.operation = 'SUBTRACT'

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.inputs[1].default_value = 3.0
    math_2.location = (-300.0, 80.0)
    math_2.operation = 'MULTIPLY'

    clamp_1 = node_tree.nodes.new(type='ShaderNodeClamp')
    clamp_1.inputs['Min'].default_value = 0.0
    clamp_1.inputs['Max'].default_value = 1.0
    clamp_1.location = (-80.0, 80.0)

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-80.0, -80.0)
    for socket in group_input_2.outputs:
        if socket.name != 'Flesh Brightness':
            socket.hide = True

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (140.0, 200.0)
    for socket in group_input_3.outputs:
        if socket.name != 'Flush Tone':
            socket.hide = True

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.location = (140.0, 80.0)
    math_3.operation = 'MULTIPLY'

    vector_math_2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_2.location = (360.0, 80.0)
    vector_math_2.operation = 'MULTIPLY'

    group_input = node_tree.nodes.new(type='NodeGroupInput')
    group_input.location = (360.0, -80.0)
    for socket in group_input.outputs:
        if socket.name != 'Diffuse Color':
            socket.hide = True

    vector_math_3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_3.location = (580.0, 80.0)
    vector_math_3.operation = 'MULTIPLY'

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (800.0, 80.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['Normal'], vector_math_1.inputs[0])
    node_tree.links.new(geometry_1.outputs['Incoming'], vector_math_1.inputs[1])
    node_tree.links.new(vector_math_1.outputs['Value'], math_1.inputs[0])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], clamp_1.inputs['Value'])
    node_tree.links.new(clamp_1.outputs['Result'], math_3.inputs[0])
    node_tree.links.new(group_input_2.outputs['Flesh Brightness'], math_3.inputs[1])
    node_tree.links.new(group_input_3.outputs['Flush Tone'], vector_math_2.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], vector_math_2.inputs[1])
    node_tree.links.new(vector_math_2.outputs['Vector'], vector_math_3.inputs[0])
    node_tree.links.new(group_input.outputs['Diffuse Color'], vector_math_3.inputs[1])
    node_tree.links.new(vector_math_3.outputs['Vector'], group_output.inputs['Flush Color'])

    return node_tree


def get_phong_specular():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'GetPhongSpecular' in bpy.data.node_groups:
        return bpy.data.node_groups['GetPhongSpecular']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='GetPhongSpecular', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='Specular Color')
        node_tree.inputs['Specular Color'].default_value = [0.0, 0.0, 0.0, 1.0]
        node_tree.inputs.new(type='NodeSocketFloat', name='Specular Alpha')
        node_tree.inputs['Specular Alpha'].default_value = 0.0
        node_tree.inputs.new(type='NodeSocketVector', name='Normal')
        node_tree.inputs.new(type='NodeSocketVector', name='-Normal')
        node_tree.inputs.new(type='NodeSocketFloat', name='MaxSpecPower')
        node_tree.inputs['MaxSpecPower'].default_value = 64.0 * 0.5
        node_tree.outputs.new(type='NodeSocketColor', name='Specular')
    else:
        node_tree.interface.new_socket('Specular Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.items_tree['Specular Color'].default_value = [0.0, 0.0, 0.0, 1.0]
        node_tree.interface.new_socket('Specular Alpha', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.items_tree['Specular Alpha'].default_value = 0.0
        node_tree.interface.new_socket('Normal', in_out='INPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('-Normal', in_out='INPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('MaxSpecPower', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.items_tree['MaxSpecPower'].default_value = 64.0 * 0.5
        node_tree.interface.new_socket('Specular', in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add and place nodes
    geometry_1 = node_tree.nodes.new(type='ShaderNodeNewGeometry')
    geometry_1.location = (-1240.0, 200.0)
    for socket in geometry_1.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.inputs[1].default_value = [-1.0, -1.0, -1.0]
    vector_math_1.location = (-1000.0, 200.0)
    vector_math_1.operation = 'MULTIPLY'

    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-1000.0, 0.0)
    for socket in group_input_1.outputs:
        if socket.name != '-Normal':
            socket.hide = True

    vector_math_2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_2.location = (-760, 200.0)
    vector_math_2.operation = 'REFLECT'

    geometry_2 = node_tree.nodes.new(type='ShaderNodeNewGeometry')
    geometry_2.location = (-760.0, 0.0)
    for socket in geometry_2.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vector_math_3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_3.location = (-520.0, 200.0)
    vector_math_3.operation = 'DOT_PRODUCT'

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-520.0, -100.0)
    for socket in group_input_2.outputs:
        if socket.name not in ['Specular Alpha', 'MaxSpecPower']:
            socket.hide = True

    clamp_1 = node_tree.nodes.new(type='ShaderNodeClamp')
    clamp_1.inputs['Min'].default_value = 0.0
    clamp_1.inputs['Max'].default_value = 1.0
    clamp_1.location = (-280.0, 200.0)

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.inputs[2].default_value = 1.0
    math_1.location = (-280.0, -100.0)
    math_1.operation = 'MULTIPLY_ADD'

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-60.0, 200.0)
    for socket in group_input_3.outputs:
        if socket.name != 'Specular Color':
            socket.hide = True

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.location = (-60.0, 80.0)
    math_2.operation = 'POWER'

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (-60.0, -100.0)
    for socket in group_input_4.outputs:
        if socket.name != 'Normal':
            socket.hide = True

    geometry_3 = node_tree.nodes.new(type='ShaderNodeNewGeometry')
    geometry_3.location = (-60.0, -180.0)
    for socket in geometry_3.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vector_math_4 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_4.location = (180.0, 80.0)
    vector_math_4.operation = 'MULTIPLY'

    vector_math_5 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_5.location = (180.0, -100.0)
    vector_math_5.operation = 'DOT_PRODUCT'

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.inputs[1].default_value = 8.0
    math_3.location = (400.0, 80.0)
    math_3.operation = 'MULTIPLY'

    clamp_2 = node_tree.nodes.new(type='ShaderNodeClamp')
    clamp_2.inputs['Min'].default_value = 0.0
    clamp_2.inputs['Max'].default_value = 1.0
    clamp_2.location = (620.0, 80.0)

    vector_math_6 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_6.location = (840.0, 80.0)
    vector_math_6.operation = 'MULTIPLY'

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (1060.0, 80.0)

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (400.0, 100.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (800.0, 100.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (800.0, 40.0)

    # Link nodes together
    node_tree.links.new(geometry_1.outputs['Incoming'], vector_math_1.inputs[0])
    node_tree.links.new(vector_math_1.outputs['Vector'], vector_math_2.inputs[0])
    node_tree.links.new(group_input_1.outputs['-Normal'], vector_math_2.inputs[1])
    node_tree.links.new(vector_math_2.outputs['Vector'], vector_math_3.inputs[0])
    node_tree.links.new(geometry_2.outputs['Incoming'], vector_math_3.inputs[1])
    node_tree.links.new(vector_math_3.outputs['Value'], clamp_1.inputs['Value'])
    node_tree.links.new(clamp_1.outputs['Result'], math_2.inputs[0])
    node_tree.links.new(group_input_2.outputs['Specular Alpha'], math_1.inputs[0])
    node_tree.links.new(group_input_2.outputs['MaxSpecPower'], math_1.inputs[1])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[1])
    node_tree.links.new(group_input_3.outputs['Specular Color'], vector_math_4.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], vector_math_4.inputs[1])
    node_tree.links.new(group_input_4.outputs['Normal'], vector_math_5.inputs[0])
    node_tree.links.new(geometry_3.outputs['Incoming'], vector_math_5.inputs[1])
    node_tree.links.new(vector_math_4.outputs['Vector'], node_reroute_1.inputs[0])
    node_tree.links.new(vector_math_5.outputs['Value'], math_3.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], clamp_2.inputs['Value'])
    node_tree.links.new(clamp_2.outputs['Result'], vector_math_6.inputs[1])
    node_tree.links.new(node_reroute_2.outputs[0], node_reroute_3.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], vector_math_6.inputs[0])
    node_tree.links.new(vector_math_6.outputs['Vector'], group_output.inputs['Specular'])

    return node_tree


def get_specular_lookup():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'GetSpecularLookup' in bpy.data.node_groups:
        return bpy.data.node_groups['GetSpecularLookup']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='GetSpecularLookup', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketVector', name='Normal')
        node_tree.outputs.new(type='NodeSocketVector', name='Vector')
    else:
        node_tree.interface.new_socket('Normal', in_out='INPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('Vector', in_out='OUTPUT', socket_type='NodeSocketVector')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-540.0, 0.0)

    geometry_1 = node_tree.nodes.new(type='ShaderNodeNewGeometry')
    geometry_1.location = (-540.0, -80.0)
    for socket in geometry_1.outputs:
        if socket.name != 'Incoming':
            socket.hide = True

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.location = (-300.0, 0.0)
    vector_math_1.operation = 'DOT_PRODUCT'

    map_range = node_tree.nodes.new(type='ShaderNodeMapRange')
    map_range.clamp = True
    map_range.inputs['From Min'].default_value = -1.0
    map_range.inputs['From Max'].default_value = 1.0
    map_range.inputs['To Min'].default_value = 0.0
    map_range.inputs['To Max'].default_value = 1.0
    map_range.interpolation_type = 'SMOOTHSTEP'
    map_range.location = (-60.0, 0.0)

    combine_xyz = node_tree.nodes.new(type='ShaderNodeCombineXYZ')
    combine_xyz.inputs['Z'].default_value = 0.0
    combine_xyz.inputs['Z'].hide = True
    combine_xyz.location = (180.0, 0.0)

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (420.0, 0.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['Normal'], vector_math_1.inputs[0])
    node_tree.links.new(geometry_1.outputs['Incoming'], vector_math_1.inputs[1])
    node_tree.links.new(vector_math_1.outputs['Value'], map_range.inputs['Value'])
    node_tree.links.new(map_range.outputs['Result'], combine_xyz.inputs['X'])
    node_tree.links.new(map_range.outputs['Result'], combine_xyz.inputs['Y'])
    node_tree.links.new(combine_xyz.outputs['Vector'], group_output.inputs['Vector'])

    return node_tree


def hue_pixel():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'HuePixel' in bpy.data.node_groups:
        return bpy.data.node_groups['HuePixel']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='HuePixel', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='_d DiffuseMap Color')
        node_tree.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
        node_tree.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        node_tree.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='Hue')
        node_tree.inputs.new(type='NodeSocketFloat', name='Saturation')
        node_tree.inputs.new(type='NodeSocketFloat', name='Brightness')
        node_tree.inputs.new(type='NodeSocketFloat', name='Contrast')
        node_tree.inputs.new(type='NodeSocketColor', name='Metallic Specular')
        node_tree.inputs.new(type='NodeSocketColor', name='Specular')
        node_tree.outputs.new(type='NodeSocketColor', name='Diffuse Color')
        node_tree.outputs.new(type='NodeSocketColor', name='Specular Color')
    else:
        node_tree.interface.new_socket('_d DiffuseMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_s GlossMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_h PaletteMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_h PaletteMap Alpha', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('_m PaletteMaskMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Hue', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Saturation', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Contrast', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Metallic Specular', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Specular', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Diffuse Color', in_out='OUTPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Specular Color', in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-1400.0, 440.0)
    for socket in group_input_1.outputs:
        if socket.name != '_m PaletteMaskMap Color':
            socket.hide = True

    separate_xyz_1 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz_1.location = (-1060.0, 440.0)

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.location = (-600.0, 440.0)
    math_1.operation = 'ADD'

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-1400.0, 240.0)
    for socket in group_input_2.outputs:
        if socket.name not in [
            '_h PaletteMap Color',
            '_h PaletteMap Alpha',
            'Hue',
            'Saturation',
            'Brightness',
                'Contrast']:
            socket.hide = True

    manipulate_hsl_ = node_tree.nodes.new(type='ShaderNodeGroup')
    manipulate_hsl_.location = (-1180.0, 240.0)
    manipulate_hsl_.name = 'ManipulateHSL'
    manipulate_hsl_.node_tree = manipulate_hsl()
    manipulate_hsl_.width = 260.0

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.location = (-840.0, 140.0)
    math_2.operation = 'MULTIPLY'

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-600.0, 240.0)
    for socket in group_input_3.outputs:
        if socket.name != '_d DiffuseMap Color':
            socket.hide = True

    convert_hsl_to_rgb_ = node_tree.nodes.new(type='ShaderNodeGroup')
    convert_hsl_to_rgb_.location = (-600.0, 140.0)
    convert_hsl_to_rgb_.name = 'ConvertHSLtoRGB'
    convert_hsl_to_rgb_.node_tree = convert_hsl_to_rgb()

    mix_rgb_1 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_1.location = (-360.0, 140.0)

    gamma_1 = node_tree.nodes.new(type='ShaderNodeGamma')
    gamma_1.inputs['Gamma'].default_value = 2.1
    gamma_1.location = (-120.0, 140.0)

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.location = (160.0, 140.0)
    vector_math_1.operation = 'MULTIPLY'

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (-1400.0, -80.0)
    for socket in group_input_4.outputs:
        if socket.name not in ['_h PaletteMap Color', 'Brightness']:
            socket.hide = True

    manipulate_ao_ = node_tree.nodes.new(type='ShaderNodeGroup')
    manipulate_ao_.location = (-1180.0, -80.0)
    manipulate_ao_.name = 'ManipulateAO'
    manipulate_ao_.node_tree = manipulate_ao()
    manipulate_ao_.width = 260.0

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.inputs[1].default_value = 0.5
    math_3.location = (-840.0, -80.0)
    math_3.operation = 'SUBTRACT'

    math_4 = node_tree.nodes.new(type='ShaderNodeMath')
    math_4.inputs[1].default_value = 2.0
    math_4.location = (-600.0, -80.0)
    math_4.operation = 'MULTIPLY'

    mix_rgb_2 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_2.inputs['Color1'].default_value = [1.0, 1.0, 1.0, 1.0]
    mix_rgb_2.location = (-360.0, -80.0)

    math_5 = node_tree.nodes.new(type='ShaderNodeMath')
    math_5.inputs[1].default_value = 0.5
    math_5.location = (-100.0, -80.0)
    math_5.operation = 'GREATER_THAN'

    math_6 = node_tree.nodes.new(type='ShaderNodeMath')
    math_6.inputs[1].default_value = 1.0
    math_6.location = (160.0, -80.0)
    math_6.operation = 'LESS_THAN'

    vector_math_2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_2.location = (400.0, -80.0)
    vector_math_2.operation = 'MULTIPLY'

    vector_math_3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_3.location = (640.0, -80.0)
    vector_math_3.operation = 'ADD'

    vector_math_4 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_4.location = (880.0, -80.0)
    vector_math_4.operation = 'MULTIPLY'

    mix_rgb_3 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_3.location = (1120.0, -80.0)

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (1360.0, -80.0)

    math_7 = node_tree.nodes.new(type='ShaderNodeMath')
    math_7.inputs[1].default_value = 2.0
    math_7.location = (-840.0, -280.0)
    math_7.operation = 'MULTIPLY'

    group_input_5 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_5.location = (-600.0, -280.0)
    for socket in group_input_5.outputs:
        if socket.name not in ['Metallic Specular', 'Specular']:
            socket.hide = True

    mix_rgb_4 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_4.inputs['Color2'].default_value = [1.0, 1.0, 1.0, 1.0]
    mix_rgb_4.location = (-360.0, -280.0)

    group_input_6 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_6.location = (400.0, -280.0)
    for socket in group_input_6.outputs:
        if socket.name != '_s GlossMap Color':
            socket.hide = True

    separate_xyz_2 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz_2.location = (640.0, -280.0)
    separate_xyz_2.outputs['Y'].hide = True
    separate_xyz_2.outputs['Z'].hide = True

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (-880.0, 320.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (-380.0, 320.0)

    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (-840.0, 180.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (-620.0, 180.0)
    node_reroute_5 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_5.location = (-620.0, 80.0)
    node_reroute_6 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_6.location = (-840.0, 160.0)
    node_reroute_7 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_7.location = (-640.0, 160.0)
    node_reroute_8 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_8.location = (-640.0, 80.0)
    node_reroute_9 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_9.location = (-380.0, 160.0)
    node_reroute_10 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_10.location = (-380.0, 60.0)
    node_reroute_11 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_11.location = (300.0, 160.0)

    node_reroute_12 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_12.location = (-880.0, -60.0)
    node_reroute_13 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_13.location = (-880.0, -140.0)
    node_reroute_14 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_14.location = (-240.0, -60.0)
    node_reroute_15 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_15.location = (-100.0, -60.0)
    node_reroute_16 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_16.location = (40.0, -60.0)
    node_reroute_17 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_17.location = (180.0, -40.0)
    node_reroute_18 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_18.location = (500.0, -20.0)
    node_reroute_19 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_19.location = (500.0, -60.0)
    node_reroute_20 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_20.location = (600.0, -60.0)
    node_reroute_21 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_21.location = (600.0, -120.0)
    node_reroute_22 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_22.location = (1100.0, -20.0)
    node_reroute_23 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_23.location = (1100.0, -160.0)
    node_reroute_24 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_24.location = (1260.0, -40.0)

    node_reroute_25 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_25.location = (-880.0, -340.0)
    node_reroute_26 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_26.location = (-600.0, -260.0)
    node_reroute_27 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_27.location = (-380.0, -260.0)
    node_reroute_28 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_28.location = (-380.0, -360.0)
    node_reroute_29 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_29.location = (-100.0, -260.0)
    node_reroute_30 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_30.location = (300.0, -260.0)
    node_reroute_31 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_31.location = (640.0, -260.0)
    node_reroute_32 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_32.location = (1020.0, -260.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['_m PaletteMaskMap Color'], separate_xyz_1.inputs['Vector'])
    node_tree.links.new(separate_xyz_1.outputs['X'], math_1.inputs[0])
    node_tree.links.new(separate_xyz_1.outputs['Y'], math_1.inputs[1])
    node_tree.links.new(separate_xyz_1.outputs['Z'], node_reroute_1.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_12.inputs[0])
    node_tree.links.new(math_1.outputs['Value'], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], node_reroute_9.inputs[0])

    node_tree.links.new(group_input_2.outputs['_h PaletteMap Color'], manipulate_hsl_.inputs['_h PaletteMap Color'])
    node_tree.links.new(group_input_2.outputs['_h PaletteMap Alpha'], manipulate_hsl_.inputs['_h PaletteMap Alpha'])
    node_tree.links.new(group_input_2.outputs['Hue'], manipulate_hsl_.inputs['Hue'])
    node_tree.links.new(group_input_2.outputs['Saturation'], manipulate_hsl_.inputs['Saturation'])
    node_tree.links.new(group_input_2.outputs['Brightness'], manipulate_hsl_.inputs['Brightness'])
    node_tree.links.new(group_input_2.outputs['Contrast'], manipulate_hsl_.inputs['Contrast'])
    node_tree.links.new(manipulate_hsl_.outputs['H'], node_reroute_3.inputs[0])
    node_tree.links.new(manipulate_hsl_.outputs['S'], node_reroute_6.inputs[0])
    node_tree.links.new(manipulate_hsl_.outputs['L'], math_2.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(node_reroute_6.outputs[0], node_reroute_7.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], convert_hsl_to_rgb_.inputs['L'])
    node_tree.links.new(node_reroute_4.outputs[0], node_reroute_5.inputs[0])
    node_tree.links.new(node_reroute_7.outputs[0], node_reroute_8.inputs[0])
    node_tree.links.new(node_reroute_8.outputs[0], convert_hsl_to_rgb_.inputs['S'])
    node_tree.links.new(node_reroute_5.outputs[0], convert_hsl_to_rgb_.inputs['H'])
    node_tree.links.new(group_input_3.outputs['_d DiffuseMap Color'], mix_rgb_1.inputs['Color1'])
    node_tree.links.new(convert_hsl_to_rgb_.outputs['RGB'], mix_rgb_1.inputs['Color2'])
    node_tree.links.new(node_reroute_9.outputs[0], node_reroute_10.inputs[0])
    node_tree.links.new(node_reroute_9.outputs[0], node_reroute_11.inputs[0])
    node_tree.links.new(node_reroute_10.outputs[0], mix_rgb_1.inputs['Fac'])
    node_tree.links.new(mix_rgb_1.outputs['Color'], gamma_1.inputs['Color'])
    node_tree.links.new(gamma_1.outputs['Color'], node_reroute_17.inputs[0])
    node_tree.links.new(vector_math_1.outputs['Vector'], node_reroute_19.inputs[0])
    node_tree.links.new(node_reroute_17.outputs[0], node_reroute_24.inputs[0])
    node_tree.links.new(node_reroute_11.outputs[0], node_reroute_18.inputs[0])

    node_tree.links.new(group_input_4.outputs['_h PaletteMap Color'], manipulate_ao_.inputs['_h PaletteMap Color'])
    node_tree.links.new(group_input_4.outputs['Brightness'], manipulate_ao_.inputs['Brightness'])
    node_tree.links.new(manipulate_ao_.outputs['AO'], math_2.inputs[1])
    node_tree.links.new(node_reroute_12.outputs[0], node_reroute_13.inputs[0])
    node_tree.links.new(node_reroute_12.outputs[0], node_reroute_14.inputs[0])
    node_tree.links.new(node_reroute_13.outputs[0], math_3.inputs[0])
    node_tree.links.new(node_reroute_13.outputs[0], node_reroute_25.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], math_4.inputs[0])
    node_tree.links.new(math_4.outputs['Value'], mix_rgb_2.inputs['Fac'])
    node_tree.links.new(mix_rgb_2.outputs['Color'], node_reroute_15.inputs[0])
    node_tree.links.new(node_reroute_14.outputs[0], math_5.inputs[0])
    node_tree.links.new(node_reroute_15.outputs[0], node_reroute_16.inputs[0])
    node_tree.links.new(math_5.outputs['Value'], vector_math_1.inputs[1])
    node_tree.links.new(math_5.outputs['Value'], math_6.inputs[0])
    node_tree.links.new(node_reroute_16.outputs[0], vector_math_1.inputs[0])
    node_tree.links.new(math_6.outputs['Value'], vector_math_2.inputs[1])
    node_tree.links.new(vector_math_2.outputs['Vector'], vector_math_3.inputs[1])
    node_tree.links.new(node_reroute_18.outputs[0], node_reroute_22.inputs[0])
    node_tree.links.new(node_reroute_19.outputs[0], node_reroute_20.inputs[0])
    node_tree.links.new(node_reroute_20.outputs[0], node_reroute_21.inputs[0])
    node_tree.links.new(node_reroute_21.outputs[0], vector_math_3.inputs[0])
    node_tree.links.new(vector_math_3.outputs['Vector'], vector_math_4.inputs[0])
    node_tree.links.new(vector_math_4.outputs['Vector'], mix_rgb_3.inputs['Color2'])
    node_tree.links.new(node_reroute_22.outputs[0], node_reroute_23.inputs[0])
    node_tree.links.new(node_reroute_23.outputs[0], mix_rgb_3.inputs['Fac'])
    node_tree.links.new(mix_rgb_3.outputs['Color'], group_output.inputs['Specular Color'])
    node_tree.links.new(node_reroute_24.outputs[0], group_output.inputs['Diffuse Color'])

    node_tree.links.new(node_reroute_25.outputs[0], math_7.inputs[0])
    node_tree.links.new(math_7.outputs['Value'], node_reroute_26.inputs[0])
    node_tree.links.new(node_reroute_26.outputs[0], node_reroute_27.inputs[0])
    node_tree.links.new(group_input_5.outputs['Metallic Specular'], mix_rgb_2.inputs['Color2'])
    node_tree.links.new(group_input_5.outputs['Specular'], mix_rgb_4.inputs['Color1'])
    node_tree.links.new(node_reroute_27.outputs[0], node_reroute_28.inputs[0])
    node_tree.links.new(node_reroute_28.outputs[0], mix_rgb_4.inputs['Fac'])
    node_tree.links.new(mix_rgb_4.outputs['Color'], node_reroute_29.inputs[0])
    node_tree.links.new(node_reroute_29.outputs[0], node_reroute_30.inputs[0])
    node_tree.links.new(node_reroute_30.outputs[0], vector_math_2.inputs[0])
    node_tree.links.new(group_input_6.outputs['_s GlossMap Color'], node_reroute_31.inputs[0])
    node_tree.links.new(group_input_6.outputs['_s GlossMap Color'], separate_xyz_2.inputs['Vector'])
    node_tree.links.new(node_reroute_31.outputs[0], node_reroute_32.inputs[0])
    node_tree.links.new(separate_xyz_2.outputs['X'], vector_math_4.inputs[1])
    node_tree.links.new(node_reroute_32.outputs[0], mix_rgb_3.inputs['Color1'])

    return node_tree


def hue_skin_pixel():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'HueSkinPixel' in bpy.data.node_groups:
        return bpy.data.node_groups['HueSkinPixel']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='HueSkinPixel', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='_d DiffuseMap Color')
        node_tree.inputs.new(type='NodeSocketColor', name='_s GlossMap Color')
        node_tree.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        node_tree.inputs.new(type='NodeSocketColor', name='_m PaletteMaskMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='Hue')
        node_tree.inputs.new(type='NodeSocketFloat', name='Saturation')
        node_tree.inputs.new(type='NodeSocketFloat', name='Brightness')
        node_tree.inputs.new(type='NodeSocketFloat', name='Contrast')
        node_tree.inputs.new(type='NodeSocketColor', name='Specular')
        node_tree.inputs.new(type='NodeSocketColor', name='Metallic Specular')
        node_tree.outputs.new(type='NodeSocketColor', name='Diffuse Color')
        node_tree.outputs.new(type='NodeSocketColor', name='Specular Color')
    else:
        node_tree.interface.new_socket('_d DiffuseMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_s GlossMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_h PaletteMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_h PaletteMap Alpha', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('_m PaletteMaskMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Hue', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Saturation', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Contrast', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Specular', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Metallic Specular', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Diffuse Color', in_out='OUTPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Specular Color', in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-1160.0, 460.0)
    for socket in group_input_1.outputs:
        if socket.name != '_m PaletteMaskMap Color':
            socket.hide = True

    separate_xyz_1 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz_1.location = (-940.0, 460.0)
    separate_xyz_1.outputs['Z'].hide = True

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.location = (-720.0, 460.0)
    math_1.operation = 'ADD'

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-1500.0, 260.0)
    for socket in group_input_2.outputs:
        if socket.name not in ['_h PaletteMap Color',
                               '_h PaletteMap Alpha',
                               'Hue',
                               'Saturation',
                               'Brightness',
                               'Contrast']:
            socket.hide = True

    manipulate_hsl_ = node_tree.nodes.new(type='ShaderNodeGroup')
    manipulate_hsl_.location = (-1280.0, 260.0)
    manipulate_hsl_.node_tree = manipulate_skin_hsl()
    manipulate_hsl_.width = 260.0

    convert_hsl_to_rgb_ = node_tree.nodes.new(type='ShaderNodeGroup')
    convert_hsl_to_rgb_.location = (-940.0, 260.0)
    convert_hsl_to_rgb_.node_tree = convert_hsl_to_rgb()

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.location = (-720.0, 260.0)
    vector_math_1.operation = 'MULTIPLY'

    mix_rgb_1 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_1.location = (-500.0, 260.0)

    gamma_1 = node_tree.nodes.new(type='ShaderNodeGamma')
    gamma_1.inputs['Gamma'].default_value = 2.1
    gamma_1.location = (-280.0, 260.0)

    separate_xyz_2 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz_2.location = (-940.0, 80.0)
    separate_xyz_2.outputs['Y'].hide = True
    separate_xyz_2.outputs['Z'].hide = True

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-720.0, 80.0)
    for socket in group_input_3.outputs:
        if socket.name != '_d DiffuseMap Color':
            socket.hide = True

    vector_math_2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_2.location = (420.0, 80.0)
    vector_math_2.operation = 'MULTIPLY'

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (-1160.0, -100.0)
    for socket in group_input_4.outputs:
        if socket.name != '_h PaletteMap Color':
            socket.hide = True

    group_input_5 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_5.location = (-940.0, -100.0)
    for socket in group_input_5.outputs:
        if socket.name != '_m PaletteMaskMap Color':
            socket.hide = True

    separate_xyz_3 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz_3.location = (-720.0, -100.0)
    separate_xyz_3.outputs['X'].hide = True
    separate_xyz_3.outputs['Y'].hide = True

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.inputs[1].default_value = 0.5
    math_2.location = (-500.0, -100.0)
    math_2.operation = 'SUBTRACT'

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.inputs[1].default_value = 2.0
    math_3.location = (-280.0, -100.0)
    math_3.operation = 'MULTIPLY'

    mix_rgb_2 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_2.inputs['Color1'].default_value = [1.0, 1.0, 1.0, 1.0]
    mix_rgb_2.location = (-60.0, -100.0)

    math_4 = node_tree.nodes.new(type='ShaderNodeMath')
    math_4.inputs[1].default_value = 0.5
    math_4.location = (180.0, -100.0)
    math_4.operation = 'GREATER_THAN'

    math_5 = node_tree.nodes.new(type='ShaderNodeMath')
    math_5.inputs[1].default_value = 1.0
    math_5.location = (420.0, -100.0)
    math_5.operation = 'LESS_THAN'

    vector_math_3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_3.location = (640.0, -100.0)
    vector_math_3.operation = 'MULTIPLY'

    vector_math_4 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_4.location = (860.0, -100.0)
    vector_math_4.operation = 'ADD'

    vector_math_5 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_5.location = (1080.0, -100.0)
    vector_math_5.operation = 'MULTIPLY'

    mix_rgb_3 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_3.location = (1300.0, -100.0)

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (1520.0, -100.0)

    math_6 = node_tree.nodes.new(type='ShaderNodeMath')
    math_6.inputs[1].default_value = 2.0
    math_6.location = (-500.0, -320.0)
    math_6.operation = 'MULTIPLY'

    group_input_6 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_6.location = (-280.0, -320.0)
    for socket in group_input_6.outputs:
        if socket.name != 'Metallic Specular':
            socket.hide = True

    group_input_7 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_7.location = (-280.0, -440.0)
    for socket in group_input_7.outputs:
        if socket.name != 'Specular':
            socket.hide = True

    mix_rgb_4 = node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_4.inputs['Color2'].default_value = [1.0, 1.0, 1.0, 1.0]
    mix_rgb_4.location = (-60.0, -320.0)

    group_input_8 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_8.location = (640.0, -320.0)
    for socket in group_input_8.outputs:
        if socket.name != '_s GlossMap Color':
            socket.hide = True

    separate_xyz_4 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz_4.location = (860.0, -320.0)
    separate_xyz_4.outputs['Y'].hide = True
    separate_xyz_4.outputs['Z'].hide = True

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (-540.0, 380.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (-540.0, 280.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (-540.0, 200.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (-100.0, 280.0)
    node_reroute_5 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_5.location = (-100.0, 180.0)
    node_reroute_6 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_6.location = (1280.0, 180.0)
    node_reroute_7 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_7.location = (1280.0, -180.0)

    node_reroute_8 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_8.location = (-60.0, 200.0)
    node_reroute_9 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_9.location = (1300.0, 200.0)
    node_reroute_10 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_10.location = (1300.0, -80.0)
    node_reroute_11 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_11.location = (1440.0, -80.0)

    node_reroute_12 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_12.location = (-540.0, -180.0)
    node_reroute_13 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_13.location = (-540.0, -300.0)
    node_reroute_14 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_14.location = (-540.0, -380.0)
    node_reroute_15 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_15.location = (80.0, -300.0)

    node_reroute_16 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_16.location = (180.0, -80.0)
    node_reroute_17 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_17.location = (320.0, -80.0)

    node_reroute_18 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_18.location = (700.0, -80.0)
    node_reroute_19 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_19.location = (820.0, -80.0)
    node_reroute_20 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_20.location = (820.0, -140.0)

    node_reroute_21 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_21.location = (-280.0, -420.0)
    node_reroute_22 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_22.location = (-140.0, -420.0)

    node_reroute_23 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_23.location = (180.0, -300.0)
    node_reroute_24 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_24.location = (520.0, -300.0)

    node_reroute_25 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_25.location = (860.0, -300.0)
    node_reroute_26 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_26.location = (1220.0, -300.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['_m PaletteMaskMap Color'], separate_xyz_1.inputs['Vector'])
    node_tree.links.new(separate_xyz_1.outputs['X'], math_1.inputs[0])
    node_tree.links.new(separate_xyz_1.outputs['Y'], math_1.inputs[1])
    node_tree.links.new(math_1.outputs['Value'], node_reroute_1.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], node_reroute_3.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], mix_rgb_1.inputs['Fac'])
    node_tree.links.new(node_reroute_4.outputs[0], node_reroute_5.inputs[0])
    node_tree.links.new(node_reroute_5.outputs[0], node_reroute_6.inputs[0])
    node_tree.links.new(node_reroute_6.outputs[0], node_reroute_7.inputs[0])
    node_tree.links.new(node_reroute_7.outputs[0], mix_rgb_3.inputs['Fac'])

    node_tree.links.new(group_input_2.outputs['_h PaletteMap Color'], manipulate_hsl_.inputs['_h PaletteMap Color'])
    node_tree.links.new(group_input_2.outputs['_h PaletteMap Alpha'], manipulate_hsl_.inputs['_h PaletteMap Alpha'])
    node_tree.links.new(group_input_2.outputs['Hue'], manipulate_hsl_.inputs['Hue'])
    node_tree.links.new(group_input_2.outputs['Saturation'], manipulate_hsl_.inputs['Saturation'])
    node_tree.links.new(group_input_2.outputs['Brightness'], manipulate_hsl_.inputs['Brightness'])
    node_tree.links.new(group_input_2.outputs['Contrast'], manipulate_hsl_.inputs['Contrast'])
    node_tree.links.new(manipulate_hsl_.outputs['H'], convert_hsl_to_rgb_.inputs['H'])
    node_tree.links.new(manipulate_hsl_.outputs['S'], convert_hsl_to_rgb_.inputs['S'])
    node_tree.links.new(manipulate_hsl_.outputs['L'], convert_hsl_to_rgb_.inputs['L'])
    node_tree.links.new(convert_hsl_to_rgb_.outputs['RGB'], vector_math_1.inputs[0])
    node_tree.links.new(vector_math_1.outputs['Vector'], mix_rgb_1.inputs['Color2'])
    node_tree.links.new(mix_rgb_1.outputs['Color'], gamma_1.inputs['Color'])
    node_tree.links.new(gamma_1.outputs['Color'], node_reroute_8.inputs[0])
    node_tree.links.new(node_reroute_8.outputs[0], node_reroute_9.inputs[0])
    node_tree.links.new(node_reroute_9.outputs[0], node_reroute_10.inputs[0])
    node_tree.links.new(node_reroute_10.outputs[0], node_reroute_11.inputs[0])
    node_tree.links.new(node_reroute_11.outputs[0], group_output.inputs['Diffuse Color'])

    node_tree.links.new(separate_xyz_2.outputs['X'], vector_math_1.inputs[1])
    node_tree.links.new(group_input_3.outputs['_d DiffuseMap Color'], mix_rgb_1.inputs['Color1'])
    node_tree.links.new(vector_math_2.outputs['Vector'], node_reroute_18.inputs[0])
    node_tree.links.new(node_reroute_18.outputs[0], node_reroute_19.inputs[0])
    node_tree.links.new(node_reroute_19.outputs[0], node_reroute_20.inputs[0])
    node_tree.links.new(node_reroute_20.outputs[0], vector_math_4.inputs[0])

    node_tree.links.new(group_input_4.outputs['_h PaletteMap Color'], separate_xyz_2.inputs['Vector'])
    node_tree.links.new(group_input_5.outputs['_m PaletteMaskMap Color'], separate_xyz_3.inputs['Vector'])
    node_tree.links.new(separate_xyz_3.outputs['Z'], node_reroute_12.inputs[0])
    node_tree.links.new(node_reroute_12.outputs[0], node_reroute_13.inputs[0])
    node_tree.links.new(node_reroute_12.outputs[0], math_2.inputs[0])
    node_tree.links.new(node_reroute_13.outputs[0], node_reroute_14.inputs[0])
    node_tree.links.new(node_reroute_13.outputs[0], node_reroute_15.inputs[0])
    node_tree.links.new(node_reroute_14.outputs[0], math_6.inputs[0])
    node_tree.links.new(node_reroute_15.outputs[0], math_4.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], math_3.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], mix_rgb_2.inputs['Fac'])
    node_tree.links.new(mix_rgb_2.outputs['Color'], node_reroute_16.inputs[0])
    node_tree.links.new(node_reroute_16.outputs[0], node_reroute_17.inputs[0])
    node_tree.links.new(node_reroute_17.outputs[0], vector_math_2.inputs[0])
    node_tree.links.new(math_4.outputs['Value'], vector_math_2.inputs[1])
    node_tree.links.new(math_4.outputs['Value'], math_5.inputs[0])
    node_tree.links.new(math_5.outputs['Value'], vector_math_3.inputs[1])
    node_tree.links.new(vector_math_3.outputs['Vector'], vector_math_4.inputs[1])
    node_tree.links.new(vector_math_4.outputs['Vector'], vector_math_5.inputs[0])
    node_tree.links.new(vector_math_5.outputs['Vector'], mix_rgb_3.inputs['Color2'])
    node_tree.links.new(mix_rgb_3.outputs['Color'], group_output.inputs['Specular Color'])

    node_tree.links.new(math_6.outputs['Value'], node_reroute_21.inputs[0])
    node_tree.links.new(node_reroute_21.outputs[0], node_reroute_22.inputs[0])
    node_tree.links.new(node_reroute_22.outputs[0], mix_rgb_4.inputs['Fac'])
    node_tree.links.new(group_input_6.outputs['Metallic Specular'], mix_rgb_2.inputs['Color2'])
    node_tree.links.new(group_input_7.outputs['Specular'], mix_rgb_4.inputs['Color1'])
    node_tree.links.new(mix_rgb_4.outputs['Color'], node_reroute_23.inputs[0])
    node_tree.links.new(node_reroute_23.outputs[0], node_reroute_24.inputs[0])
    node_tree.links.new(node_reroute_24.outputs[0], vector_math_3.inputs[0])
    node_tree.links.new(group_input_8.outputs['_s GlossMap Color'], node_reroute_25.inputs[0])
    node_tree.links.new(node_reroute_25.outputs[0], node_reroute_26.inputs[0])
    node_tree.links.new(node_reroute_26.outputs[0], mix_rgb_3.inputs['Color1'])
    node_tree.links.new(group_input_8.outputs['_s GlossMap Color'], separate_xyz_4.inputs['Vector'])
    node_tree.links.new(separate_xyz_4.outputs['X'], vector_math_5.inputs[1])

    return node_tree


def negative_normal():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'NegativeNormal' in bpy.data.node_groups:
        return bpy.data.node_groups['NegativeNormal']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='NegativeNormal', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketVector', name='Normal')
        node_tree.outputs.new(type='NodeSocketVector', name='-Normal')
    else:
        node_tree.interface.new_socket('Normal', in_out='INPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('-Normal', in_out='OUTPUT', socket_type='NodeSocketVector')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-720.0, 0.0)

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.inputs[1].default_value = [2.0, 2.0, 2.0]
    vector_math_1.location = (-480.0, 0.0)
    vector_math_1.operation = 'MULTIPLY'

    vector_math_2 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_2.inputs[1].default_value = [1.0, 1.0, 1.0]
    vector_math_2.location = (-240.0, 0.0)
    vector_math_2.operation = 'SUBTRACT'

    vector_math_3 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_3.inputs[1].default_value = [-1.0, -1.0, 1.0]
    vector_math_3.location = (0.0, 0.0)
    vector_math_3.operation = 'MULTIPLY'

    vector_math_4 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_4.inputs[1].default_value = [1.0, 1.0, 1.0]
    vector_math_4.location = (240.0, 0.0)
    vector_math_4.operation = 'ADD'

    vector_math_5 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_5.inputs[1].default_value = [2.0, 2.0, 2.0]
    vector_math_5.location = (480.0, 0.0)
    vector_math_5.operation = 'DIVIDE'

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (720.0, 0.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['Normal'], vector_math_1.inputs[0])
    node_tree.links.new(vector_math_1.outputs['Vector'], vector_math_2.inputs[0])
    node_tree.links.new(vector_math_2.outputs['Vector'], vector_math_3.inputs[0])
    node_tree.links.new(vector_math_3.outputs['Vector'], vector_math_4.inputs[0])
    node_tree.links.new(vector_math_4.outputs['Vector'], vector_math_5.inputs[0])
    node_tree.links.new(vector_math_5.outputs['Vector'], group_output.inputs['-Normal'])

    return node_tree


def manipulate_ao():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'ManipulateAO' in bpy.data.node_groups:
        return bpy.data.node_groups['ManipulateAO']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='ManipulateAO', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='Brightness')
        node_tree.outputs.new(type='NodeSocketFloat', name='AO')
    else:
        node_tree.interface.new_socket('_h PaletteMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('AO', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-840.0, 120.0)
    group_input_1.outputs['_h PaletteMap Color'].hide = True

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-840.0, -60.0)
    group_input_2.outputs['Brightness'].hide = True

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.inputs[1].default_value = 1.0
    math_1.location = (-620.0, 120.0)
    math_1.operation = 'ADD'

    separate_xyz = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz.location = (-620.0, -60.0)
    separate_xyz.outputs['Y'].hide = True
    separate_xyz.outputs['Z'].hide = True

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.inputs[0].default_value = 1.0
    math_2.location = (-400.0, 120.0)
    math_2.operation = 'SUBTRACT'

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.location = (-180.0, 120.0)
    math_3.operation = 'MULTIPLY'

    math_4 = node_tree.nodes.new(type='ShaderNodeMath')
    math_4.location = (40.0, 120.0)
    math_4.operation = 'ADD'

    math_5 = node_tree.nodes.new(type='ShaderNodeMath')
    math_5.location = (260.0, 120.0)
    math_5.operation = 'MULTIPLY'

    clamp_1 = node_tree.nodes.new(type='ShaderNodeClamp')
    clamp_1.inputs['Min'].default_value = 0.0
    clamp_1.inputs['Max'].default_value = 1.0
    clamp_1.location = (480.0, 120.0)

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (700.0, 120.0)

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (-400.0, 140.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (-400.0, -60.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (-260.0, -60.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (20.0, 140.0)
    node_reroute_5 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_5.location = (20.0, 40.0)
    node_reroute_6 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_6.location = (180.0, -60.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['Brightness'], math_1.inputs[0])
    node_tree.links.new(group_input_2.outputs['_h PaletteMap Color'], separate_xyz.inputs['Vector'])
    node_tree.links.new(math_1.outputs['Value'], node_reroute_1.inputs[0])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[1])
    node_tree.links.new(separate_xyz.outputs['X'], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], math_3.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], node_reroute_3.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], math_3.inputs[1])
    node_tree.links.new(node_reroute_3.outputs[0], node_reroute_6.inputs[0])
    node_tree.links.new(math_3.outputs['Value'], math_4.inputs[1])
    node_tree.links.new(node_reroute_4.outputs[0], node_reroute_5.inputs[0])
    node_tree.links.new(node_reroute_5.outputs[0], math_4.inputs[0])
    node_tree.links.new(math_4.outputs['Value'], math_5.inputs[1])
    node_tree.links.new(node_reroute_6.outputs[0], math_5.inputs[0])
    node_tree.links.new(math_5.outputs['Value'], clamp_1.inputs['Value'])
    node_tree.links.new(clamp_1.outputs['Result'], group_output.inputs['AO'])

    return node_tree


def manipulate_hsl():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'ManipulateHSL' in bpy.data.node_groups:
        return bpy.data.node_groups['ManipulateHSL']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='ManipulateHSL', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        node_tree.inputs.new(type='NodeSocketFloat', name='Hue')
        node_tree.inputs.new(type='NodeSocketFloat', name='Saturation')
        node_tree.inputs.new(type='NodeSocketFloat', name='Brightness')
        node_tree.inputs.new(type='NodeSocketFloat', name='Contrast')
        node_tree.outputs.new(type='NodeSocketFloat', name='H')
        node_tree.outputs.new(type='NodeSocketFloat', name='S')
        node_tree.outputs.new(type='NodeSocketFloat', name='L')
    else:
        node_tree.interface.new_socket('_h PaletteMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_h PaletteMap Alpha', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Hue', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Saturation', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Contrast', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('H', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('S', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('L', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-400.0, 200.0)
    for socket in group_input_1.outputs:
        if socket.name not in ['_h PaletteMap Color', '_h PaletteMap Alpha']:
            socket.hide = True

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-180.0, 280.0)
    for socket in group_input_2.outputs:
        if socket.name != 'Hue':
            socket.hide = True

    expand_hsl_ = node_tree.nodes.new(type='ShaderNodeGroup')
    expand_hsl_.location = (-180.0, 200.0)
    expand_hsl_.name = 'ExpandHSL'
    expand_hsl_.node_tree = expand_hsl()

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-180.0, 20.0)
    for socket in group_input_3.outputs:
        if socket.name != 'Saturation':
            socket.hide = True

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (-180.0, -120.0)
    for socket in group_input_4.outputs:
        if socket.name not in ['Brightness', 'Contrast']:
            socket.hide = True

    offset_hue_ = node_tree.nodes.new(type='ShaderNodeGroup')
    offset_hue_.location = (40.0, 280.0)
    offset_hue_.name = 'OffsetHue'
    offset_hue_.node_tree = offset_hue()

    offset_saturation_ = node_tree.nodes.new(type='ShaderNodeGroup')
    offset_saturation_.location = (40.0, 20.0)
    offset_saturation_.name = 'OffsetSaturation'
    offset_saturation_.node_tree = offset_saturation()

    adjust_lightness_ = node_tree.nodes.new(type='ShaderNodeGroup')
    adjust_lightness_.location = (40.0, -120.0)
    adjust_lightness_.name = 'AdjustLightness'
    adjust_lightness_.node_tree = adjust_lightness()

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (260.0, 280.0)

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (0.0, 80.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (0.0, -160.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (20.0, 80.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (20.0, -40.0)
    node_reroute_5 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_5.location = (200.0, 160.0)
    node_reroute_6 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_6.location = (200.0, 20.0)
    node_reroute_7 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_7.location = (220.0, 160.0)
    node_reroute_8 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_8.location = (220.0, -100.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['_h PaletteMap Color'], expand_hsl_.inputs['_h PaletteMap Color'])
    node_tree.links.new(group_input_1.outputs['_h PaletteMap Alpha'], expand_hsl_.inputs['_h PaletteMap Alpha'])
    node_tree.links.new(group_input_2.outputs['Hue'], offset_hue_.inputs['Hue'])
    node_tree.links.new(expand_hsl_.outputs['H'], offset_hue_.inputs['H'])
    node_tree.links.new(expand_hsl_.outputs['S'], node_reroute_3.inputs[0])
    node_tree.links.new(expand_hsl_.outputs['L'], node_reroute_1.inputs[0])
    node_tree.links.new(group_input_3.outputs['Saturation'], offset_saturation_.inputs['Saturation'])
    node_tree.links.new(group_input_4.outputs['Brightness'], adjust_lightness_.inputs['Brightness'])
    node_tree.links.new(group_input_4.outputs['Contrast'], adjust_lightness_.inputs['Contrast'])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], adjust_lightness_.inputs['L'])
    node_tree.links.new(node_reroute_3.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(node_reroute_4.outputs[0], offset_saturation_.inputs['S'])
    node_tree.links.new(offset_hue_.outputs['H'], group_output.inputs['H'])
    node_tree.links.new(offset_saturation_.outputs['S'], node_reroute_6.inputs[0])
    node_tree.links.new(adjust_lightness_.outputs['L'], node_reroute_8.inputs[0])
    node_tree.links.new(node_reroute_5.outputs[0], group_output.inputs['S'])
    node_tree.links.new(node_reroute_6.outputs[0], node_reroute_5.inputs[0])
    node_tree.links.new(node_reroute_7.outputs[0], group_output.inputs['L'])
    node_tree.links.new(node_reroute_8.outputs[0], node_reroute_7.inputs[0])

    return node_tree


def manipulate_skin_hsl():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'ManipulateSkinHSL' in bpy.data.node_groups:
        return bpy.data.node_groups['ManipulateSkinHSL']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='ManipulateSkinHSL', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='_h PaletteMap Color')
        node_tree.inputs.new(type='NodeSocketFloat', name='_h PaletteMap Alpha')
        node_tree.inputs.new(type='NodeSocketFloat', name='Hue')
        node_tree.inputs.new(type='NodeSocketFloat', name='Saturation')
        node_tree.inputs.new(type='NodeSocketFloat', name='Brightness')
        node_tree.inputs.new(type='NodeSocketFloat', name='Contrast')
        node_tree.outputs.new(type='NodeSocketFloat', name='H')
        node_tree.outputs.new(type='NodeSocketFloat', name='S')
        node_tree.outputs.new(type='NodeSocketFloat', name='L')
    else:
        node_tree.interface.new_socket('_h PaletteMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.new_socket('_h PaletteMap Alpha', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Hue', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Saturation', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Brightness', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Contrast', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('H', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('S', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('L', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-400.0, 360.0)
    for socket in group_input_1.outputs:
        if socket.name != 'Hue':
            socket.hide = True

    math = node_tree.nodes.new(type='ShaderNodeMath')
    math.inputs[1].default_value = 0.5
    math.location = (-180.0, 360.0)
    math.operation = 'SUBTRACT'

    offset_hue_ = node_tree.nodes.new(type='ShaderNodeGroup')
    offset_hue_.location = (40.0, 360.0)
    offset_hue_.name = 'OffsetHue'
    offset_hue_.node_tree = offset_hue()

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (260.0, 360.0)

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-400.0, 200.0)
    for socket in group_input_2.outputs:
        if socket.name != '_h PaletteMap Color':
            socket.hide = True

    separate_xyz = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz.location = (-180.0, 200.0)
    separate_xyz.outputs['X'].hide = True

    offset_saturation_ = node_tree.nodes.new(type='ShaderNodeGroup')
    offset_saturation_.location = (40.0, 200.0)
    offset_saturation_.name = 'OffsetSkinSaturation'
    offset_saturation_.node_tree = offset_skin_saturation()

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-180.0, 100.0)
    for socket in group_input_3.outputs:
        if socket.name != 'Saturation':
            socket.hide = True

    group_input_4 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_4.location = (-180.0, 20.0)
    for socket in group_input_4.outputs:
        if socket.name not in ['_h PaletteMask Alpha', 'Brightness', 'Contrast']:
            socket.hide = True

    adjust_lightness_ = node_tree.nodes.new(type='ShaderNodeGroup')
    adjust_lightness_.location = (40.0, 20.0)
    adjust_lightness_.name = 'AdjustLightness'
    adjust_lightness_.node_tree = adjust_lightness()

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (200.0, 200.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (200.0, 240.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (220.0, 40.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (220.0, 240.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['Hue'], math.inputs[0])
    node_tree.links.new(math.outputs['Value'], offset_hue_.inputs['Hue'])
    node_tree.links.new(offset_hue_.outputs['H'], group_output.inputs['H'])
    node_tree.links.new(group_input_2.outputs['_h PaletteMap Color'], separate_xyz.inputs['Vector'])
    node_tree.links.new(separate_xyz.outputs['Y'], offset_hue_.inputs['H'])
    node_tree.links.new(separate_xyz.outputs['Z'], offset_saturation_.inputs['S'])
    node_tree.links.new(offset_saturation_.outputs['S'], node_reroute_1.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], group_output.inputs['S'])
    node_tree.links.new(group_input_3.outputs['Saturation'], offset_saturation_.inputs['Saturation'])
    node_tree.links.new(group_input_4.outputs['_h PaletteMap Alpha'], adjust_lightness_.inputs['L'])
    node_tree.links.new(group_input_4.outputs['Brightness'], adjust_lightness_.inputs['Brightness'])
    node_tree.links.new(group_input_4.outputs['Contrast'], adjust_lightness_.inputs['Contrast'])
    node_tree.links.new(adjust_lightness_.outputs['L'], node_reroute_3.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(node_reroute_4.outputs[0], group_output.inputs['L'])

    return node_tree


def normal_and_alpha_from_swizzled_texture():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'NormalAndAlphaFromSwizzledTexture' in bpy.data.node_groups:
        return bpy.data.node_groups['NormalAndAlphaFromSwizzledTexture']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(
        name='NormalAndAlphaFromSwizzledTexture',
        type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketColor', name='_n RotationMap Color')
        node_tree.inputs['_n RotationMap Color'].default_value = [0.0, 0.5, 0.0, 1.0]
        node_tree.inputs.new(type='NodeSocketFloat', name='_n RotationMap Alpha')
        node_tree.inputs['_n RotationMap Alpha'].default_value = 0.5
        node_tree.outputs.new(type='NodeSocketVector', name='Normal')
        node_tree.outputs.new(type='NodeSocketFloat', name='Alpha')
        node_tree.outputs.new(type='NodeSocketFloat', name='Emission Strength')
    else:
        node_tree.interface.new_socket('_n RotationMap Color', in_out='INPUT', socket_type='NodeSocketColor')
        node_tree.interface.items_tree['_n RotationMap Color'].default_value = [0.0, 0.5, 0.0, 1.0]
        node_tree.interface.new_socket('_n RotationMap Alpha', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.items_tree['_n RotationMap Alpha'].default_value = 0.5
        node_tree.interface.new_socket('Normal', in_out='OUTPUT', socket_type='NodeSocketVector')
        node_tree.interface.new_socket('Alpha', in_out='OUTPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Emission Strength', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-1060.0, 200.0)

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.inputs[1].default_value = 2.0
    math_1.location = (-840.0, 200.0)
    math_1.operation = 'MULTIPLY'

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.inputs[1].default_value = 1.0
    math_2.location = (-620.0, 200.0)
    math_2.operation = 'SUBTRACT'

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.location = (-400.0, 200.0)
    math_3.operation = 'MULTIPLY'

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (700.0, 200.0)

    math_4 = node_tree.nodes.new(type='ShaderNodeMath')
    math_4.inputs[0].default_value = 1.0
    math_4.location = (920.0, 200.0)
    math_4.operation = 'SUBTRACT'

    math_5 = node_tree.nodes.new(type='ShaderNodeMath')
    math_5.inputs[0].default_value = 1.0
    math_5.location = (1140.0, 200.0)
    math_5.operation = 'MINIMUM'

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (1360.0, 200.0)

    group_input_3 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_3.location = (-1500.0, 0.0)

    vector_math_1 = node_tree.nodes.new(type='ShaderNodeVectorMath')
    vector_math_1.inputs[0].default_value = [1.0, 1.0, 1.0]
    vector_math_1.location = (-1280.0, 0.0)
    vector_math_1.operation = 'SUBTRACT'

    separate_xyz = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
    separate_xyz.location = (-1060.0, 0.0)

    math_6 = node_tree.nodes.new(type='ShaderNodeMath')
    math_6.inputs[1].default_value = 2.0
    math_6.location = (-840.0, 0.0)
    math_6.operation = 'MULTIPLY'

    math_7 = node_tree.nodes.new(type='ShaderNodeMath')
    math_7.inputs[1].default_value = 1.0
    math_7.location = (-620.0, 0.0)
    math_7.operation = 'SUBTRACT'

    math_8 = node_tree.nodes.new(type='ShaderNodeMath')
    math_8.location = (-400.0, 0.0)
    math_8.operation = 'MULTIPLY'

    math_9 = node_tree.nodes.new(type='ShaderNodeMath')
    math_9.location = (-180.0, 0.0)
    math_9.operation = 'ADD'

    math_10 = node_tree.nodes.new(type='ShaderNodeMath')
    math_10.inputs[0].default_value = 1.0
    math_10.location = (40.0, 0.0)
    math_10.operation = 'SUBTRACT'

    math_11 = node_tree.nodes.new(type='ShaderNodeMath')
    math_11.location = (260.0, 0.0)
    math_11.operation = 'SQRT'

    math_12 = node_tree.nodes.new(type='ShaderNodeMath')
    math_12.inputs[1].default_value = 1.0
    math_12.location = (480.0, 0.0)
    math_12.operation = 'ADD'

    math_13 = node_tree.nodes.new(type='ShaderNodeMath')
    math_13.inputs[1].default_value = 2.0
    math_13.location = (700.0, 0.0)
    math_13.operation = 'DIVIDE'

    combine_xyz = node_tree.nodes.new(type='ShaderNodeCombineXYZ')
    combine_xyz.location = (920.0, 0.0)

    math_14 = node_tree.nodes.new(type='ShaderNodeMath')
    math_14.inputs[0].default_value = 1.0
    math_14.location = (1140.0, 0.0)
    math_14.operation = 'SUBTRACT'

    # Add and place reroutes
    node_reroute_1 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_1.location = (-840.0, 20.0)
    node_reroute_2 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_2.location = (840.0, 20.0)
    node_reroute_3 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_3.location = (-880.0, -100.0)
    node_reroute_4 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_4.location = (-880.0, -180.0)
    node_reroute_5 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_5.location = (820.0, -180.0)
    node_reroute_6 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_6.location = (-900.0, -120.0)
    node_reroute_7 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_7.location = (-900.0, -200.0)
    node_reroute_8 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_8.location = (1000.0, -200.0)
    node_reroute_9 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_9.location = (1120.0, 20.0)
    node_reroute_10 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_10.location = (1340.0, 20.0)
    node_reroute_11 = node_tree.nodes.new(type='NodeReroute')
    node_reroute_11.location = (1340.0, 140.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['_n RotationMap Alpha'], math_1.inputs[0])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], math_3.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], math_3.inputs[1])
    node_tree.links.new(math_3.outputs['Value'], math_9.inputs[0])
    node_tree.links.new(group_input_2.outputs['_n RotationMap Alpha'], combine_xyz.inputs['X'])

    node_tree.links.new(group_input_3.outputs['_n RotationMap Color'], vector_math_1.inputs[1])
    node_tree.links.new(vector_math_1.outputs['Vector'], separate_xyz.inputs['Vector'])
    node_tree.links.new(separate_xyz.outputs['X'], node_reroute_1.inputs[0])
    node_tree.links.new(node_reroute_1.outputs[0], node_reroute_2.inputs[0])
    node_tree.links.new(node_reroute_2.outputs[0], math_4.inputs[1])
    node_tree.links.new(math_4.outputs['Value'], math_5.inputs[1])
    node_tree.links.new(math_5.outputs['Value'], group_output.inputs['Alpha'])

    node_tree.links.new(separate_xyz.outputs['Y'], node_reroute_3.inputs[0])
    node_tree.links.new(node_reroute_3.outputs[0], math_6.inputs[0])
    node_tree.links.new(math_6.outputs['Value'], math_7.inputs[0])
    node_tree.links.new(math_7.outputs['Value'], math_8.inputs[0])
    node_tree.links.new(math_7.outputs['Value'], math_8.inputs[1])
    node_tree.links.new(math_8.outputs['Value'], math_9.inputs[1])
    node_tree.links.new(math_9.outputs['Value'], math_10.inputs[1])
    node_tree.links.new(math_10.outputs['Value'], math_11.inputs[0])
    node_tree.links.new(math_11.outputs['Value'], math_12.inputs[0])
    node_tree.links.new(math_12.outputs['Value'], math_13.inputs[0])
    node_tree.links.new(math_13.outputs['Value'], combine_xyz.inputs['Z'])
    node_tree.links.new(node_reroute_3.outputs[0], node_reroute_4.inputs[0])
    node_tree.links.new(node_reroute_4.outputs[0], node_reroute_5.inputs[0])
    node_tree.links.new(node_reroute_5.outputs[0], combine_xyz.inputs['Y'])

    node_tree.links.new(separate_xyz.outputs['Z'], node_reroute_6.inputs[0])
    node_tree.links.new(node_reroute_6.outputs[0], node_reroute_7.inputs[0])
    node_tree.links.new(node_reroute_7.outputs[0], node_reroute_8.inputs[0])
    node_tree.links.new(node_reroute_8.outputs[0], math_14.inputs[1])
    node_tree.links.new(math_14.outputs['Value'], group_output.inputs['Emission Strength'])

    node_tree.links.new(combine_xyz.outputs['Vector'], node_reroute_9.inputs[0])
    node_tree.links.new(node_reroute_9.outputs[0], node_reroute_10.inputs[0])
    node_tree.links.new(node_reroute_10.outputs[0], node_reroute_11.inputs[0])
    node_tree.links.new(node_reroute_11.outputs[0], group_output.inputs['Normal'])

    return node_tree


def offset_hue():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'OffsetHue' in bpy.data.node_groups:
        return bpy.data.node_groups['OffsetHue']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='OffsetHue', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketFloat', name='H')
        node_tree.inputs.new(type='NodeSocketFloat', name='Hue')
        node_tree.outputs.new(type='NodeSocketFloat', name='H')
    else:
        node_tree.interface.new_socket('H', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Hue', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('H', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-440.0, 80.0)

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.location = (-200.0, 80.0)
    math_1.operation = 'ADD'

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.location = (40.0, 80.0)
    math_2.operation = 'FRACT'
    math_2.use_clamp = True

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (280.0, 80.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['H'], math_1.inputs[0])
    node_tree.links.new(group_input_1.outputs['Hue'], math_1.inputs[1])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], group_output.inputs['H'])

    return node_tree


def offset_saturation():
    # type: () -> NodeTree
    """
    """
    # Check if node tree already exists
    if 'OffsetSaturation' in bpy.data.node_groups:
        return bpy.data.node_groups['OffsetSaturation']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='OffsetSaturation', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketFloat', name='S')
        node_tree.inputs.new(type='NodeSocketFloat', name='Saturation')
        node_tree.outputs.new(type='NodeSocketFloat', name='S')
    else:
        node_tree.interface.new_socket('S', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Saturation', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('S', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-560.0, 180.0)

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-560.0, -20.0)
    group_input_2.outputs['S'].hide = True

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.location = (-320.0, 180.0)
    math_1.operation = 'POWER'

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.inputs[0].default_value = 1.0
    math_2.location = (-320.0, -20.0)
    math_2.operation = 'SUBTRACT'

    math_3 = node_tree.nodes.new(type='ShaderNodeMath')
    math_3.location = (-80.0, 180.0)
    math_3.operation = 'MULTIPLY'

    clamp_1 = node_tree.nodes.new(type='ShaderNodeClamp')
    clamp_1.inputs['Min'].default_value = 0.0
    clamp_1.inputs['Max'].default_value = 1.0
    clamp_1.location = (160.0, 180.0)

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (400.0, 180.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['S'], math_1.inputs[0])
    node_tree.links.new(group_input_1.outputs['Saturation'], math_1.inputs[1])
    node_tree.links.new(group_input_2.outputs['Saturation'], math_2.inputs[1])
    node_tree.links.new(math_1.outputs['Value'], math_3.inputs[0])
    node_tree.links.new(math_2.outputs['Value'], math_3.inputs[1])
    node_tree.links.new(math_3.outputs['Value'], clamp_1.inputs['Value'])
    node_tree.links.new(clamp_1.outputs['Result'], group_output.inputs['S'])

    return node_tree


def offset_skin_saturation():
    if 'OffsetSkinSaturation' in bpy.data.node_groups:
        return bpy.data.node_groups['OffsetSkinSaturation']

    # Make new node tree and add input/output sockets
    node_tree = bpy.data.node_groups.new(name='OffsetSkinSaturation', type='ShaderNodeTree')
    if blender_version < 4.0:
        node_tree.inputs.new(type='NodeSocketFloat', name='S')
        node_tree.inputs.new(type='NodeSocketFloat', name='Saturation')
        node_tree.outputs.new(type='NodeSocketFloat', name='S')
    else:
        node_tree.interface.new_socket('S', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('Saturation', in_out='INPUT', socket_type='NodeSocketFloat')
        node_tree.interface.new_socket('S', in_out='OUTPUT', socket_type='NodeSocketFloat')

    # Add and place nodes
    group_input_1 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_1.location = (-520.0, 40.0)
    group_input_1.outputs['S'].hide = True

    group_input_2 = node_tree.nodes.new(type='NodeGroupInput')
    group_input_2.location = (-300.0, 120.0)
    group_input_2.outputs['Saturation'].hide = True

    math_1 = node_tree.nodes.new(type='ShaderNodeMath')
    math_1.inputs[0].default_value = 0.5
    math_1.location = (-300.0, 40.0)
    math_1.operation = 'SUBTRACT'

    math_2 = node_tree.nodes.new(type='ShaderNodeMath')
    math_2.location = (-80.0, 40.0)
    math_2.operation = 'ADD'

    clamp_1 = node_tree.nodes.new(type='ShaderNodeClamp')
    clamp_1.inputs['Min'].default_value = 0.0
    clamp_1.inputs['Max'].default_value = 1.0
    clamp_1.location = (140.0, 40.0)

    group_output = node_tree.nodes.new(type='NodeGroupOutput')
    group_output.location = (360.0, 40.0)

    # Link nodes together
    node_tree.links.new(group_input_1.outputs['Saturation'], math_1.inputs[1])
    node_tree.links.new(group_input_2.outputs['S'], math_2.inputs[0])
    node_tree.links.new(math_1.outputs['Value'], math_2.inputs[1])
    node_tree.links.new(math_2.outputs['Value'], clamp_1.inputs['Value'])
    node_tree.links.new(clamp_1.outputs['Result'], group_output.inputs['S'])

    return node_tree
