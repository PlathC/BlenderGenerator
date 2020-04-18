import runpy
import bpy
import sys, os
import importlib

#sys.path.remove("D:\\Projets\\Blender\\")
#sys.path.remove("D:\\Projets\\Blender\\BlenderGenerator\\")
paths = ["D:\\Projets\\Blender\\", "D:\\Projets\\Blender\\BlenderGenerator\\"]
for path in paths:
    if path not in sys.path:
        sys.path.append(path)

import BlenderGenerator.main
importlib.reload(BlenderGenerator.main)

#runpy.run_module('BlenderGenerator')
BlenderGenerator.main.main()
