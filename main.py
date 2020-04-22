import importlib
import utils.BlenderUtils
import utils.marching_cubes
import objects.Torus
import objects.IsoSurfaceGenerator
import scenes.torus
import scenes.isosurface
import objects.Materials


def reload_modules_main():
    importlib.reload(utils.BlenderUtils)
    importlib.reload(utils.marching_cubes)
    importlib.reload(objects.Torus)
    importlib.reload(objects.IsoSurfaceGenerator)
    importlib.reload(objects.Materials)
    importlib.reload(scenes.torus)
    importlib.reload(scenes.isosurface)


def main():
    reload_modules_main()
    scenes.isosurface.isosurface()
