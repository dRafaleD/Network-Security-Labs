# Gün 6 — DNS Derinlemesine: Resolution, Record'lar, Cache ve Paket Analizi

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Bir hostname çözümlenirken gerçekte neler olduğunu anlamak ve DNS'i kara kutu gibi görmek yerine temel DNS trafiğini okuyabilmek.

Bu lab resolver rolleri, record türleri, query/response, caching, DNS TTL, NXDOMAIN, UDP/TCP, packet capture, encrypted DNS ve savunma odaklı yorumlamayı kapsar.

## 1. DNS zihinsel modeli

Uygulamalar çoğunlukla `example.com` gibi isimlerle çalışır; IP ağı ise paketleri adreslere taşır.

```text
hostname -> DNS resolution -> IP address -> network connection
```

DNS resolution ile sonrasında kurulan application connection ayrı olaylardır. DNS cevabının başarılı olması web server'ın veya başka bir servisin erişilebilir olduğunu kanıtlamaz.

## 2. Resolver rolleri

Basitleştirilmiş akış:

```text
Application
    ↓
Host üzerindeki stub resolver
    ↓
Recursive resolver
    ↓
DNS hierarchy / authoritative server
    ↓
Answer
```

- **Stub resolver:** OS/application tarafındaki client resolver.
- **Recursive resolver:** client adına cevabı bulur ve çoğunlukla cache kullanır.
- **Authoritative server:** bir DNS zone için authoritative bilgiyi sağlar.

Recursive resolver cevabı cache'de tutuyor olabilir. Bu yüzden her lookup tüm DNS hierarchy'ye yeni request göndermez.

## 3. Recursive resolution

Cache'de kullanılabilir cevap olmadığında kavramsal model:

```text
client
  ↓
recursive resolver
  ↓
root bilgisi
  ↓
TLD bilgisi
  ↓
authoritative bilgi
  ↓
answer
```

Bu öğrenme modelidir; her query'nin birebir bu network trafiğini ürettiği anlamına gelmez.

## 4. Yaygın DNS record türleri

| Type | Genel amacı |
| --- | --- |
| A | IPv4 address |
| AAAA | IPv6 address |
| CNAME | Başka bir name'e alias |
| MX | Mail exchange bilgisi |
| NS | Zone'un name server'ları |
| TXT | Çeşitli mekanizmaların kullandığı text |
| SOA | Zone authority/administrative bilgi |
| PTR | Reverse lookup mapping |

Tek bir name birden fazla record ve IP döndürebilir.

## 5. DNS query gönderme

```bash
getent hosts example.com
```

`dig` kuruluysa:

```bash
dig example.com
dig A example.com
dig AAAA example.com
dig MX example.com
dig NS example.com
```

`dig` output'unda QUESTION, ANSWER, AUTHORITY ve ADDITIONAL bölümlerini tanımaya çalış.

Kavramsal cevap:

```text
example.com.   300   IN   A   192.0.2.10
```

şöyle okunabilir:

```text
name          TTL   class type value
```

Buradaki IP documentation range'den örnektir; example.com'un gerçek adresi olduğu iddia edilmiyor.

## 6. DNS TTL ve IP TTL farkı

DNS record'larındaki TTL, cache'in record'u refresh etmeden yaklaşık ne kadar süre tutabileceğini belirtir.

```text
ilk lookup -> answer -> cache -> reuse -> TTL biter -> refresh
```

Day 4'teki IPv4 TTL ile karıştırma:

```text
DNS TTL -> cache lifetime
IP TTL  -> packet hop limit
```

Aynı kısaltma, farklı görev.

## 7. NXDOMAIN

Query edilen name mevcut değilse DNS `NXDOMAIN` döndürebilir.

Zararsız test için reserved `.invalid` TLD:

```bash
dig definitely-not-a-real-lab-name.invalid
```

Şu farkı öğren:

```text
name mevcut değil
        !=
name çözülüyor ama service erişilemiyor
```

DNS problemi otomatik olarak routing problemi değildir.

## 8. DNS transport

Classic DNS çoğunlukla port 53 kullanır. Normal query'lerin çoğu UDP kullanabilir fakat DNS yalnızca UDP değildir.

TCP de kullanılabilir; örneğin exchange UDP cevabıyla tamamlanamadığında veya operation TCP gerektirdiğinde.

Dolayısıyla:

```text
DNS = her zaman UDP
```

yanlıştır.

