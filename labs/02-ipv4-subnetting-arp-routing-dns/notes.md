# Day 2 — IPv4, Subnetting, ARP, Routing and DNS

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Build a stronger mental model of how a host decides where to send traffic. This lab connects IPv4 addressing, subnet masks, local/remote network decisions, ARP, the default gateway, routing, and DNS.

By the end of the lab, you should be able to look at a packet and explain why it was sent to a local host or to the router.

## 1. IPv4 addresses

An IPv4 address contains 32 bits and is normally written as four decimal octets:

```text
192.168.1.25
```

The address alone is not enough to determine which part represents the network. We also need the prefix length.

Example:

```text
192.168.1.25/24
```

A `/24` means that the first 24 bits describe the network and the remaining 8 bits identify hosts inside that network.

For a typical `192.168.1.0/24` network:

```text
Network address : 192.168.1.0
Host range      : 192.168.1.1 - 192.168.1.254
Broadcast       : 192.168.1.255
Subnet mask     : 255.255.255.0
```

## 2. CIDR and subnet masks

Common examples:

| CIDR | Subnet mask | Addresses per subnet |
| --- | --- | ---: |
| /24 | 255.255.255.0 | 256 |
| /25 | 255.255.255.128 | 128 |
| /26 | 255.255.255.192 | 64 |
| /27 | 255.255.255.224 | 32 |
| /28 | 255.255.255.240 | 16 |

The total number of addresses includes the network and broadcast addresses in ordinary IPv4 subnets.

Example:

```text
10.0.0.205/28
```

A `/28` has blocks of 16 addresses. The block containing 205 is:

```text
192 - 207
```

Therefore:

```text
Network   : 10.0.0.192
Hosts     : 10.0.0.193 - 10.0.0.206
Broadcast : 10.0.0.207
```

## 3. Local or remote?

Suppose your host is:

```text
192.168.1.20/24
```

Destination A:

```text
192.168.1.50
```

This is inside the same `/24` network, so the host can send the Ethernet frame directly to the destination on the local network.

Destination B:

```text
1.1.1.1
```

This is outside the local network. The host sends the frame toward its default gateway.

Important distinction:

```text
Destination IP  -> can remain the remote server
Destination MAC -> can be the local router's MAC address
```

Layer 2 and Layer 3 are solving different parts of the delivery problem.

## 4. ARP

ARP resolves an IPv4 address to a MAC address on the local network.

Inspect the neighbor table:

```bash
ip neigh
```

You may see entries similar to:

```text
192.168.1.1 dev wlan0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
```

This tells you that the host knows which MAC address corresponds to that local IPv4 address.

Generate local traffic to your gateway, then inspect the table again:

```bash
ping -c 1 <gateway-ip>
ip neigh
```

## 5. Observe ARP with tcpdump

Use only your own/local authorized network.

```bash
sudo tcpdump -n -e -i <interface> arp
```

In another terminal, communicate with a local address that requires resolution.

An ARP exchange conceptually asks:

```text
Who has 192.168.1.1?
Tell 192.168.1.20.
```

The owner replies with its MAC address.

The `-e` option is useful here because it displays link-layer information.

## 6. Routing table

Run:

```bash
ip route
```

Example:

```text
default via 192.168.1.1 dev wlan0
192.168.1.0/24 dev wlan0 src 192.168.1.20
```

The second route says the local network is directly reachable.

The default route is used when no more specific route matches the destination.

Ask Linux which route it would use:

```bash
ip route get 1.1.1.1
```

Then compare:

```bash
ip route get <another-local-ip>
```

## 7. DNS

Humans prefer names such as:

```text
example.com
```

Networks ultimately need addresses.

Try:

```bash
getent hosts example.com
```

If `dig` is installed:

```bash
dig example.com
```

Useful DNS record types to recognize:

```text
A     -> IPv4 address
AAAA  -> IPv6 address
CNAME -> alias
MX    -> mail server information
NS    -> authoritative name server information
```

## 8. Observe DNS traffic

Capture DNS traffic:

```bash
sudo tcpdump -n -i <interface> port 53
```

Then perform a lookup.

Depending on your system and network configuration, DNS traffic may not appear as plain port 53 traffic because modern systems can use encrypted DNS or a local resolver. If nothing appears, that itself is something to investigate rather than assuming the command failed.

In Wireshark, a useful display filter for classic DNS traffic is:

```text
dns
```

Inspect:

- query name
- query type
- response
- returned addresses
- source and destination

## 9. Follow one connection mentally

When you access a remote site, a simplified sequence can be:

```text
hostname
   ↓
DNS resolution
   ↓
destination IP
   ↓
routing decision
   ↓
remote destination? yes
   ↓
find gateway MAC using ARP/neighbour cache
   ↓
send local frame to gateway
   ↓
router forwards packet onward
```

This is a simplified model, but it connects several concepts that are often learned separately.

## 10. Mini exercises

### Exercise A — Subnet

Calculate:

```text
192.168.10.77/27
```

Find:

- subnet mask
- network address
- broadcast address
- usable host range

### Exercise B — Route

Run:

```bash
ip route get 1.1.1.1
```

Record:

- selected interface
- gateway
- source IP

### Exercise C — ARP

Run:

```bash
ip neigh
```

Identify your gateway entry if present. Compare its IP and MAC address.

### Exercise D — DNS

Resolve `example.com` and record at least one returned address.

## 11. Security connection

These fundamentals appear constantly in security work.

- ARP explains local Layer-2 identity and is important when understanding spoofing risks.
- Routing explains where traffic can travel.
- DNS logs can reveal which domains a system attempts to contact.
- Subnets define network boundaries and are important for segmentation.
- Packet captures let analysts verify what actually happened on the wire.

Do not jump directly to attacks. First learn what normal behavior looks like.

## Questions

1. Why does a host need both an IP address and a subnet mask/prefix?
2. What is the difference between a destination IP and destination MAC when contacting a remote server?
3. What problem does ARP solve?
4. When is the default gateway used?
5. What does the most specific matching route mean?
6. What is the difference between an A and AAAA DNS record?
7. Why might a `port 53` capture show no DNS traffic on some systems?
8. For `192.168.10.77/27`, what are the network and broadcast addresses?

## Main takeaway

Think in this order:

```text
What is my address and subnet?
        ↓
Is the destination local?
        ↓
Which route should be used?
        ↓
Which local MAC address receives the frame?
        ↓
Does a hostname first need DNS resolution?
```

Understanding this decision process is the foundation for later packet analysis, firewall rules, segmentation, and network-security troubleshooting.
