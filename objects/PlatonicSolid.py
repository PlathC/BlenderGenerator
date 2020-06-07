import math
import mathutils

from mathutils import Vector
import bpy

import bmesh

from enum import Enum

class Shape(Enum):
    TETRAHEDRON = 1
    HEXAHEDRON = 2
    OCTAHEDRON = 3
    DODECAHEDRON = 4
    ICOSAHEDRON = 5


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

    def make_quad_mesh(self, a, b, c, d):
        """
        Make a quad mesh from 4 vertices
        :param a: the first vertex
        :param b: the second vertex
        :param c: the third vertex
        :param d: the fourth vertex
        """
        self.bm.faces.new((a, b, c))
        self.bm.faces.new((c, d, a))

    def make_penta_mesh(self, a, b, c, d, e):
        """
        Make a mesh from 5 vertices in a regular pentagon shape
        :param a: the first vertex
        :param b: the second vertex
        :param c: the third vertex
        :param d: the fourth vertex
        :param e: the fifth vertex
        """
        self.bm.faces.new((a, e, d))
        self.bm.faces.new((a, d, c))
        self.bm.faces.new((a, c, b))

    def octahedron(self):
        edgeLength = self.radius

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

    def hexahedron(self):
        """
        Make the hexahedron mesh (the cube)
        """

        self.create_object([])
        r = self.radius
        e = math.sqrt(2) * r
        he = e / 2

        bottom = []
        bottom.append(self.bm.verts.new((-he, -he, 0)))
        bottom.append(self.bm.verts.new((he, -he, 0)))
        bottom.append(self.bm.verts.new((he, he, 0)))
        bottom.append(self.bm.verts.new((-he, he, 0)))

        top = []
        top.append(self.bm.verts.new((-he, -he, e)))
        top.append(self.bm.verts.new((he, -he, e)))
        top.append(self.bm.verts.new((he, he, e)))
        top.append(self.bm.verts.new((-he, he, e)))

        self.make_quad_mesh(bottom[3], bottom[2], bottom[1], bottom[0])
        self.make_quad_mesh(top[3], top[2], top[1], top[0])

        self.make_quad_mesh(bottom[0], bottom[1], top[1], top[0])
        self.make_quad_mesh(bottom[1], bottom[2], top[2], top[1])
        self.make_quad_mesh(bottom[2], bottom[3], top[3], top[2])
        self.make_quad_mesh(bottom[3], bottom[0], top[0], top[3])

        self.finish_object()

    def tetrahedron(self):

        self.create_object([])

        r = self.radius
        angle = 2 * math.pi / 3
        h = math.sqrt(2) * r


        sides = []
        for i in range(0, 3):
            x = r * math.cos(i * angle)
            y = r * math.sin(i * angle)
            sides.append(self.bm.verts.new((x, y, 0)))

        peak = self.bm.verts.new((0, 0, h))

        self.bm.faces.new((sides[0], sides[2], sides[1]))
        self.bm.faces.new((sides[0], sides[1], peak))
        self.bm.faces.new((sides[1], sides[2], peak))
        self.bm.faces.new((sides[2], sides[0], peak))

        self.finish_object()

    def dodecahedron(self):

        self.create_object([])

        r = self.radius
        m = 1 / math.sqrt(3) * r
        phi = (1 + math.sqrt(5)) / 2 # the golden ratio

        r1 = 1 * m
        phi1 = phi * m
        iphi1 = (1. / phi) * m

        cube_bot = []
        cube_bot.append([-r1, -r1, -r1])
        cube_bot.append([r1, -r1, -r1])
        cube_bot.append([r1, r1, -r1])
        cube_bot.append([-r1, r1, -r1])
        cube_bot_v = []
        for v in cube_bot:
            cube_bot_v.append(self.bm.verts.new((v[0], v[1], v[2])))

        cube_top = []
        cube_top.append([-r1, -r1, r1])
        cube_top.append([r1, -r1, r1])
        cube_top.append([r1, r1, r1])
        cube_top.append([-r1, r1, r1])
        cube_top_v = []
        for v in cube_top:
            cube_top_v.append(self.bm.verts.new((v[0], v[1], v[2])))


        x_rect = []
        x_rect.append([0, -iphi1, -phi1])
        x_rect.append([0, -iphi1, phi1])
        x_rect.append([0, iphi1, phi1])
        x_rect.append([0, iphi1, -phi1])
        x_rect_v = []
        for v in x_rect:
            x_rect_v.append(self.bm.verts.new((v[0], v[1], v[2])))


        z_rect = []
        z_rect.append([-iphi1, -phi1, 0])
        z_rect.append([iphi1, -phi1, 0])
        z_rect.append([iphi1, phi1, 0])
        z_rect.append([-iphi1, phi1, 0])
        z_rect_v = []
        for v in z_rect:
            z_rect_v.append(self.bm.verts.new((v[0], v[1], v[2])))


        y_rect = []
        y_rect.append([-phi1, 0, -iphi1])
        y_rect.append([phi1, 0, -iphi1])
        y_rect.append([phi1, 0, iphi1])
        y_rect.append([-phi1, 0, iphi1])
        y_rect_v = []
        for v in y_rect:
            y_rect_v.append(self.bm.verts.new((v[0], v[1], v[2])))

        self.make_penta_mesh(cube_top_v[0], x_rect_v[1], cube_top_v[1], z_rect_v[1], z_rect_v[0])
        self.make_penta_mesh(cube_top_v[2], x_rect_v[2], cube_top_v[3], z_rect_v[3], z_rect_v[2])

        self.make_penta_mesh(cube_bot_v[1], x_rect_v[0], cube_bot_v[0], z_rect_v[0], z_rect_v[1])
        self.make_penta_mesh(cube_bot_v[3], x_rect_v[3], cube_bot_v[2], z_rect_v[2], z_rect_v[3])

        self.make_penta_mesh(x_rect_v[0], x_rect_v[3], cube_bot_v[3], y_rect_v[0], cube_bot_v[0])
        self.make_penta_mesh(x_rect_v[3], x_rect_v[0], cube_bot_v[1], y_rect_v[1], cube_bot_v[2])

        self.make_penta_mesh(x_rect_v[2], x_rect_v[1], cube_top_v[0], y_rect_v[3], cube_top_v[3])
        self.make_penta_mesh(x_rect_v[1], x_rect_v[2], cube_top_v[2], y_rect_v[2], cube_top_v[1])

        self.make_penta_mesh(cube_top_v[2], z_rect_v[2], cube_bot_v[2], y_rect_v[1], y_rect_v[2])
        self.make_penta_mesh(cube_bot_v[1], z_rect_v[1], cube_top_v[1], y_rect_v[2], y_rect_v[1])

        self.make_penta_mesh(cube_bot_v[3], z_rect_v[3], cube_top_v[3], y_rect_v[3], y_rect_v[0])
        self.make_penta_mesh(cube_top_v[0], z_rect_v[0], cube_bot_v[0], y_rect_v[0], y_rect_v[3])

        self.finish_object()

    def icosahedron(self):
        print('icosahedron')

    def __init__(self, radius, type):
        self.__location = (0.0, 0.0, 0.0)
        self.radius = radius
        if type == Shape.TETRAHEDRON:
            self.tetrahedron()
        elif type == Shape.HEXAHEDRON:
            self.hexahedron()
        elif type == Shape.OCTAHEDRON:
            self.octahedron()
        elif type == Shape.DODECAHEDRON:
            self.dodecahedron()
        elif type == Shape.ICOSAHEDRON:
            self.icosahedron()

        self.bm = None
        self.mesh = None


