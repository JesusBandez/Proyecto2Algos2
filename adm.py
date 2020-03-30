from cancion import *
from reproductor import *
from lr import *
import pygame
from pygame.locals import *
import math
import time




# Manipulación del reproductor
def cargarOtroArchivo() -> str:
	""" Funcion para preguntar al usuario si quiere ingresar el nombre
	de otro archivo
	"""

	# Se muestra el mensaje al usuario y se dibujan las opciones: "Si" y "No"
	mensajeCargarOtroArchivo()

	# Se asignan unas coordenadas
	coordenadas = (0,0)

	while coordenadas == (0,0):
		# Bucle para mantener la pantalla y obtener la decision del usuario

		# Se itera entre los eventos de pygame
		for event in pygame.event.get():

			# Si da a salir, se cierra el programa
			if event.type == QUIT:
				exit()

			# Se obtiene la elección del usuario determinando si selecció
			# el botón de "Sí" o "No"
			elif event.type == pygame.MOUSEBUTTONUP:			
				coordenadas = pygame.mouse.get_pos()
				if 200 <= coordenadas[0] <= 285 and 150 <= coordenadas[1] <= 190:
					otro = "si"
				elif 450 <= coordenadas[0] <= 500 and 150 <= coordenadas[1] <= 190:
					otro = "no"
				# Si el usuario no selecciona ninguno de los dos, se espera
				# a que elija alguno
				else:
					coordenadas = (0,0)

	# Se retorna la elección del usuario
	return otro

def cargarCanciones(lista:object, reproductor:object) -> object:
	""" Funcion que permite la carga de canciones en el reproductor 
	desde los archivos

	lista: Arbol Binario de canciones
	reproductor: Objeto para reproducir las canciones
	"""

	# Dibujar el fondo de la interfaz
	ventana.blit(fondo, (0,0))	

	# arreglo para guardar los archivos leídos
	archivos = []

	otro = "si"
	while otro == "si":
		# Bucle para pedir al usuario los nombres de los archivos y 
		# agregar sus canciones a la lista
		nombreArchivo = pedirArchivo()

		if nombreArchivo is None:
			# Romper el bucle cuando el usuario no quiera agregar más
			# archivos	
			break

		try:
			# Se intenta abrir el archivo, si falla, se notifica
			open(nombreArchivo, "r")

			# Guardar el archivo leido
			archivos.append(nombreArchivo)

			# Preguntar al usuario si agregará otro archivo
			otro = cargarOtroArchivo()		
		except:
			# Mensaje de error si no se encuentra un archivo o no se 
			# puede abrir
			mensajeDeErrorAlAbrirArchivo()
			

	# Iterar entre los nombres de los archivos ingresados por el usuario
	for nombre in archivos:

		# Se intenta agregar las canciones del archivo a la lista
		try:
			lista.agregarLista(nombre)
		except:
			# Si no se puede, se le avisa al usuario por interfaz y 
			# por terminal
			mensajeDeAlgunasCancionesNoSeCargaron()
	
	# Si el usuario ingresó nombres de archivos, no se ha creado un
	# reproductor y hay al menos una canción en la lista.
	if (len(archivos) > 0 and reproductor is None
		and lista.root is not None):

		# Se consigue la cancion a cargar, la cual será la que tenga
		# el minimo interprete en orden lexicográfico, se crea un 
		# reproductor y se carga la canción en él
		cancionACargar = lista.minInterprete(lista.root).cancion
		reproductor = prepararReproductor(cancionACargar)		

	# Se retorna la lista de reproducción y el reproductor
	return lista, reproductor

