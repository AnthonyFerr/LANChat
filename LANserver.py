import socket
import sys
import threading


"""
Shared datastructures for all the threads. 
The client threads need to be able to broadcast to all the others
when even one sends a message to the server.
In order to do that, they must know who to send to.
!! They does not refer to the clients, it refers to client threads running on server !!
Clients don't actually have infromation about each other, only the server knows who they are!
"""
#Super-engineered datastructure that FAANG uses to track connections
connectedClients = []


#Create the socket that clients will connect to
def connectionManager():
    #Server socket
    HOST = '127.0.0.1'
    PORT = 9999
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print("Bind failed. Error code: " + {str(msg[0])} + " Message: " + {msg[1]})
        sys.exit()
        
    print("Socket bind complete")
    s.listen(10)
    print("Socket now listening")
    
    #accept connections to clients indefinitely
    while True: 
        try:
            client_socket, address = s.accept()
            print("Connected with " + address[0] + ":" + str(address[1]))
            #create a thread to communicate with this client
            clientThread = threading.Thread(target=clientHandler, args=[client_socket, address])
            clientThread.start()
            
        except socket.error as msg:
                print("Accept failed. Error code: " + {str(msg[0])} + " Message: " + {msg[1]})

"""
Dedicated thread for each client's communication channel
goal: constantly ask for input from the client
when input is detected, it must be sent to all clients (broadcasted!)
things to consider: 
    How do I broadcast?
"""
def clientHandler(socket, addr):
    print("I'm the thread!")
    print(socket, addr)
    
    #enter the client into the shared list here, not the connectionManager
    #this is because on disconnect, clientHandler will remove from the list
    #doesn't really matter, just keeping it together
    connectedClients.append(socket)
    
    while True: 
        #wait for the client to say something
        data = socket.recv(1024)
        
        #since recv put the thread in block state, we now re-enter running state
        #immediately relay (broadcast) data to EVERYONE
        for client in connectedClients:
            client.send(data)
    
    
    
if __name__ == "__main__":
    connectionManager()