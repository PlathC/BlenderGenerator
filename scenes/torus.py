import bpy
import bmesh
"""
import utils.BlenderUtils
from objects.Torus import Torus
import objects.Materials
"""

from BlenderGenerator.utils import BlenderUtils
from BlenderGenerator.objects.Torus import Torus
from BlenderGenerator.objects import Materials

def torus():
    mesh = bpy.data.meshes.new("torus_mesh")  # add a new mesh
    obj = bpy.data.objects.new("torus", mesh)  # add a new object using the mesh

    scene = bpy.context.scene

    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene

    bpy.data.objects["torus"].select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    t = Torus()

    vertices = t.vertices()
    for v in vertices:
        bm.verts.new((v.x, v.y, v.z))  # add a new vert

    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.verts.ensure_lookup_table()

    indices = t.triangles()
    for i in range(0, len(indices), 3):

        v1 = bm.verts[indices[i]]
        v2 = bm.verts[indices[i+1]]
        v3 = bm.verts[indices[i+2]]

        bm.faces.new((v1, v2, v3))

    # Recalculate normal.
    bm.normal_update()

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished
    values = [True] * len(mesh.polygons)
    mesh.polygons.foreach_set("use_smooth", values)

    Materials.SmoothColor((0., 0., 0., 0.)).apply_material(obj)
    bpy.data.objects['Camera'].location = [0, 0, 10]
    BlenderUtils.update_camera(bpy.data.objects['Camera'],
                                     focus_point=obj.location,
                                     distance=11.53)

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1920
