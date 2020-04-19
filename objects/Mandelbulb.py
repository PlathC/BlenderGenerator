import mathutils
import math
import utils.marching_cubes
import numpy


class Mandelbulb:

    def __init__(self, grid_size=1.8, step_size=0.1, max_iterations=1, degree=8):
        self.__grid_size = grid_size
        self.__step_size = step_size
        self.__max_iterations = max_iterations
        self.__degree = degree

        self.__vertices = []
        self.__faces = []

    def generate_mesh(self):
        self.__faces = []
        for i in numpy.arange(-(self.__grid_size / 2) - self.__step_size, (self.__grid_size / 2) + self.__step_size, self.__step_size):
            for j in numpy.arange(-(self.__grid_size / 2) - self.__step_size, (self.__grid_size / 2) + self.__step_size, self.__step_size):
                for k in numpy.arange(-(self.__grid_size / 2) - self.__step_size, (self.__grid_size / 2) + self.__step_size, self.__step_size):
                    vertices = [
                        mathutils.Vector((i, j, k + self.__step_size)),
                        mathutils.Vector((i + self.__step_size, j, k + self.__step_size)),
                        mathutils.Vector((i + self.__step_size, j, k)),
                        mathutils.Vector((i, j, k)),
                        mathutils.Vector((i, j + self.__step_size, k + self.__step_size)),
                        mathutils.Vector((i + self.__step_size, j + self.__step_size, k + self.__step_size)),
                        mathutils.Vector((i + self.__step_size, j + self.__step_size, k)),
                        mathutils.Vector((i, j + self.__step_size, k)),
                    ]

                    values = []
                    for l in range(0, len(vertices)):
                        values.append(math.sqrt(vertices[l].x * vertices[l].x +
                                                vertices[l].y * vertices[l].y +
                                                vertices[l].z * vertices[l].z)
                                      - 1)
                    cell = utils.marching_cubes.GridCell(vertices, values)
                    self.__faces.extend(utils.marching_cubes.marching_cubes(cell, 0))

        print(f"End of mesh generation found {str(len(self.__faces))} faces")

    def is_in_mandelbulb(self, point):
        """

        :param point: The point we want to test
        :return: 0 if the point is in the Mandelbulb set
        """
        c = point
        for ite in range(0, self.__max_iterations):
            r = math.sqrt(c.x * c.x + c.y * c.y + c.z * c.z)
            theta = math.atan2(math.sqrt(c.x * c.x + c.y * c.y), c.z)
            phi = math.atan2(c.y, c.x)
            p = r ** self.__degree
            nv = mathutils.Vector((
                p * math.sin(theta * self.__degree) * math.cos(phi * self.__degree),
                p * math.sin(theta * self.__degree) * math.sin(phi * self.__degree),
                p * math.cos(theta * self.__degree)
            ))
            c = mathutils.Vector((nv.x + c.x, nv.y + c.y, nv.z + c.z))
            result = math.sqrt(c.x * c.x + c.y * c.y + c.z * c.z)
            if result > 1:
                return 1

        return 0

    def vertices(self):
        return self.__vertices

    def faces(self):
        return self.__faces
