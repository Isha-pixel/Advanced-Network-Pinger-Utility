from socket import *
import random

#server_address along with port number which is used for binding
server_addr = ('172.21.133.124', 12001)

# Create a clinet side socket using IPV-4(AF_INET) and TCP(SOCK_STREAM)
server_socket = socket(AF_INET, SOCK_STREAM)

# Binding our socket to the tuple which contains IP address and port number
server_socket.bind(server_addr)

# Printing to know server started listening on IP_address and port number
print(f"Server Started Listening on {server_addr[0]}:{server_addr[1]}")
server_socket.listen(0)


while True:
   
   # Accepting the connection of client using accept() function and also receiving client socket and address details
   client_socket, client_addr = server_socket.accept()
   while True:
       
       # After accepting connection now start receiving message from client
       msg = client_socket.recv(1024)

       # If there is no message then break
       if not msg.decode():
           break
       
       # Generating random integer in between 1 and 10 both are included
       rand = random.randint(1,10)

       # Injecting packet loss of 20% if rand>8
       if rand>8:
           print('Packet lost')
           client_socket.send('LOST'.encode())
           break
       
       # If rand<=8 message will be sent back to client
       print(f'Message sent by client = {msg} from {client_addr}')

       # Converting the message to uppercase letters
       response = msg.upper()

       # printing the response which is going to send back to client
       print(f'Response sent back = {response}')

       # Sending the response to client
       client_socket.send(response)

    # closing the client socket
   client_socket.close()
