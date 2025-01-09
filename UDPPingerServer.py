from socket import *
import random


def start_server():
   #server_address along with port number which is used for binding
   server_addr = ('172.21.133.124',12001)

   # Create a clinet side socket using IPV-4(AF_INET) and UDP(SOCK_DGRAM)
   server_socket = socket(AF_INET, SOCK_DGRAM)

   # Binding our socket to the tuple which contains IP address and port number
   server_socket.bind(server_addr)
  
   while True:
       
       # Receiving the message and client details from client using recvfrom() function 
       msg, client_addr = server_socket.recvfrom(1024)

       # Decoding the bytes object to string object
       msg = msg.decode()

       # Printing message that is sent by the client
       print(f'Message sent = {msg} from {client_addr}')

       # Converting the message to uppercase letters
       response = msg.upper()

       # Generating random integer in between 1 and 10 both are included
       rand = random.randint(1,10)

       # Injecting packet loss of 20% if rand>8
       if rand>8:
           continue
       
       # If rand<=8 message will be sent back to client
       print(f'Response sent back = {msg}')

       # Message is sent back to client by converting response to bytes object
       server_socket.sendto(response.encode(), client_addr)

# Calling the start_server function
start_server()
