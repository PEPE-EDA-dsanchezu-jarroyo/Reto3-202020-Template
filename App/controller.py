"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from App import model
import datetime
import csv
from DISClib.DataStructures import listiterator as it
import time
import sys

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer



# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"),
                                delimiter=",")
    # print(sys.getsizeof(input_file))
    i = 0
    p = 0
    for accident in input_file:

        del accident['Description']
        del accident['Source']
        del accident['TMC']
        del accident['Number']
        del accident['Street']
        del accident['Side']
        del accident['City']
        del accident['County']
        del accident['Zipcode']
        del accident['Timezone']
        del accident['Airport_Code']
        del accident['Weather_Timestamp']
        del accident['Temperature(F)']
        del accident['Wind_Chill(F)']
        del accident['Humidity(%)']
        del accident['Pressure(in)']
        del accident['Visibility(mi)']
        del accident['Wind_Direction']
        del accident['Wind_Speed(mph)']
        del accident['Precipitation(in)']
        del accident['Weather_Condition']
        del accident['Amenity']
        del accident['Bump']
        del accident['Crossing']
        del accident['Give_Way']
        del accident['Junction']
        del accident['No_Exit']
        del accident['Railway']
        del accident['Roundabout']
        del accident['Station']
        del accident['Stop']
        del accident['Traffic_Calming']
        del accident['Traffic_Signal']
        del accident['Turning_Loop']
        del accident['Sunrise_Sunset']
        del accident['Nautical_Twilight']
        del accident['Civil_Twilight']
        del accident['Astronomical_Twilight']
        del accident['End_Lat']
        del accident['End_Lng']
        # print(sys.getsizeof(accident))
        model.addaccident(analyzer, accident)
        # if i%29743 == 0:
        if i%8787 == 0:
        #if i%30000 == 0:
            print (" " + str(p) + "%" + " completado", end="\r")
            p+=1
        i+=1
    # print(sys.getsizeof(analyzer),'Bytes')    
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def crimesSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.crimesSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)
def keyset (map):
    return model.keyset(map)

def getAccident(tree,key):
    return model.getKey(tree,key)

def filterSeverityIndividual(tree,raw_date):
    date = datetime.datetime.strptime(raw_date, '%Y-%m-%d').date()
    lst_result = getAccident(tree,date)
    result = it.newIterator(lst_result)
    severity = {"1":0,
                "2":0,
                "3":0,
                "4":0}
    while it.hasNext(result):
        accident = it.next(result)
        severity[accident['Severity']] += 1 
    return severity

def accidentBeforeDate(tree,raw_date):
    date = datetime.datetime.strptime(raw_date, '%Y-%m-%d').date()
    result = model.accidentsBeforeDate(tree,date)
    if result is None:
        return None
    total = 0
    dates = {}
    iterator1 = it.newIterator(result)
    while it.hasNext(iterator1):
        day = it.next(iterator1)
        accidents = model.getKey(tree,day)
        dates[day] = model.listSize(accidents)
        total += model.listSize(accidents)    
    return (total,dates)

def accidentsInRange(tree,low_raw_date,high_raw_date):
    loDate = datetime.datetime.strptime(low_raw_date, '%Y-%m-%d').date()
    hiDate = datetime.datetime.strptime(high_raw_date, '%Y-%m-%d').date()
    num_accidents = 0
    severity = {"1":0,
                "2":0,
                "3":0,
                "4":0}
    lst_accidents_iterator = it.newIterator(model.range_accidents(tree,loDate,hiDate))
    while it.hasNext(lst_accidents_iterator):
        bucket = it.next(lst_accidents_iterator)
        bucket_iterator = it.newIterator(bucket)
        while it.hasNext(bucket_iterator):
            element = it.next(bucket_iterator)
            num_accidents += 1
            severity[element['Severity']] += 1
    return (num_accidents,severity)
def accidentsrangetime(tree,time1,time2):
    # time1='05:46:00'
    # time2='06:07:59'

    time1=model.strtotimedate(time1,'time')
    time2=model.strtotimedate(time2,'time')
    time1=model.RedondearHoras(time1)
    time2=model.RedondearHoras(time2)

    result=model.values(tree,time1,time2)


    if result is None:
        return None
    
    total=0
    severity = {"1":0,
                "2":0,
                "3":0,
                "4":0}
    iterator1=it.newIterator(result)
    while it.hasNext(iterator1):
        lst=it.newIterator(it.next(iterator1))
        while it.hasNext(lst):
            total+=1
            severity[it.next(lst)['Severity']] += 1

    return (total, severity)







