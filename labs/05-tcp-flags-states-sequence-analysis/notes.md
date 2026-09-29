# Day 5 — TCP Deep Dive: Flags, States, Sequence Numbers and Retransmissions

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Move beyond “TCP is connection-oriented” and learn how a TCP connection actually behaves in packet captures.

This lab focuses on:

- TCP flags
- the three-way handshake
- sequence and acknowledgment numbers
- connection states
- graceful connection teardown
- RST packets
- retransmissions and packet loss
- Wireshark/Tcpdump analysis
- defensive interpretation

The goal is not to memorize every field. It is to learn how to reconstruct a connection from evidence.

## 1. TCP recap

TCP is a transport-layer protocol designed to provide an ordered, reliable byte stream between two endpoints.

A connection can be described by values such as:

```text
source IP
source port
destination IP
destination port
protocol
```

Together these identify a flow.

TCP reliability does not mean the network never loses packets. TCP detects missing data and can retransmit it.

## 2. Important TCP flags

Common flags:

| Flag | Beginner meaning |
| --- | --- |
| SYN | Start/synchronize a connection |
| ACK | Acknowledge received data/state |
| FIN | Gracefully finish one direction of a connection |
| RST | Reset/abort a connection |
| PSH | Ask for received data to be delivered promptly to the application |
| URG | Indicates urgent-pointer semantics; uncommon in normal modern traffic |

Flags can appear together. For example, the server's handshake response normally contains SYN and ACK.

## 3. Three-way handshake

A normal TCP connection begins conceptually like this:

```text
Client                         Server
  |                              |
  | -------- SYN --------------> |
  | <----- SYN, ACK ------------ |
  | -------- ACK --------------> |
  |                              |
  |        ESTABLISHED           |
```

Why three steps?

1. Client announces an initial sequence number.
2. Server acknowledges it and announces its own.
3. Client acknowledges the server.

After that, both sides have synchronized connection state.

## 4. Sequence numbers

TCP does not simply number packets. It tracks positions in a byte stream.

Conceptually:

```text
SEQ = where my data begins
ACK = next byte I expect from you
```

If a segment carries 100 bytes beginning at sequence 1000, the receiver may acknowledge 1100.

Wireshark often displays **relative sequence numbers** to make analysis easier. Therefore values may begin around 0 or 1 even though the actual TCP values are larger.

## 5. ACK does not mean “the whole application succeeded”

An ACK tells you about TCP-level receipt/state.

It does not automatically prove that:

- an HTTP request was accepted by the application,
- a login succeeded,
- a database transaction completed,
- the user saw the expected result.

Keep layers separate:

```text
TCP success != application success
```

## 6. TCP connection states

Useful states you may see with `ss`:

- `LISTEN` — waiting for incoming connections
- `SYN-SENT` — SYN sent, waiting for response
- `SYN-RECV` — SYN received, handshake not complete
- `ESTAB` / `ESTABLISHED` — connection established
- `FIN-WAIT-1` / `FIN-WAIT-2` — local side is closing
- `CLOSE-WAIT` — peer closed; local application still needs to close
- `LAST-ACK` — waiting for final acknowledgment during close
- `TIME-WAIT` — recently closed connection retained temporarily
- `CLOSED` — no connection state

You do not need to memorize the entire TCP state machine today. Learn to recognize the common states and what question each one answers.

## 7. Graceful teardown

TCP is full-duplex: each direction can close independently.

A simplified close can look like:

```text
Client                         Server
  | -------- FIN -------------> |
  | <------- ACK -------------- |
  | <------- FIN -------------- |
  | -------- ACK -------------> |
```

Real captures may combine or reorder some visible behavior depending on timing.

## 8. Why TIME-WAIT exists

The endpoint that actively closes a TCP connection may remain in `TIME-WAIT` for a period.

This helps:

- prevent delayed packets from an old connection being confused with a new one,
- allow the final ACK to be retransmitted if necessary.

Seeing TIME-WAIT is therefore not automatically an error.

## 9. RST

RST means the connection is being reset rather than gracefully closed.

A harmless local example is connecting to a TCP port where nothing is listening:

```bash
nc -v 127.0.0.1 65000
```

Depending on the OS/tool, the connection is normally refused and a local capture may show a reset.

