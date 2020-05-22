import math
import mathutils

from mathutils import Vector

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