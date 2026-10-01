# Day 6 — DNS Deep Dive: Resolution, Records, Caching and Packet Analysis

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand what happens when a hostname is resolved and learn to read basic DNS traffic instead of treating DNS as a black box.

This lab covers resolver roles, record types, queries/responses, caching, DNS TTL, NXDOMAIN, UDP/TCP transport, packet capture, encrypted DNS concepts and defensive interpretation.

## 1. DNS mental model

Applications often use names such as `example.com`, while IP networks deliver packets to addresses.

A useful simplification is:

```text
hostname -> DNS resolution -> IP address -> network connection
```

DNS resolution and the later application connection are separate events. A successful DNS answer does not prove that a web server or another service is reachable.

## 2. Resolver roles

A simplified path is:

```text
Application
    ↓
Stub resolver on the host
    ↓
Recursive resolver
    ↓
DNS hierarchy / authoritative servers
    ↓
Answer
```

- **Stub resolver:** client-side resolver used by the OS/applications.
- **Recursive resolver:** obtains an answer for the client and commonly caches it.
- **Authoritative server:** provides authoritative data for a DNS zone.

A recursive resolver may already have a cached answer, so every lookup does not necessarily contact the full DNS hierarchy.

## 3. Recursive resolution

Conceptually, when no useful cache entry exists:

```text
client
  ↓
recursive resolver
  ↓
root information
  ↓
TLD information
  ↓
authoritative information
  ↓
answer
```

This is a learning model, not a claim that every query produces exactly this traffic.

## 4. Common record types

| Type | Typical purpose |
| --- | --- |
| A | IPv4 address |
| AAAA | IPv6 address |
| CNAME | Alias to another name |
| MX | Mail exchange information |
| NS | Name servers for a zone |
| TXT | Text used by many mechanisms |
| SOA | Zone authority/administrative information |
| PTR | Reverse lookup mapping |

One name can have multiple records and multiple addresses.

## 5. Query DNS

Try:

```bash
getent hosts example.com
```

If `dig` is installed:

```bash
dig example.com
dig A example.com
dig AAAA example.com
dig MX example.com
dig NS example.com
```

In `dig` output, learn to recognize QUESTION, ANSWER, AUTHORITY and ADDITIONAL sections.

A conceptual answer:

```text
example.com.   300   IN   A   192.0.2.10
```

can be read as:

```text
name          TTL   class type value
```

The address above is from a documentation range and is only an example.

## 6. DNS TTL vs IP TTL

DNS records commonly have a TTL that controls how long a cache may retain the record before refreshing it.

```text
first lookup -> obtain answer -> cache -> reuse -> TTL expires -> refresh
```

Do not confuse this with the IPv4 TTL from Day 4:

```text
DNS TTL -> cache lifetime
IP TTL  -> packet hop limit
```

The same abbreviation describes different concepts.

## 7. NXDOMAIN

A response can indicate that a queried name does not exist.

Use the reserved `.invalid` TLD for a harmless test:

```bash
dig definitely-not-a-real-lab-name.invalid
```

Learn the distinction:

```text
name does not exist
        !=
name resolves but service is unreachable
```

DNS failure is not automatically a routing failure.

## 8. DNS transport

Classic DNS commonly uses port 53. Many ordinary queries use UDP, but DNS is not UDP-only.

TCP can also be used, including cases where an exchange cannot be completed as the original UDP response or when an operation requires TCP.

So avoid the incorrect rule:

```text
DNS = always UDP
```

## 9. Capture your own lookup

Inspect resolver configuration:

```bash
cat /etc/resolv.conf
resolvectl status
```

Start a capture:

```bash
sudo tcpdump -n -i any 'port 53'
```

Then generate your own query:

```bash
dig example.com
```

or:

```bash
getent hosts example.com
```

Caching, a local resolver or encrypted DNS may mean you do not see the classic packet you expected. Treat that as an observation to investigate.

## 10. Wireshark filters

```text
dns
dns.flags.response == 0
dns.flags.response == 1
dns.qry.name == "example.com"
dns.flags.rcode != 0
```

Inspect:

- source/destination IP
- source/destination port
- transaction ID
- query name
- query type
- response code
- answer records
- TTL values

The DNS server commonly listens on port 53, while the client normally uses an ephemeral source port.

## 11. CNAME chains

A name may be an alias:

```text
app.example
     ↓ CNAME
service.example
     ↓ A / AAAA
IP address
```

During analysis, follow the chain instead of assuming the first name directly contains the final address.

## 12. Reverse DNS

PTR records are commonly used for reverse lookups.

Example using a documentation address:

```bash
dig -x 192.0.2.10
```

A reverse DNS name can be useful context, but it is not cryptographic proof of host identity.

## 13. Troubleshooting workflow

```text
network available?
      ↓
route exists?
      ↓
resolver configured/reachable?
      ↓
name resolves?
      ↓
returned IP reachable?
      ↓
application service works?
```

Useful commands:

```bash
ip route
cat /etc/resolv.conf
resolvectl status
getent hosts example.com
dig example.com
curl -I https://example.com
```

The final command tests more than DNS, so do not attribute its result only to DNS.

## 14. Encrypted DNS

Traditional DNS traffic may be visible on the network path. Modern systems may use encrypted mechanisms such as DNS over TLS (DoT) or DNS over HTTPS (DoH).

With encrypted DNS, a simple port-53 capture may not reveal the queried hostname. This changes what a network analyst can observe.

## 15. Defensive connection

DNS evidence can help investigate failed resolution, unexpected domains, repeated NXDOMAIN responses, unusual query volume and the network activity that follows resolution.

But:

```text
DNS query observed
      ↓
useful evidence
      ↓
not proof of malicious behavior
      ↓
correlate with process + connection + time + host telemetry
```

## Mini workflow

```text
identify name
    ↓
identify resolver
    ↓
inspect query type
    ↓
inspect response code
    ↓
follow CNAME/answers
    ↓
consider TTL/cache
    ↓
correlate with connection
    ↓
document limitations
```

## Exercises

1. Find your configured DNS resolver.
2. Resolve `example.com` with `getent`.
3. Request A and AAAA records with `dig`.
4. Explain DNS TTL vs IP TTL.
5. Query a reserved `.invalid` name and inspect the response.
6. Capture one of your own classic DNS lookups if visible.
7. Identify client and resolver ports.
8. Find the query name/type in Wireshark.
9. Follow a CNAME chain if your chosen legitimate domain returns one.
10. Explain why DNS success does not prove application success.

## Questions

1. What problem does DNS solve?
2. What does a recursive resolver do?
3. What does an authoritative server do?
4. A vs AAAA?
5. What does DNS TTL control?
6. How is it different from IP TTL?
7. What does NXDOMAIN mean?
8. Does DNS always use UDP?
9. Why might port-53 capture show nothing while resolution works?
10. Why should DNS evidence be correlated with other telemetry?

## Main takeaway

```text
name
 ↓
resolver
 ↓
query / response
 ↓
record + TTL + response code
 ↓
later network connection
 ↓
correlated defensive analysis
```
