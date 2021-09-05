import bpy

# bpy.ops.mesh.primitive_cube_add(size= 5, enter_editmode=False, align="WORLD", location=(0,0,0), scale=(1,1,1))
# bpy.context.active_object.name = "a different name!"

text = bpy.data.curves.new(type="FONT", name="Hello World")
text.body = "Hello World :)"
text_obj = bpy.data.objects.new(name="Text Object", object_data=text)
bpy.context.scene.collection.objects.link(text_obj)

# How this works
# Line 6: Creates the data object (in this case a curve and the text is a type of curve)
# Line 7: Edits the data object to have the text of "Hello World :)"
# Line 8: Links the data to a scene object
# Line 9: Links the scene object to a scene!