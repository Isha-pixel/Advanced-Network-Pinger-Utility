import socket
import struct
import random
import os
import time

# Function to calculate checksum for ICMP packets
def checksum(source_string):
    count_to = (len(source_string) // 2) * 2
    sum = 0
    count = 0

    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2

    if count_to < len(source_string):
        sum = sum + source_string[-1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)

    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

# Function to create an ICMP packet
def create_icmp_packet(icmp_type, icmp_code):
    icmp_checksum = 0
    icmp_unused = 0
    header = struct.pack('!BBHI', icmp_type, icmp_code, icmp_checksum, icmp_unused)
    data = b'Error simulation'
    icmp_checksum = checksum(header + data)
    header = struct.pack('!BBHI', icmp_type, icmp_code, icmp_checksum, icmp_unused)
    return header + data

# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('192.168.241.144', 12001))
serverSocket.listen(1)

# Create a raw socket for ICMP
icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

print("Server is ready to receive connections.")

while True:
    connectionSocket, clientAddress = serverSocket.accept()

    while True:
        rand = random.randint(1, 30)
        print(f"Random value: {rand}")

        # Receive a message from the client
        message = connectionSocket.recv(1024).decode()

        if not message:
            break  # Exit the loop if no message is received

        if rand < 15:
            # Normal TCP packet
            print(f"Sending TCP response to {clientAddress}")
            response = message.upper()  # Convert the message to uppercase
            connectionSocket.send(response.encode())

        elif 15 <= rand < 20:
            # ICMP Port Unreachable
            print(f"Sending ICMP 'Port Unreachable' to {clientAddress}")
            icmp_packet = create_icmp_packet(3, 3)  # ICMP type 3, code 3 (Port Unreachable)
            icmpSocket.sendto(icmp_packet, (clientAddress[0], 0))

        elif 21 <= rand < 27:
            # ICMP Host Unreachable
            print(f"Sending ICMP 'Host Unreachable' to {clientAddress}")
            icmp_packet = create_icmp_packet(3, 1)  # ICMP type 3, code 1 (Host Unreachable)
            icmpSocket.sendto(icmp_packet, (clientAddress[0], 0))

        elif rand >= 28:
            # Timeout (no response)
            print(f"Simulating timeout for {clientAddress}")
            time.sleep(2)  # Simulating a timeout

    connectionSocket.close()