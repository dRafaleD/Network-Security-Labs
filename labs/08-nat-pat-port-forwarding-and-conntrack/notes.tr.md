# Gün 8 — NAT, PAT, Port Forwarding ve Connection Tracking

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Understand how private hosts communicate through translated addresses, how multiple internal connections can share one public address, how port forwarding changes inbound reachability, and how NAT interacts with stateful firewalls and connection tracking.

This day combines:

1. private vs public addressing,
2. NAT,
3. PAT/NAPT,
4. source and destination translation,
5. port forwarding,
6. stateful connection tracking,
7. routing before translation,
8. packet-capture interpretation,
9. common troubleshooting mistakes,
10. a local Linux namespace lab.

The goal is not to memorize commands. It is to understand how packet headers change across a translation boundary.

## 1. Why NAT exists

Many local networks use private IPv4 address space such as:

- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

These addresses are not globally routed on the public Internet.

A simplified home-network model:

```text
Laptop
192.168.1.20
     |
     v
Router/NAT
192.168.1.1
Public IP: 203.0.113.10
     |
     v
Internet
```

The public address above is documentation-only.

## 2. NAT is address translation

NAT means Network Address Translation.

At a high level, a packet may begin as:

```text
SRC = 192.168.1.20
DST = 198.51.100.50
```

and leave the NAT device as:

```text
SRC = 203.0.113.10
DST = 198.51.100.50
```

The source address changed.

That is one form of source NAT.

## 3. SNAT and DNAT

### SNAT

Source NAT changes the source side.

Typical use:

```text
private client -> Internet
```

### DNAT

Destination NAT changes the destination side.

Typical use:

```text
public address:port
      ↓
internal service
```

Port forwarding is a common DNAT use case.

## 4. PAT / NAPT

Many devices do more than translate IP addresses.

They also translate transport-layer ports.

Example:

```text
192.168.1.20:51000
192.168.1.30:51000
       ↓
same public IP
       ↓
203.0.113.10:40001
203.0.113.10:40002
```

This allows many internal connections to share one public IPv4 address.

You may hear this called:

- PAT
- NAPT
- NAT overload

## 5. Translation table

A NAT device needs state so return traffic can be mapped back correctly.

Conceptually:

| Inside connection | Translated connection |
| --- | --- |
| 192.168.1.20:51000 | 203.0.113.10:40001 |
| 192.168.1.30:51000 | 203.0.113.10:40002 |

Return traffic to port 40001 can be mapped back to the first host.

This is why NAT and connection tracking are closely related.

## 6. NAT is not the same as a firewall

A common misconception:

> “NAT makes a network secure.”

NAT changes addressing.

A firewall enforces policy.

They are often implemented on the same device, but they solve different problems.

```text
NAT -> rewrite addressing/ports
Firewall -> allow/deny/log traffic
```

A network can use NAT with weak firewall policy, or strong firewall policy without traditional NAT.

## 7. Outbound flow example

Internal client:

```text
192.168.1.20:53000
```

connects to:

```text
198.51.100.25:443
```

Before translation:

```text
SRC 192.168.1.20:53000
DST 198.51.100.25:443
```

After PAT:

```text
SRC 203.0.113.10:41023
DST 198.51.100.25:443
```

Return packet:

```text
SRC 198.51.100.25:443
DST 203.0.113.10:41023
```

Translation state maps it back to:

```text
DST 192.168.1.20:53000
```

## 8. Port forwarding

Suppose an internal web server is:

```text
192.168.1.50:8080
```

A port-forwarding policy might map:

```text
203.0.113.10:8443
      ↓
192.168.1.50:8080
```

The destination changes as the packet enters.

This creates inbound reachability that would not otherwise exist.

## 9. Port forwarding needs firewall policy too

DNAT alone should not be confused with permission.

A complete design must ask:

- Is inbound traffic allowed?
- Which source networks are allowed?
- Which protocol?
- Which external port?
- Which internal destination?
- Should the event be logged?

Think:

```text
DNAT says where
Firewall says whether
```

## 10. Routing happens too

NAT does not replace routing.

The system still needs to know:

- which interface to send through,
- where the next hop is,
- whether IP forwarding is enabled,
- whether the destination network is reachable.

A useful troubleshooting order:

```text
interface
   ↓
address
   ↓
route
   ↓
forwarding
   ↓
firewall
   ↓
NAT
   ↓
application
```

## 11. Connection tracking recap

