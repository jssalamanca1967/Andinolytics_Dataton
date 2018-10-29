# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:37:26 2018

@author: Lina
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
from sklearn.metrics import confusion_matrix
import functools
import operator 

#Cargar datos
cd_directory = "D:/Documentos/Andinolytics"
dataframe_modelo=pandas.read_csv(cd_directory+"/TransaccionesModelo.csv",sep=",")
dataset = dataframe_modelo.values

# Particion variables independientes
x=dataset[:,2:101].astype(float)
# Partición variables dependientes
y = dataset[:,119]

### Separación entre Train y Test
from sklearn.cross_validation import train_test_split
### Multi asignación de variables
X_train, X_test, y_train, y_test = train_test_split(x, y, 
                                                    # Test de 20% de los datos
                                                    test_size = 0.2,
                                                    # Semilla
                                                    random_state = 0)

# Creación de la variable dummy de la variable de respuesta
from sklearn import preprocessing

le = preprocessing.LabelEncoder()
le.fit(y)
le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
print(le_name_mapping)

encoder=LabelEncoder()
encoder.fit(y)
encoded_y_train= encoder.transform(y_train)
encoded_y_test= encoder.transform(y_test)

dummy_y_train= np_utils.to_categorical(encoded_y_train)
dummy_y_test= np_utils.to_categorical(encoded_y_test)

# Función que permite realizar un análisis de sensibilidad sobre las diferentes composiciones de la
#   red neuronal
# Se construye una red neuronal con 3 capas.
#   @param primer: Número de nodos de la primera capa
#   @param segundo: Número de nodos de la segunda capa
#   @param tercero: Número de nodos de la tercera capa
def funcion(primer, segundo, tercero):
    model=Sequential()
    model.add(Dense(primer, input_dim=99, activation="relu"))
    model.add(Dense(segundo, activation="sigmoid"))
    model.add(Dense(tercero, activation="relu"))
    model.add(Dense(17,activation="softmax"))
    
    model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
    
    model.fit(X_train, dummy_y_train, epochs=1, verbose=1)
    
    predicted_y=model.predict_classes(X_train)
    
    h = 0
    
    encoded_y = encoded_y_train
    
    matrizConfusion_train = confusion_matrix(encoded_y, predicted_y, labels=None, sample_weight=None)
    
    total = len(encoded_y)
    
    for i in range(len(encoded_y)):
        if encoded_y[i] == predicted_y[i]:
            h = h+1
    
    print("Train: 99 /" , primer , "/" , segundo , "/" , tercero , "/ 17 - Epoch:" , 1 , "- Acc:" , h, "/" , total)
    
    predicted_y=model.predict_classes(X_test)
    
    h = 0
    
    encoded_y = encoded_y_test
    
    matrizConfusion_test= confusion_matrix(encoded_y, predicted_y, labels=None, sample_weight=None)
    
    total = len(encoded_y)
    
    for i in range(len(encoded_y)):
        if encoded_y[i] == predicted_y[i]:
            h = h+1
    
    nombre = "99_" + str(primer) + "_" + str(segundo) + "_" + str(tercero) + "_17" + ".csv"
    
    
    numpy.savetxt(cd_directory+"/MatrizTransicion_Train_" + nombre + ".csv", matrizConfusion_train, delimiter=",")
    numpy.savetxt(cd_directory+"/MatrizTransicion_Test_" + nombre + ".csv", matrizConfusion_test, delimiter=",")
    
    
    print("Test: 99 /" , primer , "/" , segundo , "/" , tercero , "/ 17 - Epoch:" , 1 , "- Acc:" , h, "/" , total)
    

# Análisis de sensibilidad de la red neuronal

funcion(10, 10, 10)
funcion(20, 10, 10)
funcion(50, 10, 10)
funcion(50, 50, 10)
funcion(50, 50, 50)
funcion(100, 10, 10)
funcion(100, 50, 10)
funcion(100, 50, 50)
funcion(100, 100, 10)
funcion(100, 100, 50)
funcion(100, 100, 100)
funcion(500, 100, 100)
funcion(500, 500, 500)

del dataframe_modelo

#Definir modelo: 99 inputs, 500 hidden nodes, 100 hidden nodes, 100 hidden nodes, 17 outputs(classes)
model=Sequential()
model.add(Dense(500, input_dim=99, activation="relu"))
model.add(Dense(100, activation="sigmoid"))
model.add(Dense(100, activation="relu"))
model.add(Dense(17,activation="softmax"))

#Compilar el modelo
model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])

#Entrenar el modelo
model.fit(X_train, dummy_y_train, epochs=1, verbose=1)

# Cargue de la base que no presenta categorias asignadas
dataframe_no_modelo=pandas.read_csv(cd_directory+"/TransaccionesNoModelo.csv",sep=",")

dataset_nm = dataframe_no_modelo.values
x_nm=dataset_nm[:,2:101].astype(float)
y_nm = dataset_nm[:,119]

# Predecir
predicted_y=model.predict_classes(x_nm)

y_result =encoder.inverse_transform(predicted_y)
dataframe_result = pandas.DataFrame(y_result, columns = ['Resultado'])

dataframe_result.to_csv(cd_directory+"/Resultado_baseNoModelo.csv", sep=',')

dataframe_result.groupby(['Resultado']).size()
