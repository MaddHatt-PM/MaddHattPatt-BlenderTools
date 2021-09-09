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
import random
from bpy.props import StringProperty
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
            layout.operator("maddhatt.create_collection", text="Add To_Organize Collection").action = "make_to_organize_coll"
            
            # return {"FINSIHED"}
        else:
            layout.label(text="To_Organize collection exists")

        layout.operator("maddhatt.create_material", text="Create material").mat_id = random.randint(1, 999)

        # obj_count = len(bpy.data.collections.get("To_Organize").all_objects)
        # row = layout.row
        # row = layout.label(text=str(obj_count))

# ---------------------------------------------------------------------------
# --- Operators ---
# -----------------
class MADDHATT_OT_create_collection(Operator):
    bl_idname = "maddhatt.create_collection"
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

class MADDHATT_OT_create_material(bpy.types.Operator):
    bl_idname = "maddhatt.create_material"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED"}

    mat_id: bpy.props.IntProperty(name="mat_id")

    def execute(self, context):
        mat = bpy.data.materials.new("ID_" + str(self.mat_id).zfill(2))
        mat.diffuse_color = (random.random(), 1, 1, 1) # RGB values, I want HSL

        return {"FINISHED"}



# ---------------------------------------------------------------------------
# --- Class registration ---
# --------------------------
def register():
    bpy.utils.register_class(MADDHATT_OT_create_material)
    bpy.utils.register_class(MADDHATT_OT_create_collection)
    bpy.utils.register_class(VIEW3D_PT_pipeline)

def unregister():
    bpy.utils.unregister_class(MADDHATT_OT_create_material)
    bpy.utils.unregister_class(MADDHATT_OT_create_collection)
    bpy.utils.unregister_class(VIEW3D_PT_pipeline)        

if __name__ == "__main__":
    register()
