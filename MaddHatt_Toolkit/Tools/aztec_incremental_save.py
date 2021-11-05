import bpy
import datetime
import os
from bpy.app.handlers import persistent

@persistent
def backup_to_subfolder(dummy):
    filepath = bpy.data.filepath
    filename = filepath.split('\\')[-1]

    # backup_filename preparation
    now = datetime.datetime.now()
    month_id = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"}
    time_suffix = "_" + month_id[now.month] + str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + '-' + str(now.minute).zfill(2)
    backup_filename = filename.replace(".blend", time_suffix + ".blend")

    savefolder = filepath.replace(".blend", " - Backups") + '\\'
    if not os.path.exists(savefolder):
        os.makedirs(savefolder)

    if not os.path.exists(savefolder + backup_filename):
        bpy.ops.wm.save_as_mainfile(filepath=savefolder + backup_filename, copy=True)

    print ("being called")

# ------------------------------------------
# -- Addon-Boilerplate --
# -----------------------
def register():
    bpy.app.handlers.save_post.append(backup_to_subfolder)

def unregister():
    bpy.app.handlers.save_post.remove(backup_to_subfolder)

if __name__ == "__main__":
    register()