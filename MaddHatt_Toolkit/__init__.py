bl_info = {
    "version": (0, 2),
    "blender": (2, 91, 0),
    "name": "MaddHatt's Pipeline Tool",
    "author": "Patt @MaddHattPatt on Twitter",
    "description": "A variety of tools to help out my personal work",
    "location": "3D View on the side bar",
    "category": "3D View"
    }


moduleNames = ['main_ui', 'Organizers.constants', 'Organizers.create_collections', 'Organizers.prepare_for_export', 'Organizers.process_organization', 'Organizers.quick_export_collection', 'Tools.aztec_incremental_save', 'Tools.circular_arrays', 'Tools.material_id_painter']

import sys
import importlib
 
modulesFullNames = {}
for currentModuleName in moduleNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)
 
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
 
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()