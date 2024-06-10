/*********************************************
 * OPL 22.1.1.0 Model
 * Author: Gian
 * Creation Date: 6 jun. 2024 at 17:26:49
 *********************************************/
int n = ...;
int limiteColores = n;
int e = ...;
range nodos = 1 .. n;
range colores = 1 .. limiteColores;
range aristas = 1 .. e;

tuple peso {
  int i;
  int w;
}

peso weights[nodos] = ...;

tuple edge {
  int i;
  int j;
}

edge edges[aristas] = ...;

dvar boolean x[nodos, colores];
dvar boolean y[colores]; // Variable binaria para indicar si se usa un color
dvar int numColoresUsados;
dvar int pesoColor[colores];


minimize
  numColoresUsados;

  
subject to {
  forall ( i in nodos )
    todo_coloreado:
      sum ( k in colores ) x[i,k] == 1;
      
  forall ( i in nodos )
    forall ( k in colores )
      peso_color:
      pesoColor[k] >= weights[i].w * x[i,k];

  forall ( e in aristas )
    incompatibles:
        forall ( k in colores )
          x[edges[e].i,k]+x[edges[e].j,k]<=1;
          
  forall (k in colores)
    y[k] >= (sum(i in nodos) x[i,k] >= 1);
    
  numColoresUsados == sum(k in colores) y[k];
}

main {
  var mod = thisOplModel.modelDefinition;
  var dat = thisOplModel.dataElements;
  var cplex1 = new IloCplex();
  var opl = new IloOplModel(mod, cplex1);
  opl.addDataSource(dat);
  opl.generate();
  
  cplex1.tilim = 600; 

  if (cplex1.solve()) {
    
    writeln("Numero de colores usados: ", cplex1.getObjValue());
    
    for ( i in opl.nodos )
	  for ( k in opl.colores ){
	    if (opl.x[i][k] == 1)
	    {
	      writeln("Nodo ", i, ": ", k);
	    }
	  }
	  
	var file = new IloOplOutputFile("solucion_tercer_problema.txt");
	for (var i in opl.nodos) {
	  for (var k in opl.colores) {
	    if (opl.x[i][k] == 1) {
	      file.writeln(i, " ", k);
	      break;
	      }
	    }
	  }
	file.close();
        
    opl.end()
    cplex1.end()
  }
}
