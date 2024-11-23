import os
import gestion_doctores
import gestion_pacientes
import gestion_trabajadores
import comunicacion_base
import middleware
import socket
import threading
import os
import subprocess
import middleware
from datetime import datetime

server_ready = None
#server_ready = threading.Event() #Variable global para controlar inicializacion del servidor y sincronizar con los clientes


def mostrarOpciones(serverReady):
    serverReady.wait()
    opcionMenu = 0
    try:
        while opcionMenu != 4:
            os.system('cls') 
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

def mostrarOpRegistro(serverReady):
    serverReady.wait()
    opcionMenu = 0
    try:
        if comunicacion_base.verificaDisponibilidadCama() == 1 and comunicacion_base.verificaDisponiblidadDoctor() == 1:
            nombrePaciente = input("Nombre del paciente: ")
            edadPaciente = int(input("Edad paciente: "))
            descripcionEmergencia = input("Descripción de la emergencia: ")
            puertoNodo, ipNodo= middleware.asignar_info_nodo()
            ipMaestro, puertoMaestro = middleware.asigna_nodo_maestro(ipNodo)  
            mensaje = "INSERT|tbl_doctores|Jose Mauricio,PEPM960630HDF"
            #middleware.cliente(mensaje,12345,'192.168.252.134')
            client_thread = threading.Thread(target=middleware.cliente, args=(mensaje,12345,'192.168.252.134',server_ready))
            client_thread.start() #Envia informacion directamente al server en nodo maestro 

            #gestion_pacientes.insertaPacienteBD(nombrePaciente,edadPaciente,descripcionEmergencia)
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
                    mostrarOpciones()
                else:
                    input("Opcion incorrecta. Se regresara al menu principal. Enter para continuar...")
                    mostrarOpciones()
            else:
                input("El doctor no tiene visitas asigndas. Se regresara al menu principal. Enter para continuar...")
        else:
            input("ID de Doctor inexistente. Enter para continuar...")
    except Exception as e:
        input("Digite un numero valido. Enter para continuar...")
        mostrarOpCerrarVisita()
        
def main():
    global server_ready
    salaEmergencia = 1
    server_ready = threading.Event()
    server_thread = threading.Thread(target=middleware.server, args=(server_ready,))
    server_thread.start()
    #middleware.mandarMensajeNodoMaestro("INSERT|tbl_doctores|Jose Mauricio, PEPM960630HDF")
    #middleware.mandarMensajeNodoMaestro("UPDATE|tbl_doctores|1,v_nombre,Dr. Mauricio")
    #middleware.mandarMensajeNodoMaestro("DELETE|tbl_doctores|5")
    main_thread = threading.Thread(target=mostrarOpciones,args=(server_ready,))
    main_thread.start()


main()
