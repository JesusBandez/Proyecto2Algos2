#########################################
#			LISTA DE REPRODUCCION 		#
#	En este archivo encontrará:			#
# -> Estructura NodoCancion 			#
# -> Estructura Arbol de Canciones 		#
#										#
#	Requerimientos: 					#
# -> Modulo cancion.py   				#
#										#
#########################################



import cancion



"""
	A continuación un conjunto de funciones que facilitan
	la creación de las estructuras de datos
	antes especificadas
"""

##########################################################

#Invariante de la representacion de Arboles de busqueda de canciones
def esArbolDeBusqCancion(T : object) -> bool:
	if T!=None:
		if T.right!=None:
			r = esMenor(T.cancion.interprete,T.cancion.titulo,T.right.cancion.interprete,T.right.cancion.titulo) and esArbolDeBusqCancion(T.right)
		else:
			r = True
		if T.left!=None:
			l = esMenor(T.left.cancion.interprete,T.left.cancion.titulo,T.cancion.interprete,T.cancion.titulo) and esArbolDeBusqCancion(T.left)
		else:
			l = True

		return (r and l)


#Dado un arbol, se listan sus nodos en orden
def deArbolASecuencia(subTree:object) -> list:
	seq = []
	if subTree != None :
		if subTree.left!=None:
			seq = seq + deArbolASecuencia(subTree.left)
		seq.append(subTree)
		if subTree.right != None:
			seq = seq + deArbolASecuencia(subTree.right)
	return seq


# Orden lexicografico entre el par <a1,b1> y <a2,b2> de strings
# donde <a1,b1> < <a2,b2> sii (a1 < a2) \/ (a1 == a2 /\ b1 < b2)

def esMenor(a1 : str, b1 : str, a2 : str, b2 : str):
	return (a1 < a2 or (a1 == a2 and b1 < b2))


"""Se lleva un registro de los titulos por interprete para cada lista de reproduccion
para hacerlos unicos. Luego si se desea introducir dos canciones iguales, la segunda cancion
es diferenciada con un indice
"""

def asignarAInterpreteTituloUnico(T : object, interp : str, tit : str, ub:str) -> list:

	assert(tit != None and interp !=None)

	#Por defecto el Autor es Desconocido
	if len(interp)>0:
		interprete = interp

	else:
		interprete = "Desconocido"


	#Si el interprete no esta pero se conoce la cancion
	if (interprete not in T.d) and len(tit) > 0:
		T.d.update({interprete:[[tit,1]]})
		titulo = tit

	#Si el interprete no esta y no se conoce la cancion
	elif (interprete not in T.d) and len(tit) == 0:
		T.d.update({interprete:[["Desconocido",1]]})
		titulo = "Desconocido"

	#Si el interprete esta...
	else:
		titulo = asignarTitulo(T.d.get(interprete),tit)

	return [interprete, titulo, ub]


#Funcion auxiliar para asiganarAInterpreteTituloUnico
def asignarTitulo(l : list, tit) -> str:

	n = len(l)
	assert(n>0)

	#Por defecto
	if len(tit) == 0:
		titulo = "Desconocido"
	else:
		titulo = tit

	assert(len(titulo)>0 and n > 0)

	#Buscamos en la lista el titulo
	i = 0
	while i < n and l[i][0]!=titulo:
		i = i + 1

	#Si no esta, se agrega
	if i == n:
		l.append([titulo,1])

	#si esta, se cuenta como repetido
	else:

		titulo = titulo + " {}".format(l[i][1])
		l[i][1] = l[i][1] + 1


	return titulo

####################################################

"""A continuacion la implementación de los TAD
 NodoCancion y ArbolDeCanciones
"""


"""
				ESTRUCTURA NODO
La estructura Nodo contiene una cancion para un ABB

						^
						| self.p
						|
				------------------
	self.left	|	----------	 |     self.right
		--------|	|Cancion |	 |--------
		|		|	----------	 |		 |
		|		------------------		 |
		V 								 V

self.p es el padre del nodo
self.left es el hijo izquierdo del nodo
self.right es el hijo derecho del nodo

"""
class NodoCancion(object) :

	"""Constructor de la Clase NodoCancion

		INPUT:
		Requiere especificar los atributos:
		Luego de los tres puntos un ejemplo valido
		-> Interprete ... Chopin
		-> Titulo     ... Vals de Primavera
		-> ubicación  ... /home/usuario/Documentos/cancion.mp3
		de la cancion
		que ira dentro del nodo

		OUTPUT:
		Tipo de dato NodoCancion, con la cancion de input dentro.
		Sin Padre ni hijos

	"""
	def __init__(self, interprete : str, titulo : str, ubicacion : str):
		self.cancion = cancion.Cancion(interprete, titulo, ubicacion)
		self.p = None
		self.left = None
		self.right = None





"""Estructura arbol de canciones, TAD que implementa
	un arbol binario de busqueda donde sus nodos son canciones
	ordenadas lexicograficamente por autor y si dos canciones
	tienen al mismo autor se prosigue a comparar lexicograficamente
	sus titulos.

							ESTRUCTURA ARBOL DE CANCIONES

									  ___________
					 ----------------| self.root |---------------
					 |				  ¯¯¯¯¯¯¯¯¯¯¯				|
		  	 ________V______ 						   _________V_____
		----| Nodo  Cancion |----				  ----| Nodo  Cancion |----		
		|	 ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯	|				  |	  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯   |
 _______V_______ 	 	 _______V_______		__V____________		______V________
| Nodo  Cancion |		| Nodo  Cancion |	   | Nodo  Cancion |   | Nodo  Cancion |
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯		 ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯		¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯		¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯


self.root es la raiz del arbol

"""


class ArbolDeCanciones(object):

	"""Constructor:
	Crea una instancia de ArbolDeCanciones inicialmente vacia
	con Raiz = None
	"""	
	
	def __init__(self):

		#NodoCancion Raiz
		self.root = None

		#Catalogo de Autores-Titulos
		self.d = {}


	"""
	Metodo que permite agregar al ArbolDeCanciones
	canciones guardadas en un archivo de texto plano
	donde por cada linea se encuentras registradas
	las especificaciones de la cancion 
	separadas por punto y coma ';' :

	Ejemplo de una linea contenida en el archivo:
	Mi_Interprete_Favorto;Cancion_de_él;/home/usuario/ruta/cancion_de_él.mp3

	Input: filepath
	"""
	def agregarLista(self, file : str) ->'void':
		f = open(file, 'r')
		for l in f.readlines():
			a = l.split(';')
			a[2] = a[2].rstrip('\n')
			b = asignarAInterpreteTituloUnico(self,a[0],a[1],a[2])
			self.insertarCancion(b[0],b[1],b[2])

		f.close()

	"""Se borra un NodoCancion del ArbolDeCancones especificado mediante el interprete y
	el titulo de la cancion que el nodo contiene.

	Input: Interprete de la cancion a borrar
		   Titulo de la cancion a borrar

	"""
	def eliminarCancion(self, interprete, titulo) -> 'void':

		z = self.buscarCancion(self.root, interprete, titulo)

		if z!=None:

			if z.left == None:
				self.trasplantar(z,z.right)

			elif z.right == None:
				self.trasplantar(z,z.left)

			else:
				y = self.minInterprete(z.right)

				if y.p != z:
					self.trasplantar(y,y.right)
					y.right = z.right
					y.right.p = y

				self.trasplantar(z,y)
				y.left = z.left
				y.left.p = y
				
			

		else:
			print("No se puede borrar el elemento")
			print("El elemento no pertenece a la lista")
	

	"""Metodo que retorna un nodo, raiz de un subarbol, al encontrar una cancion,
		dado su interprete y titulo
	"""
	def buscarCancion(self, subTree, interprete, titulo) -> NodoCancion:

		if (subTree is None or 
			(interprete == subTree.cancion.interprete and titulo == subTree.cancion.titulo)):

			return subTree

		if esMenor(interprete, titulo,
					subTree.cancion.interprete,subTree.cancion.titulo):

			return self.buscarCancion(subTree.left, interprete, titulo)

		else:

			return self.buscarCancion(subTree.right, interprete, titulo)


	"""Se Inserta una Cancion en el ABB como un NodoCancion, 
		dado el interprete, titulo y ubicacion
	"""
	def insertarCancion(self, interprete, titulo, ubicacion) -> 'void':

		assert(esArbolDeBusqCancion(self.root) or self.root == None)

		#Si No esta la cancion se agrega
		if self.root==None or self.buscarCancion(self.root, interprete, titulo)==None:

			z = NodoCancion(interprete, titulo, ubicacion)
			y = None
			
			x = self.root

			while x!=None:
				y = x
				if esMenor(z.cancion.interprete,z.cancion.titulo,x.cancion.interprete,x.cancion.titulo):
					x = x.left
				else:
					x = x.right
			z.p = y 

			if y == None:
				self.root = z
			elif esMenor(z.cancion.interprete,z.cancion.titulo,y.cancion.interprete,y.cancion.titulo):
				y.left = z
			else:
				y.right = z

		#Si ta existia, se informa pero no se hace nada
		else:
			pass
			#print("La Cancion ya estaba cargada en la lista")


	"""Retorna una lista de Canciones ordenada lixicograficamente con respecto a
		los interpretes de las canciones y los titulos de las canciones
	"""
	def obtenerLR(self) -> [cancion]:
		l = deArbolASecuencia(self.root)

		for x in range(len(l)):
			l[x] = l[x].cancion
		return l

	"""Muestra la Lista de Canciones en orden lexicogracico con respecto a
		los interpretes de las canciones y los titulos de las canciones
	"""

	def mostrarLR(self) -> 'void':
		l = self.obtenerLR()

		for x in range(len(l)):
			print(l[x].aString())


	#Retorna el NodoCancion con Interprete Minimo en el arbol
	def minInterprete(self, x) -> NodoCancion:

		while x.left != None:
			x = x.left
		return x

	#Retorna el NodoCancion con Interprete Maximo en el subarbol x
	def maxInterprete(self, x) -> NodoCancion:

		while x.right != None:
			x = x.right
		return x


	#Retorna el NodoCancion con titulo Maximo en el arbol
	def maxTitulo(self) -> NodoCancion:
		l = deArbolASecuencia(self.root)
		max = None
		for i in range(len(l)):
			if max == None or max.cancion.titulo < l[i].cancion.titulo:
				max = l[i]

		return max

	#Retorna el NodoCancion con titulo Maximo en el arbol
	def minTitulo(self) -> NodoCancion:
		l = deArbolASecuencia(self.root)
		min = None
		for i in range(len(l)):
			if min == None or min.cancion.titulo > l[i].cancion.titulo:
				min = l[i]
		return min

	#Transplantar subarbol u por subarbol v
	def trasplantar(self,u,v) -> 'void':
		
		if u.p == None:
			self.root = v
		elif u == u.p.left:
			u.p.left = v
		else:
			u.p.right = v

		if v != None:
			v.p = u.p


	#Retorna el NodoCancion Predecesor de un NodoCancion k
	def predecesor(self,k) -> NodoCancion:

		try:
			if k.left != None:
				return self.maxInterprete(k.left)

			y = k.p
			while y!= None and k == y.left:
				k = y
				y = y.p
			return y
		except: return None

	#Retorna el NodoCancion Sucesor de una NodoCancion k
	def sucesor(self,k) -> NodoCancion:
		try:
			if k.right!= None:
				return self.minInterprete(k.right)

			y = k.p
			while y != None and k == y.right:
				k = y
				y = y.p
			return y
		except:
			return None

def main():
	print("Implementacion de una lista de reproduccion mediante arbol binario de Busqueda")
	print("\n\tSINTAXIS")
	print(">>  ListaDeReproduccion = lr.arbolDeCanciones()\n")
	
if __name__ == '__main__':
	main()