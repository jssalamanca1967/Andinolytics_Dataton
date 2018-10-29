# Se carga la base de las transacciones con fecha y hora
load("trx_fecha_hora.RData")

infoClientes = read.csv("dt info pagadores muestra/dt_info_pagadores_muestra.csv", header = F)

names(infoClientes) = c("id_cliente","seg_str","ocupacion","tipo_vivienda","nivel_academico","estado_civil","genero","edad","ingreso_rango")

library(dplyr)

names(trx_reducido_fecha_hora)

# Se une la base de clientes con la de transacciones

trx_final_clientes = merge(trx_reducido_fecha_hora, infoClientes,
                                      by.x = "id_cliente", by.y = "id_cliente")


summary(trx_final_clientes)


write.csv(trx_final_clientes, "Transacciones_Clientes.csv")
rm(asdf)
rm(infoClientes)
rm(trx_reducido_fecha_hora)
# save.image("trx_final_clientes.RData")

load("trx_final_clientes.RData")

# Se lee la base de la categoría asignada.

lineas = readLines("categoria_asignada.csv")

vectorNo = c()

archivo = lineas

for(i in 1:length(archivo)){
  
  vectorString = strsplit(archivo[i], ",")
  
  if(length(vectorString[[1]]) > 7){
    vectorNo = append(vectorNo, i)
  }
  
  if(i %% 500000 == 0)
    print(i)
  
}

archivo2 = archivo[-vectorNo]

matriz = matrix(NA, nrow = length(archivo2), ncol = 7)

for(i in 1:length(archivo2)){
  
  vectorString = strsplit(archivo2[i], ",")
  
  vector = c()
  
  j = 1
  
  for(j in 1:7){
    vector = append(vector, vectorString[[1]][j])
  }
  
  matriz[i,] = vector
  
}

Transacciones = as.data.frame(matriz)

Transacciones2 = select(Transacciones, V1, V7)

# Se unen las categorias con la base de transacciones con información de clientes

trx_final = merge(trx_final_clientes, Transacciones2,
                           by.x = "id_trn_ach", by.y = "V1")

names(trx_final)[which(names(trx_final) == "V7")] = "CategoriaRta"

# Se crea una variable categórica para edad
trx_final$edad = as.numeric(trx_final$edad)
summary(trx_final$edad)
quantile(trx_final$edad, probs = seq(0,1,0.01))

trx_final$Cat_edad = "< 25"
trx_final$Cat_edad[trx_final$edad >= 25] = "25-30"
trx_final$Cat_edad[trx_final$edad >= 31] = "31-35"
trx_final$Cat_edad[trx_final$edad >= 36] = "36-40"
trx_final$Cat_edad[trx_final$edad >= 41] = "41-45"
trx_final$Cat_edad[trx_final$edad >= 46] = "46-50"
trx_final$Cat_edad[trx_final$edad >= 51] = "51-59"
trx_final$Cat_edad[trx_final$edad >= 60] = "> 60"

# Se arreglan las categorias vacias de las variables categoricas

trx_final$genero = as.character(trx_final$genero)
trx_final$genero[is.na(trx_final$genero)] = "NoData"
trx_final$genero = as.factor(trx_final$genero)

trx_final$ocupacion = as.character(trx_final$ocupacion)
trx_final$ocupacion[trx_final$ocupacion == ""] = "NoData"
trx_final$ocupacion = as.factor(trx_final$ocupacion)

trx_final$nivel_academico = as.character(trx_final$nivel_academico)
trx_final$nivel_academico[trx_final$nivel_academico == ""] = "NoData"
trx_final$nivel_academico = as.factor(trx_final$nivel_academico)

trx_final$estado_civil = as.character(trx_final$estado_civil)
trx_final$estado_civil[trx_final$estado_civil == ""] = "NoData"
trx_final$estado_civil = as.factor(trx_final$estado_civil)

trx_final$estado_civil = as.character(trx_final$estado_civil)
trx_final$estado_civil[trx_final$estado_civil == ""] = "NoData"
trx_final$estado_civil = as.factor(trx_final$estado_civil)

trx_final$tipo_vivienda = as.character(trx_final$estado_civil)
trx_final$estado_civil[trx_final$estado_civil == ""] = "NoData"
trx_final$estado_civil = as.factor(trx_final$estado_civil)

trx_final$tipo_vivienda = as.character(trx_final$tipo_vivienda)
trx_final$tipo_vivienda[trx_final$tipo_vivienda == ""] = "I"
trx_final$tipo_vivienda[trx_final$tipo_vivienda == "1"] = "I"
trx_final$tipo_vivienda[trx_final$tipo_vivienda == "2"] = "I"
trx_final$tipo_vivienda[trx_final$tipo_vivienda == "3"] = "I"
trx_final$tipo_vivienda[trx_final$tipo_vivienda == "4"] = "I"
trx_final$tipo_vivienda = as.factor(trx_final$tipo_vivienda)

# Se seleccionan las variables necesarias
trx_definitiva = select(trx_final,
                        id_trn_ach
                        ,id_cliente
                        ,fecha
                        ,hora
                        ,valor_trx
                        ,sector
                        ,subsector
                        ,DiaSemana
                        ,Mes
                        ,Anio
                        ,FinDeSemana
                        ,Quincena
                        ,QuincenaCompleta
                        ,ca_hora
                        ,seg_str
                        ,ocupacion
                        ,tipo_vivienda
                        ,nivel_academico
                        ,estado_civil
                        ,genero
                        ,edad
                        ,Cat_edad
                        ,ingreso_rango
                        ,CategoriaRta)

# Se normaliza la variable de valor transacción

trx_definitiva$valor_trx = trx_definitiva$valor_trx/max(trx_definitiva$valor_trx)
summary(trx_definitiva$valor_trx)

# write.csv(trx_definitiva, "Transacciones_BaseFinal.csv")


rm(infoClientes)
rm(matriz)
rm(Transacciones)
rm(Transacciones2)
rm(trx_final_clientes)
rm(list = ls(pattern = "vector"))
rm(list = ls(pattern = "archivo"))
rm(list = ls(pattern = "vector"))
rm(trx_final)

save.image("Final.RData")
# load("Final.RData")


