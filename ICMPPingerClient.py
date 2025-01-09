from socket import *
import os
import sys
import struct
import time
import select
import binascii


ICMP_ECHO_REQUEST = 8


def checksum(string):
   csum = 0
   countTo = (len(string) // 2) * 2
   count = 0


   while count < countTo:
       thisVal = string[count+1] * 256 + string[count]
       csum = csum + thisVal
       csum = csum & 0xffffffff
       count = count + 2


   if countTo < len(string):
       csum = csum + string[len(string) - 1]
       csum = csum & 0xffffffff


   csum = (csum >> 16) + (csum & 0xffff)
   csum = csum + (csum >> 16)
   answer = ~csum
   answer = answer & 0xffff
   answer = answer >> 8 | (answer << 8 & 0xff00)
   return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
   timeLeft = timeout
   while 1:
       startedSelect = time.time()
       whatReady = select.select([mySocket], [], [], timeLeft)
       howLongInSelect = (time.time() - startedSelect)
      
       if whatReady[0] == []:  # Timeout
           return "Request timed out."


       timeReceived = time.time()
       recPacket, addr = mySocket.recvfrom(1024)


       # Fill in start
       # Extract the ICMP header from the IP packet
       icmpHeader = recPacket[20:28]  # ICMP header starts after the IP header (20 bytes)


       # Unpack the header to extract useful fields
       icmp_type, code, received_checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)


       # Check if the packet ID matches the sent ping
       if packetID == ID:
           # Extract the time sent from the data portion (following the header)
           bytesInDouble = struct.calcsize("d")  # Size of a double in bytes
           timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]


           # Calculate and return the round-trip time (timeReceived - timeSent)
           return timeReceived - timeSent
       # Fill in end


       timeLeft = timeLeft - howLongInSelect
       if timeLeft <= 0:
           return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
   # Header is type (8), code (8), checksum (16), id (16), sequence (16)
   myChecksum = 0


   # Make a dummy header with a 0 checksum
   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   data = struct.pack("d", time.time())


   # Calculate the checksum on the data and the dummy header
   myChecksum = checksum(header + data)


   # Get the correct checksum, and put it into the header
   if sys.platform == 'darwin':
       # Convert 16-bit integers from host to network byte order
       myChecksum = htons(myChecksum) & 0xffff
   else:
       myChecksum = htons(myChecksum)


   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   packet = header + data


   mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be a tuple, not a string


def doOnePing(destAddr, timeout):
   icmp = getprotobyname("icmp")
   # SOCK_RAW is a powerful socket type that allows us to work directly with IP packets
   mySocket = socket(AF_INET, SOCK_RAW, icmp)
   myID = os.getpid() & 0xFFFF  # Return the current process ID
   sendOnePing(mySocket, destAddr, myID)
   delay = receiveOnePing(mySocket, myID, timeout, destAddr)
   mySocket.close()
   return delay


def ping(host, timeout=1,count=6):
   # timeout=1 means: if one second goes by without a reply from the server,
   # the client assumes that either the client's ping or the server's pong is lost
   dest = gethostbyname(host)
   print(f"Pinging {dest} using Python:")
   # Send ping requests to a server every second
   min_rtt = float('inf')
   max_rtt = float('-inf')
   sum_rtt = 0
   successful_pings = 0
   for i in range(count):
       delay = doOnePing(dest, timeout)
       #print(delay)
       if isinstance(delay, float):  # Successful ping
           min_rtt=min(min_rtt,delay*1000)
           max_rtt=max(max_rtt,delay*1000)
           sum_rtt=sum_rtt+delay*1000
           successful_pings = successful_pings+1
           print(f"Ping {i+1}: RTT = {delay*1000:.4f} ms")
       else:
           print(f"Ping {i+1}: {delay}")
       time.sleep(1)  # Wait for one second before sending the next ping
   if successful_pings:
       print("\nPing Statistics:")
       print(f"Minimum RTT: {min_rtt:.2f} ms")
       print(f"Maximum RTT: {max_rtt:.2f} ms")
       print(f"Average RTT: {sum_rtt/successful_pings:.2f} ms")
   return delay
if __name__ == "__main__":
    ping("www.google.com")