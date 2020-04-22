import math
import mathutils
# Based on https://gamedev.stackexchange.com/questions/16845/how-do-i-generate-a-torus-mesh


class Torus:

    def __init__(self, origin=mathutils.Vector((0, 0, 0)), first_circle_diameter=2, second_circle_diameter=1.5, vertices_per_circles=80):
        """
        Torus ctor.
        Call generate function.
        :param origin: Origin of the first circle
        :param first_circle_diameter: Diameter of the first circle
        :param second_circle_diameter: Diameter of the second circle
        :param vertices_per_circles: Number of vertices per circles.
        """

        self.__vertices_dictionary = {}
        self.__origin = origin
        self.__fc_diameter = first_circle_diameter
        self.__sc_diameter = second_circle_diameter
        self.__vertices_per_circles = vertices_per_circles
        self.__vertices_number = 0
        self.__us = []
        self.__vs = []

        self.__mesh_vertices = []
        self.__mesh_triangles = []
        self.__mesh_uvs = []

        self.generate()

    def __get_w(self, u):
        """
        Generate first circle points.

        :param u: Current angle
        :return: Point corresponding to angle.
        """
        return mathutils.Vector((math.cos(u), math.sin(u), 0))

    def __get_q(self, u, v):
        """
        Generate second circle points.
        :param u: First circle angle
        :param v: Second circle angle
        :return: Point corresponding to both angles.
        """
        if u not in self.__vertices_dictionary:
            self.__vertices_dictionary[u] = {}

        self.__vertices_dictionary[u][v] = self.__vertices_number
        self.__vertices_number += 1

        w = self.__get_w(u)
        fc = self.__fc_diameter * w.xyz

        cosv = math.cos(v)
        sc = self.__sc_diameter * w.xyz
        ls = mathutils.Vector((0,
                               0,
                               self.__sc_diameter * math.sin(v)))

        return self.__origin.xyz + fc.xyz + sc.xyz + ls.xyz

    def generate(self):
        """
        Generate torus mesh data.
        """
        # Clear potential pre used data.
        self.__us.clear()
        self.__vs.clear()
        self.__mesh_vertices.clear()
        self.__mesh_triangles.clear()
        self.__vertices_dictionary.clear()

        vs_complete = False
        self.__vertices_number = 0

        angle_step = ((2. * math.pi) / self.__vertices_per_circles)
        angle = 0.

        # vertices generation
        for i in range(0, self.__vertices_per_circles):
            self.__us.append(angle)
            second_angle = 0.
            for j in range(0, self.__vertices_per_circles):
                if not vs_complete:
                    self.__vs.append(second_angle)

                self.__mesh_vertices.append(
                    self.__get_q(angle, second_angle)
                )

                second_angle += angle_step

            vs_complete = True
            angle += angle_step

        for i in range(0, len(self.__us)):
            for j in range(0, len(self.__vs)):

                # First triangle
                # (u, v)
                self.__mesh_triangles.append(
                    self.__vertices_dictionary[self.__us[i]][self.__vs[j]]
                )

                # (u, v + 1)
                if j == len(self.__vs) - 1:
                    self.__mesh_triangles.append(
                        self.__vertices_dictionary[self.__us[i]][self.__vs[0]]
                    )
                else:
                    self.__mesh_triangles.append(
                        self.__vertices_dictionary[self.__us[i]][self.__vs[j + 1]]
                    )

                # (u - 1, v)
                if i == 0:
                    self.__mesh_triangles.append(
                        self.__vertices_dictionary[self.__us[len(self.__us) - 1]][self.__vs[j]]
                    )
                else:
                    self.__mesh_triangles.append(
                        self.__vertices_dictionary[self.__us[i - 1]][self.__vs[j]]
                    )

                # Second triangle
                # (u - 1, v)
                if i == 0:
                    self.__mesh_triangles.append(
                        self.__vertices_dictionary[self.__us[len(self.__us) - 1]][self.__vs[j]]
                    )
                else:
                    self.__mesh_triangles.append(
                        self.__vertices_dictionary[self.__us[i - 1]][self.__vs[j]]
                    )

                # (u, v + 1)
                if j == len(self.__vs) - 1:
                    self.__mesh_triangles.append(
                        self.__vertices_dictionary[self.__us[i]][self.__vs[0]]
                    )
                else:
                    self.__mesh_triangles.append(
                        self.__vertices_dictionary[self.__us[i]][self.__vs[j + 1]]
                    )

                # (u - 1, v + 1)
                u_value = 0
                v_value = 0
                if i == 0:
                    u_value = self.__us[len(self.__us) - 1]
                else:
                    u_value = self.__us[i - 1]

                if j == len(self.__vs) - 1:
                    v_value = self.__vs[0]
                else:
                    v_value = self.__vs[j + 1]

                self.__mesh_triangles.append(
                    self.__vertices_dictionary[u_value][v_value]
                )

        for i in range(0, len(self.__mesh_vertices)):
            self.__mesh_uvs.append((self.__mesh_vertices[i].x, self.__mesh_vertices[i].z))

    def vertices(self):
        """
        Getter of the mesh vertices.
        Generate has to be called first (called in ctor)
        :return: Mesh vertices
        """
        return self.__mesh_vertices

    def triangles(self):
        """
        Getter of the mesh triangles
        :return: Mesh triangles
        """
        return self.__mesh_triangles

    def uvs(self):
        """
        Getter of the mesh uvs.
        :return: Mesh uvs
        """
        return self.__mesh_uvs
