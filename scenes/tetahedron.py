import bpy
import bmesh
import utils.BlenderUtils
from objects.tetahedron import Tetahedron
import objects.Materials


def tetahedron():
    mesh = bpy.data.meshes.new("tetahedron_mesh")  # add a new mesh
    obj = bpy.data.objects.new("tetahedron", mesh)  # add a new object using the mesh

    scene = bpy.context.scene

    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene

    bpy.data.objects["tetahedron"].select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    t = Tetahedron()
    t.build_mesh()
    faces = t.get_faces()

    for i in range(0, len(faces)):
        v1 = bm.verts.new(faces[i][0])  # add a new vert
        v2 = bm.verts.new(faces[i][1])  # add a new vert
        v3 = bm.verts.new(faces[i][2])  # add a new vert

        bm.faces.new((v1, v2, v3))

    # Recalculate normal.
    bm.normal_update()

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished
    values = [True] * len(mesh.polygons)

    objects.Materials.SmoothColor((0., 0., 0., 0.)).apply_material(obj)
    bpy.data.objects['Camera'].location = [0, 0, 10]
    utils.BlenderUtils.update_camera(bpy.data.objects['Camera'],
                                     focus_point=obj.location,
                                     distance=11.53)

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1920