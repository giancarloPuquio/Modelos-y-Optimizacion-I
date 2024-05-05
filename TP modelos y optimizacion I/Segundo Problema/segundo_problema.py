import networkx as nx

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
        #self.tiempoLavadoTotal = 0

    def agregarPrendaAlLavado(self, prenda):
        if (prenda not in self.prendas) and self.sePuedeAgregarPrenda(prenda):
            self.prendas.append(prenda)
            #if prenda.tiempoLavado > self.tiempoLavadoTotal:
                #self.tiempoLavadoTotal = prenda.tiempoLavado

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
        # Creamos un grafo no dirigido utilizando la biblioteca networkx
        G = nx.Graph()

        # Agregamos los vértices(prendas) al grafo
        for prenda in self.listaPrendas:
            G.add_node(prenda.getNumeroPrenda())

        # Agregamos las aristas (incompatibilidades) al grafo
        for prenda in self.listaPrendas:
            for incompatibilidad in prenda.getPrendasIncompatibles():
                G.add_edge(prenda.getNumeroPrenda(), incompatibilidad)

        # Aplicamos el algoritmo de coloreo greedy de grafos
        coloreo = nx.greedy_color(G, strategy='largest_first')

        self.listaPrendas = sorted(self.listaPrendas, key=lambda x: x.getTiempoLavado())
        # Asignamos las prendas a los lavados según el coloreo
        min_color = min(coloreo.values())

        lavados = {}
        for prenda, color in coloreo.items():
            color_actual = color - min_color + 1
            if color_actual not in lavados:
                lavados[color_actual] = Lavado(color_actual)
            lavados[color_actual].agregarPrendaAlLavado(self.listaPrendas[prenda - 1])


        self.listaLavados = list(lavados.values())
        return len(self.listaLavados)


    def escribirEnArchivo(self, nombreArchivo):
        with open(nombreArchivo + ".txt", 'w') as archivo:
            for lavado in self.listaLavados:
                for prenda in lavado.prendas:
                    archivo.write(f"{prenda.getNumeroPrenda()} {lavado.numeroLavado}\n")

def main():
    distribuidor = distribuidorPrendas()
    prendas = distribuidor.armarListaDePrendas("segundo_problema.txt")
    lavados = distribuidor.asignarPrendasALavados()
    distribuidor.escribirEnArchivo("solucion_segundo_problema")
    
    print("Cantidad de lavados:", lavados)
main()