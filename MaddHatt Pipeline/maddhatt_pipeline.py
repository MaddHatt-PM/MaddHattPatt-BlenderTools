bl_info = {
    "version": (0, 1),
    "blender": (2, 91, 0),
    "name": "MaddHatt's Pipeline Tool",
    "author": "Patt @MaddHattPatt <MaddHatt.pm@gmail.com>",
    "description": "A variety of tools to help out my personal ",
    "location": "3D View on the side bar",
    "category": "3D View"
    }

import bpy
from bpy.types import EnumProperty, Operator

# ---------------------------------------------------------------------------
# --- UI Panels ---
# ----------------- 
class VIEW3D_PT_pipeline(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pipeline Tools"
    bl_label = "Pipeline tools"

    def draw(self, context):
        layout = self.layout
        
        # Check if MidPoly collection exist
        if any(col.name == "To_Organize" for col in bpy.data.collections) == False:
            layout.operator("maddhatt.multi_tool", text="Add To_Organize Collection").action = "make_to_organize_coll"
            return {"FINSIHED"}

        obj_count = len(bpy.data.collections.get("To_Organize").all_objects)
        row = layout.row
        row = layout.label(text=str(obj_count))

# ---------------------------------------------------------------------------
# --- Operators ---
# -----------------
class MADDHATT_OT_multi_tool(Operator):
    bl_idname = "maddhatt.multi_tool"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED"}

    action: bpy.props.EnumProperty(
        items=[
            ("make_to_organize_coll", "", ""),
            ("make_low_coll", "", ""),
            ("make_mid_coll", "", ""),
            ("make_high_coll", "", "")]
    )

    def execute(self, context):
        if self.action == "make_to_organize_coll":self.create_collection(context=context, name = "To_Organize")
        elif self.action == "make_low_coll": self.create_collection(context=context, name = "Low_Poly")
        elif self.action == "make_mid_coll": self.create_collection(context=context, name = "Mid_Poly")
        elif self.action == "make_high_coll": self.create_collection(context=context, name = "High_Poly")

        return {"FINISHED"}

    @staticmethod
    def create_collection(context, name):
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)

class MADDHATT_OT_setup_midpoly(bpy.types.Operator):
    bl_idname = "maddhatt.setup_midpoly"
    bl_label = "Setup mid poly"

    def execute(self, context):
        col_midpoly = bpy.data.collections.new("MidPoly")
        bpy.context.scene.collection.children.link(col_midpoly)
        return {'FINISHED'}

# ---------------------------------------------------------------------------
# --- Class registration ---
# --------------------------
def register():
    bpy.utils.register_class(MADDHATT_OT_multi_tool)
    bpy.utils.register_class(MADDHATT_OT_setup_midpoly)
    bpy.utils.register_class(VIEW3D_PT_pipeline)

def unregister():
    bpy.utils.unregister_class(MADDHATT_OT_multi_tool)
    bpy.utils.unregister_class(MADDHATT_OT_setup_midpoly)
    bpy.utils.unregister_class(VIEW3D_PT_pipeline)        

if __name__ == "__main__":
    register()