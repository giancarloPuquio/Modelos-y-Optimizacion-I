int n = ...;
int limiteColores = 11;
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
dvar int pesoColor[colores];

minimize
  sum(k in colores) pesoColor[k];

  
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
          
  forall ( i in 2 .. limiteColores )
    simetria:
      pesoColor[i-1]>= pesoColor[i];
      
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
    writeln("solution: ", cplex1.getObjValue(), " /size: ", dat.n, " /time: ",
        cplex1.getCplexTime());
        
    var usedColors = 0;
    for (var k in opl.colores) {
      for (var i in opl.nodos) {
        if (opl.x[i][k] == 1) {
          usedColors += 1;
          break;
        }
      }
    }
    writeln("Cantidad de colores usados: ", usedColors);    
    
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
/*
    for (i in opl.cities) {
      if (i == 1)
        writeln("Ciudad ", i, ": ", -1);
      else
        writeln("Ciudad ", i, ": ", opl.u[i]);
    }*/
    opl.end()
    cplex1.end()
  }
}