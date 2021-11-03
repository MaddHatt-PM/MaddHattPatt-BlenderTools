import bpy
import bpy.path
from . import constants as consts

class MADDHATT_OT_quick_export_collection(bpy.types.Operator):
    bl_idname = "maddhatt.quick_export_collection"
    bl_label = "You shouldn't be seeing this"
    bl_options = { "INTERNAL", "REGISTER", "UNDO"}

    # target_coll: bpy.props.CollectionProperty(name="target_coll")
    coll_name: bpy.props.StringProperty(name="target_coll")

    def execute(self, context):
        target_coll = bpy.context.view_layer.layer_collection.children[self.coll_name]
        
        target_coll_exclude_prev = target_coll.exclude
        active_layer_coll_prev = bpy.context.view_layer.active_layer_collection

        suffix = consts.coll_to_suffix(self.coll_name)
        if suffix is None:
            self.report({"ERROR"}, "Only LOWPOLY and HIGHPOLY are valid collections to export")
            return {"CANCELLED"}

        filepath = bpy.path.abspath("//") 
        filepath += bpy.path.basename(bpy.data.filepath).replace(".blend", "")
        filepath += suffix + ".fbx"
        target_coll.exclude = False
        bpy.context.view_layer.active_layer_collection = target_coll
        

        bpy.ops.export_scene.fbx(
            # --- Export ---------------------------------
            filepath= filepath,
            path_mode= 'AUTO', 
            batch_mode= 'OFF', 
            use_batch_own_dir= True, 
            use_metadata = True, 
            embed_textures= False, 

            check_existing= True, 
            filter_glob= "*.fbx", 
            use_selection= False, 
            use_active_collection= True, 

            # --- Transform ------------------------------
            global_scale= 1, 
            apply_unit_scale= True, 
            apply_scale_options = 'FBX_SCALE_ALL', 
            axis_forward = '-Z',
            axis_up = 'Y',
            use_space_transform= True, 
            bake_space_transform= False, 
            use_custom_props= False,

            # --- Geometry -------------------------------
            object_types= {'MESH'}, 
            use_mesh_modifiers= True, 
            mesh_smooth_type= 'FACE', 
            use_subsurf= False, 
            use_mesh_edges= False, 
            use_tspace= True,

            # --- Armature -------------------------------
            add_leaf_bones= True, 
            primary_bone_axis= 'Y', 
            secondary_bone_axis= 'X', 
            use_armature_deform_only= False, 
            armature_nodetype= 'NULL',

            # --- Animation ------------------------------
            bake_anim= False, 
            # bake_anim_use_all_bones: bool = True, 
            # bake_anim_use_nla_strips: bool = True, 
            # bake_anim_use_all_actions: bool = True, 
            # bake_anim_force_startend_keying: bool = True, 
            # bake_anim_step: float = 1, 
            # bake_anim_simplify_factor: float = 1,
            )

        # Return to original state
        target_coll.exclude = target_coll_exclude_prev
        bpy.context.view_layer.active_layer_collection = active_layer_coll_prev

        self.report({"INFO"}, "Exported " + self.coll_name + " successfully")
        return {"FINISHED"}

classes = [
    MADDHATT_OT_quick_export_collection,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)