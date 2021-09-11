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
import math
import importlib
from bpy.props import IntProperty, StringProperty
from bpy.types import EnumProperty, LayerCollection, Operator

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
        
        layout.label(text="Workflow Helpers")
        layout.operator("maddhatt.setup_circular_array", text="Create circular array", icon="FORCE_LENNARDJONES")

        layout.separator()
        layout.label(text="Pipeline Managers")
        col = layout.column(heading="Pipeline Managers", align=True, )

        if any(col.name == "Organizer" for col in bpy.data.collections) == False:
            col.operator("maddhatt.create_collection", text="Add Organizer Collection", icon="COLLECTION_NEW").action = "make_to_organize_coll"

        else:
            col.operator("maddhatt.process_organization", text="Process Organization")
            col.operator("maddhatt.create_low_poly", text="Setup Low Poly", icon="COLLECTION_NEW")
            col.operator("maddhatt.create_low_poly", text="Setup High Poly", icon="COLLECTION_NEW")

        layout.separator()

        col = layout.column(heading="Color ID Painting", align=True)
        col.operator("maddhatt.create_material", text="Create ID Material").mat_id = len(bpy.data.materials)
        for mat_id in range(0, len(bpy.data.materials)):
            
            # If it has a custom name, cut off the prefix
            mat_name = bpy.data.materials[mat_id].name
            if len(mat_name) != 5:
                mat_name = mat_name[5:]

            row = col.row(align=True)
            row.operator("maddhatt.assign_material", text=mat_name, icon="MATERIAL").mat_id = mat_id
            row.operator("maddhatt.rename_id_material", text="", icon="SMALL_CAPS").mat_target = mat_name


# ---------------------------------------------------------------------------
# --- Workflow Tools ---
#-----------------------
class MADDHATT_OT_setup_circular_array(bpy.types.Operator):
    bl_idname = "maddhatt.setup_circular_array"
    bl_label = "Circular Array Setup"
    bl_options = {"REGISTER", "UNDO"}

    copy_count: IntProperty(name="Copy Count", default=3, min=2, soft_max=18)
    axis_id: IntProperty(name="Axis ID", default=2, min=0, max=2)

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        # Object offset setup
        util_obj = bpy.data.objects.new(bpy.context.object.name + "_CircularUtil" , None)
        bpy.context.scene.collection.objects.link(util_obj)
        util_obj.parent = bpy.context.object
        rot_amount = 360.0 / float(self.copy_count)
        util_obj.rotation_euler[self.axis_id] = math.radians(rot_amount)

        # Array Modifier setup
        bpy.ops.object.modifier_add(type="ARRAY")
        array_mod = bpy.context.object.modifiers[-1]
        array_mod.count = self.copy_count
        array_mod.name = "Circular Array"
        array_mod.use_relative_offset = False
        array_mod.use_object_offset = True
        array_mod.offset_object = util_obj

        return {"FINISHED"}


# ---------------------------------------------------------------------------
# --- Pipeline Tools ---
# ----------------------
class MADDHATT_OT_create_collection(Operator):
    bl_idname = "maddhatt.create_collection"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED"}

    action: bpy.props.EnumProperty(
        items=[
            ("make_to_organize_coll", "", ""),
            ("make_tools_coll", "", ""),
            ("make_low_coll", "", ""),
            ("make_mid_coll", "", ""),
            ("make_high_coll", "", "")]
    )

    def execute(self, context):
        if self.action == "make_to_organize_coll":self.create_collection(context=context, name = "Organizer")
        elif self.action == "make_tools_coll": self.create_collection(context=context, name = "Tools")
        elif self.action == "make_low_coll": self.create_collection(context=context, name = "Low_Poly")
        elif self.action == "make_mid_coll": self.create_collection(context=context, name = "Mid_Poly")
        elif self.action == "make_high_coll": self.create_collection(context=context, name = "High_Poly")

        return {"FINISHED"}

    @staticmethod
    def create_collection(context, name):
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)

class MADDHATT_OT_create_low_poly(bpy.types.Operator):
    bl_idname = "maddhatt.create_low_poly"
    bl_label = "you shouldn't see this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED" }

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections.get("Mid_Poly").objects) != 0

    def execute(self, context):
        MADDHATT_OT_create_collection.create_collection(context, "Low_Poly")
        bpy.data.collections["Mid_Poly"].objects[0].name.replace(".001", "_low")
        for item in bpy.data.collections["Mid_Poly"].objects:
            item.name = item.name.replace(".001", "_low")
            bpy.data.collections["Mid_Poly"].objects.unlink(item)
            bpy.data.collections["Mid_Poly"].objects.unlink(item)
            

class MADDHATT_OT_process_organization(bpy.types.Operator):
    bl_idname = "maddhatt.process_organization"
    bl_label = "You shouldn'y be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED" }

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections.get("Organizer").objects) != 0

    def execute(self, context):
        # Perform any neccessary setup
        if any(col.name == "Tools" for col in bpy.data.collections) == False:
            MADDHATT_OT_create_collection.create_collection(context, "Tools")
        if any(col.name == "Mid_Poly" for col in bpy.data.collections) == False:
            MADDHATT_OT_create_collection.create_collection(context, "Mid_Poly")

        # Clean up objects
        id = len(bpy.data.collections["Mid_Poly"].objects)
        
        for obj in bpy.data.collections["Organizer"].objects:
            bpy.data.collections["Organizer"].objects.unlink(obj)

            if obj.type == "EMPTY" or obj.type == "LIGHT" or obj.hide_viewport == True:
                obj.hide_viewport = False
                bpy.data.collections["Tools"].objects.link(obj)
            else:
                bpy.data.collections["Mid_Poly"].objects.link(obj)
                obj.name = "part_" + str(id).zfill(3)
                id += 1
        
        bpy.ops.object.select_same_collection(collection="Tools")
        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")

        bpy.ops.object.select_same_collection(collection="Mid_Poly")
        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")

        return {"FINISHED"}

class MADDHATT_OT_create_material(bpy.types.Operator):
    bl_idname = "maddhatt.create_material"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED"}

    mat_id: bpy.props.IntProperty(name="mat_id")

    def execute(self, context):
        mat = bpy.data.materials.new("ID" + str(self.mat_id).zfill(2) + "_")

        id = float(self.mat_id)

        h = (id * 0.175) % 1.0
        s = 1 - (id // 6 * 0.1314)
        v = 1 - (id // 3 * 0.045)
        difcolor = colorsys.hsv_to_rgb(h,s,v)
        mat.diffuse_color = (difcolor[0], difcolor[1], difcolor[2], 1.0) 

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
        
class MADDHATT_OT_rename_id_material(bpy.types.Operator):
    bl_idname = "maddhatt.rename_id_material"
    bl_label = "Rename id material"

    mat_target:bpy.props.StringProperty(options={"HIDDEN"})
    mat_rename: bpy.props.StringProperty(name="ID Material Name: ")
    

    def execute(self, context):
        bpy.data.materials[self.mat_target].name = self.mat_target[:5] + self.mat_rename
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
# ---------------------------------------------------------------------------
# --- Class registration ---
# --------------------------
modules = [

]

classes = [
    MADDHATT_OT_setup_circular_array,
    MADDHATT_OT_assign_material,
    MADDHATT_OT_create_material,
    MADDHATT_OT_rename_id_material,
    MADDHATT_OT_create_collection,
    MADDHATT_OT_create_low_poly,
    MADDHATT_OT_process_organization,
    VIEW3D_PT_pipeline,
]

def register():
    for mod in modules:
        importlib.reload(mod)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    

if __name__ == "__main__":
    register()
