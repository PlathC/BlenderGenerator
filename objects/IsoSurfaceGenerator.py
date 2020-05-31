import mathutils
import math
import utils.marching_cubes
import numpy
from abc import ABC, abstractmethod
import objects.Materials


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class IsoSurface(ABC):
    @abstractmethod
    def isovalue(self):
        pass

    @abstractmethod
    def test_point(self, point):
        pass

    @abstractmethod
    def material(self):
        pass


class Planet(IsoSurface):
    def __init__(self, radius=1):
        self.__radius = radius
        self.__sphere = Sphere(self.__radius)

    def isovalue(self):
        return 0.

    def test_point(self, point):
        return self.__sphere.test_point(point) + \
               mathutils.noise.hybrid_multi_fractal(point.normalized(), 1., 10.0, 12, 1, 50) * (self.__radius/3)

    def material(self):
        return objects.Materials.SmoothColor((1., 1., 1., 1.))


class ComplexTerrain(IsoSurface):
    def isovalue(self):
        return 0.

    def test_point(self, point):
        q = mathutils.Vector((mathutils.noise.noise(point.xyz + mathutils.Vector((0, 0, 0))),
                              mathutils.noise.noise(point.xyz + mathutils.Vector((5.2, 1.3, 0))),
                              0)
                             )
        r = mathutils.Vector((mathutils.noise.noise(point.xyz + 4.0*q.xyz + mathutils.Vector((1.7, 9.2, 0)).xyz),
                              mathutils.noise.noise(point.xyz + 4.0*q.xyz + mathutils.Vector((8.3, 2.8, 0)).xyz),
                              0)
                             )

        return mathutils.noise.noise((point.xyz + 4.0 * r.xyz).xyz) - point.z * 10

    def material(self):
        return objects.Materials.HeightMapColor()


class SimpleNoiseTerrain(IsoSurface):
    def isovalue(self):
        return 0.

    def test_point(self, point):
        return mathutils.noise.noise(point.xyz, noise_basis='PERLIN_ORIGINAL') - point.z

    def material(self):
        return objects.Materials.HeightMapColor()


class Heart(IsoSurface):
    def __init__(self, stretch_factor=8, size=100):
        self.__stretch = stretch_factor * 100

    def isovalue(self):
        return 0.

    def test_point(self, point):
        x = point.x
        y = point.y
        z = point.z
        cube = (x * x + 9./4. * y * y + z * z - 1)
        return cube * cube * cube - x * x * z * z * z - (9. * y * y * z * z * z)/200. * self.__stretch

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 0., 0., 0.))


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

    def material(self):
        return objects.Materials.SmoothColor(color=(0.1, 0.1, 0.1, 0.))


