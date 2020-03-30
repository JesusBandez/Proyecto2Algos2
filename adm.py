from cancion import *
from reproductor import *
from lr import *
import pygame
from pygame.locals import *
import math
import time

pygame.init()




# Mannipulación del reproductor
def cargarOtroArchivo() -> str:
	
	mensajeCargarOtroArchivo()
	coordenadas = (0,0)
	while coordenadas == (0,0):
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			elif event.type == pygame.MOUSEBUTTONUP:				
				coordenadas = pygame.mouse.get_pos()
				if 200 <= coordenadas[0] <= 285 and 150 <= coordenadas[1] <= 190:
					jugar_otra = "si"
				elif 450 <= coordenadas[0] <= 500 and 150 <= coordenadas[1] <= 190:
					jugar_otra = "no"
				else:
					coordenadas = (0,0)
	return jugar_otra

def cargarCanciones(lista:object, cancionCargada:object, reproductor:object) -> object: # Hay que comprobar que el archivo sirve
	ventana.blit(fondo, (0,0))	

	archivos = []
	otro = "si"
	while otro == "si":
		nombreArchivo = pedirArchivo()

		if nombreArchivo is None:
			archivos = []
			break

		archivos.append(nombreArchivo)
		otro = cargarOtroArchivo()

	for nombre in archivos:
		lista.agregarLista(nombre)
		
	if len(archivos) > 0:
		cancionCargada = lista.minInterprete(lista.root).cancion
		reproductor = prepararReproductor(cancionCargada)		

	return lista, cancionCargada, reproductor

def pedirArchivo() -> str:	 

	caracteres = ""
	asignado = ""
	escribir(caracteres)
	cCancelar = cancelar()
	while asignado == "":



		for event in pygame.event.get():
			
			if event.type == pygame.MOUSEBUTTONUP:
				if cCancelar.collidepoint(pygame.mouse.get_pos()):
					return None

			if event.type == KEYDOWN:

				if event.key == K_BACKSPACE:
					caracteres = caracteres[0:len(caracteres)-1]

				elif event.key == K_RETURN:
					caracteres = (caracteres[0] 
						+ caracteres[1:len(caracteres)].lower())
					asignado = caracteres	

				elif event.key == K_SPACE or len(caracteres) > 40:
					pass

				else:						
					caracteres = caracteres + event.unicode	

				escribir(caracteres)

			elif event.type == QUIT:
				exit()

			

	return caracteres

def mostrarLista(lista:object) -> object:	
	pFlechaDerecha, pFlechaizquierda = botonesDeNavegacion()
	pVolver = botonVolver()
	pEliminar = botonEliminar()
	ini, fin = 0, 8	
	while True:
		ventana.blit(fondo, (0,0))
		botonesDeNavegacion()
		botonVolver()
		botonEliminar()

		ventana.blit(panelDeCanciones, (25, 25))
		
		canciones = lista.obtenerLR()
		
		pYReferenciaACanciones = mostrarCancionesEnSecuenciaParcial(canciones[ini:fin])

		for event in pygame.event.get():
				if event.type == QUIT:
					exit()

				elif event.type == pygame.MOUSEBUTTONUP:

					if (pFlechaDerecha.collidepoint(pygame.mouse.get_pos())
						and fin < len(canciones)):
						ini = ini + 8
						fin = fin + 8

					elif (pFlechaizquierda.collidepoint(pygame.mouse.get_pos())
						and ini > 0):
						ini = ini - 8
						fin = fin - 8

					elif pEliminar.collidepoint(pygame.mouse.get_pos()):
						eliminarCancion(lista, pYReferenciaACanciones)
						
					elif pVolver.collidepoint(pygame.mouse.get_pos()):
						return

		pygame.display.flip()

def reproducirCancion(reproductor:object) -> object:

	reproductor.reproducir()

def siguienteCancion(lista:object, cancionCargada:object, reproductor:object) -> object:
	if cancionCargada is not None:
		nodoCancion = lista.buscarCancion(lista.root, cancionCargada.interprete, cancionCargada.titulo)
		cancionACargar = lista.sucesor(nodoCancion)
		if cancionACargar is not None:
			cancionACargar = cancionACargar.cancion
			reproductor.parar()
			reproductor.cargarCancion(cancionACargar)
			reproductor.reproducir()
			return cancionACargar
	return cancionCargada

def prepararReproductor(cancionCargada:object) -> "void":
	
	reproductor = Reproductor(cancionCargada)	

	return reproductor

def pausarCancion(reproductor:object) -> "void":

	reproductor.pausa()

def pararCancion(reproductor:object) -> "void":

	reproductor.parar()

# Dibujo en la interfaz
def mostrarCancionesEnSecuenciaParcial(canciones:list) -> "void":
	posY = 25
	pYReferenciaACanciones = []
	for cancion in canciones:
		pYReferencia = []
		interprete, titulo = cancion.interprete, cancion.titulo
		texto = interprete + " - " + titulo
		texto = escrituraParcial(texto, 55, 4)
		mensaje = fuentePequena.render(texto, 1, (255, 255,255))
		pYReferencia.append(ventana.blit(mensaje, (25, posY)))
		pYReferencia.append(cancion)
		pYReferenciaACanciones.append(pYReferencia)
		posY = posY + 32
		

	return pYReferenciaACanciones

