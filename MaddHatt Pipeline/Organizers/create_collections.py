import bpy

class MADDHATT_OT_create_organizer_collection(bpy.types.Operator):
    bl_idname = "maddhatt.create_organizer_collection"
    bl_label = "you shouldn't see this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED" }

    def execute(self, context):
        col = bpy.data.collections.new("Organizer")
        bpy.context.scene.collection.children.link(col)

class MADDHATT_OT_create_export_collection(bpy.types.Operator):
    bl_idname = "maddhatt.create_export_collection"
    bl_label = "you shouldn't see this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED" }

    coll_name: bpy.props.StringProperty(name="coll_name")

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections.get("Mid_Poly").objects) != 0

    def execute(self, context):
        if self.coll_type == "Low_Poly":
            coll_suffix = "_low"
        elif self.coll_type == "High_Poly":
            coll_suffix = "_high"

        col = bpy.data.collections.new(self.coll_name)
        bpy.context.scene.collection.children.link(col)

        bpy.data.collections["Mid_Poly"].objects[0].name.replace(".001", coll_suffix)
        for item in bpy.data.collections["Mid_Poly"].objects:
            item.name = item.name.replace(".001", coll_suffix)
            bpy.data.collections["Mid_Poly"].objects.unlink(item)
            bpy.data.collections[self.coll_name].objects.link(item)

classes = [
    MADDHATT_OT_create_organizer_collection,
    MADDHATT_OT_create_export_collection,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)