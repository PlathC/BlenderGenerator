
# import objects.PlatonicSolid
from BlenderGenerator.objects import PlatonicSolid


def platonic_solid():
    """
    Create the five platonic solids
    """
    PlatonicSolid.PlatonicSolid(5, PlatonicSolid.Shape.TETRAHEDRON)
    PlatonicSolid.PlatonicSolid(5, PlatonicSolid.Shape.HEXAHEDRON)
    PlatonicSolid.PlatonicSolid(5, PlatonicSolid.Shape.OCTAHEDRON)
    PlatonicSolid.PlatonicSolid(5, PlatonicSolid.Shape.DODECAHEDRON)
    PlatonicSolid.PlatonicSolid(5, PlatonicSolid.Shape.ICOSAHEDRON)
