import socket
import threading
import comunicacion_base
import os
import subprocess
from datetime import datetime

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


def server(salaEmergencia):
    PORT, ipNode= asignar_info_nodo()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nodoMaestro = asigna_nodo_maestro(ipNode)
    try:
        server_socket.bind((ipNode, PORT ))
        server_socket.listen(5)
        while True:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode()
            client_socket.send(f"El nodo {ipNode} ha recibido el mensaje: {data}".encode() )
            print(f"\nMensaje: {data} recibido desde {client_address[0]}".encode())
            if salaEmergencia == nodoMaestro[0]:
                print("Estas en el nodo maestro")
            else:
                print("No estas en el nodo maestro")
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        server_socket.close()

def cliente(mensaje,puerto,ipDestino):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ipDestino, puerto))
        client_socket.send(mensaje.encode())
        response = client_socket.recv(1024).decode()
        print(f"{response}")
        input("\nEnter para continuar... ")
    except ConnectionRefusedError as e:
        print(f"No se pudo conectar con el nodo en {ipDestino}:{puerto}. Conexión rechazada.")
        input("Presione enter para continuar...")
    finally:
        client_socket.close()

def inicializarMiddleware(salaEmergencia):
    # Crear el hilo para el servidor
    server_thread = threading.Thread(target=server, args=(salaEmergencia))
    server_thread.start()
    

def mandarMensajeNodo(mensaje):
    print(mensaje)
    print("Enviando mensaje a nodo 1... " )
    client_thread = threading.Thread(target=cliente(mensaje,int(5000),'127.0.0.1'))
    client_thread.start()


def replicarInformacion(data):
    print(f"Replicando el mensaje: {data}")
    instruccion, tabla, datos = data.split("|")
    if instruccion == "INSERT":
        comunicacion_base.insertar_en_tabla(tabla,datos)
    if instruccion == "UPDATE":
        datos = datos.split(',')
        id = datos[0]
        campo = datos[1]
        valor = datos[2]
        print(f"ID: {id} CAMPO: {campo} tabla {tabla} valor: {valor}")
        comunicacion_base.actualizar_tabla(id,campo,tabla,valor)
    if instruccion == "DELETE":
        comunicacion_base.eliminar_en_tabla(datos,tabla)


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

def asigna_nodo_maestro(ipNodoActual):
    with open("prioridadNodos.txt", "r") as nodeRelation:
        for ports in nodeRelation:
            portNode = ports.strip().split(',')
            print(portNode[1], ipNodoActual)
            if verificar_conexion(int(portNode[2]),portNode[1]):
                print("Maestro")
                return [portNode[0], portNode[1]]
            else:
                if portNode[1] == ipNodoActual:
                    return [portNode[0], portNode[1]]

inicializarMiddleware('1')
#mandarMensajeNodo("INSERT|tbl_doctores|Jose Mauricio, PEPM960630HDF|")



