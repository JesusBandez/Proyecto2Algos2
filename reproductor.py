import pygame.mixer

class Reproductor(object):
	""" Clase Reproductor
	Clase que implementa las operaciones de un reproductor de música
	"""

	def __init__(self, cancion:object):
		"""Constructor de la clase. La clase se crea inicializando la 
		librería de audio y cargando la canción que se recibe como argumento

		cancion: objeto del tipo canción
		"""

		# Se guarda la canción cargada
		self.actual = cancion

		# Se establece que la canción no está pausada
		self.pausado = False

		# Inicializar la librería de audio
		pygame.mixer.init()

		# Cargar la canción en el reproductor
		pygame.mixer.music.load(cancion.ubicacion)

	def cargarCancion(self, cancion:object):
		""" Método para cargar la canción recibida como argumento en
		el reproductor

		cancion: objeto del tipo canción
		"""
		self.actual = cancion
		self.pausado = False
		pygame.mixer.music.load(cancion.ubicacion)

	def reproducir(self):
		""" Método para reproducir la canción
		"""

		# Si la canción está pausada, entonces se continúa la reproducción
		if self.pausado == True:
			pygame.mixer.music.unpause()
			self.pausado = False

		# En cualquier otro caso, se reproduce la canción desde el principio
		else:
			pygame.mixer.music.play()

	def parar(self):
		""" Método para parar la canción
		"""

		# Se establece que la canción no está pausada
		self.pausado = False

		# Detener la reproducción
		pygame.mixer.music.stop()

	def pausa(self):
		""" Método para pausar la canción
		"""

		# Establece que la canción está pausada
		self.pausado = True

		# Pausar la canción
		pygame.mixer.music.pause()

	def estaTocandoCancion(self) -> bool:
		""" Método para saber si el reproductor está reproduciendo audio
		"""

		# Se obtiene si el reproductor está reproduciendo audio o está pausado
		tocando = pygame.mixer.music.get_busy()

		# Si está reproduciendo audio y no está pausada la canción, se retorna
		# True
		if tocando == 1 and not self.pausado:
			return True

		# En cualquier otro caso, se retorna False
		else:
			return False

		# Es necesario comprobar que la canción no está pausada por que
		# el método get_busy() de pygame retorna 1 cuando la canción se
		# encuentra en estado de pausa.