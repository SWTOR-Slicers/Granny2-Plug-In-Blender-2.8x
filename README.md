## Current state of the branch:
### Progress!

* **Our ShaderNodeHeroEngine node's disappearances were a Blender bug!** It began in 3.6.8 and has just been corrected in 3.6.12 (it had been solved in 4.0 but reappeared in 4.1.0 and again was corrected in 4.1.1). It was the most mystifying issue, and in the end it happened not to be our fault.
  
* **The Shader Editor's Add menu has our SWTOR shaders submenu implemented as a conventional fn appending, now** (see [4.0's API deprecated NodeItem and NodeCategory](https://developer.blender.org/docs/release_notes/4.0/python_api/#nodes). That impacted the previous way of doing it).

### The showstopper:
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
* Animation Import (**32 bit-only .jba**) works correctly, **BUT: there seems to be a long standing bug that makes turns bigger than 360º glitch: it can be seen in some of the Twi'lek dances**.

---

### New features:

While working on this, we've implemented a series of long wanted new features, accessible both from the importers' properties in their File Browsers and from a new Preferences Panel:

* **Use Filename as object name**: solves issues with Nautolan PCs and others.
* **Axis Conversion and Scale Factor**: they do the Z-is-Up x=90º rotation and typical x10 scaling at the mesh level instead of at the object level.
* **The .jba animation importer's scale factor is synced to the .gr2 importer's one**, although it can be set differently, too.
* **It offers a Delete 180º Rotation option so that animations don't rotate characters away from us**.
* **There is a presets system**: BLENDER (for arting), PORTING (to other apps), and NEUTRAL (the old settings). Porting settings are tentative: we need feedback from people doing actual ports to VRchat and other targets.

(Other add-ons that use this one are being made aware of these settings to react accordingly)

---

### What's different to the Master branch.

* **Excessive duplication of code**: as we didn't know how considerable the API changes between Blender 3.x and 4.x were going to be (and it was clear that 4.1 was to be full of late arrivals), **basically everything but the `__init__.py` file has been subfoldered into a `lib3` and a `lib4` subfolder containing almost-duplicates of the original single set of code**. Some elements, like  the whole `utils` subfolder, could have been left alone, but this seemed simpler to maintain.  
  
  **The thing is, Blender 4.1 has its own add-on-breaking API changes and is going to need its own lib41.** We *don't knoww about 4.2, but…

* **Messy `__init__.py` file**: again, due to the tentative nature of the 4.0-compatibility changes, the init code support for the almost-duplication of code is rather crude.
  
  Something to note is that **the SWTOR Shaders submenu** is registered and unregistered there, but a deprecation (the API for registering custom Shader nodes categories is gone in 4.x, favoring conventtional means to extend that menu) means that it **is done differently depending on Blender version** (see [4.0's API changelog on that](https://developer.blender.org/docs/release_notes/4.0/python_api/#nodes)).

  (What's more, it seems there was a shaders category deprecation of some kind circa Blender 3.3, but it never seemed to affect the workings of the add-on. It's possible that it was simply announced back then and executed with 4.0)

* **These are the changes that were done to cater to Blender 4.0, inside the lib4 subfolder:**
  * **`\types\node.py`**:  'Raw' colorspace no longer exists, so, we replaced it with 'Non-Color", which is functionally equivalent despite not meaning quite the same.
  * **`\types\node_tree.py`**: node_tree.outputs.new no longer exists (neither does node_tree.inputs). Now, one has node_tree.interface.new_socket and a different set of parameters. The substitutions are at the beginning of each SWTOR shader node_tree: a check for the existence of an output socket and the creation of it if it doesn't exist. There seems to be no easy way to count output sockets without going through the interface's items_tree, hence a function for that at the beginning being called at each shader.    
    
    Also, little changes here and there, related to setting the default_value of several Principled BSDF Shader inputs in the SWTOR Eye shader. The Principled Shader has changed considerably between versions ("Clearcoat XYZ" is now "Coat XYZ" and so on, for one thing, and some inputs mean now different things and require different default values to produce the same results).

  * **`\ops\add_swtor_shaders_menu.py`**: Shader Editor's Add menu's SWTOR submenu. Includes an Operator class, a menu layout class, and a function calling the menu plus a separator (whose actual appending to the Add menu happens in `__init__.py`).

* **The new addon_pref module is at the root of the add-on's folder and has no Blender version-dependent variants**.
* **The new features are identically implemented for each Blender version, so far**. They impact `\ops\import_gr2.py` and `\ops\import_jba.py`: new property definitions, using invoke() instead of ImportHelper to be able to match the properties with the ones from preferences, some heuristics about them, and the actual features in the mesh and animation building.