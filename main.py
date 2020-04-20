import importlib
import utils.Vec3
import utils.BlenderUtils
import utils.marching_cubes
import objects.Torus
import objects.IsoSurfaceGenerator
import scenes.torus
import scenes.plain_map
import scenes.isosurface


def reload_modules_main():
    importlib.reload(utils.Vec3)
    importlib.reload(utils.BlenderUtils)
    importlib.reload(utils.marching_cubes)
    importlib.reload(objects.Torus)
    importlib.reload(objects.IsoSurfaceGenerator)
    importlib.reload(scenes.plain_map)
    importlib.reload(scenes.torus)
    importlib.reload(scenes.isosurface)


def main():
    reload_modules_main()
    scenes.isosurface.isosurface()
