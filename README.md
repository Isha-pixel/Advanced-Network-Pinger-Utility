# Advanced Network Pinger Utility (UDP, TCP, ICMP Protocols)

This repository contains implementations of networking utilities using Python. These tools allow users to test network connectivity and measure metrics such as round-trip time (RTT), packet loss rate, and error responses. The repository includes:

1. **ICMP Ping Client**: A Python script that mimics the functionality of the traditional `ping` command using ICMP packets.
2. **TCP Ping Server and Client**: A client-server model over TCP for sending and responding to ping requests.
3. **UDP Server and Client**: A client-server implementation over UDP for measuring RTT and simulating packet loss.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Examples](#examples)
- [Code Details](#code-details)
- [Error Handling](#error-handling)
- [Notes and Modifications](#notes-and-modifications)

---

## Overview

### ICMP Ping Client
- Sends ICMP Echo Request packets to a specified host and measures RTT.
- Displays minimum, maximum, and average RTT statistics.

### TCP Ping Server and Client
- The server handles ping requests over TCP, simulating packet loss.
- The client calculates RTT statistics and packet loss rate.

### UDP Server and Client
- The server simulates packet loss when responding to client pings.
- The client measures RTT and calculates packet loss metrics.

---

## Requirements

- **Python 3.x**: Ensure Python 3.x is installed on your system.
- **Privileges**:
  - ICMP utilities require administrative/root privileges.
  - TCP/UDP tools may need elevated permissions depending on system configurations.

---

## Setup

1. Clone this repository or save the individual scripts.
2. Install Python 3.x if not already installed.
3. Configure server and client IP addresses and ports as needed.

---

## Usage

### ICMP Ping Client
Run the script with administrative privileges:
```bash
sudo python3 ICMPclient.py
```
Modify the `ping()` function to specify the target host, timeout, and number of pings:
```python
ping("www.google.com", timeout=1, count=6)
```

### TCP Ping Server and Client
1. Start the TCP server:
   ```bash
   python3 TCPPingerServer.py
   ```
2. Run the TCP client:
   ```bash
   python3 TCPPingerClient.py
   ```
   Enter the number of pings when prompted.

### UDP Server and Client
1. Start the UDP server:
   ```bash
   python3 UDPServer.py
   ```
2. Run the UDP client:
   ```bash
   python3 UDPClient.py
   ```
   Enter the number of pings when prompted.

---

## Examples

### ICMP Ping Example
```bash
$ sudo python3 ICMPclient.py
Pinging 142.250.182.196 using Python:
Ping 1: RTT = 15.4678 ms
Ping 2: RTT = 14.3982 ms
...
Average RTT: 14.93 ms
```

### TCP Ping Example
Server:
```bash
Server Started Listening on 127.0.0.1:12001
Packet lost
```
Client:
```bash
Enter number of pings (N): 5
RTT (in milliseconds) of packet 1 is 3.456000
...
Packet loss rate: 40.000000%
```

### UDP Ping Example
Client:
```bash
Enter number of pings (N): 5
RTT (in milliseconds) of packet 1 is 15.678
Packet loss rate: 20.000%
```

---

## Code Details

### ICMP Client
- **Core Functions**:
  - `checksum()`: Calculates ICMP packet checksum.
  - `ping()`: Sends multiple ICMP Echo Requests and computes RTT statistics.

### TCP Tools
- **Server**:
  - Multithreaded to handle multiple clients.
  - Simulates packet loss and processes ping messages.
- **Client**:
  - Sends ping messages and calculates RTT and packet loss.

### UDP Tools
- **Server**:
  - Simulates packet loss using Python or Linux `tc` command.
- **Client**:
  - Sends ping requests and calculates RTT metrics.

---

## Error Handling

- **Timeouts**: Detected and reported for ICMP, TCP, and UDP.
- **Administrative Permissions**: Required for ICMP utilities and raw socket operations.

---

## Notes and Modifications

- **Multithreading**: TCP server uses multithreading to handle multiple clients concurrently.
- **Packet Loss Simulation**: UDP server can use the `tc` command to simulate packet loss at the NIC level:
  ```bash
  sudo tc qdisc add dev wlp0s20f3 root netem loss 20%
  ```
