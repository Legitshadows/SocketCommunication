# Los imports del servidor central para aceptar multiple clientes y para el socket
import socket
import threading

# Configuracion del servidor vecino
host_vecino = ''
puerto_vecino = 3491

#Aqui almacenamos nuestros clientes
clientes = []

def handle_client_local(obj, addr):
    try:
        while True:
            # Esperar datos del cliente local
            data = obj.recv(1024).decode()
            
            print(f"Datos recibidos del cliente local {addr}: {data}")

            # Reenviar datos al servidor central
            servidor_central.sendall(data.encode())

            # Esperar la respuesta del servidor central
            recibido_central = servidor_central.recv(1024).decode()
            print(f"Respuesta del servidor central: {recibido_central}")

            # Enviar la respuesta de vuelta al cliente local
            obj.sendall(recibido_central.encode())
    
    except Exception as e:
        print(f"Error en la conexion con el cliente local {addr}: {e}")
    finally:
        # Cerramos la sesion con el cliente local
        obj.close()
        print(f"Conexion con el cliente local {addr} fue cerrada")

try:
    # Crear un socket para la conexion con el servidor central
    servidor_central = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_central.connect(('localhost', 3490)) 

    # Crear un socket para escuchar conexiones de clientes locales
    servidor_vecino = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_vecino.bind((host_vecino, puerto_vecino))
    servidor_vecino.listen()

    print(f"Servidor vecino escuchando en {host_vecino}:{puerto_vecino}")

    while True:
        # Esperar a que un cliente local se conecte
        obj, addr = servidor_vecino.accept()
        print(f"Conexion aceptada desde {addr}")

        # Iniciamos un hilo para manejar la conexion con el cliente local
        cli_thread = threading.Thread(target=handle_client_local, args=(obj, addr))
        cli_thread.start()

        clientes.append(obj)

except Exception as e:
    print(f"Error en el servidor vecino: {e}")

finally:
    # Cerrar los sockets
    servidor_central.close()
    servidor_vecino.close()
