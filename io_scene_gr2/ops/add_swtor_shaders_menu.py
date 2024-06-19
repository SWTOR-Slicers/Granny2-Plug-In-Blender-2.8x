# BLENDER 4.x-specific code for adding SWTOR Shaders
# to the Shader Editor's Add menu.

import bpy


# Operator that adds a SWTOR shader to the current material in context.
class NODE_MT_add_swtor_shader(bpy.types.Operator):
    bl_idname = 'node.add_swtor_shader'
    bl_label = 'Add SWTOR Shader'
    bl_description = "Adds this SWTOR Shader Nodegroup to the current Material"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.material


    swtor_shader_type : bpy.props.StringProperty()
    
    def execute(self, context):
        mat_nodes = bpy.context.material.node_tree.nodes

        swtor_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")

        # Tell the ShaderNodeHeroEngine what SWTOR shader to reproduce
        swtor_nodegroup.derived = self.swtor_shader_type
        
        # Position it to make any leftover Principled Shader
        # easy to select and remove from underneath
        swtor_nodegroup.location = -30.0, 300.0

        # Set reasonable opacity modes
        if self.swtor_shader_type in ["SKINB", "EYE"]:
            swtor_nodegroup.alpha_mode = "OPAQUE"
        else:
            swtor_nodegroup.alpha_mode = "CLIP"

        return {'FINISHED'}


# Actual SWTOR Shaders menu.
class NODE_MT_swtor_shaders_menu(bpy.types.Menu):
    bl_idname = 'NODE_MT_swtor_shaders_menu'
    bl_label = 'SWTOR Shaders'

    def draw(self, context):
        
        layout = self.layout
        
        swtor_shader_names = ["Uber", "Creature", "Garment", "SkinB", "HairC", "Eye"]
        
        for swtor_shader_name in swtor_shader_names:
            swtor_shader = layout.operator(NODE_MT_add_swtor_shader.bl_idname, text=f"{swtor_shader_name} Shader")
            swtor_shader.swtor_shader_type = swtor_shader_name.upper()
            

# Function that creates a layout element holding a separator bar plus
# the SWTOR shaders menu, to be appended to the NODE_MT_add menu
# by __init__.py's registrations.
def swtor_shaders_submenu_element(self, context):
    self.layout.separator()
    self.layout.menu(NODE_MT_swtor_shaders_menu.bl_idname)





# Registrations are being handled directly in __init__.py

# def register():
#     bpy.utils.register_class(NODE_MT_add_swtor_shader)
#     bpy.utils.register_class(NODE_MT_swtor_shaders_menu)
    
#     # Append the separator bar plus SWTOR menu to the Shader Editor's Add menu 
#     bpy.types.NODE_MT_add.append(swtor_shaders_submenu_element)

# def unregister():
#     bpy.utils.unregister_class(NODE_MT_swtor_shaders_menu)
#     bpy.utils.unregister_class(NODE_MT_add_swtor_shader)
    
#     # Remove the separator bar plus SWTOR menu from the Shader Editor's Add menu
#     bpy.types.NODE_MT_add.remove(swtor_shaders_submenu_element)

# if __name__ == "__main__":
#     register()