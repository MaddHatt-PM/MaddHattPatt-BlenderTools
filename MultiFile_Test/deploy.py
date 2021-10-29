import os
import zipfile

def zip_directory(path, zfile):
    for root, dirs, files in os.walk(path):
        for file in files:
            zfile.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file),os.path.join(path, '..')))

# Rewrite the __init__.py to add new classes

for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file == "deploy.py":
            export_directory = root

zip_name = export_directory.split("\\")[-1] + '.zip'

zfile = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
zip_directory(export_directory, zfile)
zfile.close()