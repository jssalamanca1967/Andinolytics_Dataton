require(foreign)
require(nnet)
require(ggplot2)
require(reshape2)

# Se selecciona la base final
load("Final.RData")

# Para la creaci�n del modelo, se utilizar�n las categorias que no sean "ninguna"
baseModelo = trx_definitiva[trx_definitiva$CategoriaRta != "ninguna",]

baseModelo$CategoriaRta = as.character(baseModelo$CategoriaRta)
baseModelo$CategoriaRta = as.factor(baseModelo$CategoriaRta)
summary(baseModelo$CategoriaRta)

baseModelo$Cat_edad = as.factor(baseModelo$Cat_edad)
baseModelo$Mes = as.factor(baseModelo$Mes)

rm(trx_definitiva)

set.seed(123123)

# install.packages('caTools')
library(caTools)

# Divisi�n de la base entre muestra y prueba en raz�n de 60-40
split = sample.split(baseModelo$CategoriaRta, SplitRatio = 0.6)

training_set = subset(baseModelo, split == TRUE)
test_set = subset(baseModelo, split == FALSE)

# Creaci�n del modelo
test <- multinom(CategoriaRta ~ +valor_trx
                 +DiaSemana
                 +Mes
                 +FinDeSemana
                 +Quincena
                 +ca_hora
                 +seg_str
                 # +ocupacion
                 # +tipo_vivienda
                 # +nivel_academico
                 +estado_civil
                 +genero
                 +Cat_edad
                 +ingreso_rango
                 , data = training_set)

save.image("Multinomial.RData")
# load("Multinomial.RData")

# Comprobaci�n de resultados y creaci�n de matrices de confusi�n

training_set$result = predict(test, newdata = training_set, "class")
training_set$Conteo = ifelse(training_set$result == training_set$CategoriaRta, 1, 0)

test_set$result = predict(test, newdata = test_set, "class")
test_set$Conteo = ifelse(test_set$result == test_set$CategoriaRta, 1, 0)

tabla = table(training_set$CategoriaRta, training_set$result)

write.csv(tabla, "RMatrizConfusion_Train.csv", sep = ",")

tabla = table(test_set$CategoriaRta, test_set$result)

write.csv(tabla, "RMatrizConfusion_Test.csv", sep = ",")

sum(test_set$Conteo)/nrow(test_set)
