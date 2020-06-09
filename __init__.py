import importlib

from BlenderGenerator.utils import BlenderUtils
from BlenderGenerator.utils import marching_cubes
from BlenderGenerator.objects import Torus
from BlenderGenerator.objects import tetahedron
from BlenderGenerator.objects import IsoSurfaceGenerator

from BlenderGenerator.scenes import torus

from BlenderGenerator.scenes import tetahedron
from BlenderGenerator.scenes import isosurface
from BlenderGenerator.scenes import Map
from BlenderGenerator.scenes import platonicSolid

from BlenderGenerator.objects import Materials

from BlenderGenerator.objects.IsoSurfaceGenerator import *

from BlenderGenerator.objects import PlatonicSolid

import faulthandler
import bpy

bl_info = {
    "name": "IN55 Project",
    "location": "",
    "description": "IN55 Project",
    "author": "Cyprien Plateau--Holleville and Nicolas Lepy",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Add Mesh",
}


class OBJECT_OT_mandelbox(bpy.types.Operator):
    """
    Create mandelbox fractal menu entry
    """
    bl_idname = 'object.mandelbox'
    bl_label = 'Mandelbox'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(Mandelbox())
        return {'FINISHED'}

class OBJECT_OT_moebius(bpy.types.Operator):
    """
    Create moebius fractal menu entry
    """

    bl_idname = 'object.moebius'
    bl_label = 'Moebius'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(Moebius())
        return {'FINISHED'}

class OBJECT_OT_revolution(bpy.types.Operator):
    """
    Create revolution surface fractal menu entry
    """

    bl_idname = 'object.revolution'
    bl_label = 'Revolution Surface'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(RevolutionSurface())
        return {'FINISHED'}

class OBJECT_OT_genus(bpy.types.Operator):
    """
    Create genus fractal menu entry
    """

    bl_idname = 'object.genus'
    bl_label = 'Genus'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(Genus2())
        return {'FINISHED'}

class OBJECT_OT_torus(bpy.types.Operator):
    """
    Create torus fractal menu entry
    """

    bl_idname = 'object.torus'
    bl_label = 'Torus'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(Torus())
        return {'FINISHED'}

class OBJECT_OT_sphere(bpy.types.Operator):
    """
    Create sphere fractal menu entry
    """

    bl_idname = 'object.fractalsphere'
    bl_label = 'Sphere'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(Sphere())
        return {'FINISHED'}

class OBJECT_OT_mandelbulb(bpy.types.Operator):
    """
    Create mandelbulb fractal menu entry
    """

    bl_idname = 'object.mandelbulb'
    bl_label = 'Mandelbulb'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(Mandelbulb())
        return {'FINISHED'}

class OBJECT_OT_mengersponge(bpy.types.Operator):
    """
    Create mengersponge fractal menu entry
    """

    bl_idname = 'object.mengersponge'
    bl_label = 'Menger Sponge'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(MengerSponge())
        return {'FINISHED'}

class OBJECT_OT_heart(bpy.types.Operator):
    """
    Create heart fractal menu entry
    """

    bl_idname = 'object.heart'
    bl_label = 'Heart'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(Heart())
        return {'FINISHED'}


class OBJECT_OT_simplenoiseterrain(bpy.types.Operator):
    """
    Create simple noise terrain menu entry
    """

    bl_idname = 'object.simplenoiseterrain'
    bl_label = 'Simple Noise Terrain'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(SimpleNoiseTerrain())
        return {'FINISHED'}

class OBJECT_OT_planet(bpy.types.Operator):
    """
    Create planet menu entry
    """

    bl_idname = 'object.planet'
    bl_label = 'Planet'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.isosurface.isosurface(Planet())
        return {'FINISHED'}


class OBJECT_MT_fractals(bpy.types.Menu):
    """
    Create fractal menu entry
    """

    bl_idname = 'object.fractals'
    bl_label = 'Marching cube / Fractals'

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_genus.bl_idname)
        layout.operator(OBJECT_OT_heart.bl_idname)
        layout.operator(OBJECT_OT_mandelbox.bl_idname)
        layout.operator(OBJECT_OT_mandelbulb.bl_idname)
        layout.operator(OBJECT_OT_mengersponge.bl_idname)
        layout.operator(OBJECT_OT_moebius.bl_idname)
        layout.operator(OBJECT_OT_planet.bl_idname)
        layout.operator(OBJECT_OT_simplenoiseterrain.bl_idname)
        layout.operator(OBJECT_OT_sphere.bl_idname)
        layout.operator(OBJECT_OT_torus.bl_idname)
        layout.operator(OBJECT_OT_revolution.bl_idname)

class add_torus(bpy.types.Operator):
    """
    Create torus menu entry
    """

    bl_idname = "mesh.torus"
    bl_label = "Torus"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.torus.torus()
        return {'FINISHED'}



class add_platonic_solids(bpy.types.Operator):
    """
    Create platonic solids menu entry
    """

    bl_idname = "mesh.platonic_solids"
    bl_label = "Platonic Solids"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.platonicSolid.platonic_solid()
        return {'FINISHED'}


class add_tetrahedron(bpy.types.Operator):
    """
    Create tetrahedron fractal menu entry
    """

    bl_idname = "mesh.tetrahedron"
    bl_label = "Tetrahedron"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scenes.tetahedron.fractal_tetrahedron(6)
        return {'FINISHED'}


def menu_func(self, context):
    """
    Add to context menu the three new entries
    """
    self.layout.operator(add_platonic_solids.bl_idname, icon='MOD_SUBSURF')
    self.layout.operator(add_tetrahedron.bl_idname, icon='MOD_SUBSURF')
    self.layout.operator(add_torus.bl_idname, icon='MOD_SUBSURF')
    self.layout.menu(OBJECT_MT_fractals.bl_idname)


def register():
    """
    Register components in Blender
    """

    reload_modules_main()
    """
    importlib.reload(locals()[utils])
    bpy.utils.register_class(utils.BlenderUtils)
    """
    bpy.utils.register_class(add_platonic_solids)
    bpy.utils.register_class(add_tetrahedron)
    bpy.utils.register_class(add_torus)

    bpy.utils.register_class(OBJECT_OT_mandelbox)
    bpy.utils.register_class(OBJECT_OT_revolution)
    bpy.utils.register_class(OBJECT_OT_moebius)
    bpy.utils.register_class(OBJECT_OT_genus)
    bpy.utils.register_class(OBJECT_OT_heart)
    bpy.utils.register_class(OBJECT_OT_mandelbulb)
    bpy.utils.register_class(OBJECT_OT_mengersponge)
    bpy.utils.register_class(OBJECT_OT_planet)
    bpy.utils.register_class(OBJECT_OT_simplenoiseterrain)
    bpy.utils.register_class(OBJECT_OT_torus)
    bpy.utils.register_class(OBJECT_OT_sphere)

    bpy.utils.register_class(OBJECT_MT_fractals)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    """
    Unregister components from Blender
    """

    bpy.utils.unregister_class(add_platonic_solids)
    bpy.utils.unregister_class(add_tetrahedron)
    bpy.utils.unregister_class(add_torus)

    bpy.utils.unregister_class(OBJECT_OT_mandelbox)
    bpy.utils.unregister_class(OBJECT_OT_revolution)
    bpy.utils.unregister_class(OBJECT_OT_moebius)
    bpy.utils.unregister_class(OBJECT_OT_genus)
    bpy.utils.unregister_class(OBJECT_OT_heart)
    bpy.utils.unregister_class(OBJECT_OT_mandelbulb)
    bpy.utils.unregister_class(OBJECT_OT_mengersponge)
    bpy.utils.unregister_class(OBJECT_OT_planet)
    bpy.utils.unregister_class(OBJECT_OT_simplenoiseterrain)
    bpy.utils.unregister_class(OBJECT_OT_torus)
    bpy.utils.unregister_class(OBJECT_OT_sphere)
    bpy.utils.unregister_class(OBJECT_MT_fractals)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)


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


if __name__ == "__main__":
    register()