def pedirArchivo() -> str:
	""" Función para mostrar y pedir el nombre del archivo de donde se 
	cargará las canciones a la lista al usuario por medio de la interfaz
	"""

	# Se crean variables de tipo string para guardar las entradas del 
	# usuario
	caracteres = ""
	asignado = ""

	# Se escriben en pantalla los caracteres actuales
	escribir(caracteres)

	# Se muestra en la interfaz un botón de para cancelar, y se guarda
	# su posición
	cCancelar = cancelar()

	while asignado == "":
		# Bucle para que el usuario inserte los caracteres que conforman
		# el nombre del archivo


		# Se obtiene los eventos de pygame y se iteran por ellos
		for event in pygame.event.get():
			
			# Si se pulsa el botón de cancelar, se sale de la interfaz
			# y se vuelve a los controles del reproductor
			if event.type == pygame.MOUSEBUTTONUP:
				if cCancelar.collidepoint(pygame.mouse.get_pos()):
					return None

			# Si se pulsa una tecla
			if event.type == KEYDOWN:

				# Si es backspace, se borra el último caracter ingresado
				# por el usuario
				if event.key == K_BACKSPACE:
					caracteres = caracteres[0:len(caracteres)-1]

				# Si es enter y la cantidad de caracteres que ingresó el				
				# el usuario es mayor que 0, se guardan los caracteres y
				# se sale del bucle

				elif event.key == K_RETURN:
					if len(caracteres) > 0:

						asignado = caracteres	

				# Se limita la cantidad de caracteres que puede ingresar
				# el usuario a 120.
				elif len(caracteres) > 120:
					pass

				# En cualquier otro caso, se consigue la letra o simbolo
				# que pulsó el usuario y se guarda
				else:						
					caracteres = caracteres + event.unicode	

				# Se escribe en la interfaz el nombre que ha ido escribiendo
				# el usuario
				escribir(caracteres)

			# Si se pulsa el boton salir, se sale
			elif event.type == QUIT:
				exit()

			
	# Se retornan la string formada por los caracteres que ingresó el
	# usuario
	return caracteres

def mostrarLista(lista:object) -> "void":
	""" Procedimiento que muestra por la interfaz las canciones que
	se han cargado en la lista. Así mismo, en esta pantalla es posible
	elegir si se quiere eliminar una canción de la interfaz.

	lista: Arbol Binario con las canciones
	"""

	# Se dibujan y guardan las posiciones de dos botones que permitiran
	# al usuario navegar por la lista de canciones si esta es mayor
	# a 8 canciones
	pFlechaDerecha, pFlechaizquierda = botonesDeNavegacion()

	# Se dibuja y guarda la posicion de un botón para permitir al usuario
	# volver a la pantalla del reproductor
	pVolver = botonVolver()

	# Se dibuja y guarda la posicion de un boton que permite eliminar
	# canciones de la lista de reproducción
	pEliminar = botonEliminar()

	# Se declaran las variables que permitirá partir la lista en pedazos
	# para mostrarla al usuario
	ini, fin = 0, 8	

	while True:
		# Se dibuja el fondo de la pantalla y los botones
		ventana.blit(fondo, (0,0))
		botonesDeNavegacion()
		botonVolver()
		botonEliminar()

		# Se dibuja el panel donde se escribirán los interpretes y los 
		# titulos de las canciones
		ventana.blit(panelDeCanciones, (25, 25))
		
		# Se obtiene la lista de reproducción en el orden en el que 
		# se van a reproducir
		canciones = lista.obtenerLR()
		
		# Se obtiene de la funcion un arreglo de arreglos de tamaño: 2
		# Estos arreglos guardan en su primera casilla la posición de
		# la canción en la pantalla y en su segunda casilla una referencia
		# a al nodo de la canció en el arbol
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
	if not reproductor.estaTocandoCancion():
		reproductor.reproducir()
	else:
		pass

def siguienteCancion(lista:object, reproductor:object) -> object:
	if reproductor is not None:
		nodoCancion = lista.buscarCancion(lista.root, reproductor.actual.interprete, reproductor.actual.titulo)
		cancionACargar = lista.sucesor(nodoCancion)
		if cancionACargar is not None:
			cancionACargar = cancionACargar.cancion
			reproductor.parar()
			reproductor.cargarCancion(cancionACargar)
			reproductor.reproducir()

			return reproductor.actual


		return reproductor.actual
			
	

def prepararReproductor(cancionACargar:object) -> "void":
	
	reproductor = Reproductor(cancionACargar)	

	return reproductor

def pausarCancion(reproductor:object) -> "void":

	reproductor.pausa()

def pararCancion(reproductor:object) -> "void":

	reproductor.parar()

