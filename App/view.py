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


#accidentsfile = 'US_Accidents_Dec19.csv'

accidentsfile = 'us_accidents_small.csv'

# _________________________________________________us_accidents_small.csv__
#  Menu principal
# ___________________________________________________

def printIndividualDayAccident(result):
    print("Severidad de accidentes en:",date)
    allAccidents = 0
    for severity in result:
        allAccidents += result[severity]
        print(severity+":",result[severity])
    print("Cantidad de accidentes:",allAccidents)

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
        print("\nCargando información de crimenes ....")
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
            print("Día con más atentados:","{:<12}{:<1}".format(maxim[0]+' -> ',maxim[1]),"atentados")
        else:
            print("No existen pa esa fecha")

    elif int(inputs[0]) == 5:
        print("\nBuscando accidentes en una fecha:")
        date1 = input('Por favor ingrese la fecha inicial de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        date2 = input('Por favor ingrese la fecha final de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
   
        result = controller.accidentsrangedate(cont['dateIndex'],date1, date2)
        printIndividualDayAccident(result)
        

    elif int(inputs[0]) == 6:
        print("\nBuscando accidentes en una fecha:")
        date = input('Por favor ingrese la fecha inicial de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        date = input('Por favor ingrese la fecha final de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
    
        severity = controller.filterSeverityIndividual(cont['dateIndex'],date)
        printIndividualDayAccident(severity)
       

    elif int(inputs[0]) == 7:
        print("\nBuscando accidentes en una fecha:")
        date1 = input('Por favor ingrese la hora inicial de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        date2 = input('Por favor ingrese la hora final de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')

        result = controller.accidentsrangetime(cont['hourindex'],date1, date2)
        if result is not None:
            print("El total de accidentes entre las",date1,"y las",date2,"es:",result[0])
            maxim = (0,0)
            for i in result[1]:
                if result[1][i] > maxim[1]:
                    maxim = (i,result[1][i])
            print("El momento con mas antentados del rango es:","{:<12}{:<1}".format(maxim[0]+' -> ',maxim[1]),"atentados")
        else:
            print("No existen pa esa fecha")
    
    elif int(inputs[0]) == 8:
        print("\nBuscando accidentes en una fecha:")
        date = input('Por favor ingrese la fecha inicial de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        date = input('Por favor ingrese la fecha final de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')

        severity = controller.filterSeverityIndividual(cont['dateIndex'],date)
            
   
    elif int(inputs[0]) == 9:
        print("\nBuscando accidentes en una fecha:")
        date = input('Por favor ingrese la fecha inicial de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        date = input('Por favor ingrese la fecha final de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        severity = controller.filterSeverityIndividual(cont['dateIndex'],date)
        printIndividualDayAccident(severity)

    else:
        sys.exit(0)
sys.exit(0)