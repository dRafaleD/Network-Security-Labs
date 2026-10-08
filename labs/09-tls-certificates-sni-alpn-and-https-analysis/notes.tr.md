# Gün 9 — TLS, Certificate, SNI, ALPN ve HTTPS Paket Analizi

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

TLS'in TCP üzerine ne eklediğini, certificate'ın server identity doğrulamasındaki rolünü, network üzerinde nelerin görünür kalabildiğini ve OpenSSL/curl/tcpdump/Wireshark ile tamamen local HTTPS bağlantısını analiz etmeyi öğrenmek.

Bu gün:

- TCP vs TLS vs HTTP,
- TLS handshake,
- certificate chain,
- hostname validation,
- SNI,
- ALPN,
- encryption,
- network metadata,
- local certificate,
- packet capture,
- TLS troubleshooting

konularını birlikte işler.

## 1. TLS hangi katmanda?

~~~text
HTTP
  ↓
TLS
  ↓
TCP
  ↓
IP
~~~

TCP reliable transport sağlar.

TLS confidentiality, integrity ve authentication sağlar.

## 2. HTTPS nedir?

HTTPS, TLS üzerinden taşınan HTTP'dir.

~~~text
HTTP request
  ↓
TLS encryption
  ↓
TCP
~~~

TCP görünür olabilir ama HTTP payload plaintext görünmez.

## 3. TLS ne sağlar?

Confidentiality: content okunmasını zorlaştırır.

Integrity: tampering detect edilir.

Authentication: client server identity'yi certificate/trust ile doğrulayabilir.

TLS application'ın kendisini otomatik güvenli yapmaz.

## 4. Handshake

Simplified:

~~~text
ClientHello
  ↓
ServerHello
  ↓
certificate / key agreement
  ↓
verification
  ↓
encrypted application data
~~~

TLS version'a göre sequence değişebilir.

## 5. ClientHello

Şunları içerebilir:

- TLS version seçenekleri,
- cipher seçenekleri,
- key-share/random data,
- SNI,
- ALPN.

## 6. Certificate

Certificate:

- subject,
- issuer,
- validity,
- public key,
- SAN,
- signature

gibi bilgi içerir.

Asıl amaçlardan biri public key'i identity ile bağlamaktır.

## 7. Chain

~~~text
server cert
   ↓
intermediate CA
   ↓
root CA
~~~

Client trusted root store üzerinden chain validate eder.

## 8. Self-signed

Bu lab self-signed cert üretir.

Local eğitim için uygundur ama normal browser/curl bunu default trusted saymaz.

Bu beklenen davranıştır.

## 9. Hostname validation

Requested hostname certificate SAN ile uyumlu olmalıdır.

Trusted chain + wrong hostname yine failure olabilir.

## 10. SNI

SNI client'ın istediği hostname'i handshake sırasında server'a bildirmesine yardımcı olur.

Bir IP'de birden fazla HTTPS site olabilir.

SNI geleneksel TLS'te passive observer tarafından görülebilir.

## 11. ALPN

ALPN application protocol negotiation içindir.

Örnek:

~~~text
http/1.1
h2
~~~

## 12. Local certificate

~~~bash
mkdir -p tls-lab
cd tls-lab

openssl req -x509 -newkey rsa:2048 -nodes   -keyout key.pem   -out cert.pem   -days 2   -subj "/CN=localhost"   -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
~~~

Sadece local lab için kullan.

## 13. Certificate inspect

~~~bash
openssl x509 -in cert.pem -text -noout
openssl x509 -in cert.pem -noout -sha256 -fingerprint
~~~

Issuer, subject, validity, SAN ve fingerprint bul.

## 14. Local TLS server

~~~bash
openssl s_server -accept 8443 -cert cert.pem -key key.pem -www
~~~

## 15. s_client

~~~bash
openssl s_client -connect 127.0.0.1:8443 -servername localhost
~~~

TLS version, cipher, certificate ve verification result incele.

Explicit local trust:

~~~bash
openssl s_client   -connect 127.0.0.1:8443   -servername localhost   -CAfile cert.pem
~~~

