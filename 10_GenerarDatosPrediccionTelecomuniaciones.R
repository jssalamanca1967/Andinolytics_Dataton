#Leer bases de datos
base=read.csv("Transacciones_BaseFinal.csv",header = T, sep = ",",encoding = "UTF-8")
transacciones=read.csv("trx_limpio_reducido.csv",header = T,sep = ",",encoding = "UTF-8")
clientes = read.csv("dt_info_pagadores_muestra.csv",header=F, sep = ",",encoding ="UTF-8" )
colClientes=read.csv("colnames_clientes.csv",header=T,sep=";")
colnames(clientes)=colClientes[,1]

#Crear base de registros con categoria
base_categorias=base[base$CategoriaRta!="ninguna",c(2,25)]
transacciones_valor = merge(base_categorias, transacciones,
                            by.x = "id_trn_ach", by.y = "id_trn_ach")

#Crear base de datos de transacciones de telecomunicaciones en el 2017 por cliente
transacciones_valor2017=transacciones_valor[transacciones_valor$fecha>20170000,]
transacciones_valor2017=transacciones_valor2017[transacciones_valor2017$fecha<20180000,]
trx_telecomunicaciones2017=transacciones_valor2017[transacciones_valor2017$CategoriaRta=="telecomunicaciones",
                                                   c(1,2,4,7)]
trx_tel_clientes=aggregate(trx_telecomunicaciones2017$valor_trx,
                           by=list(Cliente=trx_telecomunicaciones2017$id_cliente), FUN=sum)
colnames(trx_tel_clientes)=c("Cliente","Valor_telecom")
clientes_trx_telecom=merge(clientes,trx_tel_clientes,by.x="id_cliente",by.y = "Cliente")


#Corregir formatos de la base de datos 
base_c_trx_tel=clientes_trx_telecom
base_c_trx_tel[base_c_trx_tel$tipo_ocupacion=="",]$ocupacion="I"
base_c_trx_tel[base_c_trx_tel$tipo_vivienda=="",]$tipo_vivienda="I"
base_c_trx_tel[base_c_trx_tel$tipo_vivienda==2,]$tipo_vivienda="I"
base_c_trx_tel[base_c_trx_tel$nivel_academico=="",]$nivel_academico="I"
base_c_trx_tel[base_c_trx_tel$estado_civil=="",]$estado_civil="I"
base_c_trx_tel[is.na(base_c_trx_tel$ocupacion)=="",]$genero="I"
base_c_trx_tel=base_c_trx_tel[!is.na(base_c_trx_tel$genero),]
base_c_trx_tel$edad=as.numeric(as.character(base_c_trx_tel$edad))
base_c_trx_tel=base_c_trx_tel[base_c_trx_tel$edad<100,]
base_c_trx_tel=base_c_trx_tel[!is.na(base_c_trx_tel$edad),]
base_c_trx_tel$edad2=""
base_c_trx_tel[base_c_trx_tel$edad<25,]$edad2="menos 25"
base_c_trx_tel[base_c_trx_tel$edad>=25,]$edad2="25-30"
base_c_trx_tel[base_c_trx_tel$edad>=31,]$edad2="21-35"
base_c_trx_tel[base_c_trx_tel$edad>=36,]$edad2="36-40"
base_c_trx_tel[base_c_trx_tel$edad>=41,]$edad2="41-45"
base_c_trx_tel[base_c_trx_tel$edad>=46,]$edad2="46-50"
base_c_trx_tel[base_c_trx_tel$edad>=51,]$edad2="51-59"
base_c_trx_tel[base_c_trx_tel$edad>=60,]$edad2="mas 60"
base_c_trx_tel$edad2=as.factor(as.character(base_c_trx_tel$edad2))
base_c_trx_tel[base_c_trx_tel$ingreso_rango=="0",]$ingreso_rango="No disponible"
summary(base_c_trx_tel$ocupacion)

write.csv(base_c_trx_tel,"Clientes_telecom_2017.csv")

