import bpy
from bpy.types import Panel

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

class VIEW3D_PT_pipeline(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pipeline Tools"
    bl_label = "Pipeline tools"

    def draw(self, context):
        layout = self.layout
        
        # Check if MidPoly collection exist
        if any(col.name == "MidPoly" for col in bpy.data.collections) == False:
            layout.operator("maddhatt.setup_midpoly", text="Create MidPoly Collection")

        obj_count = len(bpy.data.collections.get("MidPoly").all_objects)
        row = layout.row
        row = layout.label(text=str(obj_count))


class MADDHATT_OT_setup_midpoly(bpy.types.Operator):
    bl_idname = "maddhatt.setup_midpoly"
    bl_label = "Setup mid poly"

    def execute(self, context):
        col_midpoly = bpy.data.collections.new("MidPoly")
        bpy.context.scene.collection.children.link(col_midpoly)
        return {'FINISHED'}

# Class registration
reg_classes = (
    MADDHATT_OT_setup_midpoly,
    VIEW3D_PT_pipeline)

def register():
    bpy.utils.register_class(MADDHATT_OT_setup_midpoly)
    bpy.utils.register_class(VIEW3D_PT_pipeline)

def unregister():
    bpy.utils.unregister_class(MADDHATT_OT_setup_midpoly)
    bpy.utils.unregister_class(VIEW3D_PT_pipeline)        

if __name__ == "__main__":
    register()