import bpy
import bmesh
import math
from utils.Vec3 import Vec3
import mathutils

class Torus:

    def __init__(self, origin=Vec3(), first_circle_diameter=2, second_circle_diameter=1.5, vertices_per_circles=80):
        self.vertices_dictionary = {}
        self.origin = origin
        self.fc_diameter = first_circle_diameter
        self.sc_diameter = second_circle_diameter
        self.vertices_per_circles = vertices_per_circles
        self.vertices_number = 0
        self.us = []
        self.vs = []

        self.mesh_vertices = []
        self.mesh_triangles = []
        self.mesh_uvs = []

        self.generate()

    def get_w(self, u):
        return Vec3(math.cos(u), math.sin(u), 0)

    def get_q(self, u, v):
        if u not in self.vertices_dictionary:
            self.vertices_dictionary[u] = {}

        self.vertices_dictionary[u][v] = self.vertices_number
        self.vertices_number += 1

        w = self.get_w(u)
        fc = Vec3(self.fc_diameter * w.x,
                  self.fc_diameter * w.y,
                  self.fc_diameter * w.z)

        cosv = math.cos(v)
        sc = Vec3(self.sc_diameter * w.x * cosv,
                  self.sc_diameter * w.y * cosv,
                  self.sc_diameter * w.z * cosv)
        ls = Vec3(0, 0, self.sc_diameter * math.sin(v))

        return self.origin + fc + sc + ls

    def generate(self):

        # Clear potential pre used data.
        self.us.clear()
        self.vs.clear()
        self.mesh_vertices.clear()
        self.mesh_triangles.clear()
        self.vertices_dictionary.clear()

        vs_complete = False
        self.vertices_number = 0

        angle_step = ((2. * math.pi) / self.vertices_per_circles)
        angle = 0.

        # vertices generation
        for i in range(0, self.vertices_per_circles):
            self.us.append(angle)
            second_angle = 0.
            for j in range(0, self.vertices_per_circles):
                if not vs_complete:
                    self.vs.append(second_angle)

                self.mesh_vertices.append(
                    self.get_q(angle, second_angle)
                )

                second_angle += angle_step

            vs_complete = True
            angle += angle_step

        for i in range(0, len(self.us)):
            for j in range(0, len(self.vs)):

                # First triangle
                # (u, v)
                self.mesh_triangles.append(
                    self.vertices_dictionary[self.us[i]][self.vs[j]]
                )

                # (u, v + 1)
                if j == len(self.vs) - 1:
                    self.mesh_triangles.append(
                        self.vertices_dictionary[self.us[i]][self.vs[0]]
                    )
                else:
                    self.mesh_triangles.append(
                        self.vertices_dictionary[self.us[i]][self.vs[j + 1]]
                    )

                # (u - 1, v)
                if i == 0:
                    self.mesh_triangles.append(
                        self.vertices_dictionary[self.us[len(self.us) - 1]][self.vs[j]]
                    )
                else:
                    self.mesh_triangles.append(
                        self.vertices_dictionary[self.us[i - 1]][self.vs[j]]
                    )

                # Second triangle
                # (u - 1, v)
                if i == 0:
                    self.mesh_triangles.append(
                        self.vertices_dictionary[self.us[len(self.us) - 1]][self.vs[j]]
                    )
                else:
                    self.mesh_triangles.append(
                        self.vertices_dictionary[self.us[i - 1]][self.vs[j]]
                    )

                # (u, v + 1)
                if j == len(self.vs) - 1:
                    self.mesh_triangles.append(
                        self.vertices_dictionary[self.us[i]][self.vs[0]]
                    )
                else:
                    self.mesh_triangles.append(
                        self.vertices_dictionary[self.us[i]][self.vs[j + 1]]
                    )

                # (u - 1, v + 1)
                u_value = 0
                v_value = 0
                if i == 0:
                    u_value = self.us[len(self.us) - 1]
                else:
                    u_value = self.us[i - 1]

                if j == len(self.vs) - 1:
                    v_value = self.vs[0]
                else:
                    v_value = self.vs[j + 1]

                self.mesh_triangles.append(
                    self.vertices_dictionary[u_value][v_value]
                )

        for i in range(0, len(self.mesh_vertices)):
            self.mesh_uvs.append((self.mesh_vertices[i].x, self.mesh_vertices[i].z))

    def vertices(self):
        return self.mesh_vertices

    def triangles(self):
        return self.mesh_triangles

    def uvs(self):
        return self.mesh_uvs


def apply_material(obj):
    """

    """
    scn = bpy.context.scene
    if not scn.render.engine == 'CYCLES':
        scn.render.engine = 'CYCLES'

    mat = bpy.data.materials.new(name="TorusMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    bsdf.inputs["Base Color"].default_value = (0., 0., 0., 0.)

    # Assign it to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    scn = bpy.context.scene
    if not scn.render.engine == 'CYCLES':
        scn.render.engine = 'CYCLES'


def update_camera(camera, focus_point=mathutils.Vector((0.0, 0.0, 0.0)), distance=10.0):
    """
    Focus the camera to a focus point and place the camera at a specific distance from that
    focus point. The camera stays in a direct line with the focus point.

    :param camera: the camera object
    :type camera: bpy.types.object
    :param focus_point: the point to focus on (default=``mathutils.Vector((0.0, 0.0, 0.0))``)
    :type focus_point: mathutils.Vector
    :param distance: the distance to keep to the focus point (default=``10.0``)
    :type distance: float
    """
    looking_direction = camera.location - focus_point
    rot_quat = looking_direction.to_track_quat('Z', 'Y')

    camera.rotation_euler = rot_quat.to_euler()
    camera.location = rot_quat @ mathutils.Vector((0.0, 0.0, distance))


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

    apply_material(obj)
    bpy.data.objects['Camera'].location = [0, 0, 10]
    update_camera(bpy.data.objects['Camera'],
                  focus_point=obj.location,
                  distance=11.53)

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1920
