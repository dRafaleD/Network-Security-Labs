# Day 9 — TLS, Certificates, SNI, ALPN and HTTPS Packet Analysis

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand what TLS adds on top of TCP, how certificates help authenticate servers, what remains visible on the network, and how tools such as OpenSSL, curl, tcpdump and Wireshark can be used to inspect an authorized local HTTPS connection.

This day combines:

1. TCP vs TLS vs HTTP,
2. TLS handshake,
3. certificates and trust chains,
4. hostname validation,
5. SNI,
6. ALPN,
7. session keys and encrypted payloads,
8. what metadata remains visible,
9. local certificate generation,
10. local HTTPS server/client testing,
11. packet capture,
12. troubleshooting certificate errors.

## 1. Where TLS fits

A simplified HTTPS stack:

~~~text
HTTP
  ↓
TLS
  ↓
TCP
  ↓
IP
  ↓
Ethernet / Wi-Fi
~~~

TCP gives reliable transport.

TLS adds confidentiality, integrity and peer authentication capabilities.

HTTP still exists above TLS, but its application payload is encrypted on the wire.

## 2. HTTPS is not a separate transport protocol

HTTPS is HTTP carried over TLS.

Conceptually:

~~~text
HTTP request
   ↓
TLS encrypts application data
   ↓
TCP transports encrypted records
~~~

This distinction matters in packet analysis.

You may see TCP clearly while the HTTP content itself is unreadable.

## 3. What TLS protects

TLS is designed to provide:

### Confidentiality
Observers should not read protected application payloads.

### Integrity
Tampering should be detected.

### Authentication
The client can validate the server identity using certificates and trust rules.

TLS does not automatically guarantee the application itself is secure.

## 4. TLS handshake

A simplified modern handshake:

~~~text
ClientHello
    ↓
ServerHello
    ↓
certificate / key agreement information
    ↓
handshake verification
    ↓
encrypted application data
~~~

Exact messages depend on TLS version and configuration.

TLS 1.3 differs from older versions, so avoid memorizing one fixed sequence as universal.

## 5. ClientHello

ClientHello may contain information such as:

- supported TLS versions,
- cipher-suite options,
- random/key-share data,
- SNI,
- ALPN proposals.

This happens before encrypted application data begins.

## 6. ServerHello

The server chooses parameters compatible with the client.

Conceptually:

~~~text
client offers possibilities
        ↓
server chooses compatible set
~~~

TLS version and cipher details can be inspected with OpenSSL/Wireshark.

## 7. Certificates

A server certificate contains identity and public-key information.

It may include:

- subject,
- issuer,
- validity period,
- public key,
- SAN entries,
- signature.

A certificate is not just “encryption.”

Its major purpose is binding a public key to an identity under a trust model.

## 8. Certificate chain

Typical model:

~~~text
server certificate
      ↓ signed by
intermediate CA
      ↓ signed by
root CA
~~~

The client trusts a root store and attempts to build/validate a chain.

A certificate can be mathematically valid but still untrusted if the chain does not lead to a trusted root.

## 9. Self-signed certificate

In this lab, you create your own self-signed certificate.

That is useful for local training.

Browsers/curl will not trust it automatically because it is not anchored in their normal trusted CA store.

That is expected.

## 10. Hostname validation

Even if a certificate is signed by a trusted CA, the hostname must match the certificate identity.

Modern validation usually relies on Subject Alternative Name entries.

Conceptually:

~~~text
requested host
     ↓
certificate names
     ↓
match?
~~~

A valid chain with the wrong hostname should still fail hostname verification.

## 11. SNI

SNI means Server Name Indication.

A client can indicate the hostname it wants during the TLS handshake.

Why useful?

One IP address may host multiple HTTPS sites.

~~~text
same IP
  ├─ site-a.example
  └─ site-b.example
~~~

SNI helps the server choose the appropriate certificate/configuration.

## 12. SNI visibility

Traditionally, SNI can be visible to passive network observers because it appears in the ClientHello.

This means TLS encrypts application content, but not necessarily all metadata.

Newer technologies such as Encrypted ClientHello aim to reduce that exposure, but deployment varies.

## 13. ALPN

ALPN means Application-Layer Protocol Negotiation.

It allows client/server to negotiate application protocols such as:

~~~text
http/1.1
h2
~~~

within the TLS handshake.

For HTTPS analysis, this can explain whether HTTP/1.1 or HTTP/2 is selected.

## 14. Cipher suite concept

A cipher suite/configuration describes cryptographic choices.

You do not need to memorize every name now.

Focus on:

- protocol version,
- key agreement,
- authenticated encryption,
- server authentication.

Modern TLS stacks negotiate secure options automatically when correctly configured.

## 15. Generate a local certificate

On a local Linux lab machine:

~~~bash
mkdir -p tls-lab
cd tls-lab
~~~

Generate a self-signed certificate with localhost SAN:

~~~bash
openssl req -x509 -newkey rsa:2048 -nodes   -keyout key.pem   -out cert.pem   -days 2   -subj "/CN=localhost"   -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
~~~

This certificate is only for the local lab.

## 16. Inspect the certificate

~~~bash
openssl x509 -in cert.pem -text -noout
~~~

Find:

- issuer,
- subject,
- validity,
- public key,
- SAN.

Also inspect fingerprint:

~~~bash
openssl x509 -in cert.pem -noout -sha256 -fingerprint
~~~

## 17. Start a local TLS server

Use OpenSSL:

~~~bash
openssl s_server -accept 8443 -cert cert.pem -key key.pem -www
~~~

This starts a simple local TLS service.

Do not expose the port beyond your lab environment unless you intend to.

## 18. Connect with OpenSSL

Another terminal:

~~~bash
openssl s_client -connect 127.0.0.1:8443 -servername localhost
~~~

Inspect:

- certificate chain,
- negotiated TLS version,
- cipher,
- verification result.

Because the certificate is self-signed, normal verification should complain unless you explicitly trust that local certificate.

## 19. Verify with the lab certificate

Use:

~~~bash
openssl s_client   -connect 127.0.0.1:8443   -servername localhost   -CAfile cert.pem
~~~

Now your local certificate acts as the explicit trust anchor for this test.

This does not install it system-wide.

## 20. curl

Try:

~~~bash
curl https://localhost:8443/
~~~

Normal trust validation should reject the self-signed certificate.

For the lab, explicitly trust it:

~~~bash
curl --cacert cert.pem https://localhost:8443/
~~~

Avoid using insecure certificate-bypass options as your normal solution.

The better lesson is to understand why verification failed and provide the correct trust material.

## 21. Certificate error taxonomy

Common causes:

- untrusted issuer,
- expired certificate,
- not-yet-valid certificate,
- hostname mismatch,
- incomplete chain,
- revoked certificate in systems that check revocation.

Do not collapse every TLS error into “certificate broken.”

## 22. Packet capture

Capture only the local test port:

~~~bash
sudo tcpdump -n -i lo 'tcp port 8443'
~~~

Then connect again.

You should observe:

- TCP handshake,
- TLS packets/records,
- encrypted application traffic,
- TCP close.

The HTTP content is not visible as plaintext in a normal passive capture.

## 23. Wireshark filters

Useful display filters for the local lab:

~~~text
tcp.port == 8443
tls
tls.handshake
~~~

Exact decoded fields depend on Wireshark version and TLS version.

Inspect the handshake before focusing on encrypted data.

## 24. What remains visible?

Even with TLS, observers may still infer metadata such as:

- IP addresses,
- TCP ports,
- timing,
- packet sizes,
- connection duration,
- traditionally SNI,
- TLS fingerprints/parameters.

Encryption protects content, not all metadata.

## 25. Encrypted payload does not mean invisible connection

A common misconception:

> “HTTPS means nobody can see anything.”

More accurate:

~~~text
content confidentiality improves
but
network-level metadata still exists
~~~

This matters for defensive monitoring.

## 26. TLS and DNS

Before connecting to a hostname, DNS resolution may occur.

A typical sequence:

~~~text
DNS lookup
   ↓
TCP connection
   ↓
TLS handshake
   ↓
HTTP request
~~~

If DNS itself is plaintext, the hostname may already be visible before TLS.

DoH/DoT changes where/how DNS is protected, but not the basic need for name resolution.

## 27. TLS and proxies

In enterprise environments, approved TLS inspection proxies may terminate and re-establish TLS using organization-managed trust.

That changes the trust boundary.

This should be authorized, documented and understood because the proxy can see decrypted application content.

## 28. TLS fingerprints

Network defenders can sometimes use handshake characteristics as one signal.

Examples conceptually include:

- offered cipher suites,
- extensions,
- TLS version,
- ordering patterns.

A fingerprint is context, not proof of maliciousness.

Different software versions/configurations can share or change fingerprints.

## 29. Session resumption

TLS can reuse prior session state to reduce handshake work.

This means not every connection looks identical.

Do not assume every HTTPS connection must show the same full handshake sequence.

## 30. Mini challenge — explain the layers

For one curl request, write:

~~~text
DNS:
TCP:
TLS:
HTTP:
~~~

For each layer, explain what it contributes.

## 31. Mini challenge — hostname mismatch

Generate another local certificate that does not include localhost in SAN.

Connect to localhost and observe the verification problem.

Do not disable verification to “fix” it.

Explain why the hostname check exists.

## 32. Mini challenge — capture analysis

Capture one successful local HTTPS request.

Identify:

1. TCP three-way handshake,
2. ClientHello,
3. ServerHello,
4. certificate-related handshake data,
5. encrypted application data,
6. TCP teardown.

Write packet/frame numbers from your own capture.

## 33. Troubleshooting checklist

~~~text
1. Does DNS resolve?
2. Can TCP connect?
3. Is the correct port used?
4. Does TLS handshake start?
5. Which TLS version is negotiated?
6. Is the certificate trusted?
7. Does hostname match?
8. Is the chain complete?
9. Which ALPN protocol is selected?
10. Does application data follow?
~~~

## Exercises

1. Generate the local certificate.
2. Inspect SAN and validity.
3. Start s_server.
4. Connect with s_client.
5. Observe self-signed verification failure.
6. Retry with CAfile.
7. Test with curl --cacert.
8. Capture traffic with tcpdump.
9. Inspect with Wireshark.
10. Identify SNI.
11. Identify ALPN if present.
12. Explain visible vs encrypted fields.
13. Perform hostname-mismatch challenge.
14. Complete the layer explanation.

## Questions

1. What does TLS add above TCP?
2. Is HTTPS a new transport protocol?
3. What does a certificate authenticate?
4. What is a certificate chain?
5. Why is a self-signed cert not trusted automatically?
6. What is hostname validation?
7. What is SNI?
8. What is ALPN?
9. What network metadata remains visible under TLS?
10. Why can curl reject a working TLS server?
11. Why should certificate bypass not be the default fix?
12. How does TLS connect to DNS and TCP analysis?
13. What is session resumption?
14. Why is a TLS fingerprint only one signal?

## Main takeaway

~~~text
DNS
  ↓
TCP
  ↓
TLS handshake
  ↓
certificate / identity verification
  ↓
encrypted application data
  ↓
metadata remains observable
~~~

TLS packet analysis is about understanding both what encryption hides and what the network still reveals.
