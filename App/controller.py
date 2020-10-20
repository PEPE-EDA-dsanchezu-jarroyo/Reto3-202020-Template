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
        model.addaccident(analyzer, accident)
        # if i%29743 == 0:
        # if i%8787 == 0:
            # print (" " + str(p) + "%" + " completado", end="\r")
            # p+=1

        i+=1
    return analyzer

def load_data_2(analyzer,accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    i = 0
    p = 0
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"),delimiter=",")
    for accident in input_file:
        model.add_accident2(analyzer,accident)
        if i%8787 == 0:
            print (" " + str(p) + "%" + " completado", end="\r")
            p+=1
        i+=1
    return analyzer



# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

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