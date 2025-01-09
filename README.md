# TCP Ping Server and Client

This project consists of a TCP server and client implemented in Python. The server listens for incoming connections and processes ping requests from the client. The client sends a series of ping messages to the server, measures the round-trip time (RTT) for each ping, and calculates the average, minimum, and maximum RTTs as well as the packet loss rate.

## Table of Contents

- [Requirements](#requirements)
- [How It Works](#how-it-works)
- [Server Setup](#server-setup)
- [Client Setup](#client-setup)
- [Example](#example)
- [Script Breakdown](#script-breakdown)
- [Error Handling](#error-handling)
- [Notes](#notes)
- [Modified TCP Server](#modified-tcp-server)
- [TCP Error Response Test](#tcp-error-response-test)

## Requirements

- Python 3.x
- A server running and listening on the specified IP address and port using TCP

## How It Works

1. The server listens for incoming TCP connections on a specified IP address and port.
2. When a client connects, the server reads the message, simulates packet loss, and responds with either the message in uppercase or a "LOST" message if the packet is considered lost.
3. The client sends a series of ping messages to the server, records the RTT for each response, and calculates statistics such as:
   - Maximum RTT
   - Minimum RTT
   - Average RTT
   - Packet loss rate

## Server Setup

1. **Edit the Server Address:**  
   Ensure that the `server_addr` in the server code matches the desired IP address and port for your server:
   ```python
   server_addr = ('172.21.133.124', 12001)  # Update to your server's IP address and port number
    ```
2. **Run the Server:**
    Start the server by running the following command in the terminal:
    ```
   python3 TCPPingerServer.py
    ```
    The server will listen for incoming connections and handle ping requests from clients.

## Client Setup
1. **Edit the Server Address:**  
   Update the `server_addr` variable in the client code to match the IP address and port of the running server:
   ```python
   server_addr = ('192.168.206.220', 12001)  # Update to match your server's IP address and port number
    ```
2. **Run the Client:**
    Execute the client script with the following command:
    ```
   python3 TCPPingerClient.py
    ```

3. **Input the Number of Pings:**
    When prompted, enter the number of pings you want the client to send to the server.

## Example

1. **Server Output:**
```
Server Started Listening on 127.0.0.1:12001
Message sent by client = ping 1 2024-09-09 12:00:00.123456 from ('127.0.0.1', 34567)
Response sent back = PING 1 2024-09-09 12:00:00.123456
Packet lost
```
2. **Client Output:**
```
$ python3 TCPPingerClient.py
Enter number of pings (N): 5
Client Connection Successful..
Response received is: PING 1 2024-09-09 12:00:00.123456
RTT (in milliseconds) of packet 1 is 3.456000
Packet 2 lost
Client Connection Successful..
Response received is: PING 3 2024-09-09 12:00:00.123456
RTT (in milliseconds) of packet 3 is 4.321000
Client Connection Successful..
Response received is: PING 4 2024-09-09 12:00:00.123456
RTT (in milliseconds) of packet 4 is 2.890000
Packet 5 lost
Maximum RTT (in milliseconds) = 4.321000
Minimum RTT (in milliseconds) = 2.890000
Average RTT (in milliseconds) = 3.555667
Packet loss rate: 40.000000%
```

## Script Breakdown

1. **Server Script:**
    - *Socket Setup*: A TCP socket is created and bound to the specified IP address and port number.
    - *Listening and Accepting Connections*: The server listens for incoming connections and accepts clients.
    - *Packet Loss Simulation*: Each received message has a 20% chance of being lost, simulating network packet loss.
    - *Responding to Clients*: If the packet is not lost, the server responds with the uppercase version of the received message.


2. **Client Script:**
    - *Sending Pings*: The client sends a message with the sequence number and timestamp to the server.
    - *Handling Responses*: If the response is received, the RTT is calculated; if not, the packet is marked as lost.
    - *Calculating Statistics*: The client calculates and prints the maximum, minimum, and average RTT values, as well as the packet loss rate.

## Error Handling

The client handles `timeout` by catching timeout exceptions, allowing it to detect lost packets and continue with the next ping.

## Notes

- Ensure the server is running and reachable at the specified IP and port before starting the client.
- The server and client should be run on systems that allow TCP connections between them, and necessary firewall rules should be configured if needed.

## Modified TCP Server

- The TCP Server is modified to use multithreading in order to handle multiple clients concurrently, by creating a separate thread for each client connection without blocking other connections, leading to improved performance and responsiveness, especially when dealing with concurrent clients.
- Steps involved in Multithreading in a TCP Server:
    - The main thread of the server starts by creating a socket and binding it to a specific IP address and port. The server socket listens for incoming client connection requests.
    - When a client attempts to connect, the server accepts the connection. At this point, the server receives a new socket object (representing the client) and the client’s address.
    - For each accepted client connection, the server spawns a new thread. This new thread is responsible for handling all communication with that specific client. The main thread continues to listen for additional incoming connections while each client thread operates independently.
    - Each client thread manages the read and write operations for its specific client. It handles requests, processes data, and sends responses back to the client. The use of separate threads prevents the server from becoming unresponsive if one client takes a long time to complete its tasks.
    - Threads run concurrently, allowing multiple clients to be served simultaneously. However, access to shared resources (e.g., a shared database or a log file) needs careful synchronization to prevent race conditions or data corruption. Thread synchronization mechanisms like locks, semaphores, or queues can be used to coordinate access to shared resources.

- Run the following code in python to incorporate multithreading by creating new thread:
```python
client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
```

## TCP Error Response Test

The client sends a series of TCP packets to the server and measures the RTT for each packet. If a packet is lost (timeout), it attempts to capture any ICMP error messages that might have been returned, such as **"Destination Host Unreachable."**