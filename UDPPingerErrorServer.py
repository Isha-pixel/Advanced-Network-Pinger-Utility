import socket
import random
import struct

# Function to create a simple ICMP error packet (Destination Host Unreachable)
def create_icmp_error_packet(original_message):
  icmp_type = 3 # Destination Unreachable
  icmp_code = 1 # Host Unreachable
  checksum = 0
# Create ICMP header (8 bytes: type, code, checksum, ID, sequence)
  header = struct.pack('bbHHh', icmp_type, icmp_code, checksum, 0, 0)
  checksum = calculate_checksum(header)
  header = struct.pack('bbHHh', icmp_type, icmp_code, checksum, 0, 0)
  icmp_socket.sendto(header, original_message)
#return header + original_message[:8] # Send part of the original message as data

# Function to calculate checksum
def calculate_checksum(data):
 checksum = 0
 length = len(data)
 for i in range(0, length, 2):
   word = (data[i] << 8) + (data[i + 1])
   checksum += word
 checksum = (checksum >> 16) + (checksum & 0xffff)
 checksum = ~checksum & 0xffff
 return checksum

# Main server loop
if __name__ == "__main__":
# Create a UDP socket for receiving pings
 udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 udp_socket.bind(('192.168.206.229', 12002))
 icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

print("Server is listening...")

while True:
 message, addr = udp_socket.recvfrom(1024)
 print(f"Received message from {addr}: {message.decode()}")

# Randomly decide whether to send an ICMP error or a valid response
 rand = random.randint(1, 10)
 if rand > 8: # Simulate an ICMP error (10% chance)
    print(f"Sending ICMP error to {addr}")
    create_icmp_error_packet(addr)
#udp_socket.sendto(icmp_error_packet, addr)
 else:
   print(f"Sending valid response to {addr}")
   response_message = message.upper()
   udp_socket.sendto(response_message, addr)