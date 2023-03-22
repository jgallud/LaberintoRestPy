#!/usr/bin/python
import time
#import wx

class JuegoLaberinto:
	def __init__(self):
		self.laberinto=None
		self.bichos=list()
	def crearLaberinto2Hab(self,unAF):
		norte = Norte()
		sur = Sur()
		este = Este()
		oeste = Oeste()
		lab = unAF.fabricarLaberinto()
		hab1 = unAF.fabricarHabitacion(1)
		hab2 = unAF.fabricarHabitacion(2)
		pt = unAF.fabricarPuerta(hab1, hab2)
		hab1.ponerEn(norte,pt)
		hab2.ponerEn(sur,pt)
		hab1.ponerEn(este, unAF.fabricarPared())
		hab1.ponerEn(oeste, unAF.fabricarPared())
		hab1.ponerEn(sur, unAF.fabricarPared())
		hab2.ponerEn(este, unAF.fabricarPared())
		hab2.ponerEn(oeste, unAF.fabricarPared())
		hab2.ponerEn(norte, unAF.fabricarPared())
		lab.agregarHijo(hab1)
		lab.agregarHijo(hab2)
		self.laberinto=lab

	def obtenerHabitacion(self,id):
		return self.laberinto.obtenerHabitacion(id)

	def agregarBicho(self,unBicho):
		self.bichos.append(unBicho)
	def numeroHab(self):
		return self.laberinto.numeroHab()

class ElementoMapa:
	def entrar(self):
		print("metodo a sobreescribir")
	def esPuerta(self):
		return False
	def esPared(self):
		return False
	def esHabtiacion(self):
		return False
	def esBomba(self):
		return False
	def esArmario(self):
		return False
	def esBaul(self):
		return False
	def enumerar(self):
		pass
	def __repr__(self):
		pass
	def asignarPuntosReales(self,unCont):
		pass
	def dibujar(self):
		pass

class Contenedor(ElementoMapa):
	def __init__(self):
		self.hijos=list()
		self.forma=None
		self.punto=None
		self.extent=None
	def agregarHijo(self,unEM):
		self.hijos.append(unEM)
	def eliminarHijo(self,unEM):
		self.hijos.remove(unEM)
	def ponerEn(self,unaOr,unEM):
		self.forma.ponerEn(unaOr,unEM)
	def enumerar(self):
		print(repr(self))
		for e in self.hijos:
			e.enumerar()
	def calcularPosicion(self):
		self.forma.calcularPosicionDesde(self)
	def asignarPuntosReales(self,unCont):
		self.forma.asignarPuntosRealesDeEn(unCont,self)
	def dibujar(self,unaVista):
		self.forma.dibujarContenedor(unaVista,self)
		for h in self.hijos:
			h.dibujar(unaVista)

class Forma:
	def __init__(self):
		self.orientaciones=list()
	def ponerEn(self,unaOr,unEM):
		unaOr.poner(unEM,self)
	def calcularPosicionDesde(self,unCont):
		for ori in self.orientaciones:
			ori.calcularPosicionDesde(unCont)
	def asignarPuntosRealesDeEn(self,unCont,otroCont):
		pass
	def dibujarContenedor(self,unaVista,unCont):
		pass

class Cuadrado(Forma):
	def __init__(self):
		self.norte=None
		self.este=None
		self.sur=None
		self.oeste=None
		Forma.__init__(self)

	def asignarPuntosRealesDeEn(self,unCont,otroCont):
		ancho=(unCont.extent.x) * otroCont.proporcion
		alto = (unCont.extent.y) * otroCont.proporcion
		#print("ancho,alto",ancho,alto)
		division=unCont.extent.x/len(unCont.hijos)
		numHijo=unCont.hijos.index(otroCont)
		x=unCont.punto.x+(division * numHijo)
		y=unCont.punto.y + (unCont.extent.y - alto)
		otroCont.punto=Point(x,y)
		otroCont.extent=Point(ancho,alto)

	def dibujarContenedor(self,unaVista,unCont):
		unaVista.dibujarContenedorRectangular(unCont)

class Octogono(Forma):
	def __init__(self):
		self.norte=None
		self.este=None
		self.sur=None
		self.oeste=None
		self.noreste = None
		self.sureste = None
		self.noroeste = None
		self.suroeste = None
		Forma.__init__(self)

class Laberinto(Contenedor):
	def obtenerHabitacion(self,id):
		for item in self.hijos:
			if item.esHabitacion and item.id==id:
				return item
		print("no encontrado")
	def __repr__(self):
		return "Laberinto"
	def numeroHab(self):
		return len(self.hijos)

class Habitacion(Contenedor):
	def __init__(self,id):
		self.id=id
		Contenedor.__init__(self)
	def __repr__(self):
		return "Habitacion"
	def entrar(self):
		print("Estas en la habitacion-"+repr(self.id))
	def esHabitacion(self):
		return True

class Hoja(ElementoMapa):
	def entrar(self):
		print("es una hoja")
	def enumerar(self):
		print(repr(self))
	def calcularPosicionDesdePunto(self,unCont,punto):
		pass
	def asignarPuntosReales(self, unCont):
		pass
	def dibujar(self,unaVista):
		pass

class Armario(Contenedor):
	def __init__(self):
		self.proporcion=0.3
		Contenedor.__init__(self)
	def esArmario(self):
		return True
	def entrar(self):
		print("estas en un armario")
	def __repr__(self):
		return "Armario"

class Baul(Contenedor):
	def __init__(self):
		self.proporcion=0.1
		Contenedor.__init__(self)
	def esBaul(self):
		return True
	def entrar(self):
		print("estas en un baul")
	def __repr__(self):
		return "Baul"

class Pared(Hoja):
	def entrar(self):
		print("Te has chocado con una pared")
	def esPared(self):
		return True
	def __repr__(self):
		return "Pared"

class Puerta(Hoja):
	def __init__(self, h1,h2):
		self.h1=h1
		self.h2=h2
		self.abierta=False
		self.visitada=False
	def entrar(self):
		if self.abierta:
			print("Puerta abierta")
		else:
			print("Puerta cerrada")
	def esPuerta(self):
		return True
	def __repr__(self):
		return "Puerta"
	def calcularPosicionDesdePunto(self,unCont,punto):
		if (not self.visitada):
			self.visitada=True
			if (unCont.id==self.h1.id):
				self.h2.punto=punto
				self.h2.calcularPosicion()
			else:
				self.h1.punto=punto
				self.h1.calcularPosicion()

class Decorator(Hoja):
	def __init__(self):
		self.componente=None

class Bomba(Decorator):
	def __init__(self,estrategia):
		self.activa=False
		self.estrategia=estrategia
	def entrar(self):
		self.estrategia.entrar(self)
	def esBomba(self):
		return True
	def __repr__(self):
		return "Bomba"

class Estrategia:
	def entrar(self,bomba):
		if bomba.activa:
			self.imprimir()
		else:
			bomba.componente.entrar()
	def imprimir(self):
		print("sobreescribir mensaje")
	def esBroma(self):
		return False
	def esMina(self):
		return False
	def esH(self):
		return False

class Broma(Estrategia):
	def imprimir(self):
		print("bomba broma")
	def esBroma(self):
		return True

class H(Estrategia):
	def imprimir(self):
		print("bomba H")
	def esH(self):
		return True

class Mina(Estrategia):
	def imprimir(self):
		print("bomba mina")
	def esMina(self):
		return True

class Orientacion:
	def poner(self,elemento,forma):
		pass
	def calcularPosicionDesde(self,unCont):
		pass

class Norte(Orientacion):
	def poner(self,elemento,forma):
		forma.norte=elemento
	def calcularPosicionDesde(self,unCont):
		x=unCont.punto.x
		y=unCont.punto.y-1
		punto=Point(x,y)
		unCont.forma.norte.calcularPosicionDesdePunto(unCont,punto)
class Sur(Orientacion):
	def poner(self,elemento,forma):
		forma.sur=elemento
	def calcularPosicionDesde(self,unCont):
		x=unCont.punto.x
		y=unCont.punto.y+1
		punto=Point(x,y)
		unCont.forma.sur.calcularPosicionDesdePunto(unCont,punto)
class Este(Orientacion):
	def poner(self,elemento,forma):
		forma.este=elemento
	def calcularPosicionDesde(self,unCont):
		x=unCont.punto.x+1
		y=unCont.punto.y
		punto=Point(x,y)
		unCont.forma.este.calcularPosicionDesdePunto(unCont,punto)
class Oeste(Orientacion):
	def poner(self,elemento,forma):
		forma.oeste=elemento
	def calcularPosicionDesde(self,unCont):
		x=unCont.punto.x-1
		y=unCont.punto.y
		punto=Point(x,y)
		unCont.forma.oeste.calcularPosicionDesdePunto(unCont,punto)
class NorOeste(Orientacion):
	def poner(self,elemento,forma):
		forma.noroeste=elemento
class SurOeste(Orientacion):
	def poner(self,elemento,forma):
		forma.suroeste=elemento
class NorEste(Orientacion):
	def poner(self,elemento,forma):
		forma.noreste=elemento
class SurEste(Orientacion):
	def poner(self,elemento,forma):
		forma.sureste=elemento

class Bicho:
	def __init__(self):
		self.modo=None
		self.posicion=None
	def actua(self):
		self.modo.actua(self)

class Modo:
	def actua(self,unBicho):
		self.dormir
		self.caminar(unBicho)
	def dormir(self):
		time.sleep(2)
	def esPerezoso(self):
		return False
	def esAgresivo(self):
		return False
	def caminar(self,unBicho):
		pass

class Agresivo(Modo):
	def dormir(self):
		time.sleep(1)
	def esAgresivo(self):
		return True

class Perezoso(Modo):
	def dormir(self):
		time.sleep(3)
	def esPerezoso(self):
		return True

class Point:
	def __init__(self,x,y):
		self.x=x
		self.y=y

# juego=JuegoLaberinto()

# lab=Laberinto()
# hab1=Habitacion(1)
# hab2=Habitacion(2)
# puerta=Puerta(hab1,hab2)
# lab.agregarHabitacion(hab1)
# lab.agregarHabitacion(hab2)
# juego.lab=lab

# hab=juego.obtenerHabitacion(1)
# hab.entrar()
# hab.norte.entrar()