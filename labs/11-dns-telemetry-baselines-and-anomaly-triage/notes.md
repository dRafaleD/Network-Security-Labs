# Day 11 — DNS Telemetry, NXDOMAIN Baselines and Anomaly Triage

[English](notes.md) · [Türkçe](notes.tr.md)

**Goal:** combine Day 6 DNS fundamentals with Day 10 monitoring into a defensive DNS telemetry workflow.

**Safe scope:** No DNS requests are sent; IPs, names, and timestamps are synthetic.

## 1. DNS telemetry fields

A resolver log often records timestamp, client identity/address, queried name, record type and response code. Capture vantage point matters: recursive resolvers may observe many clients while an endpoint sees its own traffic.

## 2. NXDOMAIN and error rates

NXDOMAIN means the requested DNS name does not exist according to the resolver's response. Bursts can come from typos, misconfiguration, browser behavior, application retries or unwanted software. It is a triage signal, not a malware label.

## 3. Baselines need denominators

Compare NXDOMAIN count to total queries per client and time window. Ten failures out of 12 queries mean something different from ten failures out of 10,000. Daily workload and client roles change the expected baseline.

## 4. Burst detection

A moving window detects concentrated failures that daily totals can hide. In the lab, a two-minute window counts NXDOMAIN responses from one synthetic client. A burst should trigger contextual investigation, not automated attribution.

## 5. Periodicity and scheduled traffic

Evenly spaced requests sometimes look like beaconing. They can also be ordinary scheduled update or health-check traffic. Interval variance, host/process ownership and destination context matter before any judgement.

## 6. DNS cache and resolver scope

Caching means one application lookup may not create one upstream query. Resolver forwarding, shared networks and NAT can distort attribution. Do not infer one query equals one human action.

## 7. Encrypted DNS visibility

DoH and DoT encrypt DNS between client and chosen resolver. A passive sensor may see transport metadata while lacking query names; permitted endpoint/resolver logs can supply context. Never claim full DNS visibility from incomplete network data.

## 8. Privacy and minimization

DNS logs may reveal browsing habits or private application names. Limit retention, access and redistribution. Use the synthetic .example.test names supplied; never upload real user DNS logs into a public repo.

## 9. Triage and cross-source correlation

Validate sensor coverage and time zones. Join client address to DHCP leases and asset inventories only when available and authorized. Correlate DNS timestamps with proxy/network flow and endpoint activity; state observations versus hypotheses.

## 10. Explainable thresholds

Toy detection thresholds are designed for a small fabricated dataset. They must not be exported as production detections. Measure false positives against representative baselines and re-evaluate after software/network changes.

## Hands-on workflow

In the lab directory (Python 3 standard library):

```bash
python3 generate_dns_events.py
python3 analyze_dns_events.py
```

The generator writes timezone-aware JSON Lines records. The analyzer reports query count, NXDOMAIN ratio, and maximum NXDOMAIN volume within a two-minute window per synthetic client. It makes **no network calls**.

Expected groups:
- `10.10.0.10`: normal requests plus one typo.
- `10.10.0.20`: mostly successful requests.
- `10.10.0.30`: a rapid NXDOMAIN burst, requiring triage.
- `10.10.0.40`: deliberately benign periodic heartbeat events.

IP addresses here are fabricated labels, not live targets. The script does not label any event malicious.

### Connection to packet analysis

On your **own authorized local** DNS captures, the following Wireshark filters can help:

```text
dns
dns.flags.rcode == 3
udp.port == 53
```

These filters do not guarantee full DNS visibility; encrypted DNS, caches and sensor placement can hide relevant events.

### Mini challenges

1. Change the moving-window duration from two minutes to one; explain the change in detections.
2. Add a client with 100 successes and 3 failures; compare raw count to ratio.
3. Analyze the periodic `10.10.0.40` records and explain why scheduled traffic can resemble beaconing.
4. Draw a scenario where DHCP changes or NAT cause incorrect client attribution.

### Exercises

1. Inspect JSONL schema.
2. Identify UTC offsets.
3. Define NXDOMAIN.
4. Count events per client.
5. Calculate error ratios.
6. Explain sliding-window logic.
7. Find the largest burst.
8. Identify a false-positive scenario.
9. Discuss caching.
10. Discuss DoH visibility.
11. Plan DHCP and endpoint correlation.
12. Draft a short DNS triage report.

### Review questions

1. What is NXDOMAIN?
2. Where does DNS telemetry come from?
3. What can a recursive resolver observe?
4. What is a baseline?
5. Count versus ratio?
6. Why use a sliding window?
7. What creates false positives?
8. Why isn't periodicity a C2 verdict?
9. How does caching change telemetry?
10. How does NAT complicate attribution?
11. What does DoH hide?
12. Why preserve time zones?
13. Is one DNS log line one user action?
14. What other logs help triage?
15. How should production thresholds be validated?

**Takeaway:** Defensive DNS anomalies need a measured baseline, an understood sensor and corroborating evidence; a high NXDOMAIN count is not a verdict.