def cancionAnterior(lista:object, reproductor:object) -> object:
	if reproductor is not None:
		nodoCancion = lista.buscarCancion(lista.root, reproductor.actual.interprete, reproductor.actual.titulo)
		cancionACargar = lista.predecesor(nodoCancion)
		if cancionACargar is not None:
			cancionACargar = cancionACargar.cancion
			reproductor.parar()
			reproductor.cargarCancion(cancionACargar)
			reproductor.reproducir()
			
	

# Dibujo en la interfaz
def mostrarCancionesEnSecuenciaParcial(canciones:list) -> list:
	"""  Funcion que dibuja de forma parcial las canciones en la lista
	de canciones. La función obtiene solo un pedazo de la lista completa
	en caso de ser muy grande y va dibujando en la interfaz este pedazo
	de la lista. Tambien, un arreglo que contiene arreglos de tamaño dos
	Los cuales tiene en su primera casilla la posición en la pantalla de 
	la canción y una referencia a la canción
	"""
	# Se establece la distancia a la que se dibujarán las canciones
	# en la pantalla
	posY = 25

	# Se genera al arreglo que se retornará para llenarlo
	pYReferenciaACanciones = []

	# Se itera entre cada canción en la lista canciones
	for cancion in canciones:

		# Generar un arreglo vacío
		pYReferencia = []

		# obtener el interprete y el titulo de la cancion y se unen,
		# separados por " - "
		interprete, titulo = cancion.interprete, cancion.titulo		
		texto = interprete + " - " + titulo

		# Se dibujan en la interfaz el nombre "-" interprete de la cancion.
		# Ademas, se obtiene mediante escritura parcial() el texto a escribir en 
		# la pantalla
		texto = escrituraParcial(texto, 55, 4)
		mensaje = fuentePequena.render(texto, 1, (255, 255,255))

		# Se guarda la posición de la canción en la pantalla
		pYReferencia.append(ventana.blit(mensaje, (25, posY)))

		# Se guarda la referencia en la cancion
		pYReferencia.append(cancion)

		# Luego, se guarda el arreglo dentro del arreglo que se va a
		# retorna
		pYReferenciaACanciones.append(pYReferencia)

		# Calcular la posicion donde se dibujará la siguiente canción
		posY = posY + 32
		
	# Retornar el arreglo de arreglos que tienen las posiciones y las 
	# referencias a las canciones
	return pYReferenciaACanciones

def dibujarReproductor(reproductor:object) -> "void":
	# Dibujar fondo
	ventana.blit(fondo, (0,0))

	# Dibujar botones
	ventana.blit(botonPausa, (25, 25))
	ventana.blit(botonParar, (130, 25))
	ventana.blit(botonReproducir, (235, 25))
	ventana.blit(botonCancionAnterior, (340, 25))
	ventana.blit(botonSiguienteCancion, (445, 25))
	ventana.blit(botonCargarCancion, (670, 25))
	ventana.blit(botonMostrar, (580, 35))
	ventana.blit(botonSalir, (715, 145))
	ventana.blit(cancionActual, (25, 225))
	mensajesSobreBotones()
	suenaActualmente(reproductor)

def suenaActualmente(reproductor:object):
	texto = "Suena:"
	mensaje = fuente.render(texto, 1, (255, 255,255))
	ventana.blit(mensaje, (50, 170))

	if reproductor is not None:
		interprete = convertirAMinuscula(reproductor.actual.interprete)
		texto = "Artista: " + escrituraParcial(interprete, 30, 4)
		mensaje = fuente.render(texto, 1, (255,255,255))
		ventana.blit(mensaje, (30, 225))

		titulo = convertirAMinuscula(reproductor.actual.titulo)
		texto = "Titulo: " + escrituraParcial(titulo, 30, 4)
		mensaje = fuente.render(texto, 1, (255,255,255))
		ventana.blit(mensaje, (30, 275))

	pygame.display.flip()

