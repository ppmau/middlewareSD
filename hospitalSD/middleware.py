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
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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


def inicializarMiddleware():
    server_thread = threading.Thread(target=server)
    server_thread.start()

def enviaInstruccion(mensaje,puerto,ipDestino): #Función para crear el hilo que enviará el mensaje
    print(f"mandando mensaje en envia instruccion {mensaje}")
    client_thread = threading.Thread(target=cliente, args=(mensaje,puerto,ipDestino))
    client_thread.start()

def mandarMensajeNodo(mensaje):
    print(mensaje)
    print("Enviando mensaje a nodo 1... " )
    client_thread = threading.Thread(target=cliente(mensaje,int(5000),'127.0.0.1'))
    client_thread.start()


def replicarInformacion(data):
    print(f"Estas en replicar informacion {data}")
    instruccion, tabla, datos = data.split("|")
    print(f"instruccion: {instruccion}")
    if instruccion == "INSERT":
        comunicacion_base.insertar_en_tabla(datos.split(','),tabla)
        input("terminando insercion visita")
    if instruccion == "UPDATE":
        datos = datos.split(',')
        id = datos[0]
        campo = datos[1]
        valor = datos[2]
        print(f"ID: {id} CAMPO: {campo} tabla {tabla} valor: {valor}")
        comunicacion_base.actualizar_tabla(id,campo,tabla,valor)
    if instruccion == "DELETE":
        comunicacion_base.eliminar_en_tabla(datos,tabla)
    if instruccion == "INSERT-PACIENTE-VISITA":
        comunicacion_base.insertar_en_tabla(datos.split(','),"tbl_pacientes")
        id_doctor = comunicacion_base.obtenDoctorDisponible()
        id_paciente =comunicacion_base.obtenIdUltimoPaciente()
        id_sala = comunicacion_base.obtenSalaDisponible()
        id_visita = int(comunicacion_base.obtenIdUltimaVisita()) + 1
        folio_visita = "P" + str(id_paciente) + "D" + str(id_doctor) + "S" + str(id_sala[0]) + "C" + str(id_sala[1]) + "V" + str(id_visita)
        valores = [id_paciente,id_doctor,id_sala[0],id_sala[1],folio_visita,1,datetime.now().strftime("%Y-%m-%d")]
        comunicacion_base.insertar_en_tabla(valores,"tbl_visitas")
        input("terminando insercion paciente visita")
    

def distribuirInformacion(data,nodoMaestro):
    with open("prioridadNodos.txt", "r") as listaNodos:
        for nodo in listaNodos:
            infoNodo = nodo.strip().split(',')
            if infoNodo[1] != nodoMaestro[0]:
                print("Recorriendo nodos")
                cliente(data,int(infoNodo[2]),infoNodo[1])

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
                return [portNode[1], portNode[2]]
            else:
                if portNode[1] == ipNodoActual:
                    return [portNode[1], portNode[2]]

#inicializarMiddleware('1')
#mandarMensajeNodo("INSERT|tbl_doctores|Jose Mauricio, PEPM960630HDF|")

