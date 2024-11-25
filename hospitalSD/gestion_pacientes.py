import os
import comunicacion_base
import middleware
import threading
from datetime import datetime

def mostrarOpPacientes():
    opcionMenu = 0
    try:
        while opcionMenu != 3:
            os.system('cls') 
            print("         Gestión de Pacientes        \n")
            print("1.Lista de pacientes ")
            print("2.Alta/Actualización/Baja de pacientes ")
            print("3.Salir")
            opcionMenu = int(input("Seleccione una opción: "))
            if opcionMenu > 3:
                input("Seleccione una opción válida. Enter para continuar...")
            if int(opcionMenu) == 1:
                listarPacientes()
            if int(opcionMenu) == 2:
                actualizarPacientes()
    except:
        input("Ingrese un numero correcto2. Enter para continuar...")
        mostrarOpPacientes()

def listarPacientes():
    os.system('cls')
    print("Lista de pacientes")
    comunicacion_base.lista_tabla("tbl_pacientes")
    input("Enter para continuar...")


def actualizarPacientes():
    opcionActualizar = int(0)
    try:
        while opcionActualizar != 3:
            os.system('cls')
            print("         Actualizar Pacientes         \n")
            print("1. Editar un paciente")
            print("2. Dar de baja un paciente")
            print("3. Salir")
            opcionActualizar = int(input("Seleccione una opción: "))
            if opcionActualizar >= 4:
                input("Seleccione una opción válida. Enter para continuar...")
            if int(opcionActualizar) == 1:
                mostrarOpEditarPaciente()
            if int(opcionActualizar) == 2:
                bajaPacienteBD()
    except:
        input("Ingrese un numero correcto1. Enter para continuar...")
        actualizarPacientes()

def mostrarOpEditarPaciente():
    print("     Edición de datos de paciente")
    listarPacientes()
    try:
        puertoNodo, ipNodo= middleware.asignar_info_nodo()
        ipMaestro, puertoMaestro = middleware.asigna_nodo_maestro(ipNodo)
        idPaciente = int(input("Ingrese el id del paciente a editar: "))
        existeId = comunicacion_base.existe_id(idPaciente, "tbl_pacientes") ######Trabajo en BASES
        if existeId == 1:
            print("1.Modificar nombre")
            print("2.Modificar edad")
            print("3.Modificar emergencia")
            campo = int(input("Ingrese la opcion deseada: "))
            valor = input("Escriba el valor actualizado:")
            if campo == 1:
                mensajePaciente = 'UPDATE|tbl_pacientes|' + str(idPaciente) + ',' + 'v_nombre' + ',' + valor
            elif campo == 2:
                mensajePaciente = 'UPDATE|tbl_pacientes|' + str(idPaciente) + ',' + 'v_edad' + ',' + valor
            elif campo == 3:
                mensajePaciente = 'UPDATE|tbl_pacientes|' + str(idPaciente) + ',' + 'v_emergencia' + ',' + valor

            client_thread = threading.Thread(target=middleware.cliente, args=(mensajePaciente,int(puertoMaestro),ipMaestro))
            client_thread.start() #Envia informacion directamente al server en nodo maestro 
        else:
            input("ID incorrecto, seleccione uno valido. Enter para continuar...")
            mostrarOpEditarPaciente()
    except Exception as e:
        input(f"Ingrese un número válido. Enter para continuar...{e}")
        mostrarOpEditarPaciente()

def insertaPacienteBD(nombrePaciente,edadPaciente,emergencia,ipNodo,puertoNodo):
    valores = [nombrePaciente,edadPaciente,emergencia]
    mensajePaciente = 'INSERT-PACIENTE-VISITA|tbl_pacientes|' + nombrePaciente + ',' + str(edadPaciente) + ',' + emergencia
    client_thread = threading.Thread(target=middleware.cliente, args=(mensajePaciente,int(puertoNodo),ipNodo))
    client_thread.start() #Envia informacion directamente al server en nodo maestro 

def bajaPacienteBD():
    print("Lista de pacientes para baja")
    listarPacientes()
    try:
        puertoNodo, ipNodo= middleware.asignar_info_nodo()
        ipMaestro, puertoMaestro = middleware.asigna_nodo_maestro(ipNodo)
        idPaciente = int(input("Ingrese el id del paciente a dar de baja: "))
        existeId = comunicacion_base.existe_id(idPaciente, "tbl_pacientes")
        if existeId == 1:
            mensajePaciente = 'DELETE|tbl_pacientes|' + str(idPaciente)
            client_thread = threading.Thread(target=middleware.cliente, args=(mensajePaciente,int(puertoMaestro),ipMaestro))
            client_thread.start() #Envia informacion directamente al server en nodo maestro 
        else:
            input("ID incorrecto, seleccione uno valido. Enter para continuar...")
            mostrarOpEditarPaciente()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarPaciente()


    
