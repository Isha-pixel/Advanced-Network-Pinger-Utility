from socket import *
import threading
# Threading is used for concurrent programming for handling multiple clients trying to reach out to the server.

#Server Ip address along with port number
server_address = ('172.21.133.124', 12001)  

# Function to handle mulitple clients trying to access the server concurrently
def multiple_client_handle(client_socket, client_address):
    print(f'Connected to {client_address}')

    while True:
        #Receive the data from client and decode it to string object using data variable
        response = client_socket.recv(1024).decode("utf-8")

        if not response:
            break 
        # Converting the response message into uppercase letters
        response = response.upper()

            # Send the response data back to the client by encoding
        client_socket.send(response.encode("utf-8"))

    # Close the client socket
    client_socket.close()
    print(f'Connection with {client_address} closed')

# Create a TCP socket
server_socket = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections (maximum 5 connections at a time)
server_socket.listen(5)

print('TCP Ping concurrent server is ready to receive connections...')

while True:
    # Waiting for a client to connect and accept its connection if received using accept() function
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle the client and sending client_socket and client_address
    client_thread = threading.Thread(target=multiple_client_handle, args=(client_socket, client_address))
    
    # Run the threads concurrently using start() function
    client_thread.start()
