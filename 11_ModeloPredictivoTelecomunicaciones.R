#Fijar el directorio
setwd("D:/Documentos/Andinolytics/RandomForest")

#Leer bases de datos
datos=read.csv("Clientes_telecom_2017_copy.csv",header = T, sep = ";",encoding = "UTF-8")

#Modelo predictivo
set.seed(12345)
N=nrow(datos)
nsample = sample(seq(1:N), N * 0.8)
train=datos[nsample,]
test=datos[-nsample,]

install.packages("randomForest")
library(randomForest)

# Modelo Random Forest

rf.fit=randomForest(Valor_telecom~seg_str
                    +ocupacion
                    +tipo_vivienda
                    +nivel_academico
                    +estado_civil
                    +genero
                    +ingreso_rango
                    +edad2
                    ,data=train,mtry=2)

# Modelo Regresión Lineal

lm = lm(Valor_telecom~seg_str
        +ocupacion
        +tipo_vivienda
        +nivel_academico
        +estado_civil
        +genero
        +ingreso_rango
        +edad2
        ,data=train)

pred.rf=predict(rf.fit,test)

pred.lm = predict(lm,test)

# save.image("Resultado.RData")
load("Resultado.RData")

test$sqerror_rf = (test$Valor_telecom - pred.rf)^2
test$sqerror_lm = (test$Valor_telecom - pred.lm)^2

# Cálculo del rmse para cada modelo
sqrt(ave(test$sqerror_rf)[1])
sqrt(ave(test$sqerror_lm)[1])

sd(datos$Valor_telecom)