## 16. curl

~~~bash
curl https://localhost:8443/
~~~

Self-signed yüzünden fail etmesi normaldir.

Lab cert'ini explicitly trust et:

~~~bash
curl --cacert cert.pem https://localhost:8443/
~~~

Default çözüm olarak certificate verification bypass etme.

## 17. Certificate error

Common nedenler:

- untrusted issuer,
- expired,
- not-yet-valid,
- hostname mismatch,
- incomplete chain.

Her error'u “cert bozuk” diye genelleme.

## 18. Packet capture

~~~bash
sudo tcpdump -n -i lo 'tcp port 8443'
~~~

Sonra tekrar connect et.

Görmen gereken concept:

- TCP handshake,
- TLS handshake/records,
- encrypted app traffic,
- close.

## 19. Wireshark

Filter:

~~~text
tcp.port == 8443
tls
tls.handshake
~~~

ClientHello / ServerHello / certificate data / encrypted application data ayır.

## 20. Ne görünür kalır?

TLS altında bile:

- IP,
- port,
- timing,
- packet size,
- duration,
- bazı handshake metadata,
- traditional SNI

gibi bilgi gözlenebilir.

~~~text
encrypted content != invisible connection
~~~

## 21. DNS bağlantısı

~~~text
DNS
  ↓
TCP
  ↓
TLS
  ↓
HTTP
~~~

Hostname DNS sırasında zaten görünür olabilir.

DoH/DoT bu kısmı farklı şekilde korur.

## 22. TLS inspection proxy

Authorized enterprise proxy TLS terminate/re-establish edebilir.

Bu trust boundary'yi değiştirir ve proxy plaintext application content görebilir.

## 23. Fingerprinting

Handshake property'leri defensive signal olabilir.

Ama fingerprint tek başına maliciousness kanıtı değildir.

## 24. Session resumption

Bazı connection'lar prior state reuse eder.

Her TLS connection'ın aynı full handshake'i göstermesini bekleme.

## 25. Mini challenge — layers

Bir curl request için:

~~~text
DNS:
TCP:
TLS:
HTTP:
~~~

her katmanın görevini yaz.

## 26. Mini challenge — hostname mismatch

localhost SAN içermeyen başka local cert üret.

Verification failure'ı gözlemle.

Bypass etmek yerine neden fail olduğunu açıkla.

## 27. Mini challenge — capture

Kendi capture'ında:

1. TCP handshake,
2. ClientHello,
3. ServerHello,
4. certificate handshake,
5. encrypted data,
6. teardown

frame number'larını yaz.

## 28. Troubleshooting

~~~text
1. DNS?
2. TCP connect?
3. Port?
4. TLS başladı mı?
5. TLS version?
6. Cert trusted?
7. Hostname match?
8. Chain complete?
9. ALPN?
10. App data?
~~~

## Alıştırmalar

1. Local cert üret.
2. SAN/validity incele.
3. s_server başlat.
4. s_client connect.
5. Verification failure gözlemle.
6. CAfile ile doğrula.
7. curl --cacert kullan.
8. tcpdump capture.
9. Wireshark inspect.
10. SNI bul.
11. ALPN varsa bul.
12. Visible/encrypted field ayır.
13. Hostname mismatch challenge yap.
14. Layer explanation tamamla.

## Sorular

1. TLS TCP üzerine ne ekler?
2. HTTPS yeni transport protocol mü?
3. Certificate neyi authenticate eder?
4. Chain nedir?
5. Self-signed neden default trusted değil?
6. Hostname validation nedir?
7. SNI nedir?
8. ALPN nedir?
9. TLS altında hangi metadata kalır?
10. curl neden working server'ı reject edebilir?
11. Verification bypass neden default çözüm değil?
12. TLS DNS/TCP ile nasıl bağlanır?
13. Session resumption nedir?
14. Fingerprint neden sadece bir signal'dır?

## Ana çıkarım

~~~text
DNS
  ↓
TCP
  ↓
TLS
  ↓
certificate verification
  ↓
encrypted HTTP data
  ↓
network metadata still visible
~~~
