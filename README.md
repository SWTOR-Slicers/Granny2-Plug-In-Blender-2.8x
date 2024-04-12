## Current state of the branch:
### We have a few showstoppers:

* **The ShaderNodeHeroEngine node** is added correctly to materials, but **upon project reload (or "equivalent" undo-then-redo action) it completely loses its custom UI and the material turns black** despite the underlying nodegroups ("SWTOR", "SWTOR.001", etc.) still existing. This happens in Blender 3.6.8 upwards, and 4.1. Strangely, it doesn't happen in Blender 4.0.
  
  [4.0's API deprecates NodeItem and NodeCategory](https://developer.blender.org/docs/release_notes/4.0/python_api/#nodes). That impacted the previous SWTOR shaders submenu in the Shader Editor's Add menu, which now is implemented as a conventional appending to that menu, but it might have to do with this issue, too. 

* **Several deprecations in bmesh break the .gr2 importer module** (See [4.1's list of API changes](https://developer.blender.org/docs/release_notes/4.1/python_api/)). They are marked with a "# DEPRECATED" in `io_scene_gr2\lib4\ops\import_gr2.py`'s code. Here there are the lines and a mention to what seems to be relevant in Blender's 4.1 changelog.

  * **`Line 352 bmesh.create_normals_split()`**  
  
    "**create_normals_split**, calc_normals_split, and free_normals_split **are removed, and are replaced by the simpler Mesh.corner_normals collection property**. Since it gives access to the normals cache, it is automatically updated when relevant data changes."
    
    ---

  * **`Line 364 bmesh.loops[loop_index].normal = [v.normals.x, v.normals.y, v.normals.z]`**
  
    "**MeshLoop.normal is now a read-only property. Custom normals should be created by normals_split_custom_set or normals_split_custom_set_from_vertices**."
    
    ---

  * **`Line 383 bmesh.use_auto_smooth = True`**
  
    "use_auto_smooth is removed. **Face corner normals are now used automatically if there are mixed smooth vs. not smooth tags. Meshes now always use custom normals if they exist**.  

    **auto_smooth_angle is removed. Replaced by a modifier (or operator) controlling the "sharp_edge" attribute**. This means the mesh itself (without an object) doesn't know anything about automatically smoothing by angle anymore."

  Commenting these lines out lets objects import (without normals and smoothing) with no more exceptions.

### Other than that:
* Skeleton objects import works correctly.
* Character Import (.json) works correctly (actual .gr2 objects import aside)
* Animation Import (32 bit-only .jba) works correctly.
* We have the SWTOR Shaders sub-menu back into the Shader Editor's Add menu.


### What's different to the Master branch.

* **Lazy duplication of code**: as we didn't know how considerable the API changes between Blender 3.x and 4.x were going to be (and it was clear that 4.1 was to be full of late arrivals), **basically everything but the `__init__.py` file has been subfoldered into a `lib3` and a `lib4` subfolder containing almost-duplicates of the original single set of code**.  
  
  The thing is, the changes in 4.0 are varied enough to make adding Blender version conditionals where they happen a nuisance to chase around. And now, Blender 4.1 has its own add-on-breaking ones (and possibly 3.6.8/9 ought to, too), further complicating things. An alternative might have been duplicating the specifically affected files. Using version conditionals in the code felt too cumbersome to do, given certain cases.
  
  (As 4.1's features are what 4.0 was meant to include but weren't ready for the release, would skipping 4.0 support (half-way between 3.6.x and 4.1) merit consideration? 4.1's deprecation of Auto Smooth for a Modifier means that many are going to stay in 4.0 until a better user experience surfaces)

* **Messy `__init__.py` file**: again, due to the tentative nature of the 4.0-compatibility changes, the init code support for the almost-duplication of code is rather crude.
  
  Something to note is that **the SWTOR Shaders submenu** is registered and unregistered there, but a deprecation (the API for registering custom Shader nodes categories is gone in 4.x, favoring conventtional means to extend that menu) means that it **is done differently depending on Blender version** (see [4.0's API changelog on that](https://developer.blender.org/docs/release_notes/4.0/python_api/#nodes)).

  (What's more, it seems there was a shaders category deprecation of some kind circa Blender 3.3, but it never seemed to affect the workings of the add-on. It's possible that it was simply announced back then and executed with 4.0)

* **These are the changes that were done to cater to Blender 4.0, inside the lib4 subfolder:**
  * **`\types\node.py`**:  'Raw' colorspace no longer exists, so, we replaced it with 'Non-Color", which is functionally equivalent despite not meaning quite the same.
  * **`\types\node_tree.py`**: node_tree.outputs.new no longer exists (neither does node_tree.inputs). Now, one has node_tree.interface.new_socket and a different set of parameters. The substitutions are at the beginning of each SWTOR shader node_tree: a check for the existence of an output socket and the creation of it if it doesn't exist. There seems to be no easy way to count output sockets without going through the interface's items_tree, hence a function for that at the beginning being called at each shader.    
    
    Also, little changes here and there, related to setting the default_value of several Principled BSDF Shader inputs in the SWTOR Eye shader. The Principled Shader has changed considerably between versions ("Clearcoat XYZ" is now "Coat XYZ" and so on, for one thing, and some inputs mean now different things and require different default values to produce the same results).

  * **`\ops\add_swtor_shaders_menu.py`**: Shader Editor's Add menu's SWTOR submenu. Includes an Operator class, a menu layout class, and a function calling the menu plus a separator (whose actual appending to the Add menu happens in `__init__.py`).
  
(Note: some time ago, the character importer module received some changes in the main branch to solve some issues with second material slots (eyes and such) and to let it process NPCs (there was some oddness going on). I remember we had a hiccup regarding having the main repository up to date. Both the current Master and this branch have them)