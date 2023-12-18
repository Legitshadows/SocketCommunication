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

#Un flag que se utiliza para ver si el servidor sigue activo o no
servidor_activo = True

#Se envia un mensaje al cliente de que el servidor se esta apagando, esto checa si ya se envio o no
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
            
            #Primer comando ls, que muestra cualqier directorio de la memoria C: (Se puede configurar despues para escoger cual disco)
            #Igual tiene ahora dos funciones /ls normal que muestra el directorio de C:/ y /ls (destination) que muestra un directorio deaseado por el usuario
            if command == 'ls':
                if len(args) == 1:
                    destination = ('C://' + args[0])
                    if os.path.exists(destination):
                        file_list = os.listdir(destination)
                        response = '\n'.join(file_list)
                    else:
                        response = f"El directorio {destination} no existe"
                else:
                    file_list = os.listdir('C://')
                    response = '\n'.join(file_list)
            
            #Segundo comando de mv que se usa para mover un archivo de origen a destino
            #Igual que ls, tuvo una nueva forma de procesar los datos y comando
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

            #Nuevo comando cat para visualizar los archivos de texto
            elif command == 'cat':
                # Encontrar y mostrar el contenido de un archivo de texto
                if args:
                    filename = args[0]
                    try:
                        with open(filename, 'r') as file:
                            content = file.read()
                            response = f"Contenido de {filename}:\n{content}"
                    except FileNotFoundError:
                        response = f"Archivo {filename} no encontrado"
                else:
                    response = "Uso: cat <nombre_del_archivo>"
            
            #Tercer comando para subir archivos al servidor y que se guarde en una carpeta especifica para evitar problemas (solo tengo una pc :(
            elif command == 'up':
                if args:
                    # El cliente debe proporcionar la ruta completa del archivo local
                    local_file_path = args[0]

                    # Construimos la ruta de destino en el servidor (por que ando en la misma pc :) )
                    server_destination = os.path.join('C:/Users/Luis/Documents/Archives', os.path.basename(local_file_path))

                    # Intentamos copiar el archivo al servidor
                    try:
                        with open(local_file_path, 'rb') as local_file:
                            with open(server_destination, 'wb') as server_file:
                                server_file.write(local_file.read())
                        response = f"Archivo {os.path.basename(local_file_path)} subido exitosamente al servidor en {server_destination}"
                    except FileNotFoundError:
                        response = f"Error: Archivo {os.path.basename(local_file_path)} no encontrado en el cliente"
                    except Exception as e:
                        response = f"Error al subir el archivo al servidor: {e}"
                else:
                    response = "Uso: up <ruta_del_archivo_local>"

            
            # Nuevo comando tree para mostrar el grafo de conexión del SD (mi pc)
            elif command == 'tree':
                # Elegi el directorio donde ejecuto mi codigo de python por que C:// excede los 1024 bytes y no puedo darle permisos :( 
                root_dir = 'C://Users/Luis/Documents/Code Projects/SocketCommunication'
                
                # Inicia la construcción del árbol desde el directorio raíz
                tree = f"{root_dir}\n"
                
                # Función recursiva para construir el árbol de directorios y archivos
                def build_tree(directory, prefix=''):
                    nonlocal tree
                    items = os.listdir(directory)
                    for item in items:
                        path = os.path.join(directory, item)
                        if os.path.isdir(path):
                            tree += f"{prefix}|-- {item}/\n"
                            build_tree(path, prefix + "|   ")
                        else:
                            tree += f"{prefix}+-- {item}\n"
                
                # Construye el árbol
                build_tree(root_dir)
                
                # Envía el árbol al cliente como respuesta
                response = tree
                                
            #Cuarto comando de bye que simplemente desconecta el cliente del servidor y cierra la consola
            #To do: Find solution to disconnect from server but not close the client console
            elif command == 'bye':
                response = "Desconectado del servidor"
                break

            #Un comando para listar todos los comandos (idea de un amigo del salon)
            elif command == 'ayuda':
                response = "Lista de comandos: ls, mv, cat, up, tree, bye, echo"
                          

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

#Un mensaje que se envia al cliente al cerrar el servidor
#To-do: This is a little bugged and doesn't actually send
def broadcast(mensaje):
    for cliente in clientes:
        try:
            cliente.sendall(mensaje.encode())
        except Exception as e:
            print(f"Error al transmitir el mensaje a un cliente: {e}")

#Los procesos del servidor ahora se manejan en un try para permitir cerrar la consola con CTRL+C
#Al igual queremos cerrar las sesiones activas para que no sean afectadas.
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
#Como la consola del cliente, CTRL+C ahora puede cerrar la consola del servidor
except KeyboardInterrupt:
    print("\nEl servidor se esta apagando")

    #Aqui checa el flag de mensaje enviado para darle el mensaje de cerrando al servidor al cliente
    if not mensaje_enviado:
        broadcast("El servidor se esta apagando.")
        mensaje_enviado = True

    # Cierra todas las sesiones de clientes al servidor cuando se apaga
    for cliente in clientes:
        try:
            cliente.shutdown(socket.SHUT_RDWR)
            cliente.close()
        except Exception as e:
            print(f"Error al cerrar la conexion con cliente: {e}")

    # Se cierra el socket del servidor
    ser.close()
    servidor_activo = False
    print("Servidor cerrado.")


