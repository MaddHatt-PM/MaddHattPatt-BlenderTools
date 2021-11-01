import bpy
from bpy.props import IntProperty

from .Tools import *
from .Organizers import *

# ---------------------------------------------------------------------------
# --- UI Panels ---
# ----------------- 
class VIEW3D_PT_pipeline(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pipeline Tools"
    bl_label = "MaddHattPatt's Toolbox"

    def draw(self, context):
        layout = self.layout
        
        row = layout.column(align=True)
        row.label(text="Workflow Helpers")

        # Circular Array Controls
        active_object = context.active_object
        fallback_to_op = True
        if active_object != None and bpy.context.selectable_objects != 0:
            if any("Circular Array" in mod_key for mod_key in active_object.modifiers.keys()):
                row.prop(active_object, "cir_array_count", slider=True)
                fallback_to_op = False

        if (fallback_to_op == True):
            row.operator("maddhatt.setup_circular_array", text="Create circular array", icon="FORCE_LENNARDJONES")


        layout.separator()

        row = layout.column(align=True)
        row.label(text="Pipeline Managers")
        if any(col.name == "Organizer" for col in bpy.data.collections) == False:
            row.operator("maddhatt.create_organizer_collection", text="Add Organizer Collection", icon="COLLECTION_NEW")
            self.layout(context.object, "prop", slider=True)

        else:
            if len(bpy.data.collections.get("Organizer").objects) == 0:
                processor_text = "Add objects to Organizer"
            else:
                processor_text = "Process Organization"

            row.operator("maddhatt.process_organization", text=processor_text)
            row.operator("maddhatt.create_export_collection", text="Setup Low Poly", icon="COLLECTION_NEW").coll_name = "Low_Poly"
            row.operator("maddhatt.create_export_collection", text="Setup High Poly", icon="COLLECTION_NEW").coll_name = "High_Poly"

            row.operator("maddhatt.add_final_modifiers", text="Add Final Modifiers")
            row.operator("maddhatt.final_check", text="Final Checks")

        layout.separator()

        row = layout.column(align=True)
        row.label(text="Mat ID Painter")
        row.operator("maddhatt.create_material", text="Create ID Material", icon="MATERIAL").mat_id = len(bpy.data.materials)
        for mat_id in range(0, len(bpy.data.materials)):
            mat_target = bpy.data.materials[mat_id].name
            if mat_target.startswith("ID"):
                # Process the material's name for readibility
                if len(mat_target) != 5:
                    mat_name = mat_target[5:]
                else:
                    mat_name = "ID Mat - " + str(int(mat_target[2:4]))

                col = row.row(align=True)
                col.operator("maddhatt.assign_material", text=mat_name).mat_id = mat_target
                col.operator("maddhatt.rename_id_material", text="", icon="RIGHTARROW_THIN").mat_target = mat_target


# ---------------------------------------------------------------------------
# --- Class registration ---
# --------------------------

classes = [
    VIEW3D_PT_pipeline,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()
