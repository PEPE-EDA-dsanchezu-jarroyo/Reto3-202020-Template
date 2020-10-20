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
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', greaterFunction)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=greaterFunction)
    return analyzer

# Funciones para agregar informacion al catalogo

def addaccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer

def add_accident2(analyzer,accident):
    """
    Añade un nuevo dato al árbol. Si las llaves son iguales no lo actualiza, lo añade a la lista
    """
    accident_data = (accident['ID'], accident['Severity'], accident['Start_Time'], accident['End_Time'], accident['Start_Lat'], accident['Start_Lng'], accident['End_Lat'], accident['End_Lng'],accident['Country'],accident['TMC'])
    lt.addLast(analyzer['accidents'],accident_data)
    if om.get(analyzer['dateIndex'],accident['Start_Time'][:10]) is None:
        lst = lt.newList(cmpfunction=greaterFunction)
        lt.addLast(lst,accident_data)
        om.put(analyzer['dateIndex'],accident['Start_Time'][:10],lst)
    else:
        entry = om.get(analyzer['dateIndex'],accident['Start_Time'][:10])
        lt.addLast(me.getValue(entry),accident_data)
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
    # accidentdate2 = accident['End_Time'][:10]
    entry = om.get(map, accidentdate.date())
    if entry == None:
        lst=lt.newList()
    else:
        lst=me.getValue(entry)
    lt.addLast(lst,accident)
    # if accidentdate != accidentdate2:
        # om.put(map,accidentdate2,lst)
    om.put(map, accidentdate.date(), lst)
    return map

# ==============================
# Funciones de consulta
# ==============================

def keyset(map):
    return m.keySet(map)

def getKey(tree,key):
    return me.getValue(om.get(tree,key))

def minKey(tree):
    return om.minKey(tree)

def maxKey(tree):
    return om.maxKey(tree)

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

def greaterFunction(el1,el2):
    if el1 > el2:
        return 1
    elif el1 < el2:
        return -1
    return 0 
"""
map = om.newMap(omaptype='BST',comparefunction=greaterFunction)
dat1 = lt.newList()
lt.addLast(dat1,"Val1.1")
om.put(map,"Key1",dat1)
print(om.get(map,"Key1"))
lt.addLast(me.getValue(om.get(map,"Key1"),"Val1.2")
print(om.get(map,"Key1"))
"""
