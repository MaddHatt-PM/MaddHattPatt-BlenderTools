import bpy
from bpy.types import Object
from . import constants as consts

class MADDHATT_OT_add_final_modifiers(bpy.types.Operator):
    bl_idname = "maddhatt.add_final_modifiers"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO"}

    def execute(self, context):
        modname_w_normals = "MHtk-WNormals"
        modname_triangulate = "MHtk-Triangulate"

        for obj in bpy.data.collections[consts.LOWPOLY].objects:
            modifier_list = obj.modifiers.keys()
            bpy.context.view_layer.objects.active = obj

            # Set up for Weighted Normals (if the mesh needs it)
            if any(modname_w_normals in mod_key for mod_key in modifier_list) == False:
                bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
                mod = bpy.context.object.modifiers[-1]
                mod.name = modname_w_normals
                mod.mode = "FACE_AREA_WITH_ANGLE"
                mod.keep_sharp = True

                mesh = obj.data
                mesh.use_auto_smooth = True
                mesh.auto_smooth_angle = 180

            # Set up for Triangulate (if the mesh needs it)
            if any(modname_triangulate in mod_key for mod_key in modifier_list) == False:
                bpy.ops.object.modifier_add(type='TRIANGULATE')
                mod = bpy.context.object.modifiers[-1]
                mod.name = modname_triangulate
                mod.quad_method = "FIXED"
                mod.keep_custom_normals = True

        return {"FINISHED"}


class MADDHATT_OT_final_check(bpy.types.Operator):
    bl_idname = "maddhatt.final_check"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO"}

    def execute(self, context):
        error_printout = {}
        error_printout.setdefault("Non Meshes", [])
        error_printout.setdefault("Unapplied Modifiers", [])
        error_printout.setdefault("Name Mismatch", [])
        error_printout.setdefault("Missing '_low'", [])

        og_active_obj = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections[consts.LOWPOLY].objects:
            if obj.type != "MESH":
                error_printout["Non Meshes"].append("\t" + obj.name)

            else:
                # Check names
                if consts.SUF_LOW in obj.name:
                    error_printout["Missing '_low'"].append("\t" + obj.name)

                # Find matches to high poly

                # Harden Normals




            if len(obj.modifiers) > 2:
                error_printout["Unapplied Modifiers"].append("\t" + obj.name)



        print(error_printout)
        bpy.context.view_layer.objects.active = og_active_obj
        return {"FINISHED"}

classes = [
    MADDHATT_OT_add_final_modifiers,
    MADDHATT_OT_final_check
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)