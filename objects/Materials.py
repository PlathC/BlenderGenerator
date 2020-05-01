import bpy
from abc import ABC, abstractmethod


class Material(ABC):
    @abstractmethod
    def apply_material(self, obj):
        pass


class Subsurface(Material):
    def apply_material(self, obj):
        mat = bpy.data.materials.new(name="Subsurface")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]

        bsdf.inputs["Base Color"].default_value = (0.142, 0.082, 0.073, 1.)
        bsdf.inputs["Subsurface"].default_value = 0.464
        bsdf.inputs["Subsurface Color"].default_value = (0.8, 0.18, 0.072, 1.)

        # Assign it to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        world_nodes = bpy.data.worlds["World"].node_tree
        color_value = world_nodes.nodes.new('ShaderNodeValue')
        color_value.outputs[0].default_value = 0.

        world_nodes.links.new(world_nodes.nodes["Background"].inputs['Color'], color_value.outputs[0])

        scn = bpy.context.scene
        if not scn.render.engine == 'CYCLES':
            scn.render.engine = 'CYCLES'


class SmoothColor(Material):
    def __init__(self, color=(0., 0., 0., 0.)):
        self.__color = color

    def apply_material(self, obj):
        mat = bpy.data.materials.new(name="SmoothBlack")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]

        bsdf.inputs["Base Color"].default_value = (self.__color[0],
                                                   self.__color[1],
                                                   self.__color[2],
                                                   self.__color[3])

        # Assign it to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        world_nodes = bpy.data.worlds["World"].node_tree
        color_value = world_nodes.nodes.new('ShaderNodeValue')
        color_value.outputs[0].default_value = 0.

        world_nodes.links.new(world_nodes.nodes["Background"].inputs['Color'], color_value.outputs[0])

        scn = bpy.context.scene
        if not scn.render.engine == 'CYCLES':
            scn.render.engine = 'CYCLES'


class HeightMapColor(Material):
    def apply_material(self, obj):
        mat = bpy.data.materials.new(name="HeightMapColor")
        mat.use_nodes = True

        tex_coord = mat.node_tree.nodes.new('ShaderNodeTexCoord')
        separate_xyz = mat.node_tree.nodes.new('ShaderNodeSeparateXYZ')

        subtract = mat.node_tree.nodes.new('ShaderNodeMath')
        subtract.operation = "SUBTRACT"
        subtract.inputs[0].default_value = 0.5

        color_ramp = mat.node_tree.nodes.new("ShaderNodeValToRGB")
        color_ramp.color_ramp.interpolation = 'CONSTANT'
        color_ramp.color_ramp.elements.new(0.138)
        color_ramp.color_ramp.elements.new(0.55)
        color_ramp.color_ramp.elements[0].position = 0
        color_ramp.color_ramp.elements[0].color = (1., 1., 1., 1.)
        color_ramp.color_ramp.elements[1].position = 0.138
        color_ramp.color_ramp.elements[1].color = (0.009, 0.128, 0.000865, 1.)
        color_ramp.color_ramp.elements[2].position = 0.543182
        color_ramp.color_ramp.elements[2].color = (0.149, 0.030, 0., 1.)
        color_ramp.color_ramp.elements[3].position = 0.636364
        color_ramp.color_ramp.elements[3].color = (0.281, 0.52, 1., 1.)

        bsdf = mat.node_tree.nodes["Principled BSDF"]

        mat.node_tree.links.new(bsdf.inputs['Base Color'], color_ramp.outputs['Color'])
        mat.node_tree.links.new(color_ramp.inputs['Fac'], subtract.outputs[0])
        mat.node_tree.links.new(subtract.inputs[1], separate_xyz.outputs['Z'])
        mat.node_tree.links.new(separate_xyz.inputs["Vector"], tex_coord.outputs['Object'])

        # Assign it to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        world_nodes = bpy.data.worlds["World"].node_tree
        color_value = world_nodes.nodes.new('ShaderNodeValue')
        color_value.outputs[0].default_value = 0.

        world_nodes.links.new(world_nodes.nodes["Background"].inputs['Color'], color_value.outputs[0])

        scn = bpy.context.scene
        if not scn.render.engine == 'CYCLES':
            scn.render.engine = 'CYCLES'


class NoiseMap(Material):
    def __init__(self,
                 ground_color=(0.149, 0.030, 0., 1.),
                 water_color=(0.281, 0.52, 1., 1.),
                 grass_color=(0.009, 0.128, 0.000865, 1.),
                 snow_color=(1., 1., 1., 1.)):
        self.__ground_color = ground_color
        self.__water_color = water_color
        self.__grass_color = grass_color
        self.__snow_color = snow_color

    def apply_material(self, obj):
        mat = bpy.data.materials.new(name="Map")
        mat.use_nodes = True

        # Color shader
        tex_coord = mat.node_tree.nodes.new('ShaderNodeTexCoord')
        separate_xyz = mat.node_tree.nodes.new('ShaderNodeSeparateXYZ')
        subtract = mat.node_tree.nodes.new('ShaderNodeMath')
        subtract.operation = "SUBTRACT"
        subtract.inputs[0].default_value = 0.6

        color_ramp = mat.node_tree.nodes.new("ShaderNodeValToRGB")
        color_ramp.color_ramp.interpolation = 'LINEAR'
        color_ramp.color_ramp.elements.new(0.524)
        color_ramp.color_ramp.elements.new(0.598)
        color_ramp.color_ramp.elements[0].position = 0.363636
        color_ramp.color_ramp.elements[0].color = self.__snow_color
        color_ramp.color_ramp.elements[1].position = 0.524
        color_ramp.color_ramp.elements[1].color = self.__grass_color
        color_ramp.color_ramp.elements[2].position = 0.598
        color_ramp.color_ramp.elements[2].color = self.__ground_color
        color_ramp.color_ramp.elements[3].position = 0.622728
        color_ramp.color_ramp.elements[3].color = self.__water_color

        bsdf = mat.node_tree.nodes["Principled BSDF"]

        mat.node_tree.links.new(bsdf.inputs['Base Color'], color_ramp.outputs['Color'])
        mat.node_tree.links.new(color_ramp.inputs['Fac'], subtract.outputs[0])
        mat.node_tree.links.new(subtract.inputs[1], separate_xyz.outputs['Z'])
        mat.node_tree.links.new(separate_xyz.inputs["Vector"], tex_coord.outputs['Object'])

        # Displacement
        tex_coord = mat.node_tree.nodes.new('ShaderNodeTexCoord')
        mapping = mat.node_tree.nodes.new('ShaderNodeMapping')
        noise_texture = mat.node_tree.nodes.new('ShaderNodeTexNoise')
        noise_texture.inputs[2].default_value = 1.5
        noise_texture.inputs[3].default_value = 6.6
        noise_texture.inputs[4].default_value = 4.3
        displacement = mat.node_tree.nodes.new('ShaderNodeDisplacement')

        mat.node_tree.links.new(mapping.inputs[0], tex_coord.outputs[0])
        mat.node_tree.links.new(noise_texture.inputs[0], mapping.outputs[0])
        mat.node_tree.links.new(displacement.inputs[0], noise_texture.outputs[0])
        mat.node_tree.links.new(mat.node_tree.nodes["Material Output"].inputs[2], displacement.outputs[0])

        mat.cycles.displacement_method = 'BOTH'

        # Assign it to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        world_nodes = bpy.data.worlds["World"].node_tree
        color_value = world_nodes.nodes.new('ShaderNodeValue')
        color_value.outputs[0].default_value = 0.8

        world_nodes.links.new(world_nodes.nodes["Background"].inputs['Color'], color_value.outputs[0])

        scn = bpy.context.scene
        if not scn.render.engine == 'CYCLES':
            scn.render.engine = 'CYCLES'