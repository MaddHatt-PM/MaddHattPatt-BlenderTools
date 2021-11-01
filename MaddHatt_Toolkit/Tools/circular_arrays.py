import bpy
import math
from bpy.props import IntProperty

class MADDHATT_OT_setup_circular_array(bpy.types.Operator):
    bl_idname = "maddhatt.setup_circular_array"
    bl_label = "Circular Array Setup"
    bl_options = {"REGISTER", "UNDO"}

    cir_array_count: IntProperty(name="Copy Count", default=3, min=2, soft_max=18)
    axis_id: IntProperty(name="Axis ID", default=2, min=0, max=2)

    @classmethod
    def poll(cls, context):
        active_obj = context.active_object
        return active_obj != None and active_obj.type != "EMPTY"

    def execute(self, context):
        util_obj = bpy.data.objects.new(bpy.context.object.name + "_CircularUtil" , None)
        
        # Object offset setup
        bpy.context.scene.collection.objects.link(util_obj)
        util_obj.parent = bpy.context.object
        rot_amount = 360.0 / float(self.cir_array_count)
        util_obj.rotation_euler[self.axis_id] = math.radians(rot_amount)

        # Array Modifier setup
        bpy.ops.object.modifier_add(type="ARRAY")
        array_mod = bpy.context.object.modifiers[-1]
        array_mod.name = "Circular Array"
        array_mod.count = self.cir_array_count
        array_mod.use_relative_offset = False
        array_mod.use_object_offset = True
        array_mod.offset_object = util_obj

        #Property setup
        return {"FINISHED"}

def edit_circular_array(self, context):
    # Array Modifier setup
    for mod in bpy.context.active_object.modifiers:
        if "Circular Array" in mod.name:
            mod.count = self.cir_array_count

            # Object offset setup
            util_obj = mod.offset_object
            rot_amount = 360.0 / float(self.cir_array_count)
            util_obj.rotation_euler[2] = math.radians(rot_amount)

def register() :
    bpy.types.Object.cir_array_count = IntProperty(
        name="Circular Array Count",
        default=2,
        min=1,
        soft_max=18,
        update=edit_circular_array
    )

    bpy.utils.register_class(MADDHATT_OT_setup_circular_array)
 
def unregister() :
    bpy.utils.unregister_class(MADDHATT_OT_setup_circular_array)