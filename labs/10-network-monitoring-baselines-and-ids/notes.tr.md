# Gün 10 — Network Monitoring, Traffic Baseline, IDS/IPS ve Alert Triage

[English](notes.md) · [Türkçe](notes.tr.md)

Amaç: Önceki TCP, DNS, firewall, NAT ve TLS bilgilerini savunma amaçlı network monitoring workflow'unda birleştirmek.

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

## 1. Pasif capture ve aktif probing

Capture gözlem yapar, probing trafik oluşturur. Sadece loopback veya izinli ortamlarda uygula.

## 2. Baseline

Normal trafik, belirli zaman aralığı ve servis yükü için referanstır; her sapma saldırı değildir.

## 3. IDS ve IPS

IDS gözlemleyip alert üretebilir; IPS inline olup bloklayabilir. Sensor yalnız gördüğü trafiği değerlendirir.

## 4. Signature ve anomaly

Signature known pattern arar; anomaly beklenen davranıştan sapmayı inceler. İkisi de false positive ve false negative üretebilir.

## 5. Flow ve packet

PCAP packet detayını, flow ise IP/port/protocol/zaman/boyut özetini taşır; flow daha az payload detayı içerebilir.

## 6. Five-tuple

Source IP/port, destination IP/port ve transport protocol birlikte flow tanımlar; NAT gözlem noktasına göre değiştirebilir.

## 7. TLS visibility

TLS payload'ı korur ama IP/port/timing/boyut ve bazı handshake metadata gözlenebilir; bunlar tek başına maliciousness kanıtı değildir.

## 8. Gözlem boşlukları

Packet loss, offloading, filter, NAT, asymmetric routing ve sensor konumu çıkarımları etkiler.

## 9. Alert triage

Zaman, sensor scope, asset ve destekleyici logları doğrula. Bir 404 tek başına olay kanıtı değildir.

## 10. Detection quality

False positive, latency, coverage ve gürültü oranını ölç. Representative test trafiği kullan.

## 11. Privacy

PCAP/log içeriğini hassas kabul et; retention ve erişimi sınırla.

## 12. Evidence correlation

tcpdump/Wireshark, HTTP log, DNS ve firewall loglarını birleştir; observation ile inference'ı ayır.

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
