import os
import zipfile

# Get exact folder containing deploy.py 
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file == "deploy.py":
            export_directory = root

# Gather all modules in this project
moduleNames = []
dir_cutoff_len = len(export_directory) + 1

for root, dirs, files in os.walk(export_directory):
    for file in files:
        if ".py" in file and "deploy.py" != file and "__init__.py" != file:
            mod_file = os.path.join(root[dir_cutoff_len:], file).replace(os.sep, ".")
            moduleNames.append(mod_file[:-3])
        if "__init__.py" in file:
            loader_path = os.path.join (export_directory, file)

# Rewrite __init__.py for Blender to load
loader_file = open(loader_path, "r")
loader_text = loader_file.readlines()
loader_file.close()

for i, line in enumerate(loader_text):
    if "moduleNames = [" in line:
        loader_text[i] = "moduleNames = " + str(moduleNames) + "\n"
        break

loader_file = open(loader_path, "w")
for line in loader_text:
    loader_file.write(line)
loader_file.close()

# Zip up addon 
zip_name = export_directory.split("\\")[-1] + '.zip'
zfile = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)

for root, dirs, files in os.walk(export_directory):
        for file in files:
            if "deploy.py" not in file and ".zip" not in file:
                zfile.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file),os.path.join(export_directory, '..')))
zfile.close()

# TODO: Can external python scripts force reload blender script?