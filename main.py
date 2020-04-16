import bpy


def apply_material(obj):
    """
    """
    mat = bpy.data.materials.new(name="MapMaterial")
    mat.use_nodes = True
    bsdf   = mat.node_tree.nodes["Principled BSDF"]
    output = mat.node_tree.nodes["Material Output"]

    coordinate = mat.node_tree.nodes.new('ShaderNodeTexCoord')
    noise = mat.node_tree.nodes.new('ShaderNodeTexNoise')
    displacement = mat.node_tree.nodes.new('ShaderNodeDisplacement')

    mat.node_tree.links.new(noise.inputs['Vector'], coordinate.outputs['UV'])
    mat.node_tree.links.new(displacement.inputs['Height'], noise.outputs['Fac'])
    mat.node_tree.links.new(output.inputs['Displacement'], displacement.outputs['Displacement'])

    mat.cycles.displacement_method = 'BOTH'

    # Assign it to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    scn = bpy.context.scene
    if not scn.render.engine == 'CYCLES':
        scn.render.engine = 'CYCLES'


if __name__ == "__main__":
    bpy.ops.mesh.primitive_plane_add(location=(0.0, 0.0, 0.0))
    bpy.ops.object.shade_smooth()

    plane = bpy.context.active_object  # Get plane object

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=200)
    bpy.ops.object.mode_set(mode='OBJECT')

    apply_material(plane)
