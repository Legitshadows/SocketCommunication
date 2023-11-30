#Variables que se declararon para el codigo
host = ''
port = 3490

#para importar el modulo socket en el cliente
import socket

def conexion_servidor(host, port):
    #Aqui creamos el objeto socket
    obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Se crea la conexion al servidor cuando el cliente introduce el ip
    obj.connect((host, port))
    return obj

def desconectar_servidor(obj):
    obj.close()

def main():

    #Un loop mientras la conexion siga establecida
    while True:
        host = input("Introducir el ip del servidor >> ")
        

        try:

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

        
    
        except (socket.error, ConnectionError):
                print("Servidor desconectado. Por favor conectate a uno nuevo")
        except KeyboardInterrupt:
                print("Se cerrara el cliente")

        finally:
            if 'obj' in locals():
                    desconectar_servidor(obj)
            print("Se desconecto del servidor")

if __name__ == "__main__":
    main()