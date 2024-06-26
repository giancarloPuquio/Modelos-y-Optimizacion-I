class Prenda:

    def __init__(self, numeroPrenda):
        self.numeroPrenda = numeroPrenda
        self.tiempoLavado = 0
        self.prendasIncompatibles = []
		
    def addPrendaIncompatible(self, prenda):
        if prenda not in self.prendasIncompatibles:
            self.prendasIncompatibles.append(prenda)
    
    def getNumeroPrenda(self): return self.numeroPrenda
    
    def getPrendasIncompatibles(self): return self.prendasIncompatibles
	
    def getTiempoLavado(self): return self.tiempoLavado
    
    def setTiempoLavado(self, tiempo): self.tiempoLavado = tiempo
		
class Lavado:
    def __init__(self, numeroDeLavado):
        self.numeroLavado = numeroDeLavado
        self.prendas = []
        self.tiempoLavadoTotal = 0

    def agregarPrendaAlLavado(self, prenda):
        if (prenda not in self.prendas) and self.sePuedeAgregarPrenda(prenda):
            self.prendas.append(prenda)
            if prenda.tiempoLavado > self.tiempoLavadoTotal:
                self.tiempoLavadoTotal = prenda.tiempoLavado

    def sePuedeAgregarPrenda(self, unaPrenda):
        for prenda in self.prendas:
            if unaPrenda.getNumeroPrenda() in prenda.prendasIncompatibles:
                return False
        return True

class distribuidorPrendas:

    def __init__(self): 
        self.listaPrendas = []
        self.listaLavados = []
    
    def armarListaDePrendas(self, nombreArchivo):
        archivo = open(nombreArchivo,"r")
        linea = archivo.readline()
        while(linea!=""):
            linea = (linea.strip()).split()
            if(linea[0] == 'p'):
                self.inicializarLista(linea)
            if(linea[0] == 'e'):                        
                self.agregarIncompatibilidad(int (linea[1]), int (linea[2]) )   
            elif(linea[0] =='n'):
                self.listaPrendas[int (linea[1])-1].setTiempoLavado(int (linea[2]))
            linea = archivo.readline()

        return self.listaPrendas
	
    def inicializarLista(self, linea):
        cantidadPrendas = int (linea[2])
        for i in range(1,cantidadPrendas+1):
            self.listaPrendas.append(Prenda(i))

    def agregarIncompatibilidad(self, valor1, valor2,):
        self.listaPrendas[valor1-1].addPrendaIncompatible(valor2)
        self.listaPrendas[valor2-1].addPrendaIncompatible(valor1)
    
    def asignarPrendasALavados(self):
        lavados = []
        for prenda in self.listaPrendas:
            lavado_existente = None
            for lavado in lavados:
                if lavado.sePuedeAgregarPrenda(prenda):
                    lavado_existente = lavado
                    break
            if lavado_existente is None:
                nuevo_lavado = Lavado(len(lavados) + 1)
                lavados.append(nuevo_lavado)
                lavado_existente = nuevo_lavado
            lavado_existente.agregarPrendaAlLavado(prenda)
        self.listaLavados = lavados


    def escribirEnArchivo(self, nombreArchivo):
        with open(nombreArchivo + ".txt", 'w') as archivo:
            for lavado in self.listaLavados:
                for prenda in lavado.prendas:
                    archivo.write(f"{prenda.getNumeroPrenda()} {lavado.numeroLavado}\n")

def main():
    distribuidor = distribuidorPrendas()
    prendas = distribuidor.armarListaDePrendas("primer_problema.txt")
    lavados = distribuidor.asignarPrendasALavados()
    distribuidor.escribirEnArchivo("solucion_primer_problema")

main()
