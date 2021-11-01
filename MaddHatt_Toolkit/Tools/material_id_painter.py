import bpy
import random
import colorsys
import math
import importlib
from bpy.props import IntProperty, StringProperty
from bpy.types import EnumProperty, LayerCollection, Operator

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

    mat_id: bpy.props.StringProperty(name="mat_id")

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def execute(self, context):
        i = self.mat_id
        print(i)
        for item in bpy.data.materials.keys():
            if (item.startswith(i)):
                print (item, i)
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

classes = [
    MADDHATT_OT_assign_material,
    MADDHATT_OT_create_material,
    MADDHATT_OT_rename_id_material,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)