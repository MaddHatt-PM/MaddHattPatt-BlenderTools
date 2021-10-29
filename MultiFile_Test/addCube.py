bl_info = {
    "version": (0, 1),
    "blender": (2, 91, 0),
    "name": "Testing Multiple Files",
    "author": "Patt @MaddHattPatt <MaddHatt.pm@gmail.com>",
    "description": "A variety of tools to help out my personal ",
    "location": "3D View on the side bar",
    "category": "3D View"
    }

import bpy
 
class addCubeSample(bpy.types.Operator):
    bl_idname = 'mesh.add_cube_sample'
    bl_label = 'Add Cube'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {"FINISHED"}
 
def register() :
    bpy.utils.register_class(addCubeSample)
 
def unregister() :
    bpy.utils.unregister_class(addCubeSample)