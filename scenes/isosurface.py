import bpy
import bmesh
import utils.BlenderUtils
from objects.IsoSurfaceGenerator import IsoSurfaceGenerator


def apply_fractal_material(obj):
    """
    Apply torus material to argument object.
    :param obj: The object we want to apply the torus material
    """

    mat = bpy.data.materials.new(name="FractalMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    bsdf.inputs["Base Color"].default_value = (0.142, 0.082, 0.073, 1.)
    bsdf.inputs["Subsurface"].default_value = 0.464
    bsdf.inputs["Subsurface Color"].default_value = (0.8, 0.18, 0.072, 1.)

    # Assign it to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    world_nodes = bpy.data.worlds["World"].node_tree
    color_value = world_nodes.nodes.new('ShaderNodeValue')
    color_value.outputs[0].default_value = 0.

    world_nodes.links.new(world_nodes.nodes["Background"].inputs['Color'], color_value.outputs[0])

    scn = bpy.context.scene
    if not scn.render.engine == 'CYCLES':
        scn.render.engine = 'CYCLES'


def isosurface():
    mesh = bpy.data.meshes.new("isosurface_mesh")  # add a new mesh
    obj = bpy.data.objects.new("isosurface", mesh)  # add a new object using the mesh

    scene = bpy.context.scene

    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene

    bpy.data.objects["isosurface"].select_set(True)
    mesh = bpy.context.object.data
    bm = bmesh.new()

    m = IsoSurfaceGenerator()
    m.generate_mesh()

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

    #bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.00001)
    bm.normal_update()

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished

    #values = [True] * len(mesh.polygons)
    #mesh.polygons.foreach_set("use_smooth", values)

    bpy.context.view_layer.objects.active = obj
    #bpy.ops.object.modifier_add(type='SUBSURF')

    apply_fractal_material(obj)

    bpy.data.objects['Camera'].location = [3, 0, 0]
    utils.BlenderUtils.update_camera(bpy.data.objects['Camera'],
                                     focus_point=obj.location,
                                     distance=5)
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1920
