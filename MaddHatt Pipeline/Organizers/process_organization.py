import bpy

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
            col = bpy.data.collections.new("Tools")
            bpy.context.scene.collection.children.link(col)

        if any(col.name == "Mid_Poly" for col in bpy.data.collections) == False:
            col = bpy.data.collections.new("Mid_Poly")
            bpy.context.scene.collection.children.link(col)

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

classes = [
    MADDHATT_OT_process_organization,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)