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


# https://strangerintheq.github.io/sdf.html
class MengerSponge(IsoSurface):
    """
    To be generated with grid of size 4 and step 0.05
    """
    def __init__(self, iterations=5):
        self.__iterations = iterations

    def isovalue(self):
        return 0.0

    def __test_point_box(self, point, b):
        d = mathutils.Vector((math.fabs(point.x) - b.x,
                               math.fabs(point.y) - b.y,
                               math.fabs(point.z) - b.z))
        return min(max(d.x, max(d.y, d.z)), 0.) + \
               mathutils.Vector((max(d.x, 0),
                                 max(d.y, 0),
                                 max(d.z, 0))).length

    def test_point(self, point):
        # https://www.shadertoy.com/view/MdfBWr
        main_width_box = 2.
        inf = 1.
        hole_x = 0.
        hole_y = 0.
        hole_z = 0.
        hole_width_b = main_width_box / 3.0

        menger = self.__test_point_box(point, mathutils.Vector((main_width_box, main_width_box, main_width_box)))
        for i in range(0, self.__iterations):
            hole_distance = hole_width_b * 6.

            c = mathutils.Vector((hole_distance, hole_distance, hole_distance))

            sx = (point.x + hole_width_b)
            sy = (point.y + hole_width_b)
            sz = (point.z + hole_width_b)
            q = mathutils.Vector((sx - c.x * math.floor(sx / c.x),
                                  sy - c.y * math.floor(sy / c.y),
                                  sz - c.z * math.floor(sz / c.z))).xyz\
                - mathutils.Vector((hole_width_b, hole_width_b, hole_width_b))

            hole_x = self.__test_point_box(q, mathutils.Vector((
                inf, hole_width_b, hole_width_b
            )))

            hole_y = self.__test_point_box(q, mathutils.Vector((
                hole_width_b, inf, hole_width_b
            )))

            hole_z = self.__test_point_box(q, mathutils.Vector((
                hole_width_b, hole_width_b, inf
            )))

            hole_width_b = hole_width_b / 3.0
            menger = max(max(max(menger, -hole_x), -hole_y), -hole_z)
        return menger


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
    def __init__(self, isosurface=MengerSponge(), grid_size=4, step_size=0.05):
        self.__isosurface = isosurface
        self.__grid_size = grid_size
        self.__step_size = step_size

        self.__vertices = []
        self.__faces = []

    def generate_mesh(self):
        low = -(self.__grid_size / 2) - self.__step_size
        up = (self.__grid_size / 2) + self.__step_size
        self.__faces = []

        for i in numpy.arange(low, up, self.__step_size):
            for j in numpy.arange(low, up, self.__step_size):
                for k in numpy.arange(low, up, self.__step_size):
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
