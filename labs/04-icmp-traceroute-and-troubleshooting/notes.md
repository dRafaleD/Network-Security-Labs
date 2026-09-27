# Day 4 — ICMP, Traceroute, TTL and Network Troubleshooting

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal
Understand ICMP, TTL/Hop Limit, ping and traceroute as network-observation tools, then connect them to defensive troubleshooting and packet analysis.

## 1. ICMP is not TCP or UDP
ICMP carries control and diagnostic information at the network layer. It does not use TCP/UDP ports.

Common examples include Echo Request/Reply and error messages generated when delivery encounters a problem.

## 2. Ping
```bash
ping -c 4 1.1.1.1
```
Ping commonly uses ICMP Echo Request and Echo Reply. Successful replies show IP reachability at that moment, but a failed ping does not automatically mean the host is offline: ICMP may be filtered or rate-limited.

## 3. TTL
IPv4 packets contain a Time To Live value. Each router forwarding the packet reduces it. When it reaches zero, the router normally discards the packet and may return ICMP Time Exceeded.

TTL prevents packets from circulating forever during routing loops.

## 4. Traceroute
Traceroute exploits hop-limit behavior to reveal intermediate routing hops.

Linux:
```bash
traceroute 1.1.1.1
```
Depending on implementation/options, traceroute may use UDP, ICMP, or TCP probes. Missing hops do not prove a router is absent; devices can filter or deprioritize responses.

## 5. Packet-capture lab
Generate only your own diagnostic traffic:
```bash
sudo tcpdump -n -i any icmp
```
In another terminal:
```bash
ping -c 4 1.1.1.1
```

Wireshark filters:
```text
icmp
icmp.type == 8
icmp.type == 0
```

Observe source/destination addresses, ICMP type/code and TTL.

## 6. Troubleshooting layers
When connectivity fails, reason in stages:
```text
interface up?
   ↓
IP address?
   ↓
local gateway reachable?
   ↓
route exists?
   ↓
remote IP reachable?
   ↓
DNS resolves?
   ↓
application/service works?
```

Useful commands:
```bash
ip addr
ip route
ip neigh
ping -c 2 <gateway>
ping -c 2 1.1.1.1
getent hosts example.com
ss -tuln
```

## 7. IP works but domain does not
If an IP is reachable but a hostname does not resolve, investigate DNS rather than immediately blaming routing.

This distinction is important:
```text
routing/reachability != name resolution
```

## 8. Security connection
ICMP and route observations help defenders understand network paths and failures. They can also appear in reconnaissance, so organizations may filter some diagnostic traffic. Filtering has trade-offs because ICMP also supports legitimate network operation and troubleshooting.

## Exercises
1. Find your default route with `ip route`.
2. Ping your own gateway and inspect the ICMP packets.
3. Ping a public IP you are allowed to contact and compare TTL values.
4. Run traceroute and record only the hop count and observations—do not assume hidden hops are down.
5. Test hostname resolution with `getent hosts`.
6. Explain whether a failed ping proves a host is offline.

## Questions
1. Does ICMP use ports?
2. Why does TTL exist?
3. What normally happens when TTL reaches zero?
4. How can traceroute discover hops?
5. Why can a traceroute contain `*` entries?
6. What is the difference between IP reachability and DNS resolution?
7. Why should troubleshooting proceed layer by layer?

## Main takeaway
```text
ICMP + TTL
    ↓
reachability/path evidence
    ↓
packet capture
    ↓
layer-by-layer troubleshooting
    ↓
better defensive diagnosis
```