Day 7 introduced stateful filtering.

Connection tracking can maintain information such as:

- original source/destination,
- translated source/destination,
- protocol,
- connection state.

That makes NAT and stateful firewalling work together naturally.

On Linux, the same networking stack can use conntrack information for both filtering and NAT.

## 12. Packet capture before and after NAT

One of the best ways to understand NAT is to capture traffic on both sides of the translating system.

Conceptually:

### Internal side

```text
192.168.1.20 -> 198.51.100.25
```

### External side

```text
203.0.113.10 -> 198.51.100.25
```

The packet represents the same connection, but the visible source differs.

This matters in incident response because logs from different observation points may show different addresses/ports.

## 13. Why NAT complicates log correlation

Imagine:

- endpoint log sees `192.168.1.20:53000`,
- firewall log sees translated `203.0.113.10:41023`,
- remote server log sees only the translated public tuple.

To correlate them, you may need NAT/conntrack logs.

```text
internal tuple
    ↓
translation record
    ↓
external tuple
```

Without translation context, multiple internal hosts can appear to share one public IP.

## 14. Hairpin NAT concept

Sometimes an internal client tries to reach an internal service using the router's public address.

Example:

```text
internal client
     ↓
public address of router
     ↓
internal server
```

Some networks use hairpin/loopback NAT to support this.

It is useful to know the concept because behavior can differ between routers and environments.

## 15. Double NAT

A device may sit behind another NAT device.

Example:

```text
Host
192.168.1.20
   ↓
Home router
192.168.100.2
   ↓
ISP/router NAT
public IP
```

This can complicate:

- inbound port forwarding,
- peer-to-peer applications,
- troubleshooting,
- log attribution.

Carrier-grade NAT can create similar shared-address situations at ISP scale.

## 16. IPv6 note

IPv6 greatly reduces the need for address conservation through traditional many-to-one NAT.

But this does **not** mean:

> “IPv6 removes the need for firewalls.”

Address translation and traffic policy are separate concepts.

IPv6 hosts may have globally routable addresses while still relying on stateful firewall policy.

## 17. Local lab overview

This lab can be reproduced safely with Linux network namespaces.

We create:

```text
client namespace
       |
       | veth
       |
router namespace
       |
       | veth
       |
server namespace
```

Then the router namespace performs source NAT.

Everything remains local to your Linux machine.

## 18. Create namespaces

Run on a disposable Linux lab VM:

```bash
sudo ip netns add client
sudo ip netns add router
sudo ip netns add server
```

Create two veth pairs:

```bash
sudo ip link add veth-c type veth peer name veth-r1
sudo ip link add veth-r2 type veth peer name veth-s
```

Move interfaces:

```bash
sudo ip link set veth-c netns client
sudo ip link set veth-r1 netns router
sudo ip link set veth-r2 netns router
sudo ip link set veth-s netns server
```

## 19. Assign addresses

Client side:

```bash
sudo ip netns exec client ip addr add 10.10.1.2/24 dev veth-c
sudo ip netns exec client ip link set veth-c up
sudo ip netns exec client ip link set lo up
```

Router:

```bash
sudo ip netns exec router ip addr add 10.10.1.1/24 dev veth-r1
sudo ip netns exec router ip addr add 10.10.2.1/24 dev veth-r2
sudo ip netns exec router ip link set veth-r1 up
sudo ip netns exec router ip link set veth-r2 up
sudo ip netns exec router ip link set lo up
```

Server:

```bash
sudo ip netns exec server ip addr add 10.10.2.2/24 dev veth-s
sudo ip netns exec server ip link set veth-s up
sudo ip netns exec server ip link set lo up
```

## 20. Add routes

Client:

```bash
sudo ip netns exec client ip route add default via 10.10.1.1
```

Server:

```bash
sudo ip netns exec server ip route add default via 10.10.2.1
```

Enable forwarding inside router namespace:

```bash
sudo ip netns exec router sysctl -w net.ipv4.ip_forward=1
```

Before NAT, verify routing:

```bash
sudo ip netns exec client ping -c 2 10.10.2.2
```

## 21. Observe routed traffic first

Capture on router side:

```bash
sudo ip netns exec router tcpdump -n -i any icmp
```

Generate ping from client to server.

Observe:

```text
10.10.1.2 -> 10.10.2.2
```

At this stage, routing works but no NAT is necessary because both networks know how to return through the router.

## 22. Add a local SNAT rule

Inside the isolated router namespace, create a simple nftables NAT table:

```bash
sudo ip netns exec router nft add table ip nat
sudo ip netns exec router nft 'add chain ip nat postrouting { type nat hook postrouting priority srcnat; policy accept; }'
sudo ip netns exec router nft add rule ip nat postrouting oifname "veth-r2" ip saddr 10.10.1.0/24 snat to 10.10.2.1
```

Now traffic crossing toward the server network can appear to originate from the router's `10.10.2.1` address.

This is a safe local demonstration of source translation.

## 23. Capture the translation

Server-side capture:

```bash
sudo ip netns exec server tcpdump -n -i veth-s icmp
```

Generate:

```bash
sudo ip netns exec client ping -c 2 10.10.2.2
```

Compare what the client thinks it sent with what the server sees.

That difference is the core NAT lesson.

## 24. Inspect rules

Inside router namespace:

```bash
sudo ip netns exec router nft list ruleset
```

Translate the rule into plain language.

Do not memorize syntax only.

Explain:

- source network,
- outgoing interface,
- translated source.

## 25. Port forwarding concept lab

Start a local HTTP server in the server namespace:

```bash
sudo ip netns exec server python3 -m http.server 8080 --bind 10.10.2.2
```

A DNAT rule can conceptually map a router-facing port to the internal server.

For this course, first draw the expected transformation before writing any additional rule:

```text
client -> router-address:8000
              ↓ DNAT
         10.10.2.2:8080
```

Then identify which firewall/forwarding decisions would also be required.

The objective is reasoning, not copying production port-forwarding rules blindly.

## 26. Cleanup

When finished:

```bash
sudo ip netns del client
sudo ip netns del router
sudo ip netns del server
```

Deleting the namespaces removes the isolated lab interfaces/rules.

## 27. Troubleshooting NAT

If translation does not work, check:

1. interfaces are up,
2. addresses are correct,
3. routes exist,
4. forwarding is enabled,
5. firewall allows forwarding,
6. NAT rule matches the intended interface/network,
7. return traffic has a valid path,
8. service is actually listening.

Avoid starting with “NAT is broken.”

## 28. Mini challenge — explain one flow

For one connection, write four tuples:

```text
1. Client before NAT
2. Router after NAT
3. Server response
4. Router after reverse translation
```

Include:

- source IP,
- source port,
- destination IP,
- destination port.

This forces you to reason about both directions.

## 29. Mini challenge — design port forwarding

Scenario:

- external-facing router address: `10.10.1.1`
- internal server: `10.10.2.2:8080`
- desired exposed port: `8000`

Describe:

- DNAT transformation,
- required forwarding path,
- firewall decision,
- return traffic,
- logs you would want.

Do not use “NAT makes it secure” as part of the design.

## 30. Exercises

1. Explain private vs public IPv4.
2. Explain SNAT vs DNAT.
3. Explain NAT vs PAT.
4. Draw a translation table for two clients.
5. Explain why NAT and firewall are different.
6. Build the namespace topology.
7. Verify routing before NAT.
8. Add the isolated SNAT rule.
9. Capture traffic before/after translation.
10. Explain what the server sees.
11. Draw a port-forward flow.
12. Explain double NAT.
13. Explain why IPv6 still needs firewall policy.
14. Complete the four-tuple mini challenge.

## Questions

1. What problem does NAT solve?
2. What does SNAT change?
3. What does DNAT change?
4. What does PAT add?
5. Why does NAT need state?
6. Why is NAT not a firewall?
7. Why does routing still matter?
8. How can NAT complicate forensic log correlation?
9. What is port forwarding?
10. What is hairpin NAT?
11. What is double NAT?
12. Why does IPv6 not eliminate firewall needs?
13. Why should packet captures be taken on both sides of NAT?
14. What should you check before blaming NAT during troubleshooting?

## Main takeaway

```text
private flow
    ↓
routing
    ↓
connection tracking
    ↓
address/port translation
    ↓
firewall policy
    ↓
translated flow
    ↓
logs/captures may show different tuples
```

NAT becomes much easier when you stop thinking of it as “Internet magic” and instead follow the packet fields before and after translation.


> Türkçe çalışma notu: Bu günün ana hedefi NAT syntax ezberlemek değil. Her packet için **NAT öncesi source/destination neydi, NAT sonrası ne oldu ve return traffic nasıl geri eşleşti?** sorularını cevaplayabilmek.
