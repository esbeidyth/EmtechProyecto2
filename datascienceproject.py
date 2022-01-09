#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 12:42:31 2022

@author: esbeidytorres
"""

#---------------------------- Librerias ---------------------------- #
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import operator
df_synergy = pd.read_csv('s_database.csv', index_col = 0, encoding = 'utf-8', parse_dates= [4,5])

#---------------------------- FUNCIONES -------------------------------------- # 
#Esta función nos dice el acumulado de total value dependiendo de un conjunto que nosotros definamos mediante el arg indice
#Indice que es el indicador de columna por la que vamos a ordenar la info 
#El diccionario viejo es nuestra base de información, que debe contener la columna total_value
#Lo que hace esta función es, dada una columna, va a sumar todos los total_value
#diccionario_nuevo contiene, por cada valor posible de la columna indice, el total_value acumulado
def acumulado (indice,diccionario_viejo) :
    diccionario_nuevo = {}
    for envio in diccionario_viejo :
        #print(envio)
        diccionario_nuevo[envio[indice]] = diccionario_nuevo.get(envio[indice],0) + int(envio["total_value"])
    return diccionario_nuevo

#---------------------------- RUTAS: PREGUNTA #1 ---------------------------- #

#**********Sección 1: Acomodo de Dataframes

#Combino el Dataframe para poder organizar mi información por origen, destino y medio de transporte
combinacion_srutas = df_synergy.groupby(by = ['origin' , 'destination' , 'transport_mode'])
describe_srutas = combinacion_srutas.describe()['total_value']

#Genero series para el promedio y para el número de envíos
mean_srutas = describe_srutas["mean"]
count_srutas = describe_srutas["count"]

#Ordenamos
mean_srutas_sort = mean_srutas.sort_values(ascending=False)
count_srutas_sort = mean_srutas.sort_values(ascending=False)

#Regresamos a Dataframe
mean_srutas_sort = mean_srutas_sort.to_frame().reset_index()
count_srutas_sort = count_srutas_sort.to_frame().reset_index()

#Generamos la columna "Rutas"
mean_srutas_sort['Rutas'] = mean_srutas_sort["origin"].str[0:3]+ " " + mean_srutas_sort["destination"].str[0:3]
count_srutas_sort['Rutas'] = count_srutas_sort["origin"].str[0:3]+ " " + count_srutas_sort["destination"].str[0:3]

#Generamos columna rutas en df_synergy y un diccionario
df_synergy['Rutas'] = df_synergy["origin"].str[0:3]+ " " + mean_srutas_sort["destination"].str[0:3]
dict_synergy = df_synergy.to_dict(orient="records")
df_synergy['Extra'] = "igual"
#print(dict_synergy)

#**********Sección 2: rutas************
diccionario_rutas = {}
diccionario_rutas = acumulado("Rutas", dict_synergy)
dict_rutas_sort = sorted(diccionario_rutas.items(), key=operator.itemgetter(1), reverse=True)
total = sum(diccionario_rutas.values())
print("Las rutas más redituables son: \n")
main_rutas = dict_rutas_sort[1:11]
print(dict_rutas_sort[1:11])
print("La suma de las rutas es:\n")
print(total)

print("las rutas principales representan el:\n")

suma_ruta = []
lasuma=0
for ruta in main_rutas :    
    suma_ruta = list(ruta)
    print(suma_ruta)
    for indice in suma_ruta : 
        lasuma = suma_ruta[1]+lasuma

print("el porcentaje que ocupan es:\n")
print(lasuma/total)



#**********Sección 3: Gráficas

#Grafica de rutas Data frame

fig, ax = plt.subplots()
ax.pie([lasuma, total], labels= ["TOP 10 RUTAS","VENTAS TOTALES" ])
plt.show()


#---------------------------- TRANSPORTES: PREGUNTA #2 ---------------------------- #
#**********Sección 1: Calculo
dict_trans = {}
dict_trans = acumulado("transport_mode", dict_synergy)
dict_trans_sort = sorted(dict_trans.items(), key=operator.itemgetter(1), reverse=True)
print("Los medios de transporte obtuvieron los siguientes ingresos: \n")
print(dict_trans_sort)

lista_trans = []

for transporte in dict_trans_sort :    
    lista_trans.append(list(transporte))
print(lista_trans)

lista_trans_valor = []
lista_trans_nombre = []

for dato in lista_trans :
    lista_trans_valor.append(dato[1])
print("Los valores son:")
print(lista_trans_valor) 

for data in lista_trans :
    lista_trans_nombre.append(data[0])
print("Los nombres son:")
print(lista_trans_nombre) 

print(lista_trans_valor[0]/total)
  
#**********Sección 2: Gráficas

#Grafica de transportes Data frame

fig, ax = plt.subplots()
ax.pie(lista_trans_valor, labels = lista_trans_nombre)
plt.show()


#---------------------------- PAISES: PREGUNTA #3 ---------------------------- #

exports = df_synergy[df_synergy['direction'] == 'Exports']
imports = df_synergy[df_synergy['direction'] == 'Imports']


pais_total_value_exports = exports.groupby('origin').sum()['total_value'].reset_index()
total_value_for_percent_exports = pais_total_value_exports['total_value'].sum()

pais_total_value_exports['percent'] = 100 * pais_total_value_exports['total_value'] / total_value_for_percent_exports

pais_total_value_exports.sort_values(by='percent', ascending=False, inplace=True)
# # Creamos la columna cumsum (suma acumulada)
pais_total_value_exports['cumsum'] = pais_total_value_exports['percent'].cumsum()

lista_pequena_1 = pais_total_value_exports[pais_total_value_exports['cumsum'] < 85]

print("Los paises más redituables en exportaciones son: \n")
print(lista_pequena_1)

pais_total_value_imports = imports.groupby('origin').sum()['total_value'].reset_index()
total_value_for_percent_imports = pais_total_value_imports['total_value'].sum()

pais_total_value_imports['percent'] = 100 * pais_total_value_imports['total_value'] / total_value_for_percent_imports

pais_total_value_imports.sort_values(by='percent', ascending=False, inplace=True)

pais_total_value_imports['cumsum'] = pais_total_value_imports['percent'].cumsum()

lista_pequena_2 = pais_total_value_imports[pais_total_value_imports['cumsum'] < 85]

print("Los paises más redituables en importaciones son: \n")
print(lista_pequena_2)



#**********Sección 2: Gráficas

pais_total_value_imports.plot.bar(x="origin", y="total_value", legend = "reverse")
pais_total_value_exports.plot.bar(x="origin", y="total_value", legend = "reverse")