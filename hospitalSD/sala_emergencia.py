import os
import gestion_doctores
import gestion_pacientes
import gestion_trabajadores
import comunicacion_base
import socket
import threading
import os
import subprocess
from datetime import datetime

#server_ready = None
#semaforo = threading.Semaphore(0)
#server_ready = threading.Event() #Variable global para controlar inicializacion del servidor y sincronizar con los clientes


def mostrarOpciones():
    #servidor_listo.wait()
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

def mostrarOpRegistro():
    #serverReady.wait()
    opcionMenu = 0
    try:
        if comunicacion_base.verificaDisponibilidadCama() == 1 and comunicacion_base.verificaDisponiblidadDoctor() == 1:
            mensaje = ''
            nombrePaciente = input("Nombre del paciente: ")
            edadPaciente = int(input("Edad paciente: "))
            descripcionEmergencia = input("Descripción de la emergencia: ")
            mensaje = 'INSERT' + '|' + 'tbl_pacientes' + '|' + nombrePaciente + ',' + str(edadPaciente) + ',' + descripcionEmergencia
            puertoNodo, ipNodo= asignar_info_nodo()
            ipMaestro, puertoMaestro = asigna_nodo_maestro(ipNodo)
            client_thread = threading.Thread(target=cliente, args=(mensaje,int(puertoMaestro),ipMaestro))
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

def server():
    PORT, ipNode= asignar_info_nodo()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    nodoMaestro = asigna_nodo_maestro(ipNode)
    #server_ready.set()
    print(f"Servidor activo: {ipNode}")
    try:
        server_socket.bind((ipNode,PORT))
        server_socket.listen(5)
        while True:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode()
            if data:
                client_socket.send(f"El nodo {ipNode} ha recibido el mensaje: {data}".encode() )
                print(f"\nMensaje: {data} recibido desde {client_address[0]}".encode())
                if ipNode == nodoMaestro[0]: #Instruccion recibida al nodo maestro
                    print("Estas en el nodo maestro")
                    replicarInformacion(data)
                    distribuirInformacion(data,nodoMaestro)
                else:
                    print("No estas en el nodo maestro")
                    #enviarInformacion(data,ipNode)

    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        server_socket.close()

def cliente(mensaje,puerto,ipDestino):
    try:
        print("Mandando mensaje")
        print(mensaje)
        print(puerto)
        print(ipDestino)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ipDestino, puerto))
        client_socket.send(mensaje.encode())
        response = client_socket.recv(1024).decode()
        print(f"{response}")
        input("\nEnter para continuar... ")
    except Exception as e:
        print(f"No se pudo conectar con el nodo en {ipDestino}:{puerto}. Conexión rechazada.{e}")
        input("Presione enter para continuar...")
    finally:
        client_socket.close()

def replicarInformacion(data):
    print(f"Estas en replicar informacion {data}")
    instruccion, tabla, datos = data.split("|")
    if instruccion == "INSERT":
        comunicacion_base.insertar_en_tabla(datos.split(','),tabla)
    if instruccion == "UPDATE":
        datos = datos.split(',')
        id = datos[0]
        campo = datos[1]
        valor = datos[2]
        print(f"ID: {id} CAMPO: {campo} tabla {tabla} valor: {valor}")
        comunicacion_base.actualizar_tabla(id,campo,tabla,valor)
    if instruccion == "DELETE":
        comunicacion_base.eliminar_en_tabla(datos,tabla)

def distribuirInformacion(data,nodoMaestro):
    with open("prioridadNodos.txt", "r") as listaNodos:
        for nodo in listaNodos:
            infoNodo = nodo.strip().split(',')
            if infoNodo[1] != nodoMaestro[0]:
                print("Recorriendo nodos")
                cliente(data,int(infoNodo[2]),infoNodo[1])

def asignar_info_nodo():
    osComand = "ip -4 addr show ens33 | awk '/inet / {print $2}' | cut -d/ -f1"
    ipNode = subprocess.check_output(osComand, shell=True, text=True).strip()
    
    with open("prioridadNodos.txt", "r") as nodeRelation:
        for ports in nodeRelation:
            portNode = ports.strip().split(',')
            if portNode[1] == ipNode:
                PORT = int(portNode[2])
    print(f"puerto asignado PORT:{PORT}")
    return PORT, ipNode

def asigna_nodo_maestro(ipNodoActual):
    with open("prioridadNodos.txt", "r") as nodeRelation:
        for ports in nodeRelation:
            portNode = ports.strip().split(',')
            print(portNode[1], ipNodoActual)
            if verificar_conexion(int(portNode[2]),portNode[1]):
                print("Maestro")
                return [portNode[1], portNode[2]]
            else:
                if portNode[1] == ipNodoActual:
                    return [portNode[1], portNode[2]]
                
def verificar_conexion(puerto, ipDestino):
    try:
        # Crear socket para el cliente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)  # Tiempo de espera para evitar bloqueos

        # Intentar conectar al nodo
        client_socket.connect((ipDestino, puerto))
        return True
    except (ConnectionRefusedError, OSError , socket.timeout) as e:
        # Conexión fallida
        return False
    finally:
        # Asegurarse de cerrar el socket
        client_socket.close()

def inicializarMiddleware():
    # Crear el hilo para el servidor
    #server_ready = threading.Event()
    server_thread = threading.Thread(target=server)
    server_thread.start()
    main_thread = threading.Thread(target=mostrarOpciones)
    main_thread.start()
#     main_thread.start()
    #mostrarOpciones()
    # client_thread = threading.Thread(target=cliente, args=('hola',12345,'192.168.252.134',server_ready))
    # client_thread.start()
# def main():
#     global server_ready
#     salaEmergencia = 1
#     server_ready = middleware.inicializarMiddleware()
#     middleware.mandarMensajeNodoMaestro("INSERT|tbl_doctores|Jose Mauricio, PEPM960630HDF")
#     middleware.mandarMensajeNodoMaestro("UPDATE|tbl_doctores|1,v_nombre,Dr. Mauricio")
#     middleware.mandarMensajeNodoMaestro("DELETE|tbl_doctores|5")
#     main_thread = threading.Thread(target=mostrarOpciones,args=(server_ready,))
#     main_thread.start()


#main()

inicializarMiddleware()
