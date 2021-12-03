# SWTOR Granny2 (.gr2) Import/Export add-on for both Blender 2.8x and 2.9x

### WARNING: there is an incompatibility with Blender's recent 3.0 release. Old projects work OK but new object imports produce incorrectly built Materials.

Blender has changed the Principled BSDF shader's Subsurface Scattering algorithm defaults from "Christensen-Burley" to "Random Walk" (see the second menu in such shader node). That introduces a few new parameters in the shader that change their previous order and break the way the nodegroup's internal wiring worked. We need to solve that for it to work again, while making sure that it keeps on being compatible with 2.8 and 2.9.

Again, there is no problem with importing meshes or assembling characters in Blender 2.9 and opening the resulting project in Blender 3.0: Blender keeps the old SSS setting so everything works OK.

As soon as we update the add-on we'll announce it in these pages and in the Slicers GUI Discord server.

---

![](https://github.com/SWTOR-Slicers/WikiPedia/blob/main/images/other-repositories/gr2-plugin/gr2_addon_010.png)

This add-on provides Blender with several import/export features for **Star Wars: The Old Republic** (**SWTOR**) 3D assets:

* Imports and exports SWTOR's specific flavor of the .gr2 3D model format, including rigging data (vertex groups, weights) and armatures ("skeletons"). **It can import multiple files at once**. Creates template SWTOR materials on import.
* Imports and applies .jba animation files. Works often enough to be worthy.
* Imports .clo files for physics-based bones (clothes, hair, Twi'lek lekku, etc.). **Experimental**.
* Imports .json files describing all the assets and data necessary to auto-assemble and auto-texture a Player Character or a NPC (please check our guides in this Github's [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/other-repositories/gr2-plugin/gr2_addon_010.png)).

**This add-on produces template materials that replicate SWTOR's shading system** (those are automatically added to the Blender project upon importing any .gr2 mesh). They allow for using the game's texture files and materials information without requiring any previous manipulation in a third party painting app: the materials' shading networks do all the massaging involved (turning "green" normal maps to "purple", etc.).

The add-on is aware of the version of Blender it is running on, and will create the template materials accordingly. Sadly, SWTOR materials created on a Blender 2.8x project will require a small modification to run on Blender 2.9x, as this version of Blender added an input socket to the Principled BDSF Shader that causes a mis-linking in the relevant shading networks. It is very easy to correct manually, and we will post a small guide to show how in the near future.

### Installation

Download the add-on through [**this link: io_scene_gr2.zip**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/raw/master/io_scene_gr2.zip).

Once downloaded, **don't unzip it**, and install it in your Blender app through the usual means (Edit menu > Preferences > Add-ons > Install).

**For directions on its usage, please consult our [**WikiPedia**](https://github.com/SWTOR-Slicers/WikiPedia/wiki).**
