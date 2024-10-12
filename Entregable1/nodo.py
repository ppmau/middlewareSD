import socket
import threading
import os
import subprocess
from datetime import datetime
PORT = 0

def asignar_puerto():
    osComand = "ip -4 addr show ens33 | awk '/inet / {print $2}' | cut -d/ -f1"
    ipNode = subprocess.check_output(osComand, shell=True, text=True).strip()
    
    with open("nodeport.txt", "r") as nodeRelation:
        for ports in nodeRelation:
            portNode = ports.strip().split(' ')
            if portNode[0] == ipNode:
                PORT = int(portNode[1])
    
    print(f"puerto asignado PORT:{PORT}")


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('0.0.0.0', PORT))
        server_socket.listen(5)
        while True:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode()
            client_socket.send(f"El servidor {client_address[0]} ha recibido el mensaje: {data}".encode())
            escribir_mensaje("nodeDB.txt","INSTRUCTION",data,"RECIVED",client_address[0],datetime.now())
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        server_socket.close()

def escribir_mensaje(archivo,instruccion,dato,estatus,nodo,fecha):
    with open("nodeDB.txt", "r") as db:
        contenido = db.read()
        with open("nodeDB.txt", "a") as archivo:
            if not contenido:
                    archivo.write(f"{instruccion}|{dato}|{estatus}|{nodo}|{fecha}")
            else:
                archivo.write(f"\n{instruccion}|{dato}|{estatus}|{nodo}|{fecha}")


def cliente(mensaje,puerto,ipDestino):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ipDestino, puerto))
    client_socket.send(mensaje.encode())
    response = client_socket.recv(1024).decode()
    escribir_mensaje("nodeDB.txt","INSTRUCTION",mensaje,"SEND",client_socket.getsockname()[0],datetime.now())
    print(f"{response}")
    client_socket.close()
    input("\nEnter para continuar... ")


def mostrar_opciones():
    opcionAccion = 0
    while opcionAccion != 3:
            #os.system('clear')
            print("\n           Menú\n")
            print("1. Enviar mensaje a un nodo\n")
            print("2. Mostrar mensajes del nodo\n")
            try:
                opcionAccion = int(input("Selecciona una opción: "))
                if opcionAccion == 1:
                    print("Enviar mensaje a un nodo \n" )
                    mostrar_menu_envio()
                elif opcionAccion == 2:
                    mostrar_mensajes()
                elif opcionAccion == 3:
                    print("Salir")
                else:
                    print("Opción no válida, por favor intenta de nuevo.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

def mostrar_mensajes():
        datos = []
        print("\n                Mensajes en el nodo     \n")
        with open("nodeDB.txt", "r") as archivo:
            for linea in archivo:
                elementos = linea.strip().split('|')
                datos.append(elementos)
                print(linea)
        input("\nEnter para continuar...")

def mostrar_menu_envio():
    opcionEnvio = 0
    while opcionEnvio != 5:
            try:
                #os.system('clear')
                print("     Envio de mensajes\n")
                print("1. Enviar mensaje al nodo 1")
                print("2. Enviar mensaje al nodo 2")
                print("3. Enviar mensaje al nodo 3")
                print("4. Enviar mensaje al nodo 4")
                print("5. Salir")
                opcionEnvio = int(input("\nSelecciona una opción: "))
                if opcionEnvio != 5:
                    mensaje = input("Mensaje a enviar: ")
                
                if opcionEnvio == 1:
                    print("Enviando mensaje a nodo 1... " )
                    client_thread = threading.Thread(target=cliente(mensaje,12345,'192.168.252.134'))
                    client_thread.start()
                elif opcionEnvio == 2:
                    print("Enviando mensaje a nodo 2... " )
                    client_thread = threading.Thread(target=cliente(mensaje,12346,'192.168.252.135'))
                    client_thread.start()
                elif opcionEnvio == 3:
                    print("Enviando mensaje a nodo 3... " )
                    cliente(mensaje, 12347, '192.168.252.132')
                elif opcionEnvio == 4:
                    print("Enviando mensaje a nodo 4... " )
                    cliente(mensaje, 12348, '192.168.252.133')
                elif opcionEnvio == 5:
                    print("Salir " )
                else:
                    input("Opción no válida, por favor intenta de nuevo. Enter para continuar...")
            except ValueError:
                input("Opción no válida, por favor intenta de nuevo. Enter para continuar...")



if __name__ == "__main__":
    # Crear el hilo para el servidor
    asignar_puerto()
    server_thread = threading.Thread(target=server)
    server_thread.start()
    mostrar_opciones()


