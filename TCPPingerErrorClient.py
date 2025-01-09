import socket
import time
import statistics
import struct

# Function to receive ICMP packets
def receive_icmp(clientSocket):
    raw_data, addr = clientSocket.recvfrom(1024)
    icmp_header = raw_data[20:28]  # Skip the IP header (first 20 bytes)
    
    icmp_type, icmp_code, icmp_checksum, icmp_unused = struct.unpack('!BBHI', icmp_header)
    
    if icmp_type == 3:
        if icmp_code == 3:
            print(f"Received ICMP 'Port Unreachable' from {addr[0]}")
        elif icmp_code == 1:
            print(f"Received ICMP 'Host Unreachable' from {addr[0]}")
    else:
        print("Received other ICMP message")

# TCP connection details
serverName = '192.168.241.110'
serverPort = 11000

# Initialize RTT and packet loss variables
rtts = []
packet_loss_count = 0
sequence_number = 0

# Create a TCP socket
clientSocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a raw socket for ICMP listening
clientSocketICMP = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

try:
    # Connect to the TCP server
    clientSocketTCP.connect((serverName, serverPort))
    print(f"Connected to {serverName} on port {serverPort}")

    sequence_number = int(input("Enter the number of pings to send: "))

    for i in range(1, sequence_number + 1):
        message = f"PING {i} {time.time()}"
        start_time = time.time()

        # Send the TCP ping message
        print(f"Sending TCP packet #{i}")
        clientSocketTCP.send(message.encode())

        # Set a timeout of 1 second for receiving a response
        clientSocketTCP.settimeout(1)

        try:
            # Try to receive the TCP response
            response = clientSocketTCP.recv(1024).decode()
            end_time = time.time()

            # Measure RTT
            rtt = (end_time - start_time) * 1000
            rtts.append(rtt)
            print(f"Received TCP response: {response} | RTT: {rtt:.2f} ms | Packet #{i}")

        except socket.timeout:
            # If TCP times out, listen for ICMP error responses
            print(f"Request timed out for packet #{i}. Checking for ICMP error...")
            try:
                receive_icmp(clientSocketICMP)
                packet_loss_count += 1
            except socket.timeout:
                print("No ICMP error received")

finally:
    # Calculate RTT statistics after all pings
    if rtts:
        min_rtt = min(rtts)
        max_rtt = max(rtts)
        avg_rtt = statistics.mean(rtts)
        print(f"\nMinimum RTT: {min_rtt:.2f} ms")
        print(f"Maximum RTT: {max_rtt:.2f} ms")
        print(f"Average RTT: {avg_rtt:.2f} ms")
    else:
        print("\nNo RTT statistics available.")

    # Calculate and display packet loss rate
    if sequence_number > 0:
        loss_rate = (packet_loss_count / sequence_number) * 100
        print(f"Packet loss rate: {loss_rate:.2f}%")

    # Close sockets
    clientSocketTCP.close()
    clientSocketICMP.close()
    print("Connection closed.")