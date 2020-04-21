# Blender Generator

This is a learning project which aims to create procedural mesh that will be rendered in Blender.

## Features

| Feature               | Progress                                                     |
|-----------------------|--------------------------------------------------------------|
| Procedural meshes     | Torus                                                        |
| Marching cubes        | Done (slow version)                                          |
| Isosurface rendering  | Heart, MengerSponge, Mandelbulb, Sphere, Torus, Genus2, RevolutionSurface, Moebius |
| L - System            | In dev                                                       |
| Terrain generator     | In dev                                                       |
| Reaction diffusion    | To do                                                        |

### Procedural meshes

This project allows to create a torus mesh based on its formula and to render it 
thanks to Blender :

![Torus](output/Resized/TorusPP1.png)

### Marching cubes

The marching cubes algorithm is used to created mesh from sdf functions such as the 3D Mandelbrot
set.

__Results__:

Here are some outputs of Mandelbulb:

![Mandelbulb](output/Resized/Mandelbrot.png) ![Mandelbulb](output/Resized/Mandelbrot1.png) ![Mandelbulb](output/Resized/Mandelbrot2.png)

![Mandelbulb](output/Resized/Mandelbrot3.png) ![Mandelbulb](output/Resized/Mandelbulb4.png) 

Menger Sponge :

![MengerSponge](output/Resized/MengerSponge.png) 

### Terrain 

A terrain generator has been implemented based on different technologies:

__Marching cubes and noise__

![NoiseTerrain](output/Resized/NoiseTerrain.png)

