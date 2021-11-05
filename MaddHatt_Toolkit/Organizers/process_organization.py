import bpy
from . import constants as consts

class MADDHATT_OT_process_organization(bpy.types.Operator):
    bl_idname = "maddhatt.process_organization"
    bl_label = "You shouldn'y be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED" }

    @classmethod
    def poll(cls, context):
        if any(col.name == consts.ORGANIZER for col in bpy.data.collections) == False:
            return False

        if len(bpy.data.collections.get(consts.ORGANIZER).objects) == 0:
            return False

        return True 

    def execute(self, context):
        # Perform any neccessary setup
        if any(col.name == consts.TOOLS for col in bpy.data.collections) == False:
            col = bpy.data.collections.new(consts.TOOLS)
            bpy.context.scene.collection.children.link(col)

        if any(col.name == consts.MIDPOLY for col in bpy.data.collections) == False:
            col = bpy.data.collections.new(consts.MIDPOLY)
            bpy.context.scene.collection.children.link(col)

        # Clean up objects
        id = len(bpy.data.collections[consts.MIDPOLY].objects)
        
        for obj in bpy.data.collections[consts.ORGANIZER].objects:
            bpy.data.collections[consts.ORGANIZER].objects.unlink(obj)

            if obj.type == "EMPTY" or obj.type == "LIGHT" or obj.hide_viewport == True:
                obj.hide_viewport = False
                bpy.data.collections[consts.TOOLS].objects.link(obj)
            else:
                bpy.data.collections[consts.MIDPOLY].objects.link(obj)
                obj.name = "part_" + str(id).zfill(3)
                id += 1
        
        bpy.ops.object.select_same_collection(collection=consts.TOOLS)
        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")

        bpy.ops.object.select_same_collection(collection=consts.MIDPOLY)
        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")

        # Clean up outliner
        bpy.context.view_layer.layer_collection.children[consts.ORGANIZER].exclude = True
        bpy.context.view_layer.layer_collection.children[consts.TOOLS].exclude = True

        bpy.ops.maddhatt.create_export_collection(coll_name=consts.HIGHPOLY)
        bpy.ops.maddhatt.create_export_collection(coll_name=consts.LOWPOLY)

        return {"FINISHED"}

classes = [
    MADDHATT_OT_process_organization,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)