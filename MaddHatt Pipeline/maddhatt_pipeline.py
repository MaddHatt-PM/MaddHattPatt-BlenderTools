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
        
        if any(col.name == "MidPoly" for col in bpy.data.collections):
            row = layout.row()
            row.label(text="MidPoly Exists")

        else:
            row = layout.row()
            col_midpoly = bpy.data.collections.new("MidPoly")
            bpy.context.scene.collection.children.link(col_midpoly)

        # for coll in bpy.data.collections:
        #     row = layout.row()
        #     row.label(text = coll.name)

class MADDHATT_OT_setup_midpoly(bpy.types.Operator):
    bl_idname = "maddhatt.setup_midpoly"
    bl_label = "Setup mid poly"

    def execute(self, context):
        print("maddhatt.setup_from_midpoly_collection was called")
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