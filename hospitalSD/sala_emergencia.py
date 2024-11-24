import os
import gestion_doctores
import gestion_pacientes
import gestion_trabajadores
import comunicacion_base
import socket
import threading
import os
import subprocess
import middleware
from datetime import datetime



def mostrarOpciones():
    opcionMenu = 0
    try:
        while opcionMenu != 4:
            os.system('clear') 
            if opcionMenu > 4:
                input("Seleccione una opción válida. Enter para continuar...")
                os.system('cls')  
            print("         Sala de emergencias 1          \n")
            print("1.Registro visita")
            print("2.Cerrar visita [Doctores]")
            print("3.Gestionar salas de emergencia")
            print("4.Salir")
            opcionMenu = int(input("Seleccione una opción: "))
            if int(opcionMenu) == 1:
                mostrarOpRegistro()
            if int(opcionMenu) == 2:
                mostrarOpCerrarVisita()
            if int(opcionMenu) == 3:
                mostrarOpGestion()

    except Exception as e:
        input(f"Ingrese un numero correcto. Enter para continuar...{e}")
        mostrarOpciones()

def mostrarOpRegistro():
    opcionMenu = 0
    try:
        if comunicacion_base.verificaDisponibilidadCama() == 1 and comunicacion_base.verificaDisponiblidadDoctor() == 1:
            mensaje = ''
            nombrePaciente = input("Nombre del paciente: ")
            edadPaciente = int(input("Edad paciente: "))
            descripcionEmergencia = input("Descripción de la emergencia: ")
            mensaje = 'INSERT' + '|' + 'tbl_pacientes' + '|' + nombrePaciente + ',' + str(edadPaciente) + ',' + descripcionEmergencia
            puertoNodo, ipNodo= middleware.asignar_info_nodo()
            ipMaestro, puertoMaestro = middleware.asigna_nodo_maestro(ipNodo)
            client_thread = threading.Thread(target=middleware.cliente, args=(mensaje,int(puertoMaestro),ipMaestro))
            client_thread.start() #Envia informacion directamente al server en nodo maestro 
        else:
            input("Enter para continuar... 1")
    except Exception as e:
        input(f"Datos erroneos, repita el registro y digite la edad correctamente. {e}")
    os.system('cls')

def mostrarOpGestion():
    opcionMenu = 0
    try:
        while opcionMenu != 4:
            os.system('cls') 
            if opcionMenu > 3:
                input("Seleccione una opción válida. Enter para continuar...")
                os.system('cls')  
            print("         Gestion de sala de emergencias 1         \n")
            print("1.Doctores")
            print("2.Pacientes")
            print("3.Trabajadores sociales")
            print("4.Salir")
            opcionMenu = int(input("Seleccione una opción: "))
            if int(opcionMenu) == 1:
                gestion_doctores.mostrarOpDoctores()
            if int(opcionMenu) == 2:
                gestion_pacientes.mostrarOpPacientes()
            if int(opcionMenu) == 3:
                gestion_trabajadores.mostrarOpTrabajadores()
    except:
        input("Ingrese un numero correcto3. Enter para continuar...")
        mostrarOpGestion()

def mostrarOpCerrarVisita():
    os.system('cls') 
    print("         Cerrar visita activa [Doctores]")
    try:
        id_doctor = int(input("Proporcione su ID: "))
        if comunicacion_base.existe_id(id_doctor,"tbl_doctores") == 1:
            folio =comunicacion_base.obtenVisitasDoctor(id_doctor)
            if folio != 0:
                print("Desea cerrar su visita?\n1.Si\n2.No")
                opcion = int(input("Seleccione una opcion: "))
                if opcion == 1:
                    comunicacion_base.cerrarVisitasDoctor(folio)
                elif opcion == 2:
                    input("op2")
                    #mostrarOpciones()
                else:
                    input("Opcion incorrecta. Se regresara al menu principal. Enter para continuar...")
                    #mostrarOpciones()
            else:
                input("El doctor no tiene visitas asigndas. Se regresara al menu principal. Enter para continuar...")
        else:
            input("ID de Doctor inexistente. Enter para continuar...")
    except Exception as e:
        input("Digite un numero valido. Enter para continuar...")
        mostrarOpCerrarVisita()


def main():
    middleware.inicializarMiddleware()
    menu_thread = threading.Thread(target=mostrarOpciones)
    menu_thread.start()




main()

