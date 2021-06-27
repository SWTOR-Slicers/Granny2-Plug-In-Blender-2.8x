# SWTOR Granny2 (.gr2) Import/Export add-on for both Blender 2.8x and 2.9x

## Now compatible with Blender 2.93

![](https://github.com/SWTOR-Slicers/WikiPedia/blob/main/images/other-repositories/gr2-plugin/gr2_addon_010.png)

This add-on provides Blender with several import/export features for **Star Wars: The Old Republic** (**SWTOR**) 3D assets:

* Importing and exporting SWTOR's specific flavor of the .gr2 3D model format, including rigging data (vertex groups, weights) and armatures.
* Importing and applying .jba animation files. Works often enough to be worthy.
* Importing .clo files for physics-based bones (clothes, hair, Twi'lek lekku, etc.). Experimental.
* Importing .json files describing all the assets and data necessary to auto-assemble and auto-texture a Player Character or a NPC (please check our guides in this Github's [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/other-repositories/gr2-plugin/gr2_addon_010.png)).

Also, this add-on produces **template materials that replicate SWTOR's shading system** (those are added to the Blender project upon importing any .gr2 mesh). They allow for using the game's texture files and materials information without requiring any previous manipulation in a third party painting app: the materials' shading networks do all the massaging involved (turning "green" normal maps to "purple", etc.).

This add-on is aware of the version of Blender it is running on, and will create the template materials accordingly. Sadly, SWTOR materials created on a Blender 2.8x project will require a small modification to run on Blender 2.9x, as this version added an input socket to the Principled BDSF Shader that causes a mis-linking in the relevant shading networks. It is very easy to correct, and we will post a small guide to show how in the near future.

### Installation

#### Download the add-on through this link: [**io_scene_gr2.zip**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/raw/master/io_scene_gr2.zip).

Once downloaded, don't unzip it, and install it in your Blender app through the usual means (Edit menu > Preferences > Add-ons > Install).

For directions on its usage, please consult the [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/wiki).
