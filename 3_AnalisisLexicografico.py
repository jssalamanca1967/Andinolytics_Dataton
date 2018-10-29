#!/usr/bin/env python3
import json, csv, re
from base64 import b64encode, b64decode
import unicodedata

# GLOBALES
# Directorio de Archivos de Cristian
cd_directory = "/Users/Cristian/Downloads/dataton-info/"
# Directorio de Archivos de Lina
# cd_directory = "C:/Users/Lina/Documents/Dataton/Analisis/"

# Nombre de base de datos
cd_name = "dt_trxpse_personas_2016_2018_muestra_adjt.csv"

# Arreglar formato palabras
def strip_accents(text):
    try:
        text=unicode(text,'utf-8')
    except NameError:
        pass
    text=unicodedata.normalize('NFD',text)
    text=text.encode('ascii','ignore')
    text=text.decode('utf-8')
    return str(text)

# Metodo que crea diccionario limpiando los datos.
# maxlineas - Numero máximo de lineas a revisar, si se coloca un número negativo se analizan todas.
# fname - path del archivo a leer
# check - Se escribe en terminal cada vez que se complete (check) transacciones.
def crearDiccionario(maxlineas, fname, check=50000):
    maxi = maxlineas 
    # Contador de lineas, equivalente a transacciones leidas
    c = 0
    # Diccionario para almacenar palabras entra por parametro
    dictionary={}
    with open(fname, encoding="UTF-8") as f:
        # Por cada linea en el archivo
        for line in f:
            # Cuenta una linea
            c=c+1
            # Separa por campos
            fields = line.split(',')
            # Numero de columnas
            number = len(fields)
            # Si hay columnas y estan entre 4 y 11
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
                    ref = ""
                    if fields[5]: # Existe valor en Ref1?
                        ref = fields[5].lower()
                    if number>6 and fields[6]: # Existe valor en Ref2?
                        ref = ref+fields[6].lower()
                    if number>7 and fields[7]: # Existe valor en Ref3?
                        ref = ref+fields[7].lower()
                    
                    # Separa por caracteres especiales
                    words = re.split(';| |:|=|;|\s|\v|[|]|(|)|_|+|-', ref)
                    # Recorre las palabras
                    for w in words:
                        w=strip_accents(str(w))
                        if w in dictionary: # Si esta registrada antes, suma el contador a 1
                            dictionary[w] = dictionary[w] + 1
                        else: # Sino esta registrada, la adiciona
                            dictionary[w] = 1
                # Si Supera el limite de transacciones procesadas, termina
                if c>maxi:
                    break
                # Revisa avance
                if c%check==0:
                    print(c)
    return dictionary

