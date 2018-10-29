setwd("C:/Users/Lina/Documents/Dataton/Analisis")

#***Cargar base de clientes
clientes = read.csv("dt_info_pagadores_muestra.csv",header=F, sep = ",",encoding ="UTF-8" )
colClientes=read.csv("colnames_clientes.csv",header=T,sep=";")
colnames(clientes)=colClientes[,1]

#***Cargar base de transacciones

#transacciones=read.csv("dt_trxpse_personas_2016_2018_muestra_adjt.csv",header = F,sep = ",",encoding = "UTF-8", nrows = 100000)
#coltransacciones=read.csv("colnames_transacciones.csv",header=T,sep=";")
#colnames(transacciones)=coltransacciones[,1]

transacciones=Transacciones[-1,] #Transacciones workspace sin mas de 11 comas por columna
rm(Transacciones)

#***Eliminar NA en columna valor_trx
transacciones$valor_trx[transacciones$valor_trx=="\\N"]=NA
transacciones=transacciones[!is.na(transacciones$valor_trx),]

#***Corregir formatos
transacciones$valor_trx=as.numeric(as.character(transacciones$valor_trx))
transacciones$hora=as.numeric(as.character(transacciones$hora))

write.csv(transacciones,"trx_limpio.csv")  

#***Elimiar valores extremos
quantile(transacciones$valor_trx,seq(0,1,0.01))
summary(transacciones$valor_trx)
transacciones_reducido=transacciones[transacciones$valor_trx>1000 & transacciones$valor_trx<50000000,]
write.csv(transacciones_reducido,"trx_limpio_reducido.csv")

# Cruce con la base de las fechas

transacciones_reducido$fecha2 = as.numeric(as.character(transacciones_reducido$fecha))

max(transacciones_reducido$fecha2)

VariablesCategoricasFecha = read.csv("AndinolyticsDatatonBC/VariablesCategoricasFecha.csv")

transacciones_reducido_fechas = merge(transacciones_reducido, VariablesCategoricasFecha,
                                      by.x = "fecha2", by.y = "FechaNumero")

trx_reducido_fecha_hora = transacciones_reducido_fechas

save.image("trx_fecha_hora.RData")
