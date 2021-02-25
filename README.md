# SWTOR Granny2 (.gr2) Import/Export add-on for both Blender 2.8x and 2.9x

This add-on provides Blender with an import/export feature for the Star Wars: The Old Republic (SWTOR) specific flavor of the .gr2 3D model format, including rigging data (vertex groups, weights) and armatures.

It also provides with **template materials that replicate SWTOR's shading system** (those are added to the Blender project upon importing any .gr2 mesh). They allow for using the game's texture files and materials information without requiring any previous manipulation in a third party painting app: the materials' shading networks do all the massaging involved (turning "green" normal maps to "purple", etc.).

This add-on is aware of the version of Blender it is running on, and will create the template materials accordingly. Sadly, SWTOR materials created on a Blender 2.8x project will require a small modification to run on Blender 2.9x, as this version added an input socket to the Principled BDSF Shader that causes a mis-linking in the relevant shading networks. It is very easy to correct, and we will post a small guide to show how in the near future.

### Installation

To install the add-on in Blender, download the file "io_scene_gr2_addon_for_blender_2.8x_and_2.9x.zip", don't unzip it, and install it in your Blender app through the usual means (Edit menu > Preferences > Add-ons > Install).

For directions on its usage, please consult the [SWTOR-Extractors-Modders-Dataminers WikiPedia](https://github.com/SWTOR-Extractors-Modders-Dataminers/WikiPedia).
