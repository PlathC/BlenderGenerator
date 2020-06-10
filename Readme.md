# Blender Generator

This is a learning project which aims to create procedural mesh that will be rendered in Blender.

## Features

| Feature               | Progress                                                       |
|-----------------------|----------------------------------------------------------------|
| Procedural meshes     | Torus                                                          |
| Marching cubes        | Done (slow version)                                            |
| Isosurface rendering  | Done (See implemented objects in objects/IsoSurfaceGenerator.py|
| Terrain generator     | Done                                                           |

### Install

To add this addon to your Blender you need to follow these steps :

1. Clone the projet 

```sh
	git clone https://github.com/PlathC/BlenderGenerator.git
```

2. Copy the folder inside the folder <PathToBlenderInstall>/Blender/<Version>/scripts/addons. Changes 
will be applyed on the next Blender startup.

3. Enable the addon in : Edit / Preferences / Addons / "Add Mesh : IN55 Project"

![Enable](output/tuto2.png)

You can now find on the right panel the panel "Marching cubes" which let you change your settings.

To create mesh with the addon you can right click on the scene and find at the bottom of the small popup
the new fields provided by the addon.

![AddonPopup](output/tuto.png)

### Procedural meshes

This project allows to create some procedural meshes:

![Torus](output/Resized/TorusPP1.png)

Tetahedron

![Tetahedron](output/Resized/Tetahedron.png) 

### Marching cubes

The marching cubes algorithm is used to created mesh from sdf functions such as the 3D Mandelbrot
set.

__Results__:

Here are some outputs of Mandelbulb:

![Mandelbulb](output/Resized/Mandelbrot.png) ![Mandelbulb](output/Resized/Mandelbrot2.png)

![Mandelbulb](output/Resized/Mandelbrot3.png) ![Mandelbulb](output/Resized/Mandelbulb4.png) 

__High resolution outputs :__

Mandelbulb grid_size=2.5, step_size=0.005, max_iterations=6, degree=8

![MandelbulbHighRes](output/Resized/MandelbulbHighRes.png)

Mandelbulb grid_size=2.7, step_size=0.005, max_iterations=5, degree=3

![MandelbulbHighRes](output/Resized/MandelbulbHighRes1.png)

Menger Sponge :

![MengerSponge](output/Resized/MengerSponge.png) 

Mandelbox grid_size=2, step_size=0.005, iterations=6, seed=[2, -2, -2]

![Mandelbox](output/Resized/Mandelbox.png) 

![Mandelbox](output/Resized/Mandelbox1.png) 

### Terrain 

A terrain generator has been implemented based on different technologies:

__Marching cubes and noise__

![NoiseTerrain](output/Resized/NoiseTerrain.png)

__Shader and noise based map__

![NoiseTerrain](output/Resized/Map.png)

### Contributors

[Nicolas Lepy](https://github.com/nicolasLepy)

[Cyprien Plateau--Holleville](https://github.com/PlathC)