from socket import *
import time
from datetime import datetime


server_addr = ('172.21.133.124', 12001)

# Taking a input from user for number of pings required
n = int(input("Enter number of pings (N): "))

sequence_number = 1

# Sum of RTT's is stored in this variable and it is set to zero initially 
total_rtt=0
# Set max_rtt to -infinity and min_rtt +infinity initially
max_rtt=float('-inf')
min_rtt=float('inf')

# Number of success pings are in this succes_pings variable and it is set to zero initially
success_pings=0

# Storing n value for using in future
copy=n


while n>0:
   try:
       # Create a clinet side socket using IPV-4(AF_INET) and TCP(SOCK_STREAM)
       client_socket = socket(AF_INET, SOCK_STREAM)

       # Set a timeout value to 1 second
       client_socket.settimeout(1)

       # Send the connection request to server
       client_socket.connect(server_addr)
       
       # Note the initial time in time_stamp variable
       time_stamp = time.time()

        # From datetime we are extracting readable time in readable_time variable
       readable_time = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S.%f')
       
       # Message that we are going to send server is stored in msg variable
       msg = f'ping {sequence_number} {readable_time}'

       # Sending the message to client in bytes object to client
       client_socket.send(msg.encode())

       # Receiving the response message from server
       response = client_socket.recv(1024)

       # check If packet is lost 
       if response.decode()=='LOST':
           print(f'Packet {sequence_number} lost')
           continue
       #Printing the received response in decoded format i.e converted into string format
       print(f'Response received is: {response.decode()}')

       # Note the time of the received response and subtract the time_stamp to calculate the Round Trip Time(RTT)
       rtt = time.time() - time_stamp

       # Convert the rtt into milliseconds
       rtt = rtt*1000
       print(f'RTT (in milliseconds) of packet {sequence_number} is {rtt:.3f}')

       # Calculating the sum of rtts of all succesful packets
       total_rtt += rtt

       # Calculating max_rtt and min_rtt using max and min functions
       max_rtt = max(max_rtt,rtt)
       min_rtt = min(min_rtt,rtt)

       # Incrementing the success_pings  
       success_pings += 1
       
       # Closing the client socket
       client_socket.close()

   except timeout:
       # If there is timeout then we can conclude packet with sequence number is lost
       print(f'Packet {sequence_number} is lost')
   finally:
       sequence_number += 1
       n -= 1

if success_pings>0:
   #printing max_RTT and min_RTT and avg_RTT if there are some successful pings
   print(f'Maximum RTT (in milliseconds) = {max_rtt:.3f}')
   print(f'Minimum RTT (in milliseconds) = {min_rtt:.3f}')
   print(f'Average RTT (in milliseconds) = {total_rtt/success_pings:.3f}')
else:
   print(f'Average RTT = 0')

# Calculating packet_loss percentage
packet_loss = ((copy - success_pings) / copy) * 100

# Printing packet loss rate
print(f"Packet loss rate: {packet_loss:.2f}%")
