#Variables que se declararon para el codigo
host = ''
port = 3490

#para importar el modulo socket en el cliente
import socket

#Aqui creamos el objeto socket
obj = socket.socket()

#Se crea la conexion al servidor cuando el cliente introduce el ip
host = input("Introducir el ip del servidor >> ")
obj.connect((host, port))
print("Conectado al servidor")

#Un loop mientras la conexion siga establecida
while True:
    mens = input("Mensaje desde el cliente al servidor >> ")

    obj.send(mens.encode('ascii'))
    
    recibido = obj.recv(1024)
    print(recibido)

#Se cierra la conexion al servidor
obj.close()

print("Conexion cerrada")