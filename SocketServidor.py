#Importamos de nuevo el modulo de socket y ahora el de threading para las conexiones de los clientes
import os
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

    #Se agrego el try para atrapar los errores de los clientes al cerrar su conexion y avisar que se cerro
    try:
        while True:
            #Esperamos los datos del cliente
            data = obj.recv(1024)
            if not data:
               break #Si el cliente no envia datos, se cierra la conexion

            #Aqui vamos a pasar lo que envia al cliente para activar nuestros comandos
            command, *args = data.decode().split()

            if command == 'ls':
                file_list = os.listdir('.')
                response = '\n'.join(file_list)
            
            elif command == 'mv':
                if len(args) == 2:
                    os.rename(args[0], args[1])
                    response = f"El archivo {args[0]} movido a {args[1]}"
                else:
                    response = "Uso: mv <origen> <destino>"
            
            elif command == 'up':
                os.chdir('..')
                response = f"Directiorio actual: {os.getcwd()}"
            
            elif command == 'bye':
                response = "Desconectado del servidor"
                break

            elif command == 'echo':
                response = ' '.join(args)


            #Enviamos los datos recibidos de vuelta al cliente
            print(f"Respuesta del cliente {addr}: {data.decode()})")
            mens = ("Si ves este mensaje, tienes un 10 en la materia!")
            obj.sendall(mens.encode())

    #Manejamos la excepcion del cliente al cerrar su session, ya que arroja un error largo, esto lo reduce :)
    except Exception as e:
        print(f"Error con la conexion con {addr}: {e}")
    finally:
        #Aqui cerramos la conexion al cliente
        obj.close()
        clientes.remove(obj)
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


