import os
import comunicacion_base
import middleware
import threading
def mostrarOpTrabajadores():
    opcionMenu = 0
    try:
        while opcionMenu != 3:
            os.system('clear') 
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
    os.system('clear')
    print("Lista de trabajadores")
    comunicacion_base.lista_tabla("tbl_trabajadores_sociales")
   


def actualizarTrabajadores():
    opcionActualizar = int(0)
    try:
        while opcionActualizar != 3:
            os.system('clear')
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
        puertoNodo, ipNodo= middleware.asignar_info_nodo()
        ipMaestro, puertoMaestro = middleware.asigna_nodo_maestro(ipNodo)
        idTrabajador = int(input("Ingrese la sala del trabajador a editar: "))
        existeId = comunicacion_base.existe_id(idTrabajador, "tbl_trabajadores_sociales") ######Trabajo en BASES
        if existeId == 1:
            if opcionEdicion == 0:
                print("1.Modificar nombre")
                print("2.Modificar curp")
                campo = int(input("Ingrese la opcion deseada: "))
                valor = input("Escriba el valor actualizado:")
                if campo == 1:
                    mensajeTrabajador = 'UPDATE|tbl_trabajadores_sociales|' + str(idTrabajador) + ',' + 'v_nombre' + ',' + valor
                elif campo == 2:
                    mensajeTrabajador = 'UPDATE|tbl_trabajadores_sociales|' + str(idTrabajador) + ',' + 'v_curp' + ',' + valor
                client_thread = threading.Thread(target=middleware.cliente, args=(mensajeTrabajador,int(puertoMaestro),ipMaestro))
                client_thread.start() #Envia informacion directamente al server en nodo maestro 
            elif opcionEdicion == 1:
                nombreTrabajador = input("Ingrese el nombre del nuevo trabajador: ")
                mensajeTrabajador = 'UPDATE|tbl_trabajadores_sociales|' + str(idTrabajador) + ',' + 'v_nombre' + ',' + nombreTrabajador
                client_thread = threading.Thread(target=middleware.cliente, args=(mensajeTrabajador,int(puertoMaestro),ipMaestro))
                client_thread.start() #Envia informacion directamente al server en nodo maestro 
                curpTrabajador = input("Ingrese el CURP del nuevo trabajador: ")
                mensajeTrabajador = 'UPDATE|tbl_trabajadores_sociales|' + str(idTrabajador) + ',' + 'v_curp' + ',' + curpTrabajador
                client_thread = threading.Thread(target=middleware.cliente, args=(mensajeTrabajador,int(puertoMaestro),ipMaestro))
                client_thread.start() #Envia informacion directamente al server en nodo maestro 
            else:
                input("ID incorrecto, seleccione uno valido. Enter para continuar...")
                mostrarOpEditarTrabajador()
    except:
        input("Ingrese un número válido. Enter para continuar...")
        mostrarOpEditarTrabajador()

    