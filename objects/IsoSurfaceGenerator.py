import mathutils
import math
import utils.marching_cubes
import numpy
from abc import ABC, abstractmethod


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class IsoSurface(ABC):
    @abstractmethod
    def isovalue(self):
        pass

    @abstractmethod
    def test_point(self, point):
        pass


class Heart(IsoSurface):
    def isovalue(self):
        return 0.

    def test_point(self, point):
        x = point.x
        y = point.y
        z = point.z
        cube = (x * x + 9./4. * y * y + z * z - 1)
        return cube * cube * cube - x * x * z * z * z - (9. * y * y * z * z * z)/200.


class MengerSponge(IsoSurface):
    def __init__(self, iterations):
        self.__iterations = iterations

    def isovalue(self):
        return 0.

    def test_point(self, point):
        for i in range(0, self.__iterations):
            point = mathutils.Vector((math.fabs(point.x),
                                      math.fabs(point.y),
                                      math.fabs(point.z)))
            point.xy = point.yx if point.x < point.y else point.xy
            point.yz = point.zy if point.y < point.z else point.yz
            point.xy = point.yx if point.x < point.y else point.xy

            point = point.xyz * 3.0 - 2.0
            point.z =  point.z + 2. if point.z < - 1.0 else point.z


# https://www.fountainware.com/Funware/Mandelbrot3D/Mandelbrot3d.htm
class Mandelbulb(IsoSurface):
    def __init__(self, max_iterations=6, degree=8):
        self.__max_iterations = max_iterations
        self.__degree = degree

    def isovalue(self):
        return 1.

    def test_point(self, point):
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
                return result

        return result


class Sphere(IsoSurface):
    def __init__(self, radius=1):
        self.__radius = radius

    def isovalue(self):
        return 0.

    def test_point(self, point):
        return point.length_squared - self.__radius


class Torus(IsoSurface):
    def __init__(self, fradius=2, sradius=1):
        self.__fradius = fradius
        self.__sradius = sradius

    def isovalue(self):
        return 0.

    def test_point(self, point):
        power = point.x * point.x + \
                point.y * point.y + \
                point.z * point.z + \
                self.__fradius * self.__fradius - \
                self.__sradius * self.__sradius

        return power * power - \
               4 * (self.__fradius * self.__fradius) * (point.x * point.x + point.y * point.y)


class Genus2(IsoSurface):
    def isovalue(self):
        return 0.

    def test_point(self, point):
        return 2 * point.y * (point.y * point.y - 3 * point.x * point.x) * \
               (1 - point.z * point.z) + (point.x * point.x + point.y * point.y) * \
               (point.x * point.x + point.y * point.y) - (9 * point.z * point.z - 1) * \
               (1 - point.z * point.z)


class RevolutionSurface(IsoSurface):
    def isovalue(self):
        return 0.

    def test_point(self, point):
        ln_z = (numpy.log(point.z + 3.2))
        return point.x * point.x + point.y * point.y - (ln_z * ln_z) - 0.02


class Moebius(IsoSurface):
    def isovalue(self):
        return 0.

    def test_point(self, point):
        return point.x * point.x * point.y + point.y * point.z * point.z +\
               point.y * point.y * point.y - point.y - 2 * point.x * point.z \
               - 2 * point.x * point.x * point.z - 2 * point.y * point.y * point.z


class IsoSurfaceGenerator:
    def __init__(self, isosurface=Heart(), grid_size=8, step_size=0.05):
        self.__isosurface = isosurface
        self.__grid_size = grid_size
        self.__step_size = step_size

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
                        values.append(self.__isosurface.test_point(vertices[l]))

                    cell = utils.marching_cubes.GridCell(vertices, values)
                    self.__faces.extend(utils.marching_cubes.marching_cubes(cell, self.__isosurface.isovalue()))

        print(f"End of mesh generation found {str(len(self.__faces))} faces")

    def vertices(self):
        return self.__vertices

    def faces(self):
        return self.__faces
