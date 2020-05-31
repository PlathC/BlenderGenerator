import math
import mathutils

from mathutils import Vector
import bpy

import bmesh

class PlatonicSolid:

    def create_object(self, verts):
        scene = bpy.context.scene

        self.mesh = bpy.data.meshes.new("platon_mesh")  # add a new mesh
        obj = bpy.data.objects.new("platon", self.mesh)  # add a new object using the mesh

        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj  # set as the active object in the scene

        bpy.data.objects["platon"].select_set(True)

        self.mesh = bpy.context.object.data
        self.bm = bmesh.new()

        for vert in verts:
            self.bm.verts.new((vert.x, vert.y, vert.z))

        if hasattr(self.bm.verts, "ensure_lookup_table"):
            self.bm.verts.ensure_lookup_table()



    def finish_object(self):
        # Recalculate normal.
        self.bm.normal_update()

        # make the bmesh the object's mesh
        self.bm.to_mesh(self.mesh)
        self.bm.free()  # always do this when finished

    def tetraedre(self):
        print('Tetraedre')


        edgeLength = 1.

        # Base
        vert1 = mathutils.Vector((0., 0., 0.))
        vert2 = vert1 + mathutils.Vector((edgeLength, 0., 0.))
        vert3 = vert1 + mathutils.Vector((edgeLength, edgeLength, 0.))
        vert4 = vert1 + mathutils.Vector((0., edgeLength, 0.))

        vert5 = mathutils.Vector((edgeLength/2, edgeLength/2, math.sqrt(2/3) * edgeLength))
        vert6 = mathutils.Vector((edgeLength/2, edgeLength/2, -math.sqrt(2/3) * edgeLength))
        verts = [vert1, vert2, vert3, vert4, vert5, vert6]
        self.create_object(verts)

        # Base
        self.bm.faces.new((self.bm.verts[0], self.bm.verts[1], self.bm.verts[2]))
        self.bm.faces.new((self.bm.verts[2], self.bm.verts[3], self.bm.verts[0]))
        for i in [4, 5]:
            self.bm.faces.new((self.bm.verts[0], self.bm.verts[1], self.bm.verts[i]))
            self.bm.faces.new((self.bm.verts[1], self.bm.verts[2], self.bm.verts[i]))
            self.bm.faces.new((self.bm.verts[2], self.bm.verts[3], self.bm.verts[i]))
            self.bm.faces.new((self.bm.verts[3], self.bm.verts[0], self.bm.verts[i]))

        self.finish_object()

    def hexaedre(self):

        self.create_object()
        edgeLength = 1.

        print('Hexaedre')

    def octaedre(self):
        print('Octaedre')

    def dodecaedre(self):
        center = [0., 0., 0.]
        edge_length = 2
        half_edges = edge_length/2
        local_pi = math.acos(-1.0)
        cos_1_5 = math.cos(local_pi / 5)
        sin_1_5 = math.sin(local_pi / 5)
        cos_1_10 = math.cos(local_pi / 10)
        sin_1_10 = math.sin(local_pi / 10)
        cos_3_10 = math.cos((local_pi * 3) / 10)
        sin_3_10 = math.sin((local_pi * 3) / 10)
        cos_2_5 = math.cos((local_pi * 2) / 5)

        radius = edge_length / 2 / cos_3_10
        radius_diff = edge_length * cos_2_5 / cos_3_10

        rise = math.sqrt(edge_length * edge_length - radius_diff * radius_diff)

        radius_ratio = (radius_diff + radius) / radius
        a = radius * radius - edge_length * edge_length / 4
        a = math.sqrt(a)
        a = radius * radius_ratio - a

        b = edge_length * (cos_1_10 + cos_3_10)
        half_height = math.sqrt(b * b - a * a)
        little_height = (half_height - rise) / 2
        half_height = little_height + rise

        vertex1 = (0.0 + center[0], radius + center[1], -half_height + center[2])
        vertex2 = (radius * cos_1_10 + center[0], radius * sin_1_10 + center[1], -half_height + center[2])
        vertex3 = (radius * cos_3_10 + center[0], -radius * sin_3_10 + center[1], -half_height + center[2])
        vertex4 = (-radis * cos_3_10 + center[0], -radius * sin_3_10 + center[1], -half_height + center[2])
        vertex5 = (-radius * cos_1_10 + center[0], radius * sin_1_10 + center[1], -half_height + center[2])

        vertexes = [vertex1, vertex2, vertex3, vertex4, vertex5]

        for i in range(5, 10):
            x = (vertexes[i-5][0] - center[0]) * radius_ratio + center[0]
            y = (vertexes[i-5][1] - center[1]) * radius_ratio + center[1]
            z = -little_height + center[2]
            vertexes.append([x, y, z])

        for i in range(10, 15):
            x = (vertexes[i-5][0] - center[0]) * cos_1_5 - (vertexes[i - 5][1] - center[1]) * sin_1_5 + center[0]
            y = (vertexes[i-5][0] - center[0]) * sin_1_5 + (vertexes[i - 5][1] - center[1]) * cos_1_5 + center[1]
            vertexes.append([x, y, little_height + center[2]])

        for i in range(15, 20):
            x = (vertexes[i-15][0] - center[0]) * cos_1_5 - (vertexes[i - 15][1] - center[1]) * sin_1_5 + center[0]
            y = (vertexes[i-15][0] - center[0]) * sin_1_5 + (vertexes[i - 15][1] - center[1]) * cos_1_5 + center[1]
            vertexes.append([x, y, half_height + center[2]])

    def icosaedre(self):
        print('Icosaedre')


    def __init__(self):
        self.__location = (0.0, 0.0, 0.0)
        self.tetraedre()
        self.bm = None
        self.mesh = None