import bpy
import math
from bpy.props import IntProperty

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
        util_obj = bpy.data.objects.new(bpy.context.object.name + "_CircularUtil" , None)
        
        # Object offset setup
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

def register() :
    bpy.utils.register_class(MADDHATT_OT_setup_circular_array)
 
def unregister() :
    bpy.utils.unregister_class(MADDHATT_OT_setup_circular_array)