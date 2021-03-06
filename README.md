# MaddHattPatt-BlenderTools
A collection of tools to help my personal workflow. Also includes files to sync back and forth for my work stations

## Task List
- [x] Incremental save from another 3d modeling program
- [ ] Workflow Tools
    - [x] Circular Array Setup Operator
    - [ ] Circular Array editor
        - [ ] 1. Check the array name, who changes the array name and if 
        - [ ] 2. Change the count value and change the rotation of the offset object
- [ ] MaddHatt Pipeline Tool
    - [ ] Quick ID Mats
        - [x] Create ID Mat
        - [x] Create random colors for ID purposes at least 10 distinct ones should be good
        - [ ] Create buttons for other ID colors
        - Give the user a list of mats with prefix 'ID_' and an option to create a new mat with a randomized color. For randomized colors, reference a premade tuple of colors
        - When in edit mesh mode with face mode on, non added materials should be greyed out. When clicked the add to the mesh's material list and then are no longer greyed out.
    - [ ] Mid Poly Setup
        - [x] 1. Create backup save (Not needed)
        - [x] 2. Target a specific collection
        - [x] 3. Unparent all objects with transformation so they're on the same level
        - [x] 4. Create _TOOLS collections
        - [x] 5. Move all hidden objects to _TOOLS
        - [x] 6. Everything else gets moved to Mid_Poly collection (create if not already made) 
        - [x] 7. Rename everything in Mid_Poly (Optional) to ie: Part05
            - [x] Naming convention should be vague and general and not something   someone would actually use for the final product 
        - [X] 8. Duplicate: Mid_Poly and rename to Low_Poly. Rename all new objects with a _low suffix
        - [ ] 9. Give the low poly meshes a material name of mat_finalname
        - [X] 10. Duplicate: Mid_Poly and rename to High_Poly. Rename all new objects with a _high suffix
    - [ ] Name check for high poly
        - [ ] 1. Search for meshes with children
        - [ ] 2. Rename meshes to have their prefix be HighestParentName_high_Part0
            - For larger parent/child floating geometry structures this might get a little confusing but I doubt I'll run into that problem for bake only   meshes
    - [ ] Propogate changes
        - [ ] 1. If any other meshes get added to Mid_Poly, create their appropriate copy to High_Poly and Low_Poly
    - [ ] Mismatch Checker
        - [ ] 1. Search if every mesh has a low/high poly pairing.
            - low polys can pair with multiple high polys (floating geometry)
            - Can multiple low poly's share the name? I don't see a reason why not but I've never tried it
        - [ ] 2. Show a warning to the user that there's a mismatch
        - [ ] 3. Prompt the user to hide matches.
        - [ ] 4. If user continues, unload collections, then load low_poly and high_poly to reset all their visibility states
        - [ ] 5. Iterate through all pairings until no pairings are left
    - [ ] Low Poly Prep
        - [ ] 1. Go through Low_Poly collection mesh by mesh
            - [ ] 1. Turn on all auto smooth and set to
            - [ ] 2. Remove edges marked sharp
            - [ ] 3. Convert UV island edges to sharpness
    - [ ] Quick Export
        - Both operations will use the final_export preset I have for low poly
        - [ ] Folder path input
        - [ ] Button for low poly models 
        - [ ] Button for high poly models 