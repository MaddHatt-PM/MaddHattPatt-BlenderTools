import bpy
from . import constants as consts

class MADDHATT_OT_create_organizer_collection(bpy.types.Operator):
    bl_idname = "maddhatt.create_organizer_collection"
    bl_label = "you shouldn't see this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED" }

    def execute(self, context):
        col = bpy.data.collections.new(consts.ORGANIZER)
        bpy.context.scene.collection.children.link(col)

        return {"FINISHED"}

class MADDHATT_OT_create_export_collection(bpy.types.Operator):
    bl_idname = "maddhatt.create_export_collection"
    bl_label = "you shouldn't see this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO_GROUPED" }

    coll_name: bpy.props.StringProperty(name="coll_name")

    @classmethod
    def poll(cls, context):
        if any(col.name == consts.MIDPOLY for col in bpy.data.collections) == False:
            return False

        if len(bpy.data.collections.get(consts.MIDPOLY).objects) == 0:
            return False

        return True

    def execute(self, context):
        if self.coll_name == consts.LOWPOLY:
            coll_suffix = "_low"
            coll_color = "COLOR_04"

        elif self.coll_name == consts.HIGHPOLY:
            coll_suffix = "_high"
            coll_color = "COLOR_05"

        else:
            print("failed")
            return {"CANCELLED"}

        # Get or create the needed collection
        if (self.coll_name not in bpy.data.collections):
            col = bpy.data.collections.new(self.coll_name)
            col.color_tag = coll_color
            bpy.context.scene.collection.children.link(col)
        else:
            col = bpy.data.collections[self.coll_name]
            
        for item in bpy.data.collections[consts.MIDPOLY].objects:
            if any(item.name in obj.name for obj in col.objects) == False:
                dup_item = item.copy()
                dup_item.data = item.data.copy()
                col.objects.link(dup_item)
                dup_item.name = dup_item.name.replace(".001", coll_suffix)

        # For the low poly collection, apply an export material
        if self.coll_name == consts.LOWPOLY:
            mat_name = bpy.path.basename(bpy.data.filepath).replace(".blend", "") + "_mat"
            export_mat = bpy.data.materials.get(mat_name, bpy.data.materials.new(mat_name))
            for item in bpy.data.collections[consts.LOWPOLY].objects:
                item.data.materials.clear()
                item.data.materials.append(export_mat)

        return {"FINISHED"}

    # def invoke(self, context, coll_name:str):
    #     self.coll_name = coll_name
    #     return self.execute(context)

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