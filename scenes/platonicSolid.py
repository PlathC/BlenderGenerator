import objects.PlatonicSolid


def platonic_solid():
    """
    Create the five platonic solids
    """
    objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.TETRAHEDRON)
    objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.HEXAHEDRON)
    objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.OCTAHEDRON)
    objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.DODECAHEDRON)
    objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.ICOSAHEDRON)
