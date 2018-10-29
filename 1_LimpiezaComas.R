## Código que carga inicialmente la base y se realiza limpieza de las filas que tienen más de las comas (,) 
##    reglamentarias del archivo .csv

setwd("D:/Documentos/Andinolytics")

archivo = readLines("dt_trxpse_personas_2016_2018_muestra_adjt.csv", encoding = "UTF-8")

vectorNo = c()

# Se selecciona todas las filas que tienen más de 11 comas.
for(i in 1:length(archivo)){
  
  vectorString = strsplit(archivo[i], ",")
  
  if(length(vectorString[[1]]) > 11){
    vectorNo = append(vectorNo, i)
  }
  
  if(i %% 500000 == 0)
    print(i)
  
}

# Se remueven las filas que tienen más de 11 comas
archivo2 = archivo[-vectorNo]

matriz = matrix(NA, nrow = length(archivo2), ncol = 11)

# Se crea una matriz con los 
for(i in 1:length(archivo2)){
  
  vectorString = strsplit(archivo2[i], ",")
  
  vector = c()
  
  for(j in 1:11){
    vector = append(vector, vectorString[[j]])
  }
  
  matriz[i,] = vector
  
}

# Se crea un dataframe con los datos filtrados
Transacciones = as.data.frame(matriz)
names(Transacciones) = matriz[1,]

Transacciones = Transacciones[-1,]