# Manipulación y modificación de strings
def escribir(caracteres:[str]) -> "void":

	ventana.blit(fondo, (0,0))
	cancelar()
	texto = "Ingrese el nombre o la ruta del archivo con la lista de canciones: "
	mensaje = fuentePequena.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (50, 25))
	
	mensaje = str(caracteres[0:41])
	mensaje = fuentePequena.render(mensaje, 1, (255,255,255))
	ventana.blit(mensaje, (5,100))

	mensaje = str(caracteres[41:82])
	mensaje = fuentePequena.render(mensaje, 1, (255,255,255))
	ventana.blit(mensaje, (5,120))

	mensaje = str(caracteres[82:123])
	mensaje = fuentePequena.render(mensaje, 1, (255,255,255))
	ventana.blit(mensaje, (5, 140))

	if len(caracteres) > 0:
		texto = "Pulse enter para continuar"
		mensaje = fuentePequena.render(texto, 1, (255,255,255))
		ventana.blit(mensaje, (100, 310))


	pygame.display.flip()

def escrituraParcial(frase: object, maxCaracteres:int, tiempoDetenido:int) -> str:
	""" Función que toma una string y la parte en pedazos de tamaño determinado y
	retorna uno de estos pedazos dependiendo del tiempo
	
	frase: string que se partirá en pedazos

	maxCaracteres: Determina la máxima cantidad de carácteres
		que puede tener cada pedazo 

	tiempoDetenido: Cantidad de tiempo que determina la espera para retornar
		cada pedazo
	"""

	# Arreglo que guardará los pedazos de la frase
	pedazos = []

	# Se obtiene la cantidad de pedazos posibles
	bloques = math.ceil(len(frase) / maxCaracteres)

	# Se corta la string en los posibles bloques
	for i in range(bloques):
		ini, fin = i*maxCaracteres, (i+1)*maxCaracteres
		pedazos.append(frase[ini:fin])

	# Se obtienen los rangos posibles
	rango = tiempoDetenido
	rango2 = rango / bloques

	# Tiempo desde que inició el programa
	tiempo = time.time()
	tiempo = tiempo % rango
	
	# Itera entre los bloques posibles
	for i in range(bloques):
		
		# Si tiempo está en el rango del bloque se retorna el pedazo
		# que corresponde al bloque
		if i*rango2 <= tiempo <= (i+1)*rango2:
			
			return pedazos[i]

def convertirAMinuscula(frase:list) -> list:
	temp = frase[0:1]
	temp2 = frase[1:len(frase)].lower()
	frase = temp + temp2
	return frase

# Botones
def botonVolver() -> object:
	""" Funcion que dibuja un boton que permite volver a la pantalla del
	reproductor al usuario y retorna la posicion de este en la pantalla
	"""
	volver = fuentePequena.render("Volver", 1, (255, 255, 255))
	volver = ventana.blit(volver, (710, 300))
	
	return volver

def botonEliminar() -> object:
	""" Funcion que dibuja un boton que permite eliminar canciones de
	la lista de reproducción y retorna la posición de este
	"""
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
							if pYReferencia[1] is reproductor.actual:
								mensajeDeNoSePuedeEliminar()
								return

							interprete = pYReferencia[1].interprete
							titulo = pYReferencia[1].titulo
							lista.eliminarCancion(interprete, titulo)
							mensajeDeEliminado()

							return					
					return

def botonesDeNavegacion() -> object:
	""" Funcion que dibuja dos botones con forma de flecha y retorna
	la posicion de ambos
	"""
	p = ventana.blit(flechaDerecha, (590, 279))
	q = ventana.blit(flechaIzquierda, (480, 279))
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
	borra = pygame.transform.scale(placa, (300, 200))
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
	borra = pygame.transform.scale(placa, (800, 119))
	texto = "No se puede eliminar la canción que se está reproduciendo"
	mensaje = fuentePequena.render(texto, 1, (255,255,255))
	ventana.blit(borra, (0 , 290))
	ventana.blit(mensaje, (25, 300))
	pygame.display.flip()
	pygame.time.delay(1200)

def mensajesSobreBotones() -> "void":	
	mensaje = fuenteDiminuta.render("Cargar canciones:", 1, (220,220,220))
	ventana.blit(mensaje, (685, 12))
	mensaje = fuenteDiminuta.render("Mostrar lista", 1, (220,220,220))
	mensaje2 = fuenteDiminuta.render("de reproduccion:", 1, (220,220,220))
	ventana.blit(mensaje, (571, 15))
	ventana.blit(mensaje2, (571, 25))

def mensajeDeErrorAlAbrirArchivo() -> "void":
	ventana.blit(fondo, (0,0))
	texto = "No se pudo abrir ese archivo"
	mensaje = fuente.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (150, 100))
	pygame.display.flip()
	pygame.time.delay(1000)

def mensajeDeAlgunasCancionesNoSeCargaron() -> "void":
	ventana.blit(fondo, (0,0))
	texto = "No se pudieron cargar algunas canciones"
	mensaje = fuente.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (50, 50))
	texto = "Revise que el archivo con la lista de canciones"
	mensaje = fuentePequena.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (10, 120))
	texto = "tiene el formato válido"
	mensaje = fuentePequena.render(texto, 1, (255,255,255))
	ventana.blit(mensaje, (514, 120))
	pygame.display.flip()
	pygame.time.delay(4000)

# Inicializar pygame
pygame.init()

# Fuentes
fuente = pygame.font.Font("fonts/BOOKOS.ttf", 40)
fuentePequena = pygame.font.Font("fonts/BOOKOS.ttf", 25)
fuenteDiminuta = pygame.font.Font("fonts/BOOKOS.ttf", 10)

# Imagenes
botonCargarCancion = pygame.image.load("images/LoadButton.png")
botonSiguienteCancion = pygame.image.load("images/NextSongButton.png")
botonCancionAnterior = pygame.image.load("images/PreviousSongButton.png")
botonPausa = pygame.image.load("images/PauseButton.png")
botonReproducir = pygame.image.load("images/PlayButton.png")
botonParar = pygame.image.load("images/StopButton.png")
botonSalir = pygame.image.load("images/ExitButton.png")
botonMostrar = pygame.image.load("images/ShowButton.png")
cancionActual = pygame.image.load("images/CurrentSong.png")
panelDeCanciones = pygame.image.load("images/ShowSongsPanel.png")
flechaDerecha = pygame.image.load("images/RightArrow.png")
flechaIzquierda = pygame.image.load("images/LeftArrow.png")
placa = pygame.image.load("images/Borra.png")

fondo = pygame.image.load("images/Background.png")

ventana = pygame.display.set_mode((800, 350))
pygame.display.set_caption("Reproductor de música")

# Dibujar fondo
ventana.blit(fondo, (0,0))

# Dibujar botones y guardar posición
pBotonPausa = ventana.blit(botonPausa, (25, 25))
pBotonParar = ventana.blit(botonParar, (130, 25))
pBotonReproducir = ventana.blit(botonReproducir, (235, 25))
pBotonCancionAnterior = ventana.blit(botonCancionAnterior, (340, 25))
pBotonSiguienteCancion = ventana.blit(botonSiguienteCancion, (445, 25))
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
reproductor = None


while True:

	while reproductor is None or reproductor.estaTocandoCancion() or reproductor.parado or reproductor.pausado:

		

		dibujarReproductor(reproductor)

		for event in pygame.event.get():
				if event.type == QUIT:
					exit()

				elif event.type == pygame.MOUSEBUTTONUP:

					if (pBotonPausa.collidepoint(pygame.mouse.get_pos()) and reproductor is not None
						and not reproductor.parado):
						pausarCancion(reproductor)
						

					elif (pBotonParar.collidepoint(pygame.mouse.get_pos()) and reproductor is not None
						and not reproductor.pausado):
						pararCancion(reproductor)
						

					elif pBotonReproducir.collidepoint(pygame.mouse.get_pos()):
						if reproductor is None:
							mensajeDeDebeCargarCancion()

						else:
							reproducirCancion(reproductor)							
							
					elif pBotonCancionAnterior.collidepoint(pygame.mouse.get_pos()):
						cancionAnterior(lista, reproductor)


					elif pBotonSiguienteCancion.collidepoint(pygame.mouse.get_pos()):
						siguienteCancion(lista, reproductor)

					elif pBotonCargarCancion.collidepoint(pygame.mouse.get_pos()):
						lista, reproductor = cargarCanciones(lista, reproductor)

					elif pBotonMostrar.collidepoint(pygame.mouse.get_pos()):
						mostrarLista(lista)



					elif pBotonSalir.collidepoint(pygame.mouse.get_pos()):
						exit()



	if siguienteCancion(lista, reproductor) is reproductor.actual:
		reproductor.parar()
	else:
		siguienteCancion(lista, reproductor)

			
			
				
				
				

			