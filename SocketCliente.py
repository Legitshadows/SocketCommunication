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

    #Este es un control para que cuando el cliente de enter, la consola no se quebre
    if not mens:
        print("Por favor, ingrese un comando valido.")
        continue

    #Aqui se envia los datos al servidor
    obj.sendall(mens.encode())

    #En vez de usar exit como salida, nuestro profesor pidio el comando de bye
    if mens.lower() == 'bye':
        break

    #Aqui se recibe y muestra la respuesta del servidor
    recibido = obj.recv(1024)
    print(f"Respuesta del servidor: {recibido.decode()}")

#Se cierra la conexion al servidor
obj.close()

#Aqui se imprime cuando se cierra la conexion, pero la consola se cierra y no se ve este mensaje
#To do: Make this show up in the console some how?
print("Conexion cerrada")