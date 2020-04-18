import importlib
import utils.Vec3
import utils.BlenderUtils
import objects.Torus
import scenes.torus
import scenes.plain_map


def reload_modules_main():
    importlib.reload(utils.Vec3)
    importlib.reload(utils.BlenderUtils)
    importlib.reload(objects.Torus)
    importlib.reload(scenes.plain_map)
    importlib.reload(scenes.torus)


def main():
    reload_modules_main()
    scenes.torus.torus()
