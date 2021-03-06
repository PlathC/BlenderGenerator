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

    def create_object(self):
        scene = bpy.context.scene

        self.mesh = bpy.data.meshes.new("platon_mesh")  # add a new mesh
        obj = bpy.data.objects.new("platon", self.mesh)  # add a new object using the mesh

        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj  # set as the active object in the scene

        bpy.data.objects["platon"].select_set(True)

        self.mesh = bpy.context.object.data
        self.bm = bmesh.new()

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
        """
        Make the octahedron
        :return:
        """
        self.create_object()

        edge_length = math.sqrt(2) * self.radius

        # the base of the octahedron is a square, so it will be composed of 4 vertices
        # the angle step between these four vertices will be 2pi / 4 = pi/2
        angle_step = math.pi / 2

        # Create the base of the object
        base = []
        for i in range(0, 4):
            x = self.radius * math.cos(angle_step * i)
            y = self.radius * math.sin(angle_step * i)
            base.append(self.bm.verts.new((x, y, 0)))

        # Create the peaks
        top = self.bm.verts.new((0, 0, self.radius))
        bottom = self.bm.verts.new((0, 0, -self.radius))

        # Link the four vertices of the base with top peak
        self.bm.faces.new((base[0], base[3], top))
        self.bm.faces.new((base[1], base[0], top))
        self.bm.faces.new((base[2], base[1], top))
        self.bm.faces.new((base[3], base[2], top))

        # Link the four vertices of the base with bottom peak
        self.bm.faces.new((base[3], base[0], bottom))
        self.bm.faces.new((base[0], base[1], bottom))
        self.bm.faces.new((base[1], base[2], bottom))
        self.bm.faces.new((base[2], base[3], bottom))

        self.finish_object()

    def hexahedron(self):
        """
        Make the hexahedron mesh (the cube)
        """

        self.create_object()
        edge_length = math.sqrt(2) * self.radius  # From radius, we can get edge length
        half_edge = edge_length / 2

        # Create bottom vertices (the 4 corners, with a z value = 0)
        bottom = []
        bottom.append(self.bm.verts.new((-half_edge, -half_edge, 0)))
        bottom.append(self.bm.verts.new((half_edge, -half_edge, 0)))
        bottom.append(self.bm.verts.new((half_edge, half_edge, 0)))
        bottom.append(self.bm.verts.new((-half_edge, half_edge, 0)))

        # Create top vertices (the 4 corners, with a z value = length of an edge)
        top = []
        top.append(self.bm.verts.new((-half_edge, -half_edge, edge_length)))
        top.append(self.bm.verts.new((half_edge, -half_edge, edge_length)))
        top.append(self.bm.verts.new((half_edge, half_edge, edge_length)))
        top.append(self.bm.verts.new((-half_edge, half_edge, edge_length)))

        # Create two quad mesh for the bottom and the top
        self.make_quad_mesh(bottom[3], bottom[2], bottom[1], bottom[0])
        self.make_quad_mesh(top[3], top[2], top[1], top[0])

        # Create mesh for the sides (between two bottom vertices and two top vertices)
        self.make_quad_mesh(bottom[0], bottom[1], top[1], top[0])
        self.make_quad_mesh(bottom[1], bottom[2], top[2], top[1])
        self.make_quad_mesh(bottom[2], bottom[3], top[3], top[2])
        self.make_quad_mesh(bottom[3], bottom[0], top[0], top[3])

        self.finish_object()

    def tetrahedron(self):
        """
        Make the tetrahedron
        """

        self.create_object()

        # we want the angle step for the vertices composing the tetrahedron
        # (2 * pi, a full circle, divided by 3 for the three vertices)
        angle = 2 * math.pi / 3

        # Determine the peak height
        h = math.sqrt(2) * self.radius

        # Create the three bottom vertices and every time the angle incremented with the step previously defined
        sides = []
        for i in range(0, 3):
            x = self.radius * math.cos(i * angle)
            y = self.radius * math.sin(i * angle)
            sides.append(self.bm.verts.new((x, y, 0)))

        # Create the peak
        peak = self.bm.verts.new((0, 0, h))

        # Create the faces of the mesh : the bottom triangle and the three triangles on the sides
        self.bm.faces.new((sides[0], sides[2], sides[1]))
        self.bm.faces.new((sides[0], sides[1], peak))
        self.bm.faces.new((sides[1], sides[2], peak))
        self.bm.faces.new((sides[2], sides[0], peak))

        self.finish_object()

    def dodecahedron(self):
        """
        Make the dodecahedron
        """

        self.create_object()

        m = 1 / math.sqrt(3) * self.radius
        phi = (1 + math.sqrt(5)) / 2  # the golden ratio

        r1 = 1 * m
        phi1 = phi * m
        iphi1 = (1. / phi) * m

        # Create the 20 vertices of the dodecahedron

        # Create a box to contain 8 vertices
        cube_bottom = []
        cube_bottom.append(self.bm.verts.new((-r1, -r1, -r1)))
        cube_bottom.append(self.bm.verts.new((r1, -r1, -r1)))
        cube_bottom.append(self.bm.verts.new((r1, r1, -r1)))
        cube_bottom.append(self.bm.verts.new((-r1, r1, -r1)))

        cube_top = []
        cube_top.append(self.bm.verts.new((-r1, -r1, r1)))
        cube_top.append(self.bm.verts.new((r1, -r1, r1)))
        cube_top.append(self.bm.verts.new((r1, r1, r1)))
        cube_top.append(self.bm.verts.new((-r1, r1, r1)))

        # Create three rectangles that contain the 12 other vertices

        # One perpendicular to x-axis of coordinates (0, +- 1/phi, +- phi)
        x_rect = []
        x_rect.append(self.bm.verts.new((0, -iphi1, -phi1)))
        x_rect.append(self.bm.verts.new((0, -iphi1, phi1)))
        x_rect.append(self.bm.verts.new((0, iphi1, phi1)))
        x_rect.append(self.bm.verts.new((0, iphi1, -phi1)))

        # One perpendicular to y-axis of coordinates (+- phi, +- 1/phi, 0)
        z_rect = []
        z_rect.append(self.bm.verts.new((-iphi1, -phi1, 0)))
        z_rect.append(self.bm.verts.new((iphi1, -phi1, 0)))
        z_rect.append(self.bm.verts.new((iphi1, phi1, 0)))
        z_rect.append(self.bm.verts.new((-iphi1, phi1, 0)))

        # One perpendicular to y-axis of coordinates (+- 1/phi, 0, +- phi)
        y_rect = []
        y_rect.append(self.bm.verts.new((-phi1, 0, -iphi1)))
        y_rect.append(self.bm.verts.new((phi1, 0, -iphi1)))
        y_rect.append(self.bm.verts.new((phi1, 0, iphi1)))
        y_rect.append(self.bm.verts.new((-phi1, 0, iphi1)))

        # Create the 12 pentagons of the dodecahedron from golden rectangles and box
        self.make_penta_mesh(cube_top[0], x_rect[1], cube_top[1], z_rect[1], z_rect[0])
        self.make_penta_mesh(cube_top[2], x_rect[2], cube_top[3], z_rect[3], z_rect[2])

        self.make_penta_mesh(cube_bottom[1], x_rect[0], cube_bottom[0], z_rect[0], z_rect[1])
        self.make_penta_mesh(cube_bottom[3], x_rect[3], cube_bottom[2], z_rect[2], z_rect[3])

        self.make_penta_mesh(x_rect[0], x_rect[3], cube_bottom[3], y_rect[0], cube_bottom[0])
        self.make_penta_mesh(x_rect[3], x_rect[0], cube_bottom[1], y_rect[1], cube_bottom[2])

        self.make_penta_mesh(x_rect[2], x_rect[1], cube_top[0], y_rect[3], cube_top[3])
        self.make_penta_mesh(x_rect[1], x_rect[2], cube_top[2], y_rect[2], cube_top[1])

        self.make_penta_mesh(cube_top[2], z_rect[2], cube_bottom[2], y_rect[1], y_rect[2])
        self.make_penta_mesh(cube_bottom[1], z_rect[1], cube_top[1], y_rect[2], y_rect[1])

        self.make_penta_mesh(cube_bottom[3], z_rect[3], cube_top[3], y_rect[3], y_rect[0])
        self.make_penta_mesh(cube_top[0], z_rect[0], cube_bottom[0], y_rect[0], y_rect[3])

        self.finish_object()

    def icosahedron(self):
        """
        Make the icosahedron
        :return:
        """
        self.create_object()

        m = 1 / math.sqrt(3) * self.radius
        phi = (1 + math.sqrt(5)) / 2  # golden ratio

        ephi = phi * m
        iphi = 1.5 * phi

        # Create three rectangles to contain the all vertices using golden ratio
        x_rectangle = []
        x_rectangle.append(self.bm.verts.new((0, -iphi, -ephi)))
        x_rectangle.append(self.bm.verts.new((0, -iphi, ephi)))
        x_rectangle.append(self.bm.verts.new((0, iphi, ephi)))
        x_rectangle.append(self.bm.verts.new((0, iphi, -ephi)))

        y_rectangle = []
        y_rectangle.append(self.bm.verts.new((-ephi, 0, -iphi)))
        y_rectangle.append(self.bm.verts.new((ephi, 0, -iphi)))
        y_rectangle.append(self.bm.verts.new((ephi, 0, iphi)))
        y_rectangle.append(self.bm.verts.new((-ephi, 0, iphi)))

        z_rectangle = []
        z_rectangle.append(self.bm.verts.new((-iphi, -ephi, 0)))
        z_rectangle.append(self.bm.verts.new((iphi, -ephi, 0)))
        z_rectangle.append(self.bm.verts.new((iphi, ephi, 0)))
        z_rectangle.append(self.bm.verts.new((-iphi, ephi, 0)))


        if hasattr(self.bm.verts, "ensure_lookup_table"):
            self.bm.verts.ensure_lookup_table()

        # Make the 20 faces between the 12 vertices

        x0 = self.bm.verts[0]
        x1 = self.bm.verts[1]
        x2 = self.bm.verts[2]
        x3 = self.bm.verts[3]
        y0 = self.bm.verts[4]
        y1 = self.bm.verts[5]
        y2 = self.bm.verts[6]
        y3 = self.bm.verts[7]
        z0 = self.bm.verts[8]
        z1 = self.bm.verts[9]
        z2 = self.bm.verts[10]
        z3 = self.bm.verts[11]

        self.bm.faces.new((x1, y2, z1))
        self.bm.faces.new((x1, z0, z1))
        self.bm.faces.new((x1, y3, z0))
        self.bm.faces.new((y1, y2, z1))
        self.bm.faces.new((y2, x2, x1))

        self.bm.faces.new((z1, x0, y1))
        self.bm.faces.new((z0, z1, x0))
        self.bm.faces.new((y2, z2, x2))
        self.bm.faces.new((y2, y1, z2))
        self.bm.faces.new((x1, x2, y3))

        self.bm.faces.new((z3, z2, x2))
        self.bm.faces.new((x2, y3, z3))
        self.bm.faces.new((y1, x0, x3))
        self.bm.faces.new((y1, x3, z2))
        self.bm.faces.new((z3, z2, x3))

        self.bm.faces.new((y0, y3, z3))
        self.bm.faces.new((z0, y3, y0))
        self.bm.faces.new((y0, x0, x3))
        self.bm.faces.new((x0, y0, z0))
        self.bm.faces.new((x3, y0, z3))

        self.finish_object()

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