def dibujarReproductor(cancionCargada:object) -> "void":
	# Dibujar fondo
	ventana.blit(fondo, (0,0))

	# Dibujar botones
	ventana.blit(botonPausa, (40, 25))
	ventana.blit(botonParar, (160, 25))
	ventana.blit(botonReproducir, (280, 25))
	ventana.blit(botonSiguienteCancion, (400, 25))
	ventana.blit(botonCargarCancion, (670, 25))
	ventana.blit(botonMostrar, (580, 35))
	ventana.blit(botonSalir, (715, 145))
	ventana.blit(cancionActual, (25, 225))

	suenaActualmente(cancionCargada)

def suenaActualmente(cancionCargada:object):
	texto = "Suena:"
	mensaje = fuente.render(texto, 1, (255, 255,255))
	ventana.blit(mensaje, (50, 170))

	if cancionCargada is not None:
		interprete = convertirAMinuscula(cancionCargada.interprete)
		texto = "Artista: " + escrituraParcial(interprete, 30, 4)
		mensaje = fuente.render(texto, 1, (255,255,255))
		ventana.blit(mensaje, (30, 225))

		titulo = convertirAMinuscula(cancionCargada.titulo)
		texto = "Titulo: " + escrituraParcial(titulo, 30, 4)
		mensaje = fuente.render(texto, 1, (255,255,255))
		ventana.blit(mensaje, (30, 275))

	pygame.display.flip()

# Manipulación y modificación de strings
def escribir(caracteres:[str]) -> "void":

	ventana.blit(fondo, (0,0))
	cancelar()
	texto = "Ingrese nombre del archivo: "
	mensaje = fuente.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (150, 25))
	pygame.display.flip()
	mensaje = str(caracteres)
	mensaje = fuente.render(mensaje, 1, (255,255,255))
	ventana.blit(mensaje, (40,100))
	if len(caracteres) > 0:
		texto = "Pulse enter para continuar"
		mensaje = fuente.render(texto, 1, (255,255,255))
		ventana.blit(mensaje, (200, 560))


	pygame.display.flip()

def escrituraParcial(frase: object, maxCaracteres:int, tiempoDetenido:int):
	pedazos = []
	bloques = math.ceil(len(frase) / maxCaracteres)
	for i in range(bloques):
		ini, fin = i*maxCaracteres, (i+1)*maxCaracteres
		pedazos.append(frase[ini:fin])

	
	rango = tiempoDetenido
	rango2 = rango / bloques

	tiempo = time.time()
	tiempo = tiempo % rango
	
	for i in range(bloques):
		
		if i*rango2 <= tiempo <= (i+1)*rango2:
			
			return pedazos[i]

def convertirAMinuscula(frase:list) -> list:
	temp = frase[0:1]
	temp2 = frase[1:len(frase)].lower()
	frase = temp + temp2
	return frase

# Botones
def botonVolver() -> object:
	volver = fuentePequena.render("Volver", 1, (255, 255, 255))
	volver = ventana.blit(volver, (710, 300))
	
	return volver

def botonEliminar() -> object:
	eliminar = fuentePequena.render("Eliminar", 1, (255, 255, 255))
	eliminar = ventana.blit(eliminar, (25, 300))
	
	return eliminar

def cancelar() -> object:
	cancelar = fuente.render("Cancelar", 1, (255, 255, 255))
	cCancelar = ventana.blit(cancelar, (600, 300))
	
	return cCancelar

def eliminarCancion(lista, pYReferenciaACanciones:list) -> "void":

	mensajeDeEliminar()

	while True:

		for event in pygame.event.get():
				if event.type == QUIT:
					exit()

				elif event.type == pygame.MOUSEBUTTONUP:
					posicionMouse = pygame.mouse.get_pos()

					for pYReferencia in pYReferenciaACanciones:
						

						if pYReferencia[0].collidepoint(posicionMouse):
							if pYReferencia[1] is cancionCargada:
								mensajeDeNoSePuedeEliminar()
								return

							interprete = pYReferencia[1].interprete
							titulo = pYReferencia[1].titulo
							lista.eliminarCancion(interprete, titulo)
							mensajeDeEliminado()

							return					
					return

def botonesDeNavegacion() -> object:
	p = ventana.blit(flechaDerecha, (590, 300))
	q = ventana.blit(flechaIzquierda, (490, 300))
	return p, q

# Mensajes
def mensajeCargarOtroArchivo() -> "void":

	ventana.blit(fondo, (0,0))
	texto = "¿Quiere cargar otro archivo?"
	mensaje = fuente.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (150,50))
	texto = "Sí"
	mensaje = fuente.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (250,150))
	texto = "No"
	mensaje = fuente.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (450,150))
	pygame.display.flip()

