import threading
import socket

HEADER = 1024
hostname = socket.gethostname()
msg = 'Welcome'
# Using localhost as the host. and declaring the vars
HOST = socket.gethostbyname(hostname)
PORT = 5555
# creating the socket and binding the location the the vars
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
# creating the arrays to hold the information
clients = []
nicknames = []

# for sending the messages


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:

        try:
            message = client.recv(HEADER)
            print(f"{nicknames[clients.index(client)]} --> {message}")
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
# encoding the chat and connecting the client with the server
        print("Connected with " + str(address))
        client.send(msg.encode('utf-8'))
# setting the username that the user typed
        nickname = client.recv(HEADER)
        nicknames.append(nickname)

        clients.append(client)
        print("Username of the client is " + str(nickname))

        broadcast(f"You have Connected with {nickname}\n".encode('utf-8'))
        client.send("Connected to the server\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server Responding...")


receive()
