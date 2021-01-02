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

<p align="center">
	<img src="output/tuto2.png" alt="Enable"/>
</p>

You can now find on the right panel the panel "Marching cubes" which let you change your settings.

To create meshes with the addon you can right click on the scene and find at the bottom of the small popup
the new fields provided by the addon.

<p align="center">
	<img src="output/tuto.png" alt="AddonPopup"/>
</p>

### Procedural meshes

This project allows to create some procedural meshes:

<p align="center">
	<img src="output/Resized/TorusPP1.png" alt="Torus"/> <img src="output/Resized/Tetahedron.png" alt="Tetahedron"/>
</p>

### Marching cubes

The marching cubes algorithm is used to created mesh from sdf functions such as the 3D Mandelbrot
set.

__Results__:

Here are some outputs of Mandelbulb:


<p align="center">
	<img src="output/Resized/Mandelbrot.png" alt="Mandelbulb"/> <img src="output/Resized/Mandelbrot2.png" alt="Mandelbulb"/> <img src="output/Resized/Mandelbrot3.png" alt="Mandelbulb"/> <img src="output/Resized/Mandelbulb4.png" alt="Mandelbulb"/>
</p>

__High resolution outputs :__

<p align="center">
	<img src="output/Resized/MandelbulbHighRes.png" alt="MandelbulbHighRes"/> <img src="output/Resized/MandelbulbHighRes1.png" alt="MandelbulbHighRes"/> <img src="output/Resized/MengerSponge.png" alt="MengerSponge"/>
</p>

<p align="center">
	 <img src="output/Resized/Mandelbox.png" alt="Mandelbox"/> <img src="output/Resized/Mandelbox1.png" alt="Mandelbox"/> 
</p>

### Terrain 

A terrain generator has been implemented based on different technologies:

<p align="center">
	<img src="output/Resized/NoiseTerrain.png" alt="NoiseTerrain"/> <img src="output/Resized/Map.png" alt="NoiseTerrain"/> 
</p>

### Contributors

[Nicolas Lepy](https://github.com/nicolasLepy)

[Cyprien Plateau--Holleville](https://github.com/PlathC)
