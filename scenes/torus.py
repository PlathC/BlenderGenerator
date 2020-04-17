import bpy
import bmesh
import utils.BlenderUtils
from objects.Torus import Torus


def apply_torus_material(obj):
    """
    Apply torus material to argument object.
    :param obj: The object we want to apply the torus material
    """

    mat = bpy.data.materials.new(name="TorusMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    bsdf.inputs["Base Color"].default_value = (0., 0., 0., 0.)

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

    apply_torus_material(obj)
    bpy.data.objects['Camera'].location = [0, 0, 10]
    utils.BlenderUtils.update_camera(bpy.data.objects['Camera'],
                                     focus_point=obj.location,
                                     distance=11.53)

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1920
