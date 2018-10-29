# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 16:41:59 2018

@author: Lina
"""

import json, csv, re, pandas 
from base64 import b64encode, b64decode

# Directorio de Archivos de Lina
cd_directory = "C:/Users/Lina/Documents/Dataton/Analisis/"

# Nombre de base de datos
cd_name = "dt_trxpse_personas_2016_2018_muestra_adjt.csv"

# Nombre del archivo a escribir
cd_write="dt_trxpse_hora.csv"

def categorizarHora(maxlines,fname):
    maxi=maxlines
    c=0
    fnames=["idtrx","ca_hora"]
    #Abrir el archivo para leer
    with open(fname, encoding="UTF-8") as f:
        #Abrir el archivo para escribir
        with open(cd_directory + cd_write, "w",encoding="UTF-8") as fp:
            w=csv.DictWriter(fp,fnames)
            w.writeheader()
            #Por cada linea en el archivo
            for line in f:
               #Cuenta la linea
               c=c+1
               #Separa por campos
               fields=line.split(",")
               #Cuenta el numero de campas
               number=len(fields)
               
               if number and number>4 and number<=11:
                    try:
                        # Revisa si se puede convertir
                        price = float(fields[4])
                    except ValueError:
                        # Sino es una transacción erronea
                        continue
                    # Identifica la transaccion
                    idtra = fields[0]
                    # Si hay Id de identifcacion y el precio esta entre 1.000 pesos y 50 millones de pesos
                    if price and idtra and price>1000 and price<50000000:
                        hora=float(fields[3])            
                        #Categoriza la hora
                        if hora>=20000 and hora<60000:
                            ca_hora="madrugada"
                        elif hora>=60000 and hora<110000:
                            ca_hora="manana"
                        elif hora>=110000 and hora<140000:
                            ca_hora="mediodia"
                        elif hora>=140000 and hora<190000:
                            ca_hora="tarde"
                        else:
                            ca_hora="noche"
                           
  
                    w.writerow({"idtrx":idtra,"ca_hora":ca_hora})
                    print(c)
    
               if c>maxi:
                   break
        fp.close   
    return c

categorizarHora(maxlines=11842000, fname=cd_directory+cd_name)

datos=pandas.read_csv(cd_directory+"dt_trxpse_hora.csv", sep=",")