def mensajeDeEliminar() -> "void":
	mensaje = fuentePequena.render("Seleccione la canción", 1, (255,255,255))
	ventana.blit(mensaje, (160, 290))
	mensaje = fuentePequena.render("a eliminar", 1, (255,255,255))
	ventana.blit(mensaje, (160, 320))
	pygame.display.flip()

def mensajeDeEliminado() -> "void":
	borra = pygame.transform.scale(fondo, (300, 200))
	mensaje = fuentePequena.render("Cancion eliminada", 1, (255,255,255))
	ventana.blit(borra, (160, 290))
	ventana.blit(mensaje, (160, 305))
	pygame.display.flip()
	pygame.time.delay(400)

def mensajeDeDebeCargarCancion() -> "void":
	texto = "Debe cargar una lista de reproducción"
	mensaje = fuentePequena.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (210, 130))
	pygame.display.flip()
	pygame.time.delay(600)

def mensajeDeNoSePuedeEliminar() -> "void":
	borra = pygame.transform.scale(fondo, (800, 119))
	texto = "No se puede eliminar la canción que se está reproduciendo"
	mensaje = fuentePequena.render(texto, 1, (255,255,255))
	ventana.blit(borra, (0 , 290))
	ventana.blit(mensaje, (25, 300))
	pygame.display.flip()
	pygame.time.delay(1200)



# Fuentes
fuente = pygame.font.Font("fonts/BOOKOS.ttf", 40)
fuentePequena = pygame.font.Font("fonts/BOOKOS.ttf", 25)

# Imagenes
botonCargarCancion = pygame.image.load("images/LoadButton.png")
botonSiguienteCancion = pygame.image.load("images/NextSongButton.png")
botonPausa = pygame.image.load("images/PauseButton.png")
botonReproducir = pygame.image.load("images/PlayButton.png")
botonParar = pygame.image.load("images/StopButton.png")
botonSalir = pygame.image.load("images/ExitButton.png")
botonMostrar = pygame.image.load("images/ShowButton.png")
cancionActual = pygame.image.load("images/CurrentSong.png")
panelDeCanciones = pygame.image.load("images/ShowSongsPanel.png")
flechaDerecha = pygame.image.load("images/RightArrow.png")
flechaIzquierda = pygame.image.load("images/LeftArrow.png")

fondo = pygame.image.load("images/Background.png")

ventana = pygame.display.set_mode((800, 350))
pygame.display.set_caption("Reproductor de música")

# Dibujar fondo
ventana.blit(fondo, (0,0))

# Dibujar botones y guardar posición
pBotonPausa = ventana.blit(botonPausa, (40, 25))
pBotonParar = ventana.blit(botonParar, (160, 25))
pBotonReproducir = ventana.blit(botonReproducir, (280, 25))
pBotonSiguienteCancion = ventana.blit(botonSiguienteCancion, (400, 25))
pBotonCargarCancion = ventana.blit(botonCargarCancion, (670, 25))
pBotonMostrar = ventana.blit(botonMostrar, (580, 35))
pBotonSalir = ventana.blit(botonSalir, (715, 145))
pCancionActual = ventana.blit(cancionActual, (25, 225))

# Suena actualmente
texto = "Suena:"
mensaje = fuente.render(texto, 1, (255, 255,255))
ventana.blit(mensaje, (50, 170))

pygame.display.flip()

# Se inicia con una lista de reproducción vacía
lista = ArbolDeCanciones()
cancionCargada = None
reproductor = None
cancionParada = True


while True:

	while reproductor == None or reproductor.estaTocandoCancion() or cancionParada:

		dibujarReproductor(cancionCargada)

		for event in pygame.event.get():
				if event.type == QUIT:
					exit()

				elif event.type == pygame.MOUSEBUTTONUP:

					if pBotonReproducir.collidepoint(pygame.mouse.get_pos()):
						if cancionCargada is None:
							mensajeDeDebeCargarCancion()
						else:
							reproducirCancion(reproductor)
							cancionParada = False
							

					elif pBotonSiguienteCancion.collidepoint(pygame.mouse.get_pos()):
						cancionCargada = siguienteCancion(lista, cancionCargada, reproductor)

					elif pBotonCargarCancion.collidepoint(pygame.mouse.get_pos()):
						lista, cancionCargada, reproductor = cargarCanciones(lista, cancionCargada, reproductor)

					elif pBotonMostrar.collidepoint(pygame.mouse.get_pos()):
						mostrarLista(lista)

					elif pBotonPausa.collidepoint(pygame.mouse.get_pos()) and not cancionParada:
						pausarCancion(reproductor)
						cancionParada = True

					elif cancionCargada is not None and pBotonParar.collidepoint(pygame.mouse.get_pos()):
						pararCancion(reproductor)
						cancionParada = True

					elif pBotonSalir.collidepoint(pygame.mouse.get_pos()):
						exit()

	cancionCargada = siguienteCancion(lista, cancionCargada, reproductor)
			
			
				
				
				

			