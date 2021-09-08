import bpy

# Addon info
bl_info = {
    "version": (0, 1),
    "blender": (2, 91, 0),
    "name": "MaddHatt's Pipeline Tool",
    "author": "Patt @MaddHattPatt <MaddHatt.pm@gmail.com>",
    "description": "A variety of tools to help out my personal ",
    "location": "3D View on the side bar",
    "category": "3D View"
    }

class MADDHATT_OT_setup_midpoly(bpy.types.Operator):
    bl_idname = "maddhatt.setup_midpoly"
    bl_label = "Setup mid poly"

    def execute(self, context):
        print("maddhatt.setup_from_midpoly_collection was called")
        return {'FINISHED'}

# Class registration
reg_classes = [
    MADDHATT_OT_setup_midpoly]

def register():
    for item in reg_classes:
        bpy.utils.register_class(item)

def unregister():
    for item in reg_classes:
        bpy.utils.unregister_class(item)
