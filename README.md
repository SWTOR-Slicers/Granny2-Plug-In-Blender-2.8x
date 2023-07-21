#### IMPORTANT NOTICE: [the latest version of this importer addon](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/releases/latest) can import objects and characters from both the old 32 bit and the new 64 bit SWTOR game apps.<br><br>Importing skeletons and animation files from the 64 bit game is still being worked on. If you need those last features, you can use the skeleton and animation files from a 32 bit game assets extraction (if needed, there is a backup of the game's .tor files that can be downloaded from **[here](https://drive.google.com/drive/folders/1ZkBNz1cK_IXBxBd4OIYL1jRImnnfHXKW?usp=sharing)**).

# SWTOR Granny2 (.gr2) Import/Export addon for Blender 2.8x and higher

![](https://github.com/SWTOR-Slicers/WikiPedia/blob/main/images/readme_gr2_addon_010.png)
### Description

This add-on provides Blender with several import/export features for **Star Wars: The Old Republic** (**SWTOR**) 3D assets:

* Imports and exports SWTOR's specific flavor of the .gr2 3D model format, including rigging data (vertex groups, weights) and armatures ("skeletons"). **It can import multiple files at once**.
* Imports and applies .jba animation files. Works often enough to be worthy.
* Imports .clo files for physics-based bones (clothes, hair, Twi'lek lekku, etc.). **Experimental**.
* Imports .json files describing all the assets and data necessary to auto-assemble and auto-texture a Player Character or a NPC (please check our guides in this Github's [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/wiki/locating-swtor-characters-assets-automatically)).

**This add-on produces a series of Shader Nodegroups that replicate SWTOR's materials system**. They allow for using the game's texture files and materials information without requiring any previous manipulation in a third party painting app: the Shaders do all the massaging involved (turning "green" normal maps to "purple", etc.) on the fly.

### Installation

Download the add-on through [**this link: io_scene_gr2.zip**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/raw/master/io_scene_gr2.zip).

Once downloaded, **don't unzip it**, and install it in your Blender app through the usual means (Edit menu > Preferences > Add-ons > Install > Enable. If you had a previous version of the addon installed, disable and remove it first).

**For directions on its usage, please consult our [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/wiki).**

### About the "Legacy" version of this add-on

The baking-friendlier **Legacy version** of the add-on **is not compatible with the 64 bit version of SWTOR's assets**. Its shaders and materials are, though, and they happen to work with Blender's baking workflow better. Given that, **we are adding modern-to-legacy material conversion tools to some of our other add-ons**, which don't depend on the presence of this one.

It can still be downloaded from [**this link**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/releases/tag/v.3.0).