A reset can have many causes. Do not infer malicious activity from RST alone.

## 10. Local handshake lab

Terminal 1 — start a local HTTP server:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Terminal 2 — capture only the local TCP traffic:

```bash
sudo tcpdump -n -i lo 'tcp port 8000'
```

Terminal 3:

```bash
curl http://127.0.0.1:8000/
```

Look for:

1. SYN
2. SYN/ACK
3. ACK
4. HTTP data carried over TCP
5. ACKs
6. connection close

Because everything stays on loopback, this is a safe and reproducible exercise.

## 11. Inspect connection state

While the server is running:

```bash
ss -ltn
```

Look for port 8000.

You can also use:

```bash
ss -tn
```

during an active connection.

Ask:

- Which endpoint is listening?
- Which port is the server port?
- Which side uses an ephemeral client port?

## 12. Wireshark filters

Useful display filters:

```text
tcp
tcp.port == 8000
tcp.flags.syn == 1
tcp.flags.reset == 1
tcp.analysis.retransmission
tcp.analysis.fast_retransmission
tcp.analysis.duplicate_ack
```

For a selected TCP packet, inspect:

- source/destination
- source/destination port
- flags
- sequence number
- acknowledgment number
- TCP payload length
- window size

## 13. Follow TCP Stream

Wireshark's **Follow TCP Stream** groups application bytes belonging to one TCP conversation.

For the local HTTP lab, it can help you see the request and response as a conversation rather than isolated packets.

Important: this is a reconstruction aid. Always return to the packet list when timing, flags, retransmissions, or packet-level behavior matters.

## 14. Retransmission

If a sender does not receive the expected acknowledgment, data may be sent again.

Conceptually:

```text
sender ---- segment A ----> receiver
             X lost

sender ---- segment A ----> receiver
          retransmission
```

Possible reasons include:

- packet loss
- congestion
- overloaded systems
- wireless interference
- routing problems
- capture artifacts

A retransmission is evidence of TCP recovery behavior, not proof of one specific root cause.

## 15. Duplicate ACKs

A receiver can acknowledge the same expected sequence position repeatedly when later data arrives but an earlier part is missing.

Multiple duplicate ACKs can be one clue that data was lost or arrived out of order.

Again, interpretation needs context.

## 16. Capture limitations

The capture point matters.

For example, checksum offloading can make locally captured outgoing packets appear to have invalid checksums even though the NIC later calculates them correctly.

Similarly, a capture on one endpoint may not show exactly what another device on the path observed.

A packet capture is evidence from a particular observation point.

## 17. Defensive security connection

TCP analysis helps defenders investigate:

- service availability problems
- refused connections
- unexpected resets
- packet loss
- unusual connection patterns
- incomplete handshakes
- scanning-like behavior
- overloaded services

For example, many SYN packets do not by themselves prove an attack. Context, rate, source distribution, server state and other telemetry matter.

## 18. Mini investigation workflow

```text
identify flow
    ↓
find handshake
    ↓
check flags
    ↓
follow seq/ack progression
    ↓
inspect application data
    ↓
look for retransmissions/resets
    ↓
inspect teardown
    ↓
correlate with host/service evidence
```

## Exercises

1. Start the local HTTP server.
2. Capture one `curl` request.
3. Identify SYN, SYN/ACK and ACK.
4. Write down client and server ports.
5. Find the first packet containing application data.
6. Follow the TCP stream.
7. Identify how the connection closes.
8. Run `ss -ltn` and find the listening socket.
9. Try the unused local port example and look for RST.
10. Explain why a retransmission alone does not identify the root cause.

## Questions

1. What is the purpose of SYN?
2. What does an ACK number conceptually represent?
3. Why does TCP use sequence numbers?
4. What is the difference between FIN and RST?
5. Why can TIME-WAIT be normal?
6. What is a retransmission?
7. What can duplicate ACKs suggest?
8. Does TCP ACK prove the application completed its task?
9. Why does the packet-capture location matter?
10. Why should unusual SYN traffic be interpreted with context?

## Main takeaway

```text
flags + states + sequence numbers
             ↓
      reconstruct connection
             ↓
 retransmissions / resets / close
             ↓
       explain observations
             ↓
 defensive network analysis
```
