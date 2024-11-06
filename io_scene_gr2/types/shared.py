# shared.py

# Dict for sharing info between this Add-on's Operators
# and functions about imported objects.
# It's defined here to work as a global of sorts by
# importing it to the relevant modules (import_gr2.py
# and import_cha.py, so far).

job_results = {'job_origin'        : "",
               'objs_names'        : [],
               'files_objs_names'  : {},
               'anims_names'       : [],
              }


# The dict is also converted to .json and placed
# in a custom scene stringProperty:
#
# bpy.context.scene.io_scene_gr2_job_results
#
# before exiting this add-on's jobs so that other
# Add-ons can read it. It's the simplest way to
# share info, as Blender Operators don't return
# data other than success or failure.

# NEVER RESET IT WITH A job_results = {}
# That would create a new var with too local a scope.
# Clear specific keys:values instead.

# Info stored so far:

# 'job_origin': <operator's bl_idname>

# 'objs_names': [<list of resulting Blender object names>]
#
# If it's a job done by import_jba.py:
# 'anim_names': [<imported animation's Blender name>]
#
# (As many SWTOR .gr2 object files hold multiple
# meshes and Blender only supports single mesh objects,
# it is possible to obtain multiple objects from a single
# .gr2 file import. In such cases, we assume that, for single
# .gr2 file import calls, the first object in the list is
# the main one.
#
# Also, as we have to deal with Blender's anti-name collisions
# .xxx suffixes system (.001, .002, etc.), we store those
# actual bpy.data.objects names instead of the original names
# to spare others the confusion)

# If the Add-on's operators set the job_results_rich parameter
# to True, 'files_objs_names' is filled with:

# 'files_objs_names': {
#       <filepath a>: [<list of resulting Blender object names>]
#       <filepath b>: [<list of resulting Blender object names>]
#       etc.
#       }
# 
# - filepaths are normalized to Unix-style forward slashes.
# - If the files belong to an assets extraction's 'resources' folder,
#   their paths start at its 'art' subdirectory, without an initial
#   forward slash. SWTOR's internal conventions regarding paths are
#   such a horror show that we might as well follow Python's.