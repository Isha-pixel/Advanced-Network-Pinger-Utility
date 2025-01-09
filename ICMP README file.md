# ICMP Ping Client

This project is a Python implementation of an ICMP ping client that sends ICMP Echo Request messages to a specified host and measures the round-trip time (RTT) for each ping. It provides basic statistics, such as minimum, maximum, and average RTT, similar to the traditional `ping` command.

## Table of Contents

- [Requirements](#requirements)
- [How It Works](#how-it-works)
- [Setup](#setup)
- [Usage](#usage)
- [Example](#example)
- [Script Breakdown](#script-breakdown)
- [Error Handling](#error-handling)
- [Permissions](#permissions)
- [ICMP Error Response Test](#icmp-error-response-test)

## Requirements

- Python 3.x
- Administrative or root privileges (required to send ICMP packets)

## How It Works

1. The client sends ICMP Echo Request packets to the target host using raw sockets.
2. For each Echo Request sent, it waits for an Echo Reply from the host or times out if no reply is received.
3. The round-trip time (RTT) is calculated for each response.
4. After sending the specified number of pings, it calculates and displays the minimum, maximum, and average RTTs.

## Setup

1. **Clone the repository or save the script**:
   Save the provided Python script as `ICMPclient.py`.

2. **Ensure Python is installed**:
   Make sure Python 3.x is installed on your system.

## Usage

1. **Run the Script**:
   Execute the script from the command line with administrative privileges:
   ```bash
   sudo python3 ICMPclient.py
   ```

2. **Ping a Specific Host**:
    By default, the script pings `www.google.com`. You can modify the `ping()` function call in the `if __name__ == "__main__"` block to target a different host or change the number of pings:
```python
ping("www.google.com", timeout=1, count=6)
```
`timeout`: The time in seconds to wait for each reply (default is 1 second).
`count`: The number of ping requests to send (default is 6).

## Example

```bash
$ sudo python3 icmp_client.py
Pinging 142.250.182.196 using Python:
Ping 1: RTT = 15.4678 ms
Ping 2: RTT = 14.3982 ms
Ping 3: RTT = 15.0423 ms
Ping 4: RTT = 13.8412 ms
Ping 5: RTT = 14.6839 ms
Ping 6: RTT = 15.2234 ms

Ping Statistics:
Minimum RTT: 13.84 ms
Maximum RTT: 15.47 ms
Average RTT: 14.93 ms
```

## Script Breakdown

1. **Key Functions**:
    - `checksum(string)`:
    Calculates the checksum for the ICMP packet to ensure data integrity.
    - `receiveOnePing(mySocket, ID, timeout, destAddr)`:
    Waits for an ICMP Echo Reply from the server. Extracts RTT if the reply matches the sent request.
    - `sendOnePing(mySocket, destAddr, ID)`:
    Constructs and sends an ICMP Echo Request packet to the specified address.
    - `doOnePing(destAddr, timeout)`:
    Manages the sending and receiving of a single ping.
    - `ping(host, timeout=1, count=6)`:
    Sends multiple pings to the specified host, measures RTT, and computes statistics.

2. **ICMP Protocol**:
    - ICMP (Internet Control Message Protocol) is used by network devices to send error messages and operational information.
    - This script uses ICMP Echo Requests to test the reachability of hosts on a network.

## Error Handling

- *Timeouts*: If a ping request times out (no reply received within the specified timeout), the script prints "Request timed out."
- *Permissions*: Since ICMP requires raw sockets, the script must be run with administrative or root privileges.

## Permissions

- *Running as Administrator/Root*:
1. Raw sockets required for ICMP packets necessitate administrative rights.
2. On Unix-like systems, use sudo to run the script:
```bash
sudo python3 ICMPclient.py
```
- On Windows, run the script from an elevated command prompt.

## ICMP Error Response Test

The client sends a series of ICMP packets to the server and measures the RTT for each packet. If a packet is lost (timeout), it attempts to capture any ICMP error messages that might have been returned.

Run the following code on Server side terminal to block packets from a certain IP address:
```bash
sudo iptables -A INPUT -s <source_ip_address> -p icmp -j REJECT --reject-with <error_response>
```

Now, when the client, with that blocked IP address, pings the server, its packets are not able to reach the destination & **"Destination Host Unreachable"** or **"Destination Port Unreachable"** error is returned to the client.
