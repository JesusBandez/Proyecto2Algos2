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

		# Precondicion
		assert(True)

		# Se guarda la canción cargada
		self.actual = cancion

		# Se establece que la canción no está pausada
		self.pausado = False

		# Inicializar la librería de audio
		pygame.mixer.init()

		# Cargar la canción en el reproductor
		pygame.mixer.music.load(cancion.ubicacion)

		# Postcondicion
		assert(self.actual is cancion)

	def cargarCancion(self, cancion:object):
		""" Método para cargar la canción recibida como argumento en
		el reproductor

		cancion: objeto del tipo canción
		"""

		# Precondicion
		assert(True)

		# Se define la nueva cancion
		self.actual = cancion

		# Se establece que no está pausado el reproductor
		self.pausado = False

		# Se carga la canción
		pygame.mixer.music.load(cancion.ubicacion)

		# Postcondicion
		assert(self.actual == cancion)

	def reproducir(self):
		""" Método para reproducir la canción
		"""

		# Precondicion
		assert(True)

		# Si la canción está pausada, entonces se continúa la reproducción
		if self.pausado == True:
			pygame.mixer.music.unpause()
			self.pausado = False

		# En cualquier otro caso, se reproduce la canción desde el principio
		else:
			pygame.mixer.music.play(0)

		# Postcondicion
		assert(self.estaTocandoCancion())

	def parar(self):
		""" Método para parar la canción
		"""

		# Precondicion
		assert(True)

		# Se establece que la canción no está pausada
		self.pausado = False

		# Detener la reproducción
		pygame.mixer.music.stop()
	
		# Postcondicion
		assert(not self.estaTocandoCancion())

	def pausa(self):
		""" Método para pausar la canción
		"""

		# Precondicion
		assert(True)

		# Establece que la canción está pausada
		self.pausado = True

		# Pausar la canción
		pygame.mixer.music.pause()

		# Postcondicion
		assert(not self.estaTocandoCancion())

	def estaTocandoCancion(self) -> bool:
		""" Método para saber si el reproductor está reproduciendo audio
		"""

		# Precondicion
		assert(True)
		# Se obtiene si el reproductor está reproduciendo audio o está pausado
		tocando = pygame.mixer.music.get_busy()

		# Si está reproduciendo audio y no está pausada la canción, se retorna
		# True
		if tocando == 1 and not self.pausado:
			return True

		# En cualquier otro caso, se retorna False
		else:
			return False

		# Postcondicion
		assert(True)

		# Es necesario comprobar que la canción no está pausada por que
		# el método get_busy() de pygame retorna 1 cuando la canción se
		# encuentra en estado de pausa.