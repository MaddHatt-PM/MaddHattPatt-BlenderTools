import bpy
import datetime

# Idea Flow
# 0. Always active on save(). Maybe with some event handler if Python has those?
# 1. Get file name
# 2. If a folder with "file name" + " Incremental Save", does not exist, create it
# 3. Save the same version with as "file name_Aug29_22H20M
#
# Other things:
# I don't want to create .backupblend files 



# Save as main file but does it work like "save as copy" 
# bpy.ops.wm.save_as_mainfile()

# Gets the filepath of the .blend file
# bpy.data.filepath

# Actives after saving is complete... need example since handlers are new to me with Python
# https://docs.blender.org/api/current/bpy.app.handlers.html
# bpy.app.handlers.save_post

def month_abbrev(input:int) -> str:
    converter = {
        1: "JAN",
        2: "FEB",
        3: "MAR",
        4: "APR",
        5: "MAY",
        6: "JUN",
        7: "JUL",
        8: "AUG",
        9: "SEP",
        10: "OCT",
        11: "NOV",
        12: "DEC"
    }

    return converter.get(input, "WAT")

filepath = bpy.data.filepath
filename = filepath.split('\\')[-1]

now = datetime.datetime.now()


time_suf = "_" + month_abbrev(now.month) + str(now.day) + "_" + str(now.hour) + 'H' + str(now.minute) + 'M'
backup_filename = filename.replace(".blend", time_suf + ".blend")

print(backup_filename)
