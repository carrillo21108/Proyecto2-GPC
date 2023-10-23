import pygame
from pygame.locals import *

from rt import RayTracer
from figures import *
from lights import *
from materials import *


width = 840
height = 840

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF|pygame.HWACCEL|pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("textures/parkingLot.bmp")
raytracer.rtClearColor(0.25,0.25,0.25)

#Texturas
earthTexture = pygame.image.load("textures/earthDay.bmp")
wallTexture = pygame.image.load("textures/wall.bmp")
woodTexture = pygame.image.load("textures/wood.bmp")

#Materiales
mirror = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.2,matType=REFLECTIVE)
blue = Material(diffuse=(16/255,26/255,62/255),spec=8,Ks=0.01)
wood = Material(diffuse=(182/255,104/255,66/255),spec=256,Ks=0.2)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32,Ks=0.15,matType=REFLECTIVE)
earth = Material(texture = earthTexture,spec=64,Ks=0.1,matType=OPAQUE)
wall = Material(texture = wallTexture,spec=64,Ks=0.1)
glass = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.15,ior=1.5,matType=TRANSPARENT)
reflectiveWood = Material(texture = woodTexture,spec=64,Ks=0.1,matType=REFLECTIVE)
brick = Material(diffuse=(1,0.4,0.4),spec=8,Ks=0.01)

#Habitacion
width = 100
height = 100
depth = 600

#Pared izquierda
raytracer.scene.append(Plane(position=(-width,height/2,0),normal=(1,0,0.5),material=blue))
#Pared derecha
raytracer.scene.append(Plane(position=(width,height/2,0),normal=(-1,0,0.15),material=blue))
#Fondo
raytracer.scene.append(Plane(position=(0,height/2,-depth/2),normal=(0,0,1),material=wood))
#Techo
raytracer.scene.append(Triangle(vertex=[(-3.8,3,-5),(4,3,-5),(1.3,2,-7)],material=reflectiveWood))
#Suelo
raytracer.scene.append(Plane(position=(0,-height/2,-depth/2),normal=(0,1,-0.1),material=wood))

#Discos
raytracer.scene.append(Disk(position=(-2.5,0.8,-8),normal=(-1,0,0),radius=1.7,material=blueMirror))
raytracer.scene.append(Disk(position=(-0.4,0.5,-8),normal=(-1,0,-0.15),radius=1.3,material=blueMirror))
raytracer.scene.append(Disk(position=(0.6,0.4,-8),normal=(-1,0,-0.25),radius=1,material=blueMirror))

#Obras
#Esfera  y luz
raytracer.scene.append(AABB(position=(1,-1,-7),size=(1.2,1.2,1.2),material=wall))
raytracer.scene.append(Sphere(position=(1,0,-7),radius=0.5,material=earth))
raytracer.lights.append(PointLight(point=(1,0.5,-5),intensity=1,color=(1,1,0)))

#Piramide y luz
raytracer.scene.append(AABB(position=(-1,-1,-6),size=(1.2,1.2,1.2),material=wall))
raytracer.scene.append(Triangle(vertex=[(-1.8,-0.4,-6),(-1,0.5,-6),(-0.5,-0.4,-5)],material=brick))
raytracer.scene.append(Triangle(vertex=[(-0.2,-0.4,-6),(-1,0.5,-6),(-0.5,-0.4,-5)],material=brick))
raytracer.lights.append(PointLight(point=(-0.5,0,-4),intensity=1,color=(1,0,0)))

#Cubo y luz
raytracer.scene.append(AABB(position=(3,-1,-6),size=(1.2,1.2,1.2),material=wall))
raytracer.scene.append(AABB(position=(3,0,-6),size=(0.8,0.8,0.8),material=glass))
raytracer.lights.append(PointLight(point=(2.5,0.5,-5),intensity=1,color=(0,1,0)))


#Luces generales
raytracer.lights.append(AmbientLight(intensity=0.9))
raytracer.lights.append(DirectionalLight(direction=(0,-1,0),intensity=0.5))


raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:",pygame.time.get_ticks()/1000,"secs")

isRunning = True
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False

rect = pygame.Rect(0,0,width,height)
sub = screen.subsurface(rect)
pygame.image.save(sub,"screenshot.png")

pygame.quit()