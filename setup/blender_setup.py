# When bpy is already in local, we know this is not the initial import...
if "bpy" in locals():
    # ...so we need to reload our submodule(s) using importlib
    import importlib

    if "BlenderGenerator" in locals():
        importlib.reload(BlenderGenerator)

import bpy
import sys, os

print(sys.path)

path = "__PATH__"

if path not in sys.path:
    sys.path.append(path)

import BlenderGenerator
BlenderGenerator.main.main()