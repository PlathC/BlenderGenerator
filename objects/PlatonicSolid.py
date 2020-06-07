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

        r = self.radius
        edge_length = math.sqrt(2) * r

        # the base of the octahedron is a square, so it will be composed of 4 vertices
        # the angle step between these four vertices will be 2pi / 4 = pi/2
        angle_step = math.pi / 2

        # Create the base of the object
        base = []
        for i in range(0, 4):
            x = r * math.cos(angle_step * i)
            y = r * math.sin(angle_step * i)
            base.append(self.bm.verts.new((x, y, 0)))

        # Create the peaks
        top = self.bm.verts.new((0, 0, r))
        bottom = self.bm.verts.new((0, 0, -r))

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

    """
    def octahedron2(self):
        edgeLength = self.radius * math.sqrt(2)

        # Base
        vert1 = mathutils.Vector((0., 0., 0.))
        vert2 = vert1 + mathutils.Vector((edgeLength, 0., 0.))
        vert3 = vert1 + mathutils.Vector((edgeLength, edgeLength, 0.))
        vert4 = vert1 + mathutils.Vector((0., edgeLength, 0.))

        vert5 = mathutils.Vector((edgeLength/2, edgeLength/2, math.sqrt(2/3) * edgeLength))
        vert6 = mathutils.Vector((edgeLength/2, edgeLength/2, -math.sqrt(2/3) * edgeLength))
        verts = [vert1, vert2, vert3, vert4, vert5, vert6]
        self.create_object()

        # Base
        self.bm.faces.new((self.bm.verts[0], self.bm.verts[1], self.bm.verts[2]))
        self.bm.faces.new((self.bm.verts[2], self.bm.verts[3], self.bm.verts[0]))
        for i in [4, 5]:
            self.bm.faces.new((self.bm.verts[0], self.bm.verts[1], self.bm.verts[i]))
            self.bm.faces.new((self.bm.verts[1], self.bm.verts[2], self.bm.verts[i]))
            self.bm.faces.new((self.bm.verts[2], self.bm.verts[3], self.bm.verts[i]))
            self.bm.faces.new((self.bm.verts[3], self.bm.verts[0], self.bm.verts[i]))

        self.finish_object()
    """

    def hexahedron(self):
        """
        Make the hexahedron mesh (the cube)
        """

        self.create_object()
        r = self.radius
        edge_length = math.sqrt(2) * r  # From radius, we can get edge length
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

        r = self.radius
        # we want the angle step for the vertices composing the tetrahedron
        # (2 * pi, a full circle, divided by 3 for the three vertices)
        angle = 2 * math.pi / 3

        # Determine the peak height
        h = math.sqrt(2) * r

        # Create the three bottom vertices and every time the angle incremented with the step previously defined
        sides = []
        for i in range(0, 3):
            x = r * math.cos(i * angle)
            y = r * math.sin(i * angle)
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

        r = self.radius
        m = 1 / math.sqrt(3) * r
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

        # Create three golden rectangle that contain the 12 other vertices
        x_rect = []
        x_rect.append(self.bm.verts.new((0, -iphi1, -phi1)))
        x_rect.append(self.bm.verts.new((0, -iphi1, phi1)))
        x_rect.append(self.bm.verts.new((0, iphi1, phi1)))
        x_rect.append(self.bm.verts.new((0, iphi1, -phi1)))

        z_rect = []
        z_rect.append(self.bm.verts.new((-iphi1, -phi1, 0)))
        z_rect.append(self.bm.verts.new((iphi1, -phi1, 0)))
        z_rect.append(self.bm.verts.new((iphi1, phi1, 0)))
        z_rect.append(self.bm.verts.new((-iphi1, phi1, 0)))

        y_rect = []
        y_rect.append(self.bm.verts.new((-phi1, 0, -iphi1)))
        y_rect.append(self.bm.verts.new((phi1, 0, -iphi1)))
        y_rect.append(self.bm.verts.new((phi1, 0, iphi1)))
        y_rect.append(self.bm.verts.new((-phi1, 0, iphi1)))

        # Create the 12 pentagones of the dodecahedron from golden rectangles and box
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
        self.create_object()

        r = self.radius
        m = 1 / math.sqrt(3) * r
        phi = (1 + math.sqrt(5)) / 2  # golden ratio

        ephi = phi * m
        iphi = (1.0 / phi) * m

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


        """
        self.bm.faces.new((x_rectangle[0], x_rectangle[1], x_rectangle[2]))
        self.bm.faces.new((x_rectangle[2], x_rectangle[3], x_rectangle[0]))
        self.bm.faces.new((y_rectangle[0], y_rectangle[1], y_rectangle[2]))
        self.bm.faces.new((y_rectangle[2], y_rectangle[3], y_rectangle[0]))
        self.bm.faces.new((z_rectangle[0], z_rectangle[1], z_rectangle[2]))
        self.bm.faces.new((z_rectangle[2], z_rectangle[3], z_rectangle[0]))

        self.bm.faces.new((x_rectangle[1], x_rectangle[2], y_rectangle[2]))
        self.bm.faces.new((x_rectangle[1], y_rectangle[2], z_rectangle[1]))
        self.bm.faces.new((x_rectangle[1], z_rectangle[0], z_rectangle[1]))
        self.bm.faces.new((x_rectangle[1], z_rectangle[0], y_rectangle[3]))
        self.bm.faces.new((x_rectangle[1], x_rectangle[2], y_rectangle[3]))

        self.bm.faces.new((y_rectangle[2], y_rectangle[1], z_rectangle[1]))
        self.bm.faces.new((y_rectangle[2], x_rectangle[2], z_rectangle[2]))
        """

        """
        x = []
        x.append(self.bm.verts.new((0, 1, -phi)))
        x.append(self.bm.verts.new((0, 1, phi)))
        x.append(self.bm.verts.new((0, -1, -phi)))
        x.append(self.bm.verts.new((0, -1, phi)))

        y = []
        y.append(self.bm.verts.new((-phi, 0, 1)))
        y.append(self.bm.verts.new((phi, 0, 1)))
        y.append(self.bm.verts.new((-phi, 0, -1)))
        y.append(self.bm.verts.new((phi, 0, -1)))


        z = []
        z.append(self.bm.verts.new((1, phi, 0)))
        z.append(self.bm.verts.new((1, -phi, 0)))
        z.append(self.bm.verts.new((-1, phi, 0)))
        z.append(self.bm.verts.new((-1, -phi, 0)))

        self.bm.faces.new((x[0], x[1], x[2]))
        self.bm.faces.new((x[2], x[3], x[0]))
        self.bm.faces.new((y[0], y[1], y[2]))
        self.bm.faces.new((y[2], y[3], y[0]))
        self.bm.faces.new((z[0], z[1], z[2]))
        self.bm.faces.new((z[2], z[3], z[0]))
        """

        """
        r = self.radius / 2
        edge_length = r * math.sqrt(2)
        angle_step = 2 * math.pi / 5

        first_line = []
        second_line = []
        for i in range(0, 5):
            x = r * math.cos(i * angle_step)
            y = r * math.sin(i * angle_step)
            first_line.append(self.bm.verts.new((x, y, r)))
            x = -r * math.cos(i * angle_step + angle_step/2)
            y = -r * math.sin(i * angle_step + angle_step/2)
            second_line.append(self.bm.verts.new((x, y, -r)))

        top = self.bm.verts.new((0, 0, 2*r))
        bottom = self.bm.verts.new((0, 0, -2*r))

        self.bm.faces.new((first_line[0], first_line[1], top))
        self.bm.faces.new((first_line[1], first_line[2], top))
        self.bm.faces.new((first_line[2], first_line[3], top))
        self.bm.faces.new((first_line[3], first_line[4], top))
        self.bm.faces.new((first_line[4], first_line[0], top))

        self.bm.faces.new((second_line[0], second_line[1], bottom))
        self.bm.faces.new((second_line[1], second_line[2], bottom))
        self.bm.faces.new((second_line[2], second_line[3], bottom))
        self.bm.faces.new((second_line[3], second_line[4], bottom))
        self.bm.faces.new((second_line[4], second_line[0], bottom))
        """

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


