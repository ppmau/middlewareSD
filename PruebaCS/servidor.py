import socket
import threading

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('0.0.0.0', 12346))
        server_socket.listen(5)
        print("Servidor escuchando en el puerto 12346...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Conexión establecida con {client_address}")
            data = client_socket.recv(1024).decode()
            client_socket.send(f"¡Mensaje {data} recibido desde el nodo".encode())
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        server_socket.close()



server()