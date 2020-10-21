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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None,
                'hourindex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED',greaterFunction)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=greaterFunction)
    analyzer['hourindex'] = om.newMap(omaptype='RBT',
                                      comparefunction=greaterFunction)
    return analyzer

# Funciones para agregar informacion al catalogo

def addaccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer, accident)
    return analyzer

def updateDateIndex(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """

    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')

    entrydate = om.get(map['dateIndex'], str(accidentdate.date()))
    entryhour = om.get(map['hourindex'], str(accidentdate.time()))

    if entrydate == None:
        lstdate=lt.newList()
    else:
        lstdate=me.getValue(entrydate)

    if entryhour == None:
        lsthour=lt.newList()
    else:
        lsthour=me.getValue(entryhour)

    lt.addLast(lsthour,accident)
    lt.addLast(lstdate,accident)

    om.put(map['dateIndex'], str(accidentdate.date()), lstdate)
    om.put(map['hourindex'], str(accidentdate.time()), lsthour)

    return map

def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstaccidents': None}
    entry['offenseIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=greaterFunction)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', greaterFunction)
    return entry

# ==============================
# Funciones de consulta
# ==============================

def crimesSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer)


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer)

def keyset(map):
    return m.keySet(map)

def getKey(tree,key):
    return me.getValue(om.get(tree,key))

def getkey2(tree,key):
    return om.get(tree,key)

def values(tree, key1, key2):
    return om.values(tree,key1,key2)

def accidentsBeforeDate(tree,date):
    if greaterFunction(date,maxKey(tree)) == 1:
        return om.keys(tree,minKey(tree),maxKey(tree))
    elif greaterFunction(date,minKey(tree)) == -1:
        return None
    return om.keys(tree,minKey(tree),date)


def listSize(lst):
    return lt.size(lst)

# ==============================
# Funciones de Comparacion
# ==============================

def greaterFunction(el1 ,el2):
    if str(el1) > str(el2):
        return 1
    elif str(el1) < str(el2):
        return -1
    return 0 


