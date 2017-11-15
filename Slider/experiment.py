# Experimento de analisis de la gestualidad del ojo humano en relacion a un robot industrial colaborativo. 
# Ignacio Fourmentel, Universidad Nacional de Tres de Febrero.
# contact: ignacio.fourmentel@gmail.com
#
# version 1 (25 april 2017)

# Nativos de python
import os
import random

# PyGaze
from constants import *
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from pygaze.eyetracker import EyeTracker
from pygaze.liblog import Logfile
import pygaze.libtime as timer

# # # # #
# SETUP
# visuals
disp = Display()
scr = Screen()
# input
kb = Keyboard()
tracker = EyeTracker(disp)
# output
log = Logfile()
log.write(["NumeroDePrueba","Imagen","TiempoDeImagen"])


# # # # #
# Preparacion del expermiento

# Cargamos las instrucciones desde un archivo.
instfile = open(INSTFILE)
instructions = instfile.read()
instfile.close()

# Leemos el directorio de las imagenes.
images = os.listdir(IMGDIR)
prueba = 1

# Instrucciones.
scr.draw_text(text="Presiona cualquier tecla para comenzar la calibracion.", fontsize=TEXTSIZE)
disp.fill(scr)
disp.show()

# Esperamos la tecla.
kb.get_key(keylist=None, timeout=None, flush=True)

# Calibracion
tracker.calibrate()


# # # # #
# Comienza el experimento.

# Display de instrucciones.
scr.clear()
scr.draw_text(text=instructions, fontsize=TEXTSIZE)
disp.fill(scr)
disp.show()

# Esperamos tecla
kb.get_key(keylist=None, timeout=None, flush=True)

# loop trials
ntrials = len(images)
for trialnr in range(ntrials):
	
	# PREPARACION DE LOS TRIALS
	# presentamos imagen.
	scr.clear()
	scr.draw_image(os.path.join(IMGDIR,images[trialnr]))

	# drift check  se puede sacar a posteiori.
	tracker.drift_correction()
	
	# CORRE EL  TRIAL
	# comenzamos a trackear.
	tracker.start_recording()
	tracker.log("TRIALSTART %d" % trialnr)
	tracker.log("IMAGENAME %s" % images[trialnr])
	tracker.status_msg("trial %d/%d" % (trialnr+1, ntrials))
	
	# presentamos imagen
	disp.fill(scr)
	t0 = disp.show()
	tracker.log("image online at %d" % t0)
	
	# Esperamos el tiempo de prueba establecido.
	timer.pause(TRIALTIME)
			
	# Limpiamos el screen
	disp.fill()
	t1 = disp.show()
	tracker.log("image offline at %d" % t1)
	# Frenamos el recording del eyetracker.
	tracker.stop_recording()
	
	# FIN TRIAL
	# logeo..
	log.write([trialnr, images[trialnr], t1-t0])
	
	# inter trial interval
	timer.pause(ITI)


# # # # #
# CIERRE

# MENSAJE..
scr.clear()
scr.draw_text(text="Transfiriendo data files... Espere.", fontsize=TEXTSIZE)
disp.fill(scr)
disp.show()

# cerramos conexion con el tracker
# enviamos los datos a la pc.
tracker.close()

# cerramos el log.
log.close()

# Mensaje de salida.
scr.clear()
scr.draw_text(text="Este es el final de el experimento. Gracias por participar! !\n\n(Presione cualquier tecla para salir)", fontsize=TEXTSIZE)
disp.fill(scr)
disp.show()

# Esperamos tecla..
kb.get_key(keylist=None, timeout=None, flush=True)

# Cierra display
disp.close()
