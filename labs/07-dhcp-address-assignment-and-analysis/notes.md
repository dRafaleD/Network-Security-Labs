# Day 7 — DHCP, Address Assignment and Packet Analysis

## Goals
By the end of this lab you should be able to explain how a host obtains IPv4 configuration, distinguish DHCP from DNS/ARP, read the DORA exchange in a packet capture, identify important DHCP fields, and reason about DHCP from a defensive perspective.

## 1. Why DHCP exists
A host normally needs an IP address, prefix/subnet mask, default gateway and DNS resolver before it can communicate normally. DHCP automates delivery of this configuration. DHCP is configuration, not name resolution: DNS maps names to data such as IP addresses; ARP resolves a local IPv4 next hop to a MAC address.

## 2. Client and server ports
DHCPv4 normally uses UDP:
- server: UDP 67
- client: UDP 68

A new client may not yet know its own address or the DHCP server address, so broadcast traffic is important during early discovery.

## 3. DORA
The common DHCPv4 flow is:
1. **DHCPDISCOVER** — client searches for DHCP servers.
2. **DHCPOFFER** — server proposes configuration.
3. **DHCPREQUEST** — client requests/accepts an offered address.
4. **DHCPACK** — server confirms the lease.

DORA is a learning model for the normal initial lease process; real captures can include retransmissions, multiple offers, NAK messages and renewal traffic.

## 4. Lease lifecycle
An address is usually leased for a limited period. Clients try to renew before expiry. Two useful concepts are **T1 (renewal)** and **T2 (rebinding)**. A client can often renew directly with the known server first; later it may broaden the request if renewal fails.

Other messages you may encounter include DHCPNAK, DHCPDECLINE, DHCPRELEASE and DHCPINFORM.

## 5. Fields worth inspecting
In Wireshark, inspect:
- transaction ID (xid)
- client hardware/MAC address
- your/client IP fields
- offered address
- server identifier
- lease time
- subnet mask
- router/default gateway option
- DNS server option
- DHCP message type

Options are especially important because DHCP distributes more than an IP address.

## 6. DHCP relay
Broadcasts normally do not cross routers. Larger networks therefore use DHCP relay so clients in another subnet can reach a centralized DHCP service. This is one reason DHCP analysis must include the network topology instead of assuming the server is on the same LAN.

## 7. Defensive security view
A rogue DHCP server can hand out incorrect gateway or DNS settings. Defensive controls can include switch features such as DHCP snooping, trusted/untrusted port design, segmentation, monitoring for unexpected DHCP servers, and alerting on unusual lease behavior.

Do not experiment with rogue DHCP services on shared networks. Use an isolated VM/lab network you control.

## 8. Lab A — Inspect your current configuration
Linux examples:
```bash
ip addr
ip route
cat /etc/resolv.conf
resolvectl status 2>/dev/null
```
Record:
- interface name
- IPv4 address/prefix
- default gateway
- DNS resolver(s)

Do not assume every value came from DHCP; static configuration and local resolver stubs are possible.

## 9. Lab B — Capture DHCP safely
Prefer an isolated VM network. Start Wireshark and use:
```text
dhcp
```
or capture/display BOOTP/DHCP traffic with UDP ports 67 and 68.

On a disposable lab VM, renewing the lease may produce useful traffic. The exact command depends on NetworkManager/systemd-networkd/dhclient and your distribution. Avoid disrupting a remote connection or a network you do not administer.

For each observed message, note:
| Message | Source | Destination | Broadcast? | Important options |
|---|---|---|---|---|
| Discover | | | | |
| Offer | | | | |
| Request | | | | |
| ACK | | | | |

Then compare the ACK options with `ip route` and resolver configuration.

## 10. Lab C — tcpdump
Find your interface:
```bash
ip link
```
Capture only DHCPv4:
```bash
sudo tcpdump -i <interface> -nn -vvv 'udp port 67 or udp port 68'
```
Explain why `-nn` is useful during protocol analysis and identify the client/server UDP ports.

## 11. Analysis questions
1. Why can a DHCP client use broadcast before it owns an IPv4 address?
2. What is the difference between OFFER and ACK?
3. Which DHCP option normally supplies the default gateway?
4. Why is malicious DNS configuration delivered by DHCP security-relevant?
5. Why may a relay be necessary across subnets?
6. How would you distinguish DHCP traffic from DNS traffic in a capture?
7. What evidence would suggest more than one DHCP server answered a client?
8. Why should a packet capture be correlated with host configuration?

## 12. Mini challenge
Create a short report containing:
- topology/environment description
- four DORA messages if available
- transaction ID
- offered/assigned address
- gateway and DNS options
- lease time
- one defensive observation
- limitations of your capture

## Takeaway
DHCP is not simply “the protocol that gives an IP.” It bootstraps network configuration. Understanding its broadcasts, UDP ports, options, lease lifecycle and trust assumptions makes later segmentation, NAC, monitoring and incident-analysis topics much easier.
