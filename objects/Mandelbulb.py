import mathutils
import math
import utils.marching_cubes

class Mandelbulb:

    def __init__(self, grid_size, max_iterations=1, degree=8):
        self.__grid_size = grid_size
        self.__max_iterations = max_iterations
        self.__degree = degree

        self.__vertices = []

    def generate_mesh(self):
        faces = []
        for i in range(0, self.__grid_size):
            for j in range(0, self.__grid_size):
                for k in range(0, self.__grid_size):
                    vertices = [
                        mathutils.Vector((i, j, k + 1)),
                        mathutils.Vector((i + 1, j, k + 1)),
                        mathutils.Vector((i + 1, j, k)),
                        mathutils.Vector((i, j, k)),
                        mathutils.Vector((i, j + 1, k + 1)),
                        mathutils.Vector((i + 1, j + 1, k + 1)),
                        mathutils.Vector((i + 1, j + 1, k)),
                        mathutils.Vector((i, j + 1, k)),
                    ]

                    values = []
                    for l in range(0, len(vertices)):
                        values.append(self.is_in_mandelbulb(vertices[l]))
                    cell = utils.marching_cubes.GridCell(vertices, values)
                    faces.extend(utils.marching_cubes.marching_cubes(cell, 1))

        print(f"End of mesh generation found {str(len(faces))} faces")

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