# Metodo que crea diccionario SOLO usando las transacciones con SECTOR.
# maxlineas - Numero máximo de lineas a revisar, si se coloca un número negativo se analizan todas.
# fname - path del archivo a leer
# check - Se escribe en terminal cada vez que se complete (check) transacciones.
def crearDiccionarioDeTransaccionesConSectores(maxlineas, fname, check=50000):
    maxi = maxlineas 
    # Contador de lineas, equivalente a transacciones leidas
    c = 0
    # Diccionario para almacenar palabras entra por parametro
    dictionary={}
    with open(fname, encoding="UTF-8") as f:
        # Por cada linea en el archivo
        for line in f:
            # Cuenta una linea
            c=c+1
            # Separa por campos
            fields = line.split(',')
            # Numero de columnas
            number = len(fields)
            # Si hay columnas y estan entre 4 y 11
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
                    ref = ""
                    if fields[5]: # Existe valor en Ref1?
                        ref = fields[5].lower()
                    if number>6 and fields[6]: # Existe valor en Ref2?
                        ref = ref+' '+fields[6].lower()
                    if number>7 and fields[7]: # Existe valor en Ref3?
                        ref = ref+' '+fields[7].lower()
                    if number>10 and fields[10] and not fields[10].lower().startswith("\\n"): # Existe valor en Descripcion?
                        ref = ref+' '+fields[10].lower().strip()
                    
                    # Reuniendo informacion del sector
                    sec = ""
                    if number>8 and fields[8] and not fields[8].lower().startswith("\\n"):
                        sec = fields[8].lower()
                        if number>9 and fields[9] and not fields[9].lower().startswith("\\n"):
                            sec = sec + ' ' + fields[9].lower()
                    else:
                        # Si no tiene información del sector no lo toma en cuenta
                        continue


                    # Separa por caracteres especiales
                    words = re.split('_|-|;| |:|=|;|\s|\v|[|]|(|)', ref)
                    #words = re.split('(; :=;\s\v_-)|\(|\)', ref)
                    
                    # Recorre las palabras
                    for w in words:
                        w=strip_accents(str(w))
                        if w in dictionary: # Si esta registrada antes, suma el contador a 1
                            dictionary[w]["numero"] = dictionary[w]["numero"] + 1
                            if sec in dictionary[w]: # El sector ya estaba relacionado con la palabra
                                dictionary[w][sec] = dictionary[w][sec] + 1
                            else: # El sector no estaba relacionado con la palabra, hay que crearla
                               dictionary[w][sec] = 1 
                        else: # Sino esta registrada, la adiciona
                            dictionary[w] = {}
                            dictionary[w]["numero"] = 1
                            dictionary[w][sec] = 1
                # Si Supera el limite de transacciones procesadas, termina
                if c>maxi:
                    break
                # Revisa avance
                if c%check==0:
                    print(c)
    return dictionary

# Método para imprimir el archivo en JSON
def printFileJSON(path, param):
    with open(path, 'w', encoding='utf-8') as fp:
        json.dump(param, fp, ensure_ascii=False)

# Método para imprimir el archivo en CSV
def printFileCSV(path, param):
    with open(path, 'w', encoding='utf-8') as fp:
        w = csv.writer(fp)
        w.writerow(["Word", "Count"])
        for k,v in param.items():
            w.writerow([k,v])

# Método para imprimir el archivo en CSV
def printFileCSVTransaccionesConSectores(path, param):
    with open(path, 'w', encoding='utf-8') as fp:
        w = csv.writer(fp)
        w.writerow(["Word", "Count"])
        for k,v in param.items():
            listRow = [k,v["numero"]]
            for l,b in v.items():
                if l!="numero":
                    listRow.append(l)
                    listRow.append(b)
            w.writerow(listRow)
#------------------------------------
# MAIN
#------------------------------------

def extraerTodasLasPalabras():
    # Ejecuta el divisor de palabras
    maxlineas = 11000000
    cd_file = cd_directory+cd_name
    wordsCount = crearDiccionario(maxlineas, cd_file)

    #print(len(wordsCount))
    #print(wordsCount)

    # Almacena en un archivo JSON
    cd_file_wordcount = cd_directory+'countwords'+'.json'
    printFileJSON(cd_file_wordcount, wordsCount)

    # Almacena en un archivo CSV
    cd_file_wordcount = cd_directory+'countwords'+'.csv'
    printFileCSV(cd_file_wordcount, wordsCount)

def extraerTodasLasPalabrasDeTransaccionesConSectores():
    # Ejecuta el divisor de palabras
    maxlineas = 12000000
    cd_file = cd_directory+cd_name
    wordsCountSectores = crearDiccionarioDeTransaccionesConSectores(maxlineas, cd_file)

    # Almacena en un archivo JSON
    cd_file_wordcount = cd_directory+'countwordsSectorizado'+'.json'
    printFileJSON(cd_file_wordcount, wordsCountSectores)

    # Almacena en un archivo CSV
    cd_file_wordcount = cd_directory+'countwordsSectorizado'+'.csv'
    printFileCSVTransaccionesConSectores(cd_file_wordcount, wordsCountSectores)

#------------------------------------
# Macro a Ejecutar
#------------------------------------

#extraerTodasLasPalabras()
extraerTodasLasPalabrasDeTransaccionesConSectores()