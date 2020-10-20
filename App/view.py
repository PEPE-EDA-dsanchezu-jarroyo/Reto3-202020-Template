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

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config
import time 

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


# accidentsfile = 'us_accidents_dis_2019.csv'
accidentsfile = 'us_accidents_small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printIndividualDayAccident(result):
    print("Severidad de accidentes en:",date)
    allAccidents = 0
    for severity in result:
        allAccidents += result[severity]
        print(severity+":",result[severity])
    print("Cantidad de accidentes:",allAccidents)

def printSeverity(severity_dict):
    print("Severidad de accidentes entre: ",loDate,"-",hiDate)
    for severity in severity_dict:
        print(severity+":",severity_dict[severity])

def printMenu():
    print("\n")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Conocer accidentes en una fecha (Requerimento 1)")
    print("4- Conocer accidentes anteriores a una fecha (Requerimento 2)")
    print("5- Conocer accidentes en un rango de fechas (Requerimento 3)")
    print("0- Salir")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        t1=time.process_time()
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accidentsfile)
        # controller.loadData(cont,accidentsfile)
        t2=time.process_time()
        print('\nTiempo de ejecución:',t2-t1,"segundos")

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha:")
        date = input('Por favor ingrese la fecha de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        try:
            severity = controller.filterSeverityIndividual(cont['dateIndex'],date)
            printIndividualDayAccident(severity)
        except KeyError or TypeError:
            print("No se encontró la llave")


    elif int(inputs[0]) == 4:
        print("\nBuscando accidentes antes de una fecha: ")
        date = input('Por favor ingrese la fecha de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        result = controller.accidentBeforeDate(cont['dateIndex'],date)
        # print(result[1])
        if result is not None:
            print("El total de accidentes antes el",date,"es:",result[0])
            maxim = (0,0)
            for i in result[1]:
                if result[1][i] > maxim[1]:
                    maxim = (i,result[1][i])
            print("Día con más atentados:",maxim[0],'->',maxim[1],"atentados (accidentes)")
        else:
            print("No existen pa esa fecha")
    
    elif int(inputs[0]) == 5:
        print("\n Buscando accidentes en un rango de fechas: ")
        loDate = input('Por favor ingrese la fecha inferior de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        hiDate = input('Por favor ingrese la fecha superior de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        num_accidents, severity = controller.accidentsInRange(cont['dateIndex'],loDate,hiDate)
        printSeverity(severity)
        print("Cantidad de accidentes:",num_accidents)



    else:
        sys.exit(0)
sys.exit(0)
