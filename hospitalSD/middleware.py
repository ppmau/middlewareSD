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
    return PORT, ipNode


def server():
    PORT, ipNode= asignar_info_nodo()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    nodoMaestro = asigna_nodo_maestro(ipNode)
    try:
        server_socket.bind((ipNode,PORT))
        server_socket.listen(5)
        while True:  #Siempre se reciben los mensajes al nodo maestro
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode()
            if data:
                client_socket.send(f"El nodo {ipNode} ha recibido el mensaje: {data}".encode() )
                #print(f"\nMensaje: {data} recibido desde {client_address[0]}".encode())
                if ipNode == nodoMaestro[0]:
                    distribuirInformacion(data,nodoMaestro)
                    replicarInformacion(data)
                else:
                    replicarInformacion(data)
                    

    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        server_socket.close()

def cliente(mensaje,puerto,ipDestino):
    nombreArchivo = f"mensajesPendientes{ipDestino}"
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if os.path.exists(nombreArchivo):
            print(ipDestino)
            if os.stat(nombreArchivo).st_size == 0:
                input("El archivo existe y tiene")
            else:
                input("El archivo no está vacío.")       
        else:
            input("El archivo no existe, puede enviar mensaje")
        client_socket.connect((ipDestino, puerto))
        client_socket.send(mensaje.encode())
        response = client_socket.recv(1024).decode()
        #print(f"{response}")
    except Exception as e:
        print(f"No se pudo conectar con el nodo en {ipDestino}:{puerto}. Conexión rechazada.{e}. Seleccione otra opcion: ")
        escribeMensajePendiente((mensaje + '|'  + ipDestino + '|' + str(puerto) + '\n'), ipDestino)
    finally:
        client_socket.close()


def inicializarMiddleware():
    server_thread = threading.Thread(target=server)
    server_thread.start()

def enviaDatoAMaestro(mensaje,ipMaestro,puertoMaestro): #Función para crear el hilo que enviará el mensaje
    print(f"mandando mensaje a nodo maestro {mensaje}")
    client_thread = threading.Thread(target=cliente, args=(mensaje,puertoMaestro,ipMaestro))
    client_thread.start()

def replicarInformacion(data):
    instruccion, tabla, datos = data.split("|")
    if instruccion == 'INSERT':
        comunicacion_base.insertar_en_tabla(datos.split(','),tabla)
    if instruccion == 'UPDATE':
        datos = datos.split(',')
        id = datos[0]
        campo = datos[1]
        valor = datos[2]
        comunicacion_base.actualizar_tabla(id,campo,tabla,valor)
    if instruccion == "DELETE":
        comunicacion_base.eliminar_en_tabla(datos,tabla)
    if instruccion == 'INSERT-PACIENTE-VISITA':
        comunicacion_base.insertar_en_tabla(datos.split(','),"tbl_pacientes")
        id_doctor = comunicacion_base.obtenDoctorDisponible()
        id_paciente =comunicacion_base.obtenIdUltimoPaciente()
        id_sala = comunicacion_base.obtenSalaDisponible()
        id_visita = int(comunicacion_base.obtenIdUltimaVisita()) + 1
        folio_visita = "P" + str(id_paciente) + "D" + str(id_doctor) + "S" + str(id_sala[0]) + "C" + str(id_sala[1]) + "V" + str(id_visita)
        valores = [id_paciente,id_doctor,id_sala[0],id_sala[1],folio_visita,1,datetime.now().strftime("%Y-%m-%d")]
        comunicacion_base.insertar_en_tabla(valores,"tbl_visitas")
    if instruccion == 'UPDATE-CERRAR-VISITAS':
        comunicacion_base.cerrarVisitasDoctor(datos)
    

def distribuirInformacion(data,nodoMaestro):
    with open("prioridadNodos.txt", "r") as listaNodos:
        for nodo in listaNodos:
            infoNodo = nodo.strip().split(',')
            if infoNodo[1] != nodoMaestro[0]:
                client_thread = threading.Thread(target=cliente, args=(data,int(infoNodo[2]),infoNodo[1]))
                client_thread.start()
                #cliente(data,int(infoNodo[2]),infoNodo[1])

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
            if verificar_conexion(int(portNode[2]),portNode[1]):
                return [portNode[1], portNode[2]]
            else:
                if portNode[1] == ipNodoActual:
                    return [portNode[1], portNode[2]]

def escribeMensajePendiente(mensaje,ipDestino):
    with open(f"mensajesPendientes{ipDestino}.txt", "a") as archivo:  # Usa "a" para agregar al archivo sin borrar su contenido
        archivo.write(mensaje)

