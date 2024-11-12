import os
import comunicacion_base

def mostrarOpDoctores():
    opcionMenu = 0
    try:
        while opcionMenu != 3:
            os.system('cls') 
            print("         Gestión de Doctores         \n")
            print("1.Lista de doctores disponibles ")
            print("2.Actualizar datos de un doctor ")
            print("3.Salir")
            opcionMenu = int(input("Seleccione una opción: "))
            if opcionMenu > 3:
                input("Seleccione una opción válida. Enter para continuar...")
            if int(opcionMenu) == 1:
                listarDoctores()
            if int(opcionMenu) == 2:
                actualizarDoctores()
    except:
        input("Ingrese un numero correcto. Enter para continuarrrrrrrr...")
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
                mostrarOpAgregarDoctor()
            if int(opcionActualizar) == 3:
                mostrarOpBajaDoctor()
    except:
        input("Ingrese un numero correcto. Enter para continuar...")
        actualizarDoctores()

def mostrarOpEditarDoctor():
    print("     Edición de datos de doctor")
    listarDoctores()
    try:
        idDoctor = int(input("Ingrese el id del doctor a editar: "))
        existeId = comunicacion_base.existe_id(idDoctor, "tbl_doctores") ######Trabajo en BASES
        if existeId == 1:
            print("1.Modificar nombre")
            print("2.Modificar curp")
            print("3.Modificar nombre y curp")
            datoActualizar = input("Ingrese la opcion deseada: ")
            editarDoctorBD(idDoctor, datoActualizar)
        else:
            input("ID incorrecto, seleccione uno valido. Enter para continuar...")
            mostrarOpEditarDoctor()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarDoctor()

def editarDoctorBD(idDoctor, campo):
    print("Update en base del doctor. Exitoso") ##Trabajo en BASES 

def mostrarOpAgregarDoctor():
    nombreDoctor = input("Nombre doctor: ")
    curpDoctror = input("CURP: ")
    insertarDoctorBD(nombreDoctor,curpDoctror)

def insertarDoctorBD(nombreDoctor,curpDoctor):
    input("Insertando doctor. Enter para continuar...") ##Trabajo en BASES

def mostrarOpBajaDoctor():
    print("     Baja de datos Doctor")
    listarDoctores()
    try:
        idDoctor = int(input("Ingrese el id del doctor a dar de baja: "))
        print("Validación de que id es existente") ######Trabajo en BASES
        existeId = True
        if existeId == True:
            bajaDoctorBD(idDoctor)
        else:
            input("Numero de id invalido. Enter para continuar...")
            os.system('cls')
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpBajaDoctor()

def bajaDoctorBD(idDoctor):
    input("Dando de baja Doctor. Enter para continuar...") ##Trabajo en BASES