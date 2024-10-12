import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.252.134', 12346))
print("Puerto local después de la conexión:", client_socket.getsockname())
client_socket.send("Mensaje desde cliente".encode())
response = client_socket.recv(1024).decode()
print(f"Respuesta del servidor: {response}")
client_socket.close()
    