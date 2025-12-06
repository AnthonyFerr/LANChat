import socket
import threading

"""
Client design
We need to open a socket for the client just like the server
connect to the server
Then ask the user for input to send
Problem: IO enters client into blocked state! Might miss messages 
Sol: Thread for sending, thread for recieving
"""

#Server socket
serverHOST = '127.0.0.1'
serverPORT = 9999

#create a dynamically-assigned client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")
#Concept #1

#Connect with the server
client_socket.connect((serverHOST, serverPORT))

"""
A thread for receiving messages from the server
"""
def messageListener():
    while True:
        inMessage = client_socket.recv(1024)
        print(inMessage.decode())


"""
A thread for sending messages to the server
"""
def messageSender():
    while True: 
        outMessage = input("Message: ")
        client_socket.send(outMessage.encode())

if __name__ == "__main__":
    listener = threading.Thread(target=messageListener)
    sender = threading.Thread(target=messageSender)
    listener.start()
    sender.start()