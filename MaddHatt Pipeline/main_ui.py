bl_info = {
    "version": (0, 1),
    "blender": (2, 91, 0),
    "name": "MaddHatt's Pipeline Tool",
    "author": "Patt @MaddHattPatt <MaddHatt.pm@gmail.com>",
    "description": "A variety of tools to help out my personal ",
    "location": "3D View on the side bar",
    "category": "3D View"
    }

import bpy
import random
import colorsys
import math
import importlib
from bpy.props import IntProperty, StringProperty
from bpy.types import EnumProperty, LayerCollection, Operator

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
        
        col = layout.column(align=True)
        col.label(text="Workflow Helpers")
        col.operator("maddhatt.setup_circular_array", text="Create circular array", icon="FORCE_LENNARDJONES")

        layout.separator()

        col = layout.column(align=True)
        col.label(text="Pipeline Managers")
        if any(col.name == "Organizer" for col in bpy.data.collections) == False:
            col.operator("maddhatt.create_organizer_collection", text="Add Organizer Collection", icon="COLLECTION_NEW")

        else:
            col.operator("maddhatt.process_organization", text="Process Organization")
            col.operator("maddhatt.create_export_collection", text="Setup Low Poly", icon="COLLECTION_NEW").coll_name = "Low_Poly"
            col.operator("maddhatt.create_export_collection", text="Setup High Poly", icon="COLLECTION_NEW").coll_name = "High_Poly"

        layout.separator()

        col = layout.column(heading="Color ID Painting", align=True)
        col.operator("maddhatt.create_material", text="Create ID Material", icon="MATERIAL").mat_id = len(bpy.data.materials)
        for mat_id in range(0, len(bpy.data.materials)):
            mat_target = bpy.data.materials[mat_id].name
            if mat_target.startswith("ID"):
                # Process the material's name for readibility
                if len(mat_target) != 5:
                    mat_name = mat_target[5:]
                else:
                    mat_name = "ID Mat - " + str(int(mat_target[2:4]))

                row = col.row(align=True)
                row.operator("maddhatt.assign_material", text=mat_name).mat_id = mat_target
                row.operator("maddhatt.rename_id_material", text="", icon="RIGHTARROW_THIN").mat_target = mat_target


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
