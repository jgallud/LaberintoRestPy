import json
from modelo.solucionLaberinto import *

class Director:
    def __init__(self):
        self.builder=None
        self.dic=None
    def leerConfig(self,unArchivo):
        with open(unArchivo) as json_data:
            self.dic=json.load(json_data)
            #print self.dic
    def iniBuilder(self):
        #if (self.dic["forma"]=="cuadrado"):
            self.builder=LaberintoCuadradoBuilder()
        #if (self.dic["forma"]=="octogono"):
        #    self.builder=LaberintoOctogonoBuilder()
    def crearLaberinto(self):
        self.builder.construirLaberinto()
        for each in self.dic["laberinto"]:
            self.crearLaberintoRecursivo(each,None)
        for each in self.dic["puertas"]:
            self.builder.construirPuerta(each[0],each[1],each[2],each[3])
    def crearLaberintoRecursivo(self,unDic,padre):
        if (unDic["tipo"]=="habitacion"):
            con=self.builder.construirHabitacion()
        if (unDic["tipo"]=="armario"):
            con=self.builder.construirArmarioEn(padre)
        if (unDic["tipo"]=="baul"):
            con=self.builder.construirBaulEn(padre)
        if (unDic["tipo"]=="bomba"):
            if (unDic["argumento"]=="broma"):
                self.builder.construirBombaBromaEn(padre)
            if (unDic["argumento"]=="H"):
                self.builder.construirBombaHEn(padre)
            if (unDic["argumento"]=="mina"):
                self.builder.construirBombaMinaEn(padre)
        if "hijos" in unDic:
            for each in unDic["hijos"]:
                self.crearLaberintoRecursivo(each,con)
    def crearJuego(self):
        self.builder.construirJuego()
    def crearBichos(self):
        if "bichos" in self.dic:
            for each in self.dic["bichos"]:
                if (each["modo"]=="agresivo"):
                    self.builder.construirBichoAgresivoEn(each["habitacion"])
                if (each["modo"]=="perezoso"):
                    self.builder.construirBichoPerezosoEn(each["habitacion"])
    def procesar(self,unArchivo):
        self.leerConfig(unArchivo)
        self.iniBuilder()
        self.crearLaberinto()
        self.crearJuego()
        self.crearBichos()
    def obtenerJuego(self):
        return self.builder.obtenerJuego()


class LaberintoBuilder:
    def __init__(self):
        self.juego=None
        self.laberinto=None
        self.orientaciones={}
    def construirLaberinto(self):
        self.laberinto=Laberinto()
    def construirHabitacion(self):
        num=len(self.laberinto.hijos) +1
        hab=Habitacion(num)
        hab.forma=self.construirForma()
        for each in hab.forma.orientaciones:
            hab.ponerEn(each,self.construirPared())
        self.laberinto.agregarHijo(hab)
        return hab
    def construirForma(self):
        pass
    def construirPared(self):
        return Pared()
    def construirArmarioEn(self,contenedor):
        armario=Armario()
        armario.forma=self.construirForma()
        for each in armario.forma.orientaciones:
            armario.ponerEn(each,self.construirPared())
        self.construirPuertaEspecial(armario,contenedor)
        contenedor.agregarHijo(armario)
        return armario
    def construirBaulEn(self,contenedor):
        baul=Baul()
        baul.forma=self.construirForma()
        for each in baul.forma.orientaciones:
            baul.ponerEn(each,self.construirPared())
        self.construirPuertaEspecial(baul,contenedor)
        contenedor.agregarHijo(baul)
        return baul
    def construirPuertaEspecial(self,cont1,cont2):
        puerta=Puerta(cont1,cont2)
        cont1.ponerEn(Este(),puerta)
    def construirBombaBromaEn(self,contenedor):
        bomba=Bomba(Broma())
        contenedor.agregarHijo(bomba)
    def construirBombaHEn(self,contenedor):
        bomba=Bomba(H())
        contenedor.agregarHijo(bomba)
    def construirBombaMinaEn(self,contenedor):
        bomba=Bomba(Mina())
        contenedor.agregarHijo(bomba)
    def construirPuerta(self,num1,or1,num2,or2):
        hab1=self.laberinto.obtenerHabitacion(num1)
        hab2=self.laberinto.obtenerHabitacion(num2)
        puerta=Puerta(hab1,hab2)
        hab1.ponerEn(self.orientaciones[or1],puerta)
        hab2.ponerEn(self.orientaciones[or2],puerta)
    def construirJuego(self):
        self.juego=JuegoLaberinto()
        self.juego.laberinto=self.laberinto
    def construirBichoAgresivoEn(self,num):
        hab=self.juego.obtenerHabitacion(num)
        bicho=Bicho()
        bicho.modo=Agresivo()
        bicho.posicion=hab
        self.juego.agregarBicho(bicho)
    def construirBichoPerezosoEn(self,num):
        hab=self.juego.obtenerHabitacion(num)
        bicho=Bicho()
        bicho.modo=Perezoso()
        bicho.posicion=hab
        self.juego.agregarBicho(bicho)
    def obtenerJuego(self):
        return self.juego

class LaberintoCuadradoBuilder(LaberintoBuilder):
    def __init__(self):
        LaberintoBuilder.__init__(self)
    def construirForma(self):
        cuadrado=Cuadrado()
        cuadrado.orientaciones.append(Norte())
        cuadrado.orientaciones.append(Este())
        cuadrado.orientaciones.append(Sur())
        cuadrado.orientaciones.append(Oeste())
        self.orientaciones["Norte"]=Norte()
        self.orientaciones["Este"] = Este()
        self.orientaciones["Sur"] = Sur()
        self.orientaciones["Oeste"] = Oeste()
        return cuadrado

class LaberintoOctogonoBuilder(LaberintoBuilder):
    def __init__(self):
        LaberintoBuilder.__init__(self)
    def construirForma(self):
        octogono=Octogono()
        octogono.orientaciones.append(Norte())
        octogono.orientaciones.append(Este())
        octogono.orientaciones.append(Sur())
        octogono.orientaciones.append(Oeste())
        octogono.orientaciones.append(NorEste())
        octogono.orientaciones.append(NorOeste())
        octogono.orientaciones.append(SurEste())
        octogono.orientaciones.append(SurOeste())
        self.orientaciones["Norte"]=Norte()
        self.orientaciones["Este"] = Este()
        self.orientaciones["Sur"] = Sur()
        self.orientaciones["Oeste"] = Oeste()
        self.orientaciones["NorEste"]=NorEste()
        self.orientaciones["SurEste"]=SurEste()
        self.orientaciones["NorOeste"]=NorOeste()
        self.orientaciones["SurOeste"]=SurOeste()
        return octogono

#director=Director()
#ruta='/soft/dev/laberintos/laberintos/'
#ruta='/Users/jose.gallud/CloudStation/asignaturas/diseño de sofware/curso22-23/laberintos/'
#director.procesar(ruta+'lab2hab.json')