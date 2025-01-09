# Import all the necessary libraries
from socket import *
import os
import struct
import time
import select
import statistics

# Constants for ICMP message types
ICMP_ECHO_REQUEST = 8  # Type 8 is Echo Request
ICMP_ECHO_REPLY = 0    # Type 0 is Echo Reply

# Function to calculate the checksum of the packet
def checksum(source_string):
    csum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0

    # Sum up 16-bit chunks of the packet
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        csum += thisVal
        csum &= 0xffffffff  # Keep the result within 32 bits
        count += 2

    # Add left-over byte if the packet length is odd
    if countTo < len(source_string):
        csum += source_string[len(source_string) - 1]
        csum &= 0xffffffff

    # Fold any overflow from high-order bits into low-order bits
    csum = (csum >> 16) + (csum & 0xffff)
    csum += (csum >> 16)
    answer = ~csum  # One's complement
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)  # Swap bytes for network order
    return answer

# Function to receive an ICMP Echo Reply
def receiveOnePing(mySocket, ID, sequence, timeout, destAddr):
    timeLeft = timeout  # Time left before the function times out
    while timeLeft > 0:
        startTime = time.time()  # Mark the start time
        ready = select.select([mySocket], [], [], timeLeft)  # Wait for a response from the socket
        selectDuration = time.time() - startTime  # Time spent waiting

        # Check if the select call returned due to timeout
        if ready[0] == []:
            return None, "Request timed out."

        timeReceived = time.time()  # Time when the packet was received
        recPacket, addr = mySocket.recvfrom(1024)  # Receive the packet
        icmpHeader = recPacket[20:28]  # ICMP header starts after the first 20 bytes of the IP header
        icmpType, code, _, packetID, packetSequence = struct.unpack("bbHHh", icmpHeader)  # Unpack ICMP header

        # Verify the packet is an ICMP Echo Reply with matching ID and sequence number
        if icmpType == ICMP_ECHO_REPLY and packetID == ID and packetSequence == sequence:
            timeSent = struct.unpack("d", recPacket[28:28 + struct.calcsize("d")])[0]  # Extract the send time from the packet
            ttl = recPacket[8]  # TTL is located in the 8th byte of the IP header
            rtt = (timeReceived - timeSent) * 1000  # Calculate round-trip time in milliseconds
            return rtt, f"Reply from {addr[0]}: bytes={len(recPacket)} time={rtt:.3f}ms TTL={ttl} Sequence={packetSequence}"
        elif icmpType == 3:  # ICMP Type 3 is "Destination Unreachable"
            icmp_errors = ["Network Unreachable", "Host Unreachable", "Protocol Unreachable", "Port Unreachable"]
            return None, f"Destination {icmp_errors[code] if code < len(icmp_errors) else 'Unreachable'}"

        # Decrease the remaining time left before timeout
        timeLeft -= selectDuration

    return None, "Request timed out."  # Return timeout message if no response

# Function to send an ICMP Echo Request
def sendOnePing(mySocket, destAddr, ID, sequence):
    # Create ICMP header with type, code, checksum (initially zero), ID, and sequence number
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, ID, sequence)
    data = struct.pack("d", time.time())  # Add current time as the payload
    myChecksum = checksum(header + data)  # Calculate checksum for the packet

    # Network byte order conversion for checksum
    myChecksum = htons(myChecksum) & 0xffff
    # Pack header again with correct checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    packet = header + data  # Combine header and payload

    mySocket.sendto(packet, (destAddr, 1))  # Send the packet to the destination address, using protocol number 1 for ICMP

# Function to perform a single ping
def doOnePing(destAddr, timeout, sequence):
    icmp = getprotobyname("icmp")  # Get the protocol number for ICMP
    try:
        mySocket = socket(AF_INET, SOCK_RAW, icmp)  # Create a raw socket
    except PermissionError as e:
        # Inform the user if raw socket creation fails due to permissions
        sys.exit(f"Permission Error: {e}. Run the script with elevated privileges.")

    myID = os.getpid() & 0xFFFF  # Use the process ID as the identifier for the packet
    sendOnePing(mySocket, destAddr, myID, sequence)  # Send the ICMP Echo Request
    delay = receiveOnePing(mySocket, myID, sequence, timeout, destAddr)  # Receive the response
    mySocket.close()  # Close the socket
    return delay  # Return the delay and message

# Main function to send multiple pings and display statistics
def ping(host, count=10, timeout=1):
    dest = gethostbyname(host)  # Resolve the host name to an IP address
    print(f"Pinging {dest} with ICMP:")  # Display the destination
    print("")

    rtt_times = []  # List to store round-trip times
    packets_received = 0  # Counter for received packets

    for i in range(count):
        delay, message = doOnePing(dest, timeout, i + 1)  # Send a ping and receive response
        if delay:
            packets_received += 1  # Increment received packet count
            rtt_times.append(delay)  # Append RTT to the list
        print(message)  # Print the response message
        time.sleep(1)  # Wait one second between pings

    # Calculate RTT statistics
    if rtt_times:
        min_rtt = min(rtt_times)
        max_rtt = max(rtt_times)
        avg_rtt = statistics.mean(rtt_times)
    else:
        min_rtt = max_rtt = avg_rtt = 0

    packet_loss = ((count - packets_received) / count) * 100  # Calculate packet loss percentage

    # Print summary statistics
    print("\n--- Ping statistics ---")
    print(f"{count} packets transmitted, {packets_received} received, {packet_loss:.1f}% packet loss")
    print(f"rtt min = {min_rtt:.3f} ms, avg = {avg_rtt:.3f} ms, max = {max_rtt:.3f} ms")

# Example call to ping google.com
ping("google.com", timeout=1, count=10)  # Perform ping to google.com