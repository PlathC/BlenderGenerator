import bpy
import bmesh
import utils.BlenderUtils
from objects.tetahedron import Tetrahedron3
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


def generate_iteration(objects, scale):
    new_objects = []

    for tetrahedron in objects:
        for point in tetrahedron.get_midpoints():
            temp = Tetrahedron3(scale)
            temp.set_scale(tetrahedron.get_scale() / 2)
            temp.set_location(point)
            temp.set_vertices(temp.calculate_vertices())

            new_objects.append(temp)

    return new_objects


def fractal_tetrahedron():
    scale = 4
    initial_tetrahedron = Tetrahedron3(scale)

    initial_tetrahedron.set_vertices(initial_tetrahedron.calculate_vertices())

    objects = [initial_tetrahedron]

    for i in range(0, 5):
        objects = generate_iteration(objects, scale)

    # Get all vertices of every tetrahedron cells
    vertices = []
    for obj in objects:
        obj_vertices = obj.get_vertices()
        for vert in obj_vertices:
            vertices.append(vert)

    mesh = bpy.data.meshes.new("teta_mesh")  # add a new mesh
    obj = bpy.data.objects.new("tetahedron", mesh)  # add a new object using the mesh

    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene

    bpy.data.objects["tetahedron"].select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    for v in vertices:
        bm.verts.new((v[0], v[1], v[2]))
    
    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.verts.ensure_lookup_table()

    # Create groups of 4 tetrahedron-cell to create every triangles of the full tetrahedron
    groups = int(len(vertices) / 4)
    for i in range(0, groups):
        v0 = bm.verts[4*i]
        v1 = bm.verts[4*i+1]
        v2 = bm.verts[4*i+2]
        v3 = bm.verts[4*i+3]
        bm.faces.new((v0, v1, v2))
        bm.faces.new((v0, v1, v3))
        bm.faces.new((v1, v2, v3))
        bm.faces.new((v2, v3, v0))

    # Recalculate normal.
    bm.normal_update()

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished
