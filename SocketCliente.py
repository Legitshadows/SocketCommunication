#Variables que se declararon para el codigo
host = ''
port = 3490

#para importar el modulo socket en el cliente
import socket

#Aqui creamos el objeto socket
obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Se crea la conexion al servidor cuando el cliente introduce el ip
host = input("Introducir el ip del servidor >> ")
obj.connect((host, port))
print("Conectado al servidor")

#Un loop mientras la conexion siga establecida
while True:
    #Aqui se puede enviar mensajes al servidor
    mens = input("Ingresar un comando (o 'bye' para salir) >> ")

    #Aqui se envia los datos al servidor
    obj.sendall(mens.encode())

    if mens.lower() == 'bye':
        break

    #Aqui se recibe y muestra la respuesta del servidor
    recibido = obj.recv(1024)
    print(f"Respuesta del servidor: {recibido.decode()}")

#Se cierra la conexion al servidor
obj.close()

print("Conexion cerrada")