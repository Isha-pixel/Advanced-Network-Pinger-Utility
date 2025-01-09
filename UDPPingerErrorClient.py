from socket import *
import time
from datetime import datetime
import struct

# Define the server address and port
server_address = ('192.168.241.110', 12000)

# Create a UDP socket for sending pings
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

# Create a raw socket to capture ICMP errors
icmp_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
icmp_socket.settimeout(1)
# Ask for the number of pings to send
N = int(input("Enter the number of pings: "))

# Variables to track RTT and packet statistics
max_rtt = float('-inf')
min_rtt = float('inf')
successful_pings = 0
total_rtt = 0

# Loop to send pings and capture responses
for sequence in range(1, N + 1):
    try:
        # Record the time before sending the ping
        time_stamp = time.time()
        readable_time = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S.%f')

        # Construct the ping message and send it via the UDP socket
        message = f'PING {sequence} {readable_time}'
        client_socket.sendto(message.encode(), server_address)

        # Wait for the response or timeout
        response, _ = client_socket.recvfrom(1024)
        print(f'Message received from server: {response.decode()}')

        # Calculate RTT for the successful response
        rtt = time.time() - time_stamp
        #Converting RTT into milliseconds
        rtt=rtt*1000
        print(f'RTT of successful packet {sequence} is: {rtt:.3f} ms')
        min_rtt = min(min_rtt, rtt)
        max_rtt = max(max_rtt, rtt)
        total_rtt += rtt
        successful_pings += 1

    except timeout:
        print(f'Request for packet {sequence} timed out')

        # Check if an ICMP error has been received
            
        icmp_packet, _ = icmp_socket.recvfrom(1024)

            # Decode the ICMP packet header to extract the type and code fields
        icmp_header = icmp_packet[20:28]
        icmp_type, icmp_code, _, _, _ = struct.unpack('bbHHh', icmp_header)

        if icmp_type == 3 and icmp_code == 1:  # ICMP Destination Unreachable, Code 1 = Host Unreachable
            print(f'ICMP Destination Host Unreachable error received for packet {sequence}')
        
        #    print(f"No ICMP error received for packet {sequence}")

# Ping statistics
print("Ping Statistics\n")
if successful_pings:
    avg_rtt = total_rtt / successful_pings
    print(f'Maximum RTT: {max_rtt:.3f} ms')
    print(f'Minimum RTT: {min_rtt:.3f} ms')
    print(f'Average RTT: {avg_rtt:.3f} ms')
else:
    print('No successful pings to calculate RTT.')

packet_loss_rate = ((N - successful_pings) / N) * 100
print(f'Packet loss rate: {packet_loss_rate:.2f}%')

# Close the sockets
client_socket.close()