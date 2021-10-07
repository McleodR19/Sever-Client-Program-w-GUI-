import threading
import socket

# Using localhost as the host. and declaring the vars
HOST = '127.0.0.1'
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
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
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
        print(f"Connected with{str(address)}!")
        client.send("NICK".encode('utf-8'))
# setting the username that the user typed
        nickname = client.recv(1024)
        nicknames.append(nickname)

        clients.append(client)
        print(f"Nickname of the client is {nickname}")

        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server Responding...")
receive()



