import importlib
import utils.BlenderUtils
import utils.marching_cubes
import objects.Torus
import objects.IsoSurfaceGenerator
import scenes.torus
import scenes.isosurface
import scenes.tree
import scenes.Map
import objects.Materials
import objects.Tree
import faulthandler


def reload_modules_main():
    importlib.reload(utils.BlenderUtils)
    importlib.reload(utils.marching_cubes)
    importlib.reload(objects.Torus)
    importlib.reload(objects.IsoSurfaceGenerator)
    importlib.reload(objects.Materials)
    importlib.reload(objects.Tree)
    importlib.reload(scenes.torus)
    importlib.reload(scenes.isosurface)
    importlib.reload(scenes.tree)
    importlib.reload(scenes.Map)


def main():
    reload_modules_main()
    faulthandler.enable()
    scenes.Map.Map()
    faulthandler.dump_traceback()
