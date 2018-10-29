#!/usr/bin/env python3
import json, csv, re
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

def leerClasificatorio(maxlineas, fname, check=100):
    maxi = maxlineas 
    # Contador de lineas, equivalente a transacciones leidas
    c = 0
    # Diccionario para almacenar palabras entra por parametro
    clasifier = {}
    with open(fname, encoding="UTF-8") as f:
        # Por cada linea en el archivo
        for line in f:
            # Cuenta una linea
            c=c+1
            # Separa por campos
            fields = line.lower().split(',')
            # Numero de columnas
            number = len(fields)
            # Palabra
            word = strip_accents(str(fields[0]))
            # Categoria
            category = strip_accents(str(fields[1]))
            
            # Asignacion palabra-categoria
            clasifier[word] = category

            if c>maxi:
                break
            # Revisa avance
            if c%check==0:
                print(c)
    return clasifier

# Metodo que crea asigna categoria.
# maxlineas - Numero máximo de lineas a revisar, si se coloca un número negativo se analizan todas.
# f_before - Path archivo a leer
# f_after - Path archivo a escribir
# check - Se escribe en terminal cada vez que se complete (check) transacciones.
def asignarCategoria(maxlineas, f_before, f_after, clasifier, check=50000):
    maxi = maxlineas
    # Contador de lineas, equivalente a transacciones leidas
    c = 0
    # Archivo de transacciones sin clasificar
    with open(f_before, encoding="UTF-8") as f_read:
        # Archivo de transacciones con clasificacion
        with open(f_after, 'w', encoding="UTF-8") as f_write:
            for line in f_read:
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
                        words = re.split('_|-|;| |:|=|;|\s|\v|[|]|(|)', ref)
                        #words = re.split(';| |:|=|;|\s|\v|[|]|(|)|_|+|-', ref);
                        category = "ninguna\n"
                        # Recorre las palabras
                        description = ""
                        for w in words:
                            w=strip_accents(str(w))
                            description = description+w+" "
                            if w in clasifier: # Si esta en el clasificador
                                category = clasifier[w]
                    
                    # Escribe resultado
                    f_write.write(idtra+','+fields[1]+','+fields[2]+','+fields[3]+','+str(price)+','+description+','+category)
                    # Si Supera el limite de transacciones procesadas, termina
                    if c>maxi:
                        break
                    # Revisa avance
                    if c%check==0:
                        print(c)
    return
#---------------------------------------
#  MAIN
#---------------------------------------
maxlineas = 12000000
#maxlineas = 100000
cd_address = cd_directory+'palabrasycategorias.csv'

clasificatorio = leerClasificatorio(maxlineas, cd_address, check=100)
print(clasificatorio)

cd_address_read = cd_directory+cd_name
cd_address_write = cd_directory+'categoria_asignada.csv'

asignarCategoria(maxlineas, cd_address_read, cd_address_write, clasificatorio, check=50000)
