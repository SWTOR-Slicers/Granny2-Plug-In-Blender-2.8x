# SWTOR Granny2 (.gr2) Import/Export add-on for Blender 2.8x and higher

### NOW COMPATIBLE WITH BLENDER 3.0. Please download and install this new version of the Add-on.

![](https://github.com/SWTOR-Slicers/WikiPedia/blob/main/images/other-repositories/gr2-plugin/gr2_addon_010.png)

This add-on provides Blender with several import/export features for **Star Wars: The Old Republic** (**SWTOR**) 3D assets:

* Imports and exports SWTOR's specific flavor of the .gr2 3D model format, including rigging data (vertex groups, weights) and armatures ("skeletons"). **It can import multiple files at once**. Creates template SWTOR materials on import.
* Imports and applies .jba animation files. Works often enough to be worthy.
* Imports .clo files for physics-based bones (clothes, hair, Twi'lek lekku, etc.). **Experimental**.
* Imports .json files describing all the assets and data necessary to auto-assemble and auto-texture a Player Character or a NPC (please check our guides in this Github's [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/other-repositories/gr2-plugin/gr2_addon_010.png)).

**This add-on produces template materials that replicate SWTOR's shading system** (those are automatically added to the Blender project upon importing any SWTOR object, be it as such or as part of a whole character import). They allow for using the game's texture files and materials information without requiring any previous manipulation in a third party painting app: the materials' shading networks do all the massaging involved (turning "green" normal maps to "purple", etc.).

The add-on is aware of the version of Blender it is running on, and will create the template materials accordingly.

* Blender 3.0 has introduced changes that required catering to those in the add-on, hence this last release.

* There is no problem opening Blender 2.9x projects in Blender 3.0: everything works OK.

* Sadly, SWTOR materials created in Blender 2.8x projects do require a small modification to run in Blender 2.9x and higher. It is very easy to apply manually.

### Installation

Download the add-on through [**this link: io_scene_gr2.zip**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/raw/master/io_scene_gr2.zip).

Once downloaded, **don't unzip it**, and install it in your Blender app through the usual means (Edit menu > Preferences > Add-ons > Install).

**For directions on its usage, please consult our [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/wiki).**
