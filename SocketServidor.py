#Importamos de nuevo el modulo de socket y ahora el de threading para las conexiones de los clientes
import os
import shutil
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

servidor_activo = True

mensaje_enviado = False



#Una funcion para manejar las conexiones de los clientes
def handle_client(obj, addr):
    print(f"Conexion establecida de la IP: {addr[0]} Puerto: {addr[1]}")

    #Se agrego el try para atrapar los errores de los clientes al cerrar su conexion y avisar que se cerro
    try:
        while servidor_activo:
            #Esperamos los datos del cliente
            data = obj.recv(1024)
            if not data:
               break #Si el cliente no envia datos, se cierra la conexion

            #Aqui vamos a pasar lo que envia al cliente para activar nuestros comandos
            command, *args = data.decode().split()

            #Aqui se controla del lado servidor para que al dar enter, no se quebre la consola
            if not command:
                continue
            
            #Primer comando ls, que muestra una lista de los contenidos del directorio tmp
            #To do: ls makes console act weird, might have to redo the command
            if command == 'ls':
                if len(args) == 1:
                    destination = ('C://' + args[0])
                    if os.path.exists(destination):
                        file_list = os.listdir('C://' + destination)
                        response = '\n'.join(file_list)
                    else:
                        response = f"El directorio {destination} no existe"
                else:
                    file_list = os.listdir('C://')
                    response = '\n'.join(file_list)
            
            #Segundo comando de mv que se usa para mover un archivo de origen a destino
            elif command == 'mv':
                # Mover un archivo (args[0] = origen, args[1] = destino)
                if len(args) == 2:
                    source_file = args[0]
                    destination_file = args[1]

                    # Validar extensiones permitidas (txt, jpg, jpeg, png, gif)
                    valid_extensions = {".txt", ".jpg", ".jpeg", ".png", ".gif"}
                    _, source_extension = os.path.splitext(source_file)
                    _, destination_extension = os.path.splitext(destination_file)

                    if source_extension.lower() in valid_extensions and destination_extension.lower() in valid_extensions:
                        if os.path.exists(source_file):
                            os.rename(source_file, destination_file)
                            response = f"Archivo {source_file} fue movido a {destination_file}"
                        else:
                            response = f"Archivo {source_file} no fue encontrado"
                    else:
                        response = f"Extensiones no permitidas. Solo se permiten: {', '.join(valid_extensions)}"
                else:
                    response = "Uso: mv <origen> <destino>"
            
            #Tercer comando para subir un lugar en el directorio por ejemplo: C:/Windows11/Documents/Code Projects
            #Le das al comando up y pasa a C:/Windows11/Documents
            elif command == 'up':
                os.chdir('..')
                response = f"Directiorio actual: {os.getcwd()}"
            
            #Cuarto comando de bye que simplemente desconecta el cliente del servidor y cierra la consola
            #To do: Find solution to disconnect from server but not close the client console
            elif command == 'bye':
                response = "Desconectado del servidor"
                break

            #Un comando para listar todos los comandos (idea de un amigo del salon)
            elif command == 'ayuda':
                response = "Lista de comandos: ls, mv, up, bye, echo"
                          

            #Quinto comando que simplemente replica el mensaje de vuelta que envio el cliente via echo
            elif command == 'echo':
                #Este control es para prevenir que el cliente crashee su consola por mandar echo sin mensaje
                if not (args):
                    response = "Por favor incluye un mensaje con el comando."
                else:
                    response = ' '.join(args)
            else:
                #Control de comandos por si el cliente manda algo no reconocido por el servidor
                response = "Comando no reconocido"


            #Enviamos los datos recibidos de vuelta al cliente
            print(f"Respuesta del cliente {addr}: {data.decode()})")
            obj.sendall(response.encode())

    #Manejamos la excepcion del cliente al cerrar su session, ya que arroja un error largo, esto lo reduce :)
    except Exception as e:
        print(f"Error con la conexion con {addr}: {e}")
    finally:
        #Aqui cerramos la conexion al cliente
        obj.close()
        clientes.remove(obj)
        print(f"Conexion con {addr} cerrada")

def broadcast(mensaje):
    for cliente in clientes:
        try:
            cliente.sendall(mensaje.encode())
        except Exception as e:
            print(f"Error al transmitir el mensaje a un cliente: {e}")

try:
    ser.settimeout(1)
    #Un loop mientras la conexion siga establecida
    while True:
        try:
            #Esperamos conexion de los clientes
            obj, addr = ser.accept()

            #Iniciamos un hilo para manejar las conexiones con los clientes
            cli_thread = threading.Thread(target=handle_client, args=(obj, addr))
            cli_thread.start()

            #Agregamos nuestro cliente a la lista
            clientes.append(obj)

        except socket.timeout:
            pass # Continua esperando por conexiones si pasa el timeout
except KeyboardInterrupt:
    print("\nEl servidor se esta apagando")

    if not mensaje_enviado:
        broadcast("El servidor se esta apagando.")
        mensaje_enviado = True

    # Close all client connections
    for cliente in clientes:
        try:
            cliente.shutdown(socket.SHUT_RDWR)
            cliente.close()
        except Exception as e:
            print(f"Error al cerrar la conexion con cliente: {e}")

    # Close the server socket
    ser.close()
    servidor_activo = False
    print("Servidor cerrado.")


