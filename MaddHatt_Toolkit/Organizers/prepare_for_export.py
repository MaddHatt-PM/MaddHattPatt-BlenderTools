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

        # Edit normals
        og_active_obj = bpy.context.view_layer.objects.active
        #TODO: for edge is uv seam -> mark sharp

        for obj in bpy.data.collections[consts.LOWPOLY].objects:
            bpy.ops.object.shade_smooth()
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

        bpy.context.view_layer.objects.active = og_active_obj
        return {"FINISHED"}


class MADDHATT_OT_final_check(bpy.types.Operator):
    bl_idname = "maddhatt.final_check"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO"}

    def execute(self, context):
        error_printout = {}
        error_printout.setdefault("Non Meshes", [])
        error_printout.setdefault("Missing HiPoly Partner", [])
        error_printout.setdefault("Missing '_low'", [])
        error_printout.setdefault("Unapplied Modifiers", [])
        error_printout.setdefault("Missing WNormal and Triangulate", [])

        modname_w_normals = "MHtk-WNormals"
        modname_triangulate = "MHtk-Triangulate"
        
        og_active_obj = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections[consts.LOWPOLY].objects:
            obj.hide_set(True)
            
            if obj.type != "MESH":
                error_printout["Non Meshes"].append( obj.name)
                obj.hide_set(False)

            else:
                # Check names
                if consts.SUF_LOW not in obj.name:
                    error_printout["Missing '_low'"].append(obj.name)
                    obj.hide_set(False)

                # Find matches to high poly
                high_obj_name = obj.name.replace(consts.SUF_LOW, consts.SUF_HIGH)
                if bpy.data.collections[consts.HIGHPOLY].objects.get(high_obj_name, None) == None:
                    error_printout["Missing HiPoly Partner"].append(obj.name)
                    obj.hide_set(False)
                
                # Find modifiers length
                if len(obj.modifiers) > 2:
                    error_printout["Unapplied Modifiers"].append(obj.name)
                    obj.hide_set(False)
                else:
                    # Check for weighted and triangulate modifiers
                    if obj.modifiers.get(modname_w_normals, None) is None and obj.modifiers.get(modname_triangulate, None) is None:
                        error_printout["Unapplied Modifiers"].append(obj.name)
                        error_printout["Missing WNormal and Triangulate"].append(obj.name)
                        obj.hide_set(False)

        output_text = ""
        errors_present = False

        for key in error_printout.keys():
            if len(error_printout[key]) != 0:
                errors_present = True
                output_text += key + ": "
                output_text += str(error_printout[key]).replace('[', '').replace(']', '')
                output_text += "\n"

        if (errors_present):
            self.report({"WARNING"}, "Issues found, see 'Info' panel for breakdown\n" + output_text[:-1])
        else:
            self.report({"INFO"}, "No issues found, good for export!")
            for obj in bpy.data.collections[consts.LOWPOLY].objects:
                obj.hide_set(False)

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