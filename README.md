# SWTOR Granny2 (.gr2) Import/Export add-on for Blender 2.8x and higher

### NEW COMPACT, SMART VERSION, MORE FAITHFUL TO THE GAME'S LOOKS, WITH SCARS!!!

**If you were a user of [the previous version of the addon](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/releases/tag/v.3.0)**, don't delete and replace it just yet. There are a few fundamental differences between this version and previous ones that you might have to weight in:

* Instead of materials holding a tree of texturemap image nodes linked to a SWTOR Shader nodegroup, the texturemap images' controls are now in the Shader itself, making everything simpler and more self-contained. Also, the Shader takes care of alpha and colorspace issues for us.

  Because of this, there are no SWTOR materials templates any longer, so prone to accidental overwriting: now, in order to create a SWTOR material, we only need to add the appropriate SWTOR shader node, via the Add Node menu (shift-a), to any new or existing material, and link it to the Output Node.
  
  On the other hand, this compactness makes extending and customizing such materials (by interposing other nodes or exposing internal parameters) harder. We'll explore how to go at it through new guides. Given this, if we happen to depend on doing such modifications, we might want to hold on to the previous version for a little while longer, or maybe keep around a Blender project holding the old template materials so that we can append them to new projects.
  
  The previous, "classic" version of the addon can be downloaded from [**this link**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/releases/tag/v.3.0).
  
  **Installing this addon DOESN'T break previous Blender projects' materials**.

* SWTOR shaders' controls have been re-labelled to allow for more intuitive hand-tweaking (changing the color of gear and skin by eye).

* In general, the shaders are even more faithful to the game's own than before.

* **Scars!!!**

The wiki's guides will be updated to reflect these differences as quickly as possible. In general, they only affect non-automated processes (manually texture a weapon, a vehicle, etc.), while automated ones (auto-assemble a player character or a NPC) aren't impacted at all.

![](https://github.com/SWTOR-Slicers/WikiPedia/blob/main/images/readme_gr2_addon_010.png)
### Description

This add-on provides Blender with several import/export features for **Star Wars: The Old Republic** (**SWTOR**) 3D assets:

* Imports and exports SWTOR's specific flavor of the .gr2 3D model format, including rigging data (vertex groups, weights) and armatures ("skeletons"). **It can import multiple files at once**.
* Imports and applies .jba animation files. Works often enough to be worthy.
* Imports .clo files for physics-based bones (clothes, hair, Twi'lek lekku, etc.). **Experimental**.
* Imports .json files describing all the assets and data necessary to auto-assemble and auto-texture a Player Character or a NPC (please check our guides in this Github's [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/other-repositories/gr2-plugin/gr2_addon_010.png)).

**This add-on produces a series of Shader Nodes that replicate SWTOR's materials system**. They allow for using the game's texture files and materials information without requiring any previous manipulation in a third party painting app: the Shaders do all the massaging involved (turning "green" normal maps to "purple", etc.) on the fly.

The add-on is aware of the version of Blender it is running on, and will create the Shaders accordingly (Blender has been introducing slight differences in its Principled BSDF shader's number of inputs and parameters and their order since the 2.8 version, and the addon caters to those when creating new materials).

### Installation

Download the add-on through [**this link: io_scene_gr2.zip**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/raw/master/io_scene_gr2.zip).

Once downloaded, **don't unzip it**, and install it in your Blender app through the usual means (Edit menu > Preferences > Add-ons > Install. If you had a previous version of the addon installed, disable and remove it first).

**For directions on its usage, please consult our [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/wiki).**
