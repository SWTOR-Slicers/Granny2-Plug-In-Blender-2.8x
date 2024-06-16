# shared.py

job_results = {'job_origin'        : "",
               'objs_names'        : [],
               'files_objs_names' : {},}

# Dict for collecting info about imported objects that
# the add-on's operators and functions can read and use.
# It's defined here to work as a global of sorts by
# importing it to the relevant modules (import_gr2.py
# and import_cha.py, so far).

# The dict is converted to .json and placed in
# bpy.types.Scene.io_scene_gr2_job_results
# before exiting this add-on so that others
# can read it. It's the simplest way to share
# info, as Blender Operators don't return data
# other than success or failure.

# NEVER RESET IT WITH A job_results = {}
# That would create a new var with new scope.
# Reset specific keys:values instead.

# Info stored so far:

# 'job_origin': <operator's bl_idname>

# 'obj_list': [<list of resulting Blender object names>]
#
# As many SWTOR .gr2 object files hold multiple
# meshes and Blender only supports single mesh objects,
# it is possible to obtain multiple objects from a single
# .gr2 file import. In such cases, we assume that, for single
# .gr2 file import calls, the first object in the list is
# the main one.
#
# Also, as we have to deal with Blender's anti-name collisions
# .xxx suffixes system (.001, .002, etc.), we store those
# names instead of the original names to avoid confusion.

# If the Add-on's operators set the job_results_rich parameter
# to True, 'files_and_folders' is filled with:
#
# 'files_and_objects': {
#       <filepath a>: [<list of resulting Blender object names>]
#       <filepath b>: [<list of resulting Blender object names>]
#       etc.
#       }
# 
# - filepaths are normalized to Unix-style forward slashes.
# - If the files belong to an assets extraction's 'resources' folder,
#   their paths start at its 'art' subdirectory.