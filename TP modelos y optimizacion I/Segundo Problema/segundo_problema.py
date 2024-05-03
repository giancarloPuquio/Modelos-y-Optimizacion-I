class Prenda:
    def __init__(self, numeroPrenda):
        self.numeroPrenda = numeroPrenda
        self.tiempoLavado = 0
        self.prendasIncompatibles = set()  # Usamos un conjunto para almacenar las prendas incompatibles
        
    def addPrendaIncompatible(self, prenda):
        self.prendasIncompatibles.add(prenda)
    
    def getNumeroPrenda(self):
        return self.numeroPrenda
    
    def getPrendasIncompatibles(self):
        return self.prendasIncompatibles
    
    def getTiempoLavado(self):
        return self.tiempoLavado
    
    def setTiempoLavado(self, tiempo):
        self.tiempoLavado = tiempo

class Lavado:
    def __init__(self, numeroDeLavado):
        self.numeroLavado = numeroDeLavado
        self.prendas = []
        self.tiempoLavadoTotal = 0

    def agregarPrendaAlLavado(self, prenda):
        if self.sePuedeAgregarPrenda(prenda):
            self.prendas.append(prenda)
            if prenda.tiempoLavado > self.tiempoLavadoTotal:
                self.tiempoLavadoTotal = prenda.tiempoLavado

    def sePuedeAgregarPrenda(self, unaPrenda):
        return not any(otraPrenda.numeroPrenda in unaPrenda.prendasIncompatibles for otraPrenda in self.prendas)

class distribuidorPrendas:
    def __init__(self): 
        self.listaPrendas = []
        self.listaLavados = []
    
    def armarListaDePrendas(self, nombreArchivo):
        with open(nombreArchivo, "r") as archivo:
            for linea in archivo:
                linea = linea.strip().split()
                if linea[0] == 'p':
                    self.inicializarLista(linea)
                elif linea[0] == 'e':                        
                    self.agregarIncompatibilidad(int(linea[1]), int(linea[2]))
                elif linea[0] == 'n':
                    self.listaPrendas[int(linea[1])-1].setTiempoLavado(int(linea[2]))

    def inicializarLista(self, linea):
        cantidadPrendas = int(linea[2])
        for i in range(1, cantidadPrendas+1):
            self.listaPrendas.append(Prenda(i))

    def agregarIncompatibilidad(self, valor1, valor2):
        self.listaPrendas[valor1-1].addPrendaIncompatible(valor2)
        self.listaPrendas[valor2-1].addPrendaIncompatible(valor1)
    
    def asignarPrendasALavados(self):
        for prenda in self.listaPrendas:
            lavado_disponible = None
        self.colorearPrendas()
        for prenda in self.listaPrendas:
            lavado = prenda.lavadoAsignado
            self.listaLavados[lavado - 1].agregarPrendaAlLavado(prenda)
        return self.listaLavados

    def colorearPrendas(self):
        #Se ordenan la prenda en funcion de la cantidad de prendas incompatibles que tienen. 
        #La prenda con mas prendas incompatibles estara primera en la lista.
        self.listaPrendas.sort(key=lambda x: len(x.prendasIncompatibles), reverse=True)

        #En el peor de los casos, habra igual numero de lavados que prendas (Cada prenda seria incompatible con todas las otras prendas).
        self.listaLavados = [Lavado(i + 1) for i in range(len(self.listaPrendas))]
        
        #Asignamos a cada prenda un numero de lavado.
        for prenda in self.listaPrendas:
            lavado_disponible = None
            for lavado in self.listaLavados:
                if lavado.sePuedeAgregarPrenda(prenda):
                    lavado_disponible = lavado
                    break
            if lavado_disponible:
                lavado_disponible.agregarPrendaAlLavado(prenda)
                prenda.lavadoAsignado = lavado_disponible.numeroLavado

    def escribirEnArchivo(self, nombreArchivo):
        prendas_escritas = set()  # Conjunto para rastrear las prendas ya escritas
        with open(nombreArchivo + ".txt", 'w') as archivo:
            for lavado in self.listaLavados:
                for prenda in lavado.prendas:
                    if prenda.getNumeroPrenda() not in prendas_escritas:
                        archivo.write(f"{prenda.getNumeroPrenda()} {lavado.numeroLavado}\n")
                        prendas_escritas.add(prenda.getNumeroPrenda())  # Agregar la prenda al conjunto de prendas escritas

def main():
    distribuidor = distribuidorPrendas()
    distribuidor.armarListaDePrendas("primer_problema.txt")
    lavados = distribuidor.asignarPrendasALavados()
    distribuidor.escribirEnArchivo("solucion_primer_problema")

main()
