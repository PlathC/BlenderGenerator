import bpy
import bmesh

# import objects.Materials
from BlenderGenerator.objects import Materials


def Map():
    bpy.ops.mesh.primitive_plane_add(2, enter_editmode=True)
    obj = bpy.context.object
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.subdivide(number_cuts=100)
    bpy.ops.object.mode_set(mode="OBJECT")

    Materials.NoiseMap().apply_material(obj)
