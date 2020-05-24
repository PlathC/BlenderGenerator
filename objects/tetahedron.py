import math
import mathutils

from mathutils import Vector
import bpy

import bmesh


class Tetrahedron3:
    # Define the four points of the triangle
    def calculate_vertices(self):
        """
        calculate vertices of the tetrahedron cell
        Coordinates of a single tetrahedron cell are multiplied by scale
        """
        scale = self.__scale
        array = [
            (0 * scale, -1 / math.sqrt(3) * scale, 0 * scale),
            (0.5 * scale, 1 / (2 * math.sqrt(3)) * scale, 0 * scale),
            (-0.5 * scale, 1 / (2 * math.sqrt(3)) * scale, 0 * scale),
            (0 * scale, 0 * scale, math.sqrt(2 / 3) * scale)
        ]
        return array

    def get_midpoints(self):
        """
        get midpoints of the current tetradehron cell
        """

        midpoints = []
        vertices = self.calculate_vertices()

        for vertex in vertices:
            coordinate = (
                (vertex[0] * 0.5) + self.__location[0],
                (vertex[1] * 0.5) + self.__location[1],
                (vertex[2] * 0.5) + self.__location[2]
            )
            midpoints.append(coordinate)

        return midpoints

    def get_scale(self):
        return self.__scale

    def set_scale(self, scale):
        self.__scale = scale

    def set_location(self, location):
        self.__location = location

    def set_vertices(self, vertices):
        self.__vertices = vertices

    def get_vertices(self):
        res = []
        for vert in self.__vertices:
            res.append((vert[0] + self.__location[0], vert[1] + self.__location[1], vert[2] + self.__location[2]))
        return res

    def __init__(self, scale):
        self.__location = (0.0, 0.0, 0.0)
        self.__scale = scale
        self.__vertices = []

class Tetahedron:
    def __init__(self, depth=6, size=2):
        self.__depth = depth
        self.__size = size

        self.faces = []

    def build_mesh(self):
        first_triangle = [Vector((0, 0, 0)),
                          Vector((0, self.__size, 0)),
                          Vector((self.__size, self.__size/2., 0))]

        second_triangle = [Vector((self.__size / 3., self.__size / 2., self.__size)),
                           Vector((0, 0, 0)),
                           Vector((self.__size, self.__size / 2., 0))]

        third_triangle = [Vector((self.__size / 3., self.__size / 2., self.__size)),
                          Vector((0, self.__size, 0)),
                          Vector((self.__size, self.__size / 2., 0))]

        fourth_triangle = [Vector((self.__size / 3., self.__size / 2., self.__size)),
                           Vector((0, self.__size, 0)),
                           Vector((0, 0, 0))]

        self.depth_triangle(first_triangle,  self.__depth)
        self.depth_triangle(second_triangle, self.__depth)
        self.depth_triangle(third_triangle,  self.__depth)
        self.depth_triangle(fourth_triangle, self.__depth)


    def depth_triangle(self, triangle, depth):
        p1 = triangle[0]
        p2 = triangle[1]
        p3 = triangle[2]

        mid_point_v1_v2 = Vector(((p1.x + p2.x) / 2.,
                                  (p1.y + p2.y) / 2.,
                                  (p1.z + p2.z) / 2.))
        mid_point_v1_v3 = Vector(((p1.x + p3.x) / 2.,
                                  (p1.y + p3.y) / 2.,
                                  (p1.z + p3.z) / 2.))
        mid_point_v2_v3 = Vector(((p3.x + p2.x) / 2.,
                                  (p3.y + p2.y) / 2.,
                                  (p3.z + p2.z) / 2.))

        subtriangle1 = [p1, mid_point_v1_v2, mid_point_v1_v3]
        subtriangle2 = [p2, mid_point_v1_v2, mid_point_v2_v3]
        subtriangle3 = [p3, mid_point_v1_v3, mid_point_v2_v3]

        if depth == 0:
            self.faces.extend([subtriangle1, subtriangle2, subtriangle3])
        else:
            depth = depth - 1
            self.depth_triangle(subtriangle1, depth)
            self.depth_triangle(subtriangle2, depth)
            self.depth_triangle(subtriangle3, depth)

    def get_faces(self):
        return self.faces