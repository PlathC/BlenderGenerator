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

    faces = m.faces()
    faces_indices = []
    indices = 0
    for i in range(0, len(faces)):
        face_vertices = faces[i]

        bm.verts.new((face_vertices[0].x, face_vertices[0].y, face_vertices[0].z))
        bm.verts.new((face_vertices[1].x, face_vertices[1].y, face_vertices[1].z))
        bm.verts.new((face_vertices[2].x, face_vertices[2].y, face_vertices[2].z))
        indices += 3
        faces_indices.append([indices, indices-1, indices - 2])

    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.verts.ensure_lookup_table()

    for i in range(0, len(faces_indices)):
        v1 = bm.verts[faces_indices[i][0]-1]
        v2 = bm.verts[faces_indices[i][1]-1]
        v3 = bm.verts[faces_indices[i][2]-1]
        bm.faces.new((v1, v2, v3))

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished
