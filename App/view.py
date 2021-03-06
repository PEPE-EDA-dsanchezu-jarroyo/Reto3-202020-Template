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

accidentsfile = 'us_accidents_small.csv'
# accidentsfile = 'us_accidents_dis_2019.csv'
#accidentsfile = 'US_Accidents_Dec19.csv'

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
    print("Severidad de accidentes entre: ",loDate,"y",hiDate)
    for severity in severity_dict:
        print(severity+":",severity_dict[severity])

def printhorasinrange(total,severity_dict):
    print('el total de accidentes entre fue '+str(total))
    for severidad in severity_dict:
        print("{:<5}{:<7}{:<7}".format(severidad+":",str(severity_dict[severidad]),str(round((severity_dict[severidad]/total)*100,2))+'%'))

def printStates(state_dict):
    print("Accidentes por estado entre: ",loDate,"y",hiDate)
    max_state = [0,'']
    for state in state_dict:
        print("{:<5}{:<5}".format(state,state_dict[state]))
        if state_dict[state] > max_state[0]:
            max_state[0] = state_dict[state]
            max_state[1] = state
    return (max_state[0],max_state[1])

def printReq6(result):
    print("{:<15}{:<15}".format("Lunes",result[1][0]))
    print("{:<15}{:<15}".format("Martes",result[1][1]))
    print("{:<15}{:<15}".format("Miércoles",result[1][2]))
    print("{:<15}{:<15}".format("Jueves",result[1][3]))
    print("{:<15}{:<15}".format("Viernes",result[1][4]))
    print("{:<15}{:<15}".format("Sábado",result[1][5]))
    print("{:<15}{:<15}".format("Domingo",result[1][6]))
    print()
    print("El total de accidentes en el área indicada es:",result[0],"accidentes")

def printMenu():
    print("\n")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- REQ. 1: Conocer los accidentes en una fecha")
    print("4- REQ. 2: Conocer los accidentes anteriores a una fecha")
    print("5- REQ. 3: Conocer los accidentes en un rango de fechas (Individual)")
    print("6- REQ. 4: Conocer el estado con mas accidentes (Individual)")
    print("7- Req. 5: Conocer los accidentes por rango de horas")
    print("8- REQ. 6: Conocer la zona geográfica mas accidentada")
    print("9- REQ. 7: Usar el conjunto completode datos")
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
        print('Crimenes cargados: ' + str(controller.crimesSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont['dateIndex'])))
        print('Mayor Llave: ' + str(controller.maxKey(cont['dateIndex'])))
        t2=time.process_time()
        print('\n',t2-t1)

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
        num_accidents, severity = controller.accidentsInDateRange(cont['dateIndex'],loDate,hiDate)
        printSeverity(severity)
        print("Cantidad de accidentes:",num_accidents)


    elif int(inputs[0]) == 6:
        print("\nFiltrando accidentes por estado:")
        loDate = input('Por favor ingrese la fecha inferior de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        hiDate = input('Por favor ingrese la fecha superior de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        max_accidents_date, num_accidents, states_dict_result = controller.accidents4state(cont['dateIndex'],loDate,hiDate)
        num_max_state, max_state = printStates(states_dict_result)
        print()
        print("El estado con más accidentes entre las fechas es:",max_state,"con",num_max_state,"atentados (accidentes)")       
        print("El día con más accidentes entre las dos fechas es:",max_accidents_date,"con",num_accidents,"atentados (accidentes)")


    elif int(inputs[0]) == 7:
        print("\nBuscando accidentes en una fecha:")
        date1 = input('Por favor ingrese la hora inicial de la cuál desea buscar los accidentes: (HH:MM:SS)\n')
        date2 = input('Por favor ingrese la hora final de la cuál desea buscar los accidentes: (HH:MM:S)\n')

        total,severity = controller.accidentsrangetime(cont['hourindex'],date1, date2)

        printhorasinrange(total,severity)
       
    
    elif int(inputs[0]) == 8:
        print("\nBuscando accidentes en una fecha:")
        lat = float(input('Por favor ingrese la latitud del centro: \n'))
        lon = float(input('Por favor ingrese la longitud del centro: \n'))
        radius = float(input('Por favor ingrese el radio que quiere buscar: \n'))
        result = controller.filter_distance(cont['accidents'],lon,lat,radius)
        printReq6(result)
            
   
    elif int(inputs[0]) == 9:
        print("\nBuscando accidentes en una fecha:")
        date = input('Por favor ingrese la fecha inicial de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        date = input('Por favor ingrese la fecha final de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        severity = controller.filterSeverityIndividual(cont['dateIndex'],date)
        printIndividualDayAccident(severity)

    else:
        sys.exit(0)
sys.exit(0)