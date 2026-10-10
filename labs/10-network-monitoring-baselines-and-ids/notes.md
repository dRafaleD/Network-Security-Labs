# Day 10 — Network Monitoring, Traffic Baselines, IDS/IPS and Alert Triage

[English](notes.md) · [Türkçe](notes.tr.md)

Goal: combine earlier TCP, DNS, firewall, NAT and TLS concepts in a defensive network-monitoring workflow.

**Prerequisites:** Days 3–9. **Scope:** localhost-only Python server and synthetic logs; no public network scanning.

## Detection pipeline / Tespit akışı

```text
local client -> TCP connection -> loopback HTTP service
                                   |
                     capture (tcpdump / Wireshark)
                                   |
                              service log
                                   |
                           baseline comparison
                                   |
                         triage + context checks
```

## 1. Passive capture vs active probing

Capture observes traffic at a point; probing generates new traffic. Use only loopback and authorized systems.

## 2. Baseline

A baseline is expected traffic over a defined period, service, workload and vantage point; do not call every deviation an attack.

## 3. IDS and IPS

IDS alerts on observed patterns or anomalies; IPS is inline and may block. Network taps and SPAN ports see only their observation scope.

## 4. Signature and anomaly detection

Signature-based detection looks for known patterns; anomaly-based detection compares against a learned/defined norm. Both can create false positives and misses.

## 5. Flows vs packets

Packet captures record detail; flows summarize endpoints, ports, protocol, timing and byte/packet counts, often with less payload context.

## 6. Five-tuple

A flow can be identified by source IP/port, destination IP/port and transport protocol, subject to observation and translation.

## 7. Monitoring encrypted traffic

TLS protects application content but IPs, ports, timing, sizes and some handshake metadata may still be visible; metadata alone is not proof.

## 8. Visibility gaps

Packet loss, offloading, capture filters, NAT, asymmetric paths and sensor placement can distort observations.

## 9. Alert triage

Validate time, sensor scope, affected asset and corroborating evidence before escalation. A single failed request is not an incident.

## 10. Detection quality

Track signal-to-noise, false positives, detection latency and meaningful coverage. Test on representative traffic.

## 11. Privacy

Prefer data minimization, access controls and retention limits for captures and logs; these may contain sensitive content.

## 12. Correlating evidence

Combine tcpdump/Wireshark with service logs, DNS and firewall decisions. State observation versus inference explicitly.

## Local lab / Yerel lab

Terminal 1, start harmless loopback-only service:

```bash
python3 local_service.py 2>access.log
```

Terminal 2, observe only lab TCP traffic (Linux loopback interface):

```bash
sudo tcpdump -n -i lo 'tcp port 8765'
```

Terminal 3, generate authorized, ordinary requests:

```bash
curl http://127.0.0.1:8765/
curl http://127.0.0.1:8765/hello
curl http://127.0.0.1:8765/missing
```

Use `Ctrl+C` to stop the server and capture. The sample log is intentionally deterministic, so the parser is reproducible even if the host logging format differs.

```bash
python3 summarize_access_log.py sample_access.log
```

Expected concept: 5 parsed requests; GET/200 = 4, GET/404 = 1. The URLs are synthetic and no alert should be inferred merely from the 404.

To save your own loopback capture for Wireshark, optionally run:

```bash
sudo tcpdump -n -i lo -s 0 -w day10-local.pcap 'tcp port 8765'
```

Stop capture with Ctrl+C before inspecting. PCAPs may contain application payloads, so do not commit arbitrary real-world captures.

### Wireshark display filters

```text
tcp.port == 8765
http
tcp.flags.syn == 1 && tcp.flags.ack == 0
tcp.analysis.retransmission
```

Local HTTP is plaintext for packet analysis. In contrast, Day 9 TLS traffic carries encrypted application data.

## Baseline worksheet / Baseline şablonu

| Metric | Baseline | Observation | Possible explanations |
| --- | --- | --- | --- |
| Requests | 5 synthetic log entries | Your capture/log count | Different workload or incomplete capture |
| Response status | Four 200, one 404 | Count by status | Missing path may be benign |
| Transport | Loopback TCP/8765 | SYN/ACK, connection closure | OS/tool differences |
| Sensor coverage | lo only | Which traffic is seen? | Other interfaces are not observed |

## Mini challenges / Mini görevler

1. Extend the parser to count requests by client IP and path. Explain what NAT could change in a real deployment.
2. Add a timestamp-window summary; keep source time zone and precision explicit.
3. Simulate 20 extra harmless requests to one endpoint. Identify the anomaly, then explain why elevated volume alone is not proof of an attack.
4. Compare PCAP packet evidence with service log entries, noting any missed/duplicated observations.

## Exercises / Alıştırmalar

1. Start/stop the service and capture.
2. Identify TCP handshake and request/response frames.
3. Explain why a loopback capture is limited.
4. Count status codes with the supplied parser.
5. Explain signature vs anomaly detection.
6. Compare IDS and IPS placement.
7. Describe flow five-tuples and NAT influence.
8. Create a simple request-rate baseline.
9. Identify packet-loss and sensor-placement limitations.
10. Draft an alert triage note distinguishing fact from inference.
11. Compare local HTTP with TLS visibility from Day 9.
12. Write a privacy-aware PCAP handling policy.

## Questions / Sorular

1. What is a traffic baseline? / Baseline nedir?
2. What makes an IDS different from an IPS? / IDS-IPS farkı?
3. What is a five-tuple? / Five-tuple nedir?
4. Why does sensor placement matter? / Sensor konumu niye önemli?
5. Can a 404 prove an attack? / 404 saldırı kanıtı mı?
6. What does TLS hide? / TLS neyi gizler?
7. Why can NAT alter log attribution? / NAT log attribution'ı nasıl etkiler?
8. What makes false positives costly? / False positive maliyeti?
9. How can logs corroborate a PCAP? / Log PCAP'ı nasıl destekler?
10. What should triage document? / Triage neleri kaydetmeli?

## Main takeaway / Ana çıkarım

**A useful network alert requires observation, baseline, context, and corroboration—not just a suspicious-looking packet.**