## 9. Kendi DNS lookup'ını capture et

Resolver configuration:

```bash
cat /etc/resolv.conf
resolvectl status
```

Capture:

```bash
sudo tcpdump -n -i any 'port 53'
```

Başka terminal:

```bash
dig example.com
```

veya:

```bash
getent hosts example.com
```

Cache, local resolver veya encrypted DNS nedeniyle beklediğin classic DNS packet görünmeyebilir. Bunu direkt hata saymak yerine araştırılacak bir gözlem olarak düşün.

## 10. Wireshark filter'ları

```text
dns
dns.flags.response == 0
dns.flags.response == 1
dns.qry.name == "example.com"
dns.flags.rcode != 0
```

Şunları incele:

- source/destination IP
- source/destination port
- transaction ID
- query name
- query type
- response code
- answer record
- TTL

DNS server çoğunlukla port 53'te listen eder; client ise genellikle ephemeral source port kullanır.

## 11. CNAME zinciri

Bir name alias olabilir:

```text
app.example
     ↓ CNAME
service.example
     ↓ A / AAAA
IP address
```

Analizde ilk name'in doğrudan final IP tuttuğunu varsaymak yerine chain'i takip et.

## 12. Reverse DNS

PTR record reverse lookup için yaygın kullanılır.

Documentation IP ile örnek:

```bash
dig -x 192.0.2.10
```

Reverse DNS name faydalı context sağlayabilir fakat host identity için cryptographic proof değildir.

## 13. Troubleshooting workflow

```text
network var mı?
      ↓
route var mı?
      ↓
resolver configured/reachable mı?
      ↓
name resolve oluyor mu?
      ↓
dönen IP reachable mı?
      ↓
application service çalışıyor mu?
```

Araçlar:

```bash
ip route
cat /etc/resolv.conf
resolvectl status
getent hosts example.com
dig example.com
curl -I https://example.com
```

Son komut DNS dışında başka katmanları da test eder. Sonucu sadece DNS'e bağlama.

## 14. Encrypted DNS

Traditional DNS network path üzerindeki cihazlar tarafından görülebilir. Modern sistemlerde DNS over TLS (DoT) veya DNS over HTTPS (DoH) kullanılabilir.

Encrypted DNS varsa basit port-53 capture query edilen hostname'i göstermeyebilir. Bu, network analyst'in görebileceği evidence'ı değiştirir.

## 15. Savunma bağlantısı

DNS evidence şu konularda yardımcı olabilir:

- failed resolution
- unexpected domain
- tekrarlanan NXDOMAIN
- unusual query volume
- resolution sonrası network activity

Ama:

```text
DNS query görüldü
      ↓
faydalı evidence
      ↓
tek başına malicious behavior kanıtı değil
      ↓
process + connection + time + host telemetry ile correlate et
```

## Mini workflow

```text
name'i belirle
    ↓
resolver'ı belirle
    ↓
query type incele
    ↓
response code incele
    ↓
CNAME/answer takip et
    ↓
TTL/cache context düşün
    ↓
sonraki connection ile correlate et
    ↓
limitations belgele
```

## Alıştırmalar

1. Configured DNS resolver'ını bul.
2. `getent` ile `example.com` resolve et.
3. `dig` ile A ve AAAA record iste.
4. DNS TTL ve IP TTL farkını açıkla.
5. Reserved `.invalid` name query edip response'u incele.
6. Görünüyorsa kendi classic DNS lookup'ını capture et.
7. Client ve resolver portlarını belirle.
8. Wireshark'ta query name/type bul.
9. Legitimate bir domain CNAME döndürüyorsa chain'i takip et.
10. DNS başarısının neden application başarısını kanıtlamadığını açıkla.

## Sorular

1. DNS hangi problemi çözer?
2. Recursive resolver ne yapar?
3. Authoritative server ne yapar?
4. A ve AAAA farkı nedir?
5. DNS TTL neyi kontrol eder?
6. IP TTL'den farkı nedir?
7. NXDOMAIN ne demektir?
8. DNS her zaman UDP mi kullanır?
9. Resolution çalışırken port-53 capture neden boş olabilir?
10. DNS evidence neden diğer telemetry ile correlate edilmelidir?

## Ana çıkarım

```text
name
 ↓
resolver
 ↓
query / response
 ↓
record + TTL + response code
 ↓
sonraki network connection
 ↓
correlated defensive analysis
```