# https://www.fountainware.com/Funware/Mandelbrot3D/Mandelbrot3d.htm
class Mandelbulb(IsoSurface):
    def __init__(self, max_iterations=5, degree=3):
        self.__max_iterations = max_iterations
        self.__degree = degree

    def isovalue(self):
        return 1.

    def test_point(self, point):
        """
        :param point: The point we want to test
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

    def material(self):
        return objects.Materials.SmoothColor(color=(0.1, 0.1, 0.1, 0.))


class Sphere(IsoSurface):
    def __init__(self, radius=1):
        self.__radius = radius

    def isovalue(self):
        return 0.

    def test_point(self, point):
        return point.length_squared - self.__radius

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


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

        return power * power - 4 * \
               (self.__fradius * self.__fradius) *\
               (point.x * point.x + point.y * point.y)

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


class Genus2(IsoSurface):
    def isovalue(self):
        return 0.

    def test_point(self, point):
        return 2 * point.y * (point.y * point.y - 3 * point.x * point.x) * \
               (1 - point.z * point.z) + (point.x * point.x + point.y * point.y) * \
               (point.x * point.x + point.y * point.y) - (9 * point.z * point.z - 1) * \
               (1 - point.z * point.z)

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


class RevolutionSurface(IsoSurface):
    def __init__(self, height=2.2, radius=3.02):
        self.__height = height
        self.__radius = radius

    def isovalue(self):
        return 0.

    def test_point(self, point):
        ln_z = (numpy.log(point.z + self.__height))
        return point.x * point.x + point.y * point.y - (ln_z * ln_z) - self.__radius

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


class Moebius(IsoSurface):
    def __init__(self, curve=0.8):
        self.__curve = curve

    def isovalue(self):
        return 0.

    def test_point(self, point):
        return point.x * point.x * point.y + point.y * point.z * point.z +\
               point.y * point.y * point.y - point.y - self.__curve * point.x * point.z \
               - self.__curve * point.x * point.x * point.z - self.__curve * point.y * point.y * point.z

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


class Sin(IsoSurface):
    def __init__(self):
        print('init')

    def isovalue(self):
        return 0.

    def test_point(self, point):
        vec = mathutils.Vector((point.x * 3 + 3, point.y * 3 + 3, point.z * 3 + 3))
        dot = vec.dot(mathutils.Vector((1., 1., 1.)))
        dotPow = dot.xyz * dot.xyz
        subtDotPow = 0.1 - dotPow
        lengthPoint = point.length - 1.7
        if lengthPoint < 0:
            lengthPoint = 0
        lengthPoint = lengthPoint * lengthPoint * 10.
        return subtDotPow - lengthPoint

        #return math.sin(point.x) + math.sin(point.y) + math.sin(point.z)

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


class Mandelbox(IsoSurface):
    def __init__(self):
        print('init')

    def isovalue(self):
        return 1.

    def test_point(self, point):
        x = point.x
        y = point.y
        z = point.z
        n = 6
        scale = 2.5
        for i in range(0, n):
            de_factor = scale
            fixedRadius = 1.0
            fR2 = fixedRadius * fixedRadius
            minRadius = 0.5
            mR2 = minRadius * minRadius

            if x > 1.0:
                x = 2.0 - x
            elif x < -1.0:
                x = -2.0 - x
            if y > 1.0:
                y = 2.0 - y
            elif y < -1.0:
                y = -2.0 - y
            if z > 1.0:
                z = 2.0 - z
            elif z < - 1.0:
                z = -2.0 - z

            r2 = x*x + y*y + z*z

            if r2 < mR2:
                x = x * fR2 / mR2
                y = y * fR2 / mR2
                z = z * fR2 / mR2
                de_factor = de_factor * fR2 / mR2
            elif r2 < fR2:
                x = x * fR2 / r2
                y = y * fR2 / r2
                z = z * fR2 / r2
                de_factor = de_factor * fR2/r2
            x = x * scale + 2
            y = y * scale + -2
            z = z * scale + -2
            de_factor = de_factor * scale

        distance = math.sqrt(x * x + y * y + z * z) / math.fabs(de_factor)
        return distance

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


class Julia(IsoSurface):
    def __init__(self):
        print('init')

    def isovalue(self):
        return 1.

    # square a quaterion
    def qsqr(self, a):
        return mathutils.Vector((a.x * a.x - a.y * a.y - a.z * a.z - a.w * a.w,
                                 2.0 * a.x * a.y,
                                 2.0 * a.x * a.z,
                                 2.0 * a.x * a.w))

    def test_point(self, point):
        z = mathutils.Vector((point.x, point.y, point.z, 0.0))
        md2 = 1.0
        mz2 = z.dot(z)
        trap = mathutils.Vector((math.fabs(point.x), math.fabs(point.y), math.fabs(point.z), z.dot(z)))
        n = 1.0
        for i in range(0, 4):
            md2 = md2 * mz2
            c = mathutils.Vector((0.10, 0.40, 0.40, 0.40))
            z = self.qsqr(z).xyzw + c.xyzw
            if trap > mathutils.Vector((math.fabs(point.x), math.fabs(point.y), math.fabs(point.z),z.dot(z))):
                trap = mathutils.Vector((math.fabs(point.x), math.fabs(point.y), math.fabs(point.z),z.dot(z)))
            mz2 = z.dot(z)
            if mz2>4.0:
                break
            n = n+1

        return 0.25 * math.sqrt( mz2 / md2) * math.pow(2, -n) * math.log(mz2)

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


class Sphere(IsoSurface):
    def __init__(self):
        print('init')

    def isovalue(self):
        return 0.

    def test_point(self, point):
        return math.fabs(math.sqrt(point.x * point.x + point.y * point.y + point.z * point.z) - 0.8)

    def material(self):
        return objects.Materials.SmoothColor(color=(1., 1., 1., 1.))


class IsoSurfaceGenerator:
    def __init__(self, isosurface=Tetahedron(), grid_size=4, step_size=0.01):
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

    def material(self):
        return self.__isosurface.material()