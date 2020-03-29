import cancion
import reproductor


cancion = cancion.Cancion("Blind", "Beast in Black", "/home/jesus/Documents/07. Crazy_ Mad_ Insane.mp3")

reproductor = reproductor.Reproductor(cancion)

reproductor.reproducir()

while True:
	pass