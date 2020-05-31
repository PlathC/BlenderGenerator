import importlib
import utils.BlenderUtils
import utils.marching_cubes
import objects.Torus
import objects.tetahedron
import objects.IsoSurfaceGenerator
import scenes.torus
import scenes.tetahedron
import scenes.isosurface
import scenes.Map
import scenes.platonicSolid
import objects.Materials
import objects.PlatonicSolid
import faulthandler


def reload_modules_main():
    """
    Reload every module in Blender to record changes
    """
    importlib.reload(utils.BlenderUtils)
    importlib.reload(utils.marching_cubes)
    importlib.reload(objects.Torus)
    importlib.reload(objects.tetahedron)
    importlib.reload(objects.IsoSurfaceGenerator)
    importlib.reload(objects.Materials)
    importlib.reload(objects.PlatonicSolid)
    importlib.reload(scenes.torus)
    importlib.reload(scenes.tetahedron)
    importlib.reload(scenes.isosurface)
    importlib.reload(scenes.Map)
    importlib.reload(scenes.platonicSolid)


def main():
    """
    Main function of the script
    """
    reload_modules_main()
    scenes.platonicSolid.platonic_solid()



