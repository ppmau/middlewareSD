import os
import comunicacion_base

def mostrarOpTrabajadores():
    opcionMenu = 0
    try:
        while opcionMenu != 3:
            os.system('cls') 
            print("         Gestión de Trabajadores         \n")
            print("1.Lista de trabajadores disponibles ")
            print("2.Actualización de trabajadores")
            print("3.Salir")
            opcionMenu = int(input("Seleccione una opción: "))
            if opcionMenu > 3:
                input("Seleccione una opción válida. Enter para continuar...")
            if int(opcionMenu) == 1:
                listarTrabajadores()
                input("Enter para continuar...")
            if int(opcionMenu) == 2:
                actualizarTrabajadores()
    except:
        input("Ingrese un numero correcto. Enter para continuar...")
        mostrarOpTrabajadores()

def listarTrabajadores():
    os.system('cls')
    print("Lista de trabajadores")
    comunicacion_base.lista_tabla("tbl_trabajadores_sociales")
   


def actualizarTrabajadores():
    opcionActualizar = int(0)
    try:
        while opcionActualizar != 3:
            os.system('cls')
            print("         Actualizar Trabajadores         \n")
            print("1. Actualizar datos de trabajador de sala")
            print("2. Cambiar trabajador de sala")
            print("3. Salir")
            opcionActualizar = int(input("Seleccione una opción: "))
            if opcionActualizar >= 4:
                input("Seleccione una opción válida. Enter para continuar...")
            if int(opcionActualizar) == 1:
                mostrarOpEditarTrabajador(0)
            if int(opcionActualizar) == 2:
                mostrarOpEditarTrabajador(1)
            
    except:
        input("Ingrese un numero correcto. Enter para continuar...")
        actualizarTrabajadores()

def mostrarOpEditarTrabajador(opcionEdicion):
    print("     Edición de datos de doctor")
    listarTrabajadores()
    try:
        idTrabajador = int(input("Ingrese la sala del trabajador a editar: "))
        existeId = comunicacion_base.existe_id(idTrabajador, "tbl_trabajadores_sociales") ######Trabajo en BASES
        if existeId == 1:
            if opcionEdicion == 0:
                print("1.Modificar nombre")
                print("2.Modificar curp")
                campo = int(input("Ingrese la opcion deseada: "))
                valor = input("Escriba el valor actualizado:")
                if campo == 1:
                    comunicacion_base.actualizar_tabla(idTrabajador,"v_nombre","tbl_trabajadores_sociales",valor)
                elif campo == 2:
                    comunicacion_base.actualizar_tabla(idTrabajador,"v_curp","tbl_trabajadores_sociales", valor)   
            elif opcionEdicion == 1:
                nombreTrabajador = input("Ingrese el nombre del nuevo trabajador: ")
                comunicacion_base.actualizar_tabla(idTrabajador,"v_nombre","tbl_trabajadores_sociales",nombreTrabajador)
                curpTrabajador = input("Ingrese el CURP del nuevo trabajador: ")
                comunicacion_base.actualizar_tabla(idTrabajador,"v_curp","tbl_trabajadores_sociales",curpTrabajador)
            else:
                input("ID incorrecto, seleccione uno valido. Enter para continuar...")
                mostrarOpEditarTrabajador()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarTrabajador()

def insertarDoctor():
    print("Escriba los datos del Doctor")
    nombreDoctor = input("Nombre doctor: ")
    curpDoctror = input("CURP: ")
    valores = [nombreDoctor,curpDoctror]
    comunicacion_base.insertar_en_tabla(valores,"tbl_doctores")

def bajaDoctorBD():
    print("Lista de doctores para baja")
    listarTrabajadores()
    try:
        idDoctor = int(input("Ingrese el id del doctor a dar de bajaaa: "))
        existeId = comunicacion_base.existe_id(idDoctor, "tbl_doctores")
        if existeId == 1:
            comunicacion_base.eliminar_en_tabla(idDoctor,"tbl_doctores")
        else:
            input("ID incorrecto, seleccione uno valido. Enter para continuar...")
            mostrarOpEditarTrabajador()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarTrabajador()

    