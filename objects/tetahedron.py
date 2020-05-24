import math
import mathutils

from mathutils import Vector
import bpy

import bmesh


class Tetrahedron3:

    def __init__(self, scale):
        self.__location = (0.0, 0.0, 0.0)
        self.__scale = scale
        self.__vertices = []

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
