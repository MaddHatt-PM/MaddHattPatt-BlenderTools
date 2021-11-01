import bpy
from . import constants as consts

class MADDHATT_OT_quick_export_collection(bpy.types.Operator):
    bl_idname = "maddhatt.quick_export_collection"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO"}

    target_coll: bpy.props.CollectionProperty(name="target_coll")

    def execute(self, context):
        # bpy.ops.export_scene.fbx(filepath=None,)
        pass

classes = [
    MADDHATT_OT_quick_export_collection,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)