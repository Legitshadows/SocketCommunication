#Importamos de nuevo el modulo de socket
import socket

#Definimos el objeto servidor del tipo socket STREAM del dominio AF_INET
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Se le asigna el servidor (localhost) y el puerto asigando en la tarea 3490
ser.bind(("",3490))

#Para aceptar las conexiones con el metodo listen
ser.listen(1)

#Aqui es donde el servidor acepta la instancia cliente, representado como cli y addr para obtener ip y puerto
cli, addr = ser.accept()

#Un loop mientras la conexion siga establecida
while True:

    recibido = cli.recv(1024)


    print("Conexion establecida de la IP: " + str(addr[0]) + " Puerto: " + str(addr[1]))
    print(recibido)

    msg_toSend = ("Hola! si ves este mensaje, pasaste con 10 la materia ")
    cli.send(msg_toSend.encode("ascii"))

#Cerramos la conexion del socket cliente y servidor
cli.close()
ser.close()

print("Conexiones cerradas")
    


