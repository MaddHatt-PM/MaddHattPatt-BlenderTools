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
import colorsys
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

        matcount = len(bpy.data.materials)

        layout.operator("maddhatt.create_material", text="Create material").mat_id = matcount

        for id in range(0, matcount):
            layout.operator("maddhatt.assign_material", text="Assign mat" + str(id)).mat_id = id

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

        id = float(self.mat_id)

        h = (id * 0.175) % 1.0
        s = 1 - (id // 6 * 0.1314)
        v = 1 - (id // 3 * 0.045)
        difcolor = colorsys.hsv_to_rgb(h,s,v)
        mat.diffuse_color = (difcolor[0], difcolor[1], difcolor[2], 1.0) 
        print (h, s, v)

        return {"FINISHED"}
        
class MADDHATT_OT_assign_material(bpy.types.Operator):
    bl_idname = "maddhatt.assign_material"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO"}

    mat_id: bpy.props.IntProperty(name="mat_id")

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def execute(self, context):
        i = "ID_" + str(self.mat_id).zfill(2)
        for item in bpy.data.materials.keys():
            if (item.startswith(i)):
                i = item

        mat = bpy.data.materials.get(i)

        for sel_obj in bpy.context.selected_objects:
            if sel_obj.type != "MESH":
                continue

            if (context.mode == "OBJECT"):
                sel_obj.data.materials.clear()
                sel_obj.data.materials.append(mat)

            elif (context.mode == "EDIT_MESH"):
                slotID = -1
                i = 0
                for mat_slot in sel_obj.material_slots:
                    if (mat == mat_slot.material):
                        slotID = i
                        break
                    i += 1

                if slotID == -1:
                    sel_obj.data.materials.append(mat)
                    slotID = len(sel_obj.data.materials) - 1

                sel_obj.active_material_index = slotID
                bpy.ops.object.material_slot_assign()

        return {"FINISHED"}

        

# ---------------------------------------------------------------------------
# --- Class registration ---
# --------------------------
def register():
    bpy.utils.register_class(MADDHATT_OT_assign_material)
    bpy.utils.register_class(MADDHATT_OT_create_material)
    bpy.utils.register_class(MADDHATT_OT_create_collection)
    bpy.utils.register_class(VIEW3D_PT_pipeline)

def unregister():
    bpy.utils.unregister_class(MADDHATT_OT_assign_material)
    bpy.utils.unregister_class(MADDHATT_OT_create_material)
    bpy.utils.unregister_class(MADDHATT_OT_create_collection)
    bpy.utils.unregister_class(VIEW3D_PT_pipeline)        

if __name__ == "__main__":
    register()
