
# import objects.PlatonicSolid
from BlenderGenerator.objects import PlatonicSolid


def platonic_solid(shape):
    """
    Create the five platonic solids
    """
    PlatonicSolid.PlatonicSolid(5, shape)
