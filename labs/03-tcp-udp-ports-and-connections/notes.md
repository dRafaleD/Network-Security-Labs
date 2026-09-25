# Day 3 — TCP, UDP, Ports and Connection Analysis

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand how TCP and UDP carry application traffic, what ports represent, how a TCP connection is established and closed, and how to recognize these behaviors in packet captures.

## 1. Transport layer

After IP gets a packet toward the correct host, the transport layer helps deliver data to the correct application.

Two protocols appear constantly:

- **TCP** — connection-oriented and reliable byte stream.
- **UDP** — connectionless datagrams with lower protocol overhead.

Neither is universally "better". Applications choose based on their requirements.

## 2. Ports

A port is a transport-layer number used to distinguish services/processes communicating through an IP address.

Examples commonly associated with services:

| Port | Typical service |
| ---: | --- |
| 22/TCP | SSH |
| 53/UDP or TCP | DNS |
| 80/TCP | HTTP |
| 443/TCP | HTTPS |

A port number alone does not prove which application is actually running there.

Inspect listening sockets on Linux:

```bash
ss -tuln
```

Useful flags:

```text
-t -> TCP
-u -> UDP
-l -> listening
-n -> numeric addresses/ports
```

## 3. TCP three-way handshake

A simplified TCP connection begins:

```text
Client                         Server
  | ------ SYN ----------------> |
  | <----- SYN, ACK ------------ |
  | ------ ACK ----------------> |
```

After this, application data can flow.

Important TCP flags to recognize:

```text
SYN -> start/synchronize connection
ACK -> acknowledge data/state
FIN -> orderly connection close
RST -> reset connection
```

## 4. Sequence and acknowledgement numbers

TCP tracks the byte stream with sequence numbers and confirms received data with acknowledgement numbers.

You do not need to memorize every number. At this stage, recognize the idea:

```text
send bytes
   ↓
receiver acknowledges progress
   ↓
missing data can be retransmitted
```

This reliability behavior is one major difference from UDP.

## 5. TCP capture lab

Start a harmless local web server:

```bash
python3 -m http.server 8000
```

Capture loopback TCP traffic:

```bash
sudo tcpdump -n -i lo tcp port 8000
```

In another terminal:

```bash
curl http://127.0.0.1:8000/
```

Try to identify:

1. SYN
2. SYN-ACK
3. ACK
4. application data
5. connection termination

Because everything stays on localhost, this is a controlled practice environment.

## 6. Wireshark filters

Useful display filters:

```text
tcp
tcp.port == 8000
tcp.flags.syn == 1
tcp.flags.reset == 1
```

Select a packet and expand the TCP section.

Observe:

- source port
- destination port
- flags
- sequence number
- acknowledgement number

## 7. Client ports and server ports

When connecting to a local server, you may see:

```text
127.0.0.1:53422 -> 127.0.0.1:8000
```

The server is listening on port 8000 while the client normally uses a temporary source port.

A flow can be identified conceptually using:

```text
source IP
source port
destination IP
destination port
transport protocol
```

This combination is often called a five-tuple.

## 8. UDP

UDP does not perform a TCP-style three-way handshake.

Conceptually:

```text
Host A ---- datagram ----> Host B
```

The protocol itself does not establish a reliable byte stream or guarantee retransmission and ordering in the same way TCP does.

Applications can implement their own reliability behavior when needed.

Inspect UDP sockets:

```bash
ss -uln
```

## 9. TCP vs UDP

| Property | TCP | UDP |
| --- | --- | --- |
| Connection setup | Yes | No TCP-style handshake |
| Reliable ordered stream | Yes | Not provided by UDP itself |
| Retransmission | TCP provides it | Application-dependent |
| Data model | Byte stream | Datagram |
| Typical uses | Web, SSH | DNS, streaming/real-time protocols |

Modern protocols can complicate simple examples—for instance HTTP/3 uses QUIC over UDP—so protocol identification should come from evidence rather than assumptions.

## 10. Connection states

Run:

```bash
ss -tan
```

You may encounter states such as:

```text
LISTEN
ESTAB
TIME-WAIT
SYN-SENT
SYN-RECV
```

These states describe where a TCP socket is in its connection lifecycle.

## 11. Security connection

Transport-layer visibility is useful for defensive analysis.

A packet capture or connection table can help answer:

- Which host initiated the connection?
- Which destination port was contacted?
- Was a TCP handshake completed?
- Was the connection reset?
- Are repeated connection attempts occurring?
- Which services are listening locally?

A listening port is not automatically a vulnerability. It is an exposed communication endpoint that must be interpreted together with the service, configuration and network access.

## 12. Mini exercises

### A — Local sockets

Run:

```bash
ss -tuln
```

Record three entries if available and classify them as TCP or UDP.

### B — Handshake

Capture the localhost HTTP connection and locate SYN, SYN-ACK and ACK.

### C — Five-tuple

Choose one TCP connection from your capture and write its five-tuple.

### D — Connection lifecycle

Run:

```bash
ss -tan
```

while repeatedly requesting your local server. Observe whether states change.

## Questions

1. What problem do ports solve?
2. Why does a TCP connection use a handshake?
3. What are SYN and ACK used for?
4. How does UDP differ from TCP?
5. What is an ephemeral/client source port?
6. What five values form a five-tuple?
7. Does an open/listening port automatically mean a vulnerability?
8. Why might packet captures show retransmissions or resets?

## Main takeaway

Think of communication as multiple layers working together:

```text
application
    ↓
TCP/UDP + ports
    ↓
IP + routing
    ↓
local link delivery
```

Being able to identify a flow, its direction and its TCP state is a core skill for later firewall, IDS/IPS and packet-analysis labs.
