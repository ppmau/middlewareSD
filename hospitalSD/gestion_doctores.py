import os
import comunicacion_base
import middleware
import threading

def mostrarOpDoctores():
    opcionMenu = 0
    try:
        while opcionMenu != 3:
            os.system('cls') 
            print("         Gestión de Doctores         \n")
            print("1.Lista de doctores disponibles ")
            print("2.Alta/Actualización/Baja de doctor ")
            print("3.Salir")
            opcionMenu = int(input("Seleccione una opción: "))
            if opcionMenu > 3:
                input("Seleccione una opción válida. Enter para continuar...")
            if int(opcionMenu) == 1:
                listarDoctores()
            if int(opcionMenu) == 2:
                actualizarDoctores()
    except:
        input("Ingrese un numero correcto. Enter para continuar...")
        mostrarOpDoctores()

def listarDoctores():
    os.system('cls')
    print("Lista de doctores")
    comunicacion_base.lista_tabla("tbl_doctores")
    input("Enter para continuar...")


def actualizarDoctores():
    opcionActualizar = int(0)
    try:
        while opcionActualizar != 4:
            os.system('cls')
            print("         Actualizar Doctores         \n")
            print("1. Editar un doctor")
            print("2. Agregar un doctor")
            print("3. Dar de baja un doctor")
            print("4. Salir")
            opcionActualizar = int(input("Seleccione una opción: "))
            if opcionActualizar >= 5:
                input("Seleccione una opción válida. Enter para continuar...")
            if int(opcionActualizar) == 1:
                mostrarOpEditarDoctor()
            if int(opcionActualizar) == 2:
                insertarDoctor()
            if int(opcionActualizar) == 3:
                bajaDoctorBD()
    except:
        input("Ingrese un numero correcto. Enter para continuar...")
        actualizarDoctores()

def mostrarOpEditarDoctor():
    print("     Edición de datos de doctor")
    listarDoctores()
    try:
        puertoNodo, ipNodo= middleware.asignar_info_nodo()
        ipMaestro, puertoMaestro = middleware.asigna_nodo_maestro(ipNodo)
        idDoctor = int(input("Ingrese el id del doctor a editar: "))
        existeId = comunicacion_base.existe_id(idDoctor, "tbl_doctores") ######Trabajo en BASES
        if existeId == 1:
            print("1.Modificar nombre")
            print("2.Modificar curp")
            campo = int(input("Ingrese la opcion deseada: "))
            valor = input("Escriba el valor actualizado:")
            if campo == 1:
                mensajeDoctor = 'UPDATE|tbl_doctores|' + str(idDoctor) + ',' + 'v_nombre' + ',' + valor
            elif campo == 2:
                mensajeDoctor = 'UPDATE|tbl_doctores|' + str(idDoctor) + ',' + 'v_nombre' + ',' + valor
            client_thread = threading.Thread(target=middleware.cliente, args=(mensajeDoctor,int(puertoMaestro),ipMaestro))
            client_thread.start() #Envia informacion directamente al server en nodo maestro 
        else:
            input("ID incorrecto, seleccione uno valido. Enter para continuar...")
            mostrarOpEditarDoctor()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarDoctor()

def insertarDoctor():
    puertoNodo, ipNodo= middleware.asignar_info_nodo()
    ipMaestro, puertoMaestro = middleware.asigna_nodo_maestro(ipNodo)
    print("Escriba los datos del Doctor")
    nombreDoctor = input("Nombre doctor: ")
    curpDoctror = input("CURP: ")
    mensajeDoctor = 'INSERT|tbl_doctores|' + nombreDoctor + ',' + curpDoctror
    client_thread = threading.Thread(target=middleware.cliente, args=(mensajeDoctor,int(puertoMaestro),ipMaestro))
    client_thread.start() #Envia informacion directamente al server en nodo maestro 

def bajaDoctorBD():
    print("Lista de doctores para baja")
    listarDoctores()
    try:
        puertoNodo, ipNodo= middleware.asignar_info_nodo()
        ipMaestro, puertoMaestro = middleware.asigna_nodo_maestro(ipNodo)
        idDoctor = int(input("Ingrese el id del doctor a dar de bajaaa: "))
        existeId = comunicacion_base.existe_id(idDoctor, "tbl_doctores")
        if existeId == 1:
            mensajeDoctor = 'DELETE|tbl_doctores|' + str(idDoctor)
            client_thread = threading.Thread(target=middleware.cliente, args=(mensajeDoctor,int(puertoMaestro),ipMaestro))
            #comunicacion_base.eliminar_en_tabla(idDoctor,"tbl_doctores")
        else:
            input("ID incorrecto, seleccione uno valido. Enter para continuar...")
            mostrarOpEditarDoctor()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarDoctor()