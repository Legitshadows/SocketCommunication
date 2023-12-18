#para importar el modulo socket en el cliente
import socket

#Generamos una nueva funcion que se usa para conectarse al servidor 
def conexion_servidor(host, port):
    #Aqui creamos el objeto socket y se crea la conexion al servidor cuando el cliente introduce el ip
    obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    obj.connect((host, port))
    return obj

#Generamos igual una nueva funcion para llamar la desconexion al servidor
def desconectar_servidor(obj):
    obj.close()

#Finalmente una funcion main donde queda igual todo nuestro codigo
def main():

    #Un loop mientras la conexion siga establecida
    while True:
        host = input("Introducir el ip del servidor >> ")
        port = int(input("Introducir el puerto del servidor >> "))
        

        try:
            #Nueva manera de manejar la conexion al servidor
            obj = conexion_servidor(host, port)
            print(f"Conectado al servidor {host}:{port}")

            while True:
                     
                #Aqui se puede enviar mensajes al servidor
                mens = input("Ingresar un comando (o 'bye' para salir) >> ")
                    

                #Este es un control para que cuando el cliente de enter, la consola no se quebre
                if not mens:
                    print("Por favor, ingrese un comando valido.")
                    print("Si quiere ver una lista de comandos, use el comando ayuda.")
                    continue

                #Aqui se envia los datos al servidor
                obj.sendall(mens.encode())

                #En vez de usar exit como salida, nuestro profesor pidio el comando de bye
                if mens.lower() == 'bye':
                    desconectar_servidor(obj)
                    break

                #Aqui se recibe y muestra la respuesta del servidor
                recibido = obj.recv(1024)
                print(f"Respuesta del servidor: {recibido.decode()}")

        
        #El primero maneja la conexion al servidor por si se llega a caer o desconectarse, permite que el cliente no se cierra y puede reconectarse a otro servidor
        except (socket.error, ConnectionError):
                print("Servidor desconectado. Por favor conectate a uno nuevo")
        #Aqui permite cerrar la consola del cliente mediante el comando bye o dandole a CTRL+C
        except KeyboardInterrupt:
                print("Se cerrara el cliente")
        #Aqui se maneja la desconexion al servidor para permitir entrar a otro
        finally:
            if 'obj' in locals():
                    desconectar_servidor(obj)
            print("Se desconecto del servidor")

if __name__ == "__main__":
    main()