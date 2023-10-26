#Importamos de nuevo el modulo de socket
import socket
import threading

#Definimos el objeto servidor del tipo socket STREAM del dominio AF_INET
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Se le asigna el servidor (localhost) y el puerto asigando en la tarea 3490
ser.bind(("",3490))

#Para aceptar las conexiones con el metodo listen
ser.listen()

#Aqui almacenamos nuestros clientes
clientes = []

#Una funcion para manejar las conexiones de los clientes
def handle_client(obj, addr):
    print(f"Conexion establecida de la IP: {addr[0]} Puerto: {addr[1]}")

    while True:
        #Esperamos los datos del cliente
        data = obj.recv(1024)
        if not data:
            break

        #Enviamos los datos recibidos de vuelta al cliente
        print(f"Respuesta del cliente {addr}: {data.decode()})")
        mens = ("Si ves este mensaje, tienes un 10 en la materia!")
        obj.sendall(mens.encode())

    #Aqui cerramos la conexion al cliente
    obj.close()
    print(f"Conexion con {addr} cerrada")

#Un loop mientras la conexion siga establecida
while True:
    #Esperamos conexion de los clientes
    obj, addr = ser.accept()

    #Iniciamos un hilo para manejar las conexiones con los clientes
    cli_thread = threading.Thread(target=handle_client, args=(obj, addr))
    cli_thread.start()

    #Agregamos nuestro cliente a la lista
    clientes.append(obj)


