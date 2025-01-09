from socket import *
import random
import time
from datetime import datetime

# Server_address along with port number which is used to connect server
server_addr = ('172.21.134.130',12001) 

# Create a clinet side socket using IPV-4(AF_INET) and UDP(SOCK_DGRAM)
client_socket = socket(AF_INET, SOCK_DGRAM)

# Set a timeout value to 1 second
client_socket.settimeout(1)

# Take a input from user for number of pings required
n = int(input("Enter number of pings (N): "))

sequence_number = 1
total_rtt=0

# Set max_rtt to -infinity and min_rtt +infinity initially
max_rtt=float('-inf')
min_rtt=float('inf')

success_pings=0
copy=n
while n>0:
   try:
       # Note the initial time in time_stamp variable
       time_stamp = time.time()

       # From datetime we are extracting readable time in readable_time variable
       readable_time = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S.%f')

       # Message that we are going to send server is stored in msg variable
       msg = f'ping {sequence_number} {readable_time}'

       # Send the msg in encoded part to server_addr using sendto() function
       client_socket.sendto(msg.encode(), server_addr)

       # Collecting the response from server using recvfrom() function
       reponse, _ = client_socket.recvfrom(1024)

       # Note the time of the received response and subtract the time_stamp to calculate the Round Trip Time(RTT)
       rtt = time.time() - time_stamp

       # Printing the response in string object by using decode() function
       print(f'Response received is: {reponse.decode()}')

       # Convert the rtt into milliseconds
       rtt = rtt*1000

       # Printing RTT of packet along with sequence_number
       print(f'RTT (in milliseconds) of packet {sequence_number} is {rtt:.3f}')

       # Calculating the sum of rtts of all succesful packets
       total_rtt += rtt
       
       # Calculating max_rtt and min_rtt using max and min functions
       max_rtt = max(max_rtt,rtt)
       min_rtt = min(min_rtt,rtt)

       #Incrementing the number of pings
       success_pings += 1

   except timeout:
       # If there is timeout then we can conclude packet with sequence number is lost
       print(f'Packet {sequence_number} is lost')


   finally:
       sequence_number += 1
       n -= 1

      
if success_pings>0:
   #printing max_RTT and min_RTT and avg_RTT if there are some successful pings
   print(f'Maximum RTT = {max_rtt:.3f}')
   print(f'Minimum RTT = {min_rtt:.3f}')
   print(f'Average RTT = {total_rtt/success_pings:.3f}')

else:
   print(f'Average RTT = 0')

# Calculating packet_loss percentage
packet_loss = ((copy - success_pings) / copy) * 100

# Printing packet loss rate
print(f"Packet loss rate: {packet_loss:.3f}%")
client_socket.close()
