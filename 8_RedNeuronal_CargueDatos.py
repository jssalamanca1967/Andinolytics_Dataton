# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 17:43:29 2018

@author: Johnathan Salamanca
"""

import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

#Cargar datos
cd_directory = "D:/Documentos/Andinolytics"
dataframe=pandas.read_csv(cd_directory+"/Transacciones_BaseFinal.csv",sep=",")
dataframemodelo = dataframe[['id_trn_ach','valor_trx','DiaSemana','Mes','Anio','FinDeSemana','Quincena','ca_hora','seg_str','ocupacion','tipo_vivienda','nivel_academico','estado_civil','genero','edad','Cat_edad','ingreso_rango','CategoriaRta']] 
dataframemodelo['genero'] = dataframemodelo['genero'].fillna('NoData')

# Elimina el dataframe completo
del dataframe

dataset = dataframemodelo.values

#### Creación de las variables dummy por cada variable categórica
# DiaSemana

datasetDiaSemana = dataset[:,2]

datasetDiaSemana[1:10]

encoder=LabelEncoder()
encoder.fit(datasetDiaSemana)
encoded_DiaSemana = encoder.transform(datasetDiaSemana)
dummy_DiaSemana = np_utils.to_categorical(encoded_DiaSemana)

# Mes

datasetMes = dataset[:,3]

datasetMes[1:10]

encoder=LabelEncoder()
encoder.fit(datasetMes)
encoded_Mes = encoder.transform(datasetMes)
dummy_Mes = np_utils.to_categorical(encoded_Mes)

# FinDeSemana

datasetFinDeSemana = dataset[:,5]

datasetFinDeSemana[1:10]

encoder=LabelEncoder()
encoder.fit(datasetFinDeSemana)
encoded_FinDeSemana = encoder.transform(datasetFinDeSemana)
dummy_FinDeSemana = np_utils.to_categorical(encoded_FinDeSemana)

# Quincena

datasetQuincena = dataset[:,6]

datasetQuincena[1:10]

encoder=LabelEncoder()
encoder.fit(datasetQuincena)
encoded_Quincena = encoder.transform(datasetQuincena)
dummy_Quincena = np_utils.to_categorical(encoded_Quincena)

# ca_hora

datasetca_hora = dataset[:,7]

datasetca_hora[1:10]

encoder=LabelEncoder()
encoder.fit(datasetca_hora)
encoded_ca_hora = encoder.transform(datasetca_hora)
dummy_ca_hora = np_utils.to_categorical(encoded_ca_hora)

# seg_str

datasetseg_str = dataset[:,8]

datasetseg_str[1:10]

encoder=LabelEncoder()
encoder.fit(datasetseg_str)
encoded_seg_str = encoder.transform(datasetseg_str)
dummy_seg_str = np_utils.to_categorical(encoded_seg_str)

# ocupacion

datasetocupacion = dataset[:,9]

datasetocupacion[1:10]

encoder=LabelEncoder()
encoder.fit(datasetocupacion)
encoded_ocupacion = encoder.transform(datasetocupacion)
dummy_ocupacion = np_utils.to_categorical(encoded_ocupacion)

# tipo_vivienda

datasettipo_vivienda= dataset[:,10]

datasettipo_vivienda[1:10]

encoder=LabelEncoder()
encoder.fit(datasettipo_vivienda)
encoded_tipo_vivienda = encoder.transform(datasettipo_vivienda)
dummy_tipo_vivienda = np_utils.to_categorical(encoded_tipo_vivienda)

# nivel_academico

datasetnivel_academico= dataset[:,11]

datasetnivel_academico[1:10]

encoder=LabelEncoder()
encoder.fit(datasetnivel_academico)
encoded_nivel_academico = encoder.transform(datasetnivel_academico)
dummy_nivel_academico = np_utils.to_categorical(encoded_nivel_academico)

# estado_civil

datasetestado_civil= dataset[:,12]

datasetestado_civil[1:10]

encoder=LabelEncoder()
encoder.fit(datasetestado_civil)
encoded_estado_civil= encoder.transform(datasetestado_civil)
dummy_estado_civil= np_utils.to_categorical(encoded_estado_civil)

# genero

datasetgenero= dataset[:,13]

datasetgenero[1:10]

encoder=LabelEncoder()
encoder.fit(datasetgenero)
encoded_genero= encoder.transform(datasetgenero)
dummy_genero= np_utils.to_categorical(encoded_genero)

# Cat_edad

datasetCat_edad= dataset[:,15]

datasetCat_edad[1:10]

encoder=LabelEncoder()
encoder.fit(datasetCat_edad)
encoded_Cat_edad= encoder.transform(datasetCat_edad)
dummy_Cat_edad= np_utils.to_categorical(encoded_Cat_edad)

# ingreso_rango

datasetingreso_rango= dataset[:,16]

datasetingreso_rango[1:10]

encoder=LabelEncoder()
encoder.fit(datasetingreso_rango)
encoded_ingreso_rango= encoder.transform(datasetingreso_rango)
dummy_ingreso_rango= np_utils.to_categorical(encoded_ingreso_rango)

# CategoriaRta

datasetCategoriaRta= dataset[:,17]

datasetCategoriaRta[1:10]

encoder=LabelEncoder()
encoder.fit(datasetCategoriaRta)
encoded_CategoriaRta= encoder.transform(datasetCategoriaRta)
dummy_CategoriaRta= np_utils.to_categorical(encoded_CategoriaRta)

# Union Variables

dataframeprueba = pandas.DataFrame(dataset[:,0:2], columns = ['id_trn_ach', 'valor_trx'])
dataframe_DiaSemana = pandas.DataFrame(dummy_DiaSemana, columns = ['DiaSemana_1','DiaSemana_2','DiaSemana_3','DiaSemana_4','DiaSemana_5','DiaSemana_6','DiaSemana_7'])
dataframe_Mes = pandas.DataFrame(dummy_Mes, columns = ['Mes_1','Mes_2','Mes_3','Mes_4','Mes_5','Mes_6','Mes_7','Mes_8','Mes_9','Mes_10','Mes_11','Mes_12'])
dataframe_FinDeSemana = pandas.DataFrame(dummy_FinDeSemana, columns = ['FinDeSemana_1','FinDeSemana_2'])
dataframe_Quincena = pandas.DataFrame(dummy_Quincena, columns = ['Quincena_1','Quincena_2','Quincena_3'])
dataframe_ca_hora = pandas.DataFrame(dummy_ca_hora, columns = ['ca_hora_1','ca_hora_2','ca_hora_3','ca_hora_4','ca_hora_5'])
dataframe_seg_str = pandas.DataFrame(dummy_seg_str, columns = ['seg_str_1','seg_str_2','seg_str_3','seg_str_4','seg_str_5'])
dataframe_ocupacion = pandas.DataFrame(dummy_ocupacion, columns = ['ocupacion_1','ocupacion_2','ocupacion_3','ocupacion_4','ocupacion_5','ocupacion_6','ocupacion_7','ocupacion_8','ocupacion_9','ocupacion_10','ocupacion_11','ocupacion_12','ocupacion_13','ocupacion_14','ocupacion_15','ocupacion_16'])
dataframe_tipo_vivienda = pandas.DataFrame(dummy_tipo_vivienda, columns = ['tipo_vivienda_1','tipo_vivienda_2','tipo_vivienda_3','tipo_vivienda_4','tipo_vivienda_5','tipo_vivienda_6','tipo_vivienda_7','tipo_vivienda_8'])
dataframe_nivel_academico = pandas.DataFrame(dummy_nivel_academico, columns = ['nivel_academico_1','nivel_academico_2','nivel_academico_3','nivel_academico_4','nivel_academico_5','nivel_academico_6','nivel_academico_7','nivel_academico_8','nivel_academico_9','nivel_academico_10'])
dataframe_estado_civil = pandas.DataFrame(dummy_estado_civil, columns = ['estado_civil_1','estado_civil_2','estado_civil_3','estado_civil_4','estado_civil_5','estado_civil_6','estado_civil_7','estado_civil_8'])
dataframe_genero = pandas.DataFrame(dummy_genero, columns = ['genero_1','genero_2','genero_3'])
dataframe_Cat_edad= pandas.DataFrame(dummy_Cat_edad, columns = ['Cat_edad_1','Cat_edad_2','Cat_edad_3','Cat_edad_4','Cat_edad_5','Cat_edad_6','Cat_edad_7','Cat_edad_8'])
dataframe_ingreso_rango = pandas.DataFrame(dummy_ingreso_rango, columns = ['ingreso_rango_1','ingreso_rango_2','ingreso_rango_3','ingreso_rango_4','ingreso_rango_5','ingreso_rango_6','ingreso_rango_7','ingreso_rango_8','ingreso_rango_9','ingreso_rango_10','ingreso_rango_11'])
dataframe_CategoriaRta = pandas.DataFrame(dummy_CategoriaRta, columns = ['CategoriaRta_1','CategoriaRta_2','CategoriaRta_3','CategoriaRta_4','CategoriaRta_5','CategoriaRta_6','CategoriaRta_7','CategoriaRta_8','CategoriaRta_9','CategoriaRta_10','CategoriaRta_11','CategoriaRta_12','CategoriaRta_13','CategoriaRta_14','CategoriaRta_15','CategoriaRta_16','CategoriaRta_17','CategoriaRta_18'])
dataframe_CategoriaRtaValor = pandas.DataFrame(dataset[:,17], columns = ['CategoriaRta'])
dataframe_Encoded_CategoriaRta = pandas.DataFrame(encoded_CategoriaRta, columns = ['Encoded_CategoriaRta'])

dfresult = pandas.concat([dataframeprueba, dataframe_DiaSemana,dataframe_Mes,dataframe_FinDeSemana,dataframe_Quincena,dataframe_ca_hora,dataframe_seg_str,dataframe_ocupacion,dataframe_tipo_vivienda,dataframe_nivel_academico,dataframe_estado_civil,dataframe_genero,dataframe_Cat_edad,dataframe_ingreso_rango,dataframe_CategoriaRta,dataframe_CategoriaRtaValor,dataframe_Encoded_CategoriaRta], axis = 1)

del dataframeprueba
del dataframe_DiaSemana
del dataframe_Mes
del dataframe_FinDeSemana
del dataframe_Quincena
del dataframe_ca_hora
del dataframe_seg_str
del dataframe_ocupacion
del dataframe_tipo_vivienda
del dataframe_nivel_academico
del dataframe_estado_civil
del dataframe_genero
del dataframe_Cat_edad
del dataframe_ingreso_rango
del dataframe_CategoriaRta
del dataframe_CategoriaRtaValor 

# Partición de las bases entre la que va a construir el modelo y la que no
# Base para el modelo: Aquella que tiene categorías diferentes a ´ninguna´

dfresult_modelo = dfresult.loc[dfresult['CategoriaRta'] != 'ninguna']
dfresult_no_modelo = dfresult.loc[dfresult['CategoriaRta'] == 'ninguna']

dfresult_modelo.to_csv(cd_directory+"/TransaccionesModelo.csv", sep=',')
dfresult_no_modelo.to_csv(cd_directory+"/TransaccionesNoModelo.csv", sep=',')
