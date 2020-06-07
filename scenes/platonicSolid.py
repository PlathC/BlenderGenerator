import objects.PlatonicSolid


def platonic_solid():
    print('Building platonic solid')
    platonic = objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.TETRAHEDRON)
    platonic = objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.HEXAHEDRON)
    platonic = objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.OCTAHEDRON)
    platonic = objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.DODECAHEDRON)
    platonic = objects.PlatonicSolid.PlatonicSolid(5, objects.PlatonicSolid.Shape.ICOSAHEDRON)