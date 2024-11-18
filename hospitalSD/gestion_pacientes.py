import os
import comunicacion_base
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
        idPaciente = int(input("Ingrese el id del paciente a editar: "))
        existeId = comunicacion_base.existe_id(idPaciente, "tbl_pacientes") ######Trabajo en BASES
        if existeId == 1:
            print("1.Modificar nombre")
            print("2.Modificar edad")
            print("3.Modificar emergencia")
            campo = int(input("Ingrese la opcion deseada: "))
            valor = input("Escriba el valor actualizado:")
            if campo == 1:
                comunicacion_base.actualizar_tabla(idPaciente,"v_nombre","tbl_pacientes",valor)
            elif campo == 2:
                comunicacion_base.actualizar_tabla(idPaciente, "v_edad","tbl_pacientes", valor)
            elif campo == 3:
                comunicacion_base.actualizar_tabla(idPaciente,"v_emergencia", "tbl_pacientes", valor)
        else:
            input("ID incorrecto, seleccione uno valido. Enter para continuar...")
            mostrarOpEditarPaciente()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarPaciente()

def insertaPacienteBD(nombrePaciente,edadPaciente,emergencia):
    valores = [nombrePaciente,edadPaciente,emergencia]
    comunicacion_base.insertar_en_tabla(valores,"tbl_pacientes")
    id_doctor = comunicacion_base.obtenDoctorDisponible()
    id_paciente =comunicacion_base.obtenIdUltimoPaciente()
    id_sala = comunicacion_base.obtenSalaDisponible()
    id_visita = int(comunicacion_base.obtenIdUltimaVisita()) + 1
    folio_visita = "P" + str(id_paciente) + "D" + str(id_doctor) + "S" + str(id_sala[0]) + "C" + str(id_sala[1]) + "V" + str(id_visita)
    input(folio_visita)
    valores = [id_paciente,id_doctor,id_sala[0],id_sala[1],folio_visita,1,datetime.now().strftime("%Y-%m-%d")]
    comunicacion_base.insertar_en_tabla(valores,"tbl_visitas")

def bajaPacienteBD():
    print("Lista de pacientes para baja")
    listarPacientes()
    try:
        idPaciente = int(input("Ingrese el id del paciente a dar de baja: "))
        existeId = comunicacion_base.existe_id(idPaciente, "tbl_pacientes")
        if existeId == 1:
            comunicacion_base.eliminar_en_tabla(idPaciente,"tbl_pacientes")
        else:
            input("ID incorrecto, seleccione uno valido. Enter para continuar...")
            mostrarOpEditarPaciente()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarPaciente()


    
