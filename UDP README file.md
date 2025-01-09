# UDP Server and Client

This project implements a simple UDP server and client using Python's socket library. The server listens for incoming UDP packets, processes them, and sends a response back to the client. The client sends a specified number of ping messages to the server, measures the round-trip time (RTT) for each ping, and calculates statistics on the RTT.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Example](#example)
- [Code Breakdown](#code-breakdown)
- [Error Handling](#error-handling)
- [Notes](#notes)
- [Modified UDP Server](#modified-udp-server)
- [UDP Error Response Test](#udp-error-response-test)

## Overview

- **Server**:
  - Receives messages from the client.
  - Randomly decides whether to respond or simulate a packet loss (20% chance of loss).
  - Sends the message back in uppercase if not lost.

- **Client**:
  - Sends a specified number of ping requests to the server.
  - Receives responses and calculates the RTT for each ping.
  - Displays the minimum, maximum, and average RTT, and calculates the packet loss rate.

## Requirements

- Python 3.x
- Basic understanding of networking and sockets.

## Setup

1. **Clone the Repository**:
   Save the server code as `UDPServer.py` and the client code as `UDPClient.py`.

2. **Ensure Python is installed**:
   Make sure Python 3.x is installed on your system.

## Usage

#### Running the Server:

1. Open a terminal.
2. Run the server script:
   ```bash
   python3 UDPServer.py
   ```
3. The server will start listening on the IP address `172.21.134.130` and port `12001`.

#### Running the Client:

1. Open another terminal.
2. Run the client script:
   ```bash
   python3 UDPClient.py
    ```
3. Enter the number of pings you want to send when prompted.

#### Client-Side Configuration:

- *Server Address*: Ensure the client connects to the correct server IP address and port as defined in the client code (`server_addr = ('172.21.133.124', 12001)`).
- *Ping Count*: Input the desired number of pings when prompted by the client script.

## Example
Sample Output from Client:
```bash
Enter number of pings (N): 5
Response received is: PING 1 2023-09-09 12:34:56.789123
RTT (in milliseconds) of packet 1 is 15.678
Response received is: PING 2 2023-09-09 12:34:57.789123
RTT (in milliseconds) of packet 2 is 12.345
Packet 3 is lost
Response received is: PING 4 2023-09-09 12:34:58.789123
RTT (in milliseconds) of packet 4 is 13.456
Response received is: PING 5 2023-09-09 12:34:59.789123
RTT (in milliseconds) of packet 5 is 11.789
Maximum RTT (in milliseconds) = 15.678
Minimum RTT (in milliseconds) = 11.789
Average RTT (in milliseconds) = 13.317
Packet loss rate: 20.000%

```

## Code Breakdown

1. **Server Code:**
    The script imports necessary Python libraries:

    - `socket`: For creating UDP sockets.
    - `random`: For generating random values.
    - `time`: For measuring RTT.
    - `datetime`: For formatting the timestamp of each ping message.

2. **Client Code:**
    - Imports:
        - Uses Python's `socket` library for networking, `time` for RTT calculation, and `datetime` for timestamp formatting.
    - Functionality:
        - Creates a UDP socket and connects to the server at `172.21.133.124` on port `12001`.
        - Sends ping messages and waits for responses.
        - Calculates RTT for each successful ping.
        - Tracks the number of successful pings and calculates RTT statistics.
        - Displays the minimum, maximum, and average RTT along with the packet loss rate.

3. **Creating the UDP Socket:**
    A UDP socket is created and set with a 1-second timeout:
    ```python
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(1)
    ```

4. **Ping Loop:**
    The script prompts the user for the number of pings and then enters a loop to send ping messages:

    - Sends a message with the current sequence number and timestamp.
    - Waits for a response and calculates RTT if the response is received.
    - Tracks successful pings and updates RTT statistics.

5. **Calculating and Printing Statistics:**
    After all pings are sent, the script prints:

    - Maximum RTT
    - Minimum RTT
    - Average RTT (only if there were successful pings)
    - Packet loss rate

6. **Closing the Socket:**
    The UDP socket is closed after all pings are complete:
    ```python
    client_socket.close()
    ```


## Error Handling

The script handles `timeout` by catching timeout exceptions, allowing it to print a message indicating that a packet was lost and continue with the next ping.

## Notes

- Ensure the server is running and reachable at the specified IP and port.
- The server should respond to the client's ping messages; otherwise, all packets will be reported as lost.
- The script should be run with elevated privileges (sudo) due to the use of raw sockets, which require administrative access.

## Modified UDP Server:

- The UDP Server is modified to emulate packet loss at the network interface card (NIC) level by using tc (traffic control) netem utility in Linux.
- Since you are emulating losses at the NIC level, your server program no longer requires any code to simulate packet losses using randint( ) function and therefore modify it accordingly.

Run the following code in your Terminal window to emulate 20% packet loss:
```bash
sudo tc qdisc add dev wlp0s20f3 root netem loss 20%
```

## UDP Error Response Test

The client sends a series of UDP packets to the server and measures the RTT for each packet. If a packet is lost (timeout), it attempts to capture any ICMP error messages that might have been returned, such as **"Destination Host Unreachable."**
