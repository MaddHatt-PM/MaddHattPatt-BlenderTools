bl_info = {
    "version": (0, 1),
    "blender": (2, 91, 0),
    "name": "Testing Multiple Files B",
    "author": "Patt @MaddHattPatt <MaddHatt.pm@gmail.com>",
    "description": "A variety of tools to help out my personal ",
    "location": "3D View on the side bar",
    "category": "3D View"
    }

import bpy
 
class addCubePanel(bpy.types.Panel):
    bl_idname = "panel.add_cube_panel"
    bl_label = "AddCube"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
 
    def draw(self, context):
        self.layout.operator("mesh.add_cube_sample", icon='MESH_CUBE', text="Add Cube")
 
def register() :
    bpy.utils.register_class(addCubePanel)
 
def unregister() :
    bpy.utils.unregister_class(addCubePanel)