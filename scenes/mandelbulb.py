import bpy
import bmesh
import utils.BlenderUtils
from objects.Mandelbulb import Mandelbulb


def mandelbulb():
    mesh = bpy.data.meshes.new("mandelbulb_mesh")  # add a new mesh
    obj = bpy.data.objects.new("mandelbulb", mesh)  # add a new object using the mesh

    scene = bpy.context.scene

    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene

    bpy.data.objects["mandelbulb"].select_set(True)
    mesh = bpy.context.object.data
    bm = bmesh.new()

    m = Mandelbulb()
    m.generate_mesh()
    # vertices = m.vertices()
    # for v in vertices:
    #     bm.verts.new((v.x, v.y, v.z))  # add a new vert

    # if hasattr(bm.verts, "ensure_lookup_table"):
    #     bm.verts.ensure_lookup_table()

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished
