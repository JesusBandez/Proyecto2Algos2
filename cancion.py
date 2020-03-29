import re
import os.path as path

class Cancion(object):
	"""Clase Cancion
		Se establece la estructura Canción
		incluida su ubicacion en el sistema de ficheros
		con ruta absoluta
	"""

	#Constructor
	def __init__(self, interprete : str, titulo : str, ubicacion : str):
		try:
			#Invariante de la representacion
			assert(
				titulo != None and interprete !=None
				and ubicacion!=None and self.esUbicacionValida(ubicacion))

			#Estableciendo atributos
			if len(titulo)>0:
				self.titulo = titulo
			else:
				self.titulo = "Desconocido"
			if len(interprete)>0:
				self.interprete = interprete
			else:
				self.interprete = "Desconocido"

			self.ubicacion = ubicacion

		#Manejando errores en la inicializacion de la estructura
		except:
			print("Error Inicializando la estructura Canción")
			if not self.esUbicacionValida(ubicacion):
				print("La ubicacion de la cancion no es válida o no existe el archivo")
				print("Recuerde que la extenciones validas son .mp3 y .wav")
			if titulo == None:
				print("La canción debe poseer un titulo")
			if interprete == None:
				print("La canción debe poseer un interprete")
			if ubicacion==None:
				print("Debe indicar la ruta de la canción a crear")

	def esUbicacionValida(self, ubicacion : str) -> bool:
		
		"""Mediante REGEX verificamos si la secuencia 
			corresponde a la expresion regular buscada
			y si su extención es mp3 o wav.

			Luego verificamos que el archivo exista dentro del sistema
			de ficheros
		"""
		pattern_valid = re.compile(r"/home/[a-zA-Z0-9\./]*/.*\.(mp3|wav)$")
		exists = path.isfile(ubicacion)

		if pattern_valid.match(ubicacion) and exists:
			return True

		return False

	def aString(self) -> str:
		return "Interprete: "+ self.interprete + "; Titulo: " + self.titulo

#Funcion informativa de la clase cancion
def about():
	print("\n\tSINTAXIS")
	print(">>  cancion = cancion.cancion(titulo : str, interprete : str, ubicacion : str)")
	print("\n\t¡RECUERDA!\nLa ubicacion es una ruta absoluta en el sistema de ficheros tipo unix\n")
	print("\n\tMETODOS:")
	print("\n>> aString() -> str \tRetorna titulo e interprete\n")


if __name__ == '__main__':
	about()