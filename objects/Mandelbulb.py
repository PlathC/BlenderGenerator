import mathutils
import math
import utils.marching_cubes
import numpy


# https://www.fountainware.com/Funware/Mandelbrot3D/Mandelbrot3d.htm
class Mandelbulb:

    def __init__(self, grid_size=1.8, step_size=0.05, max_iterations=6, degree=8):
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
                        values.append(self.is_in_mandelbulb(vertices[l]))
                    cell = utils.marching_cubes.GridCell(vertices, values)
                    self.__faces.extend(utils.marching_cubes.marching_cubes(cell, 1))

        print(f"End of mesh generation found {str(len(self.__faces))} faces")

    def is_in_mandelbulb(self, point):
        """

        :param point: The point we want to test
        :return: a number <= 1 if the point is in the Mandelbulb set
        """
        c = point
        result = 0
        for ite in range(0, self.__max_iterations):
            r = c.length
            theta = math.atan2(math.sqrt(c.x * c.x + c.y * c.y), c.z)
            phi = math.atan2(c.y, c.x)
            p = math.pow(r, self.__degree)
            nv = mathutils.Vector((
                p * math.sin(theta * self.__degree) * math.cos(phi * self.__degree),
                p * math.sin(theta * self.__degree) * math.sin(phi * self.__degree),
                p * math.cos(theta * self.__degree)
            ))
            c = mathutils.Vector((nv.x + c.x, nv.y + c.y, nv.z + c.z))

            result = c.length
            if result > 1:
                return 1

        return result

    def vertices(self):
        return self.__vertices

    def faces(self):
        return self.__faces
