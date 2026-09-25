# Gün 3 — TCP, UDP, Portlar ve Bağlantı Analizi

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

TCP ve UDP'nin uygulama trafiğini nasıl taşıdığını, portların neyi temsil ettiğini, TCP bağlantısının nasıl kurulup kapandığını ve bunların packet capture içinde nasıl tanınacağını öğrenmek.

## 1. Transport layer

IP paketi doğru hosta yönlendirirken transport layer verinin doğru uygulamaya ulaşmasına yardım eder.

İki temel protokol:

- **TCP** — connection-oriented ve güvenilir byte stream.
- **UDP** — connectionless datagram yapısı ve daha düşük protokol overhead'i.

Hiçbiri her durumda diğerinden iyi değildir; uygulamanın ihtiyacına göre seçilir.

## 2. Portlar

Port, aynı IP üzerinden iletişim kuran servis/process'leri ayırmaya yarayan transport-layer numarasıdır.

| Port | Tipik servis |
| ---: | --- |
| 22/TCP | SSH |
| 53/UDP veya TCP | DNS |
| 80/TCP | HTTP |
| 443/TCP | HTTPS |

Port numarası tek başına o portta hangi uygulamanın çalıştığını kanıtlamaz.

Linux'ta listening socket'leri incele:

```bash
ss -tuln
```

```text
-t -> TCP
-u -> UDP
-l -> listening
-n -> adres/portları sayısal göster
```

## 3. TCP three-way handshake

Basitleştirilmiş bağlantı:

```text
Client                         Server
  | ------ SYN ----------------> |
  | <----- SYN, ACK ------------ |
  | ------ ACK ----------------> |
```

Ardından application data taşınabilir.

Tanıman gereken flag'ler:

```text
SYN -> bağlantıyı başlat/synchronize et
ACK -> alınan veri/state'i onayla
FIN -> düzenli bağlantı kapatma
RST -> bağlantıyı resetle
```

## 4. Sequence ve acknowledgement

TCP byte stream'i sequence number ile takip eder ve alınan ilerlemeyi acknowledgement ile bildirir.

Şimdilik sayıları ezberleme. Mantığı tanı:

```text
byte'ları gönder
   ↓
receiver ilerlemeyi ACK'ler
   ↓
eksik veri yeniden gönderilebilir
```

## 5. TCP capture labı

Zararsız local server:

```bash
python3 -m http.server 8000
```

Loopback TCP trafiğini yakala:

```bash
sudo tcpdump -n -i lo tcp port 8000
```

Başka terminalde:

```bash
curl http://127.0.0.1:8000/
```

Şunları bulmaya çalış:

1. SYN
2. SYN-ACK
3. ACK
4. application data
5. connection termination

Her şey localhost üzerinde kaldığı için kontrollü bir alıştırmadır.

## 6. Wireshark filtreleri

```text
tcp
tcp.port == 8000
tcp.flags.syn == 1
tcp.flags.reset == 1
```

TCP bölümünde şunları incele:

- source port
- destination port
- flags
- sequence number
- acknowledgement number

## 7. Client ve server portları

Şuna benzer trafik görebilirsin:

```text
127.0.0.1:53422 -> 127.0.0.1:8000
```

Server 8000'de listening durumundayken client genellikle geçici bir source port kullanır.

Bir flow kavramsal olarak şu beş değerle tanımlanabilir:

```text
source IP
source port
destination IP
destination port
transport protocol
```

Buna sıkça **five-tuple** denir.

## 8. UDP

UDP, TCP tarzı three-way handshake yapmaz.

```text
Host A ---- datagram ----> Host B
```

UDP kendi başına TCP'deki gibi güvenilir sıralı byte stream, retransmission ve ordering garantisi sağlamaz. Gerektiğinde uygulamalar kendi mekanizmalarını oluşturabilir.

```bash
ss -uln
```

ile UDP socket'lerini inceleyebilirsin.

## 9. TCP ve UDP karşılaştırması

| Özellik | TCP | UDP |
| --- | --- | --- |
| Bağlantı kurulumu | Var | TCP tarzı handshake yok |
| Güvenilir sıralı stream | Var | UDP tarafından sağlanmaz |
| Retransmission | TCP sağlar | Uygulamaya bağlı |
| Veri modeli | Byte stream | Datagram |
| Tipik kullanım | Web, SSH | DNS, streaming/real-time protokoller |

Modern protokoller basit örnekleri değiştirebilir. Örneğin HTTP/3, UDP üzerinde QUIC kullanır. Bu yüzden protokolü varsayımla değil kanıtla belirle.

## 10. Connection state'leri

```bash
ss -tan
```

Şunlarla karşılaşabilirsin:

```text
LISTEN
ESTAB
TIME-WAIT
SYN-SENT
SYN-RECV
```

Bunlar TCP socket'in bağlantı yaşam döngüsündeki durumunu gösterir.

## 11. Güvenlik bağlantısı

Transport-layer görünürlüğü savunma analizinde önemlidir.

Şunları cevaplamaya yardım eder:

- Bağlantıyı hangi host başlattı?
- Hangi destination port ile iletişim kuruldu?
- TCP handshake tamamlandı mı?
- Bağlantı resetlendi mi?
- Tekrarlanan bağlantı denemeleri var mı?
- Yerelde hangi servisler listening durumda?

Listening port otomatik olarak vulnerability değildir. Servis, yapılandırma ve network erişimiyle birlikte yorumlanması gereken bir iletişim endpoint'idir.

## 12. Mini alıştırmalar

### A — Local socketler

```bash
ss -tuln
```

Varsa üç kayıt seç ve TCP/UDP olarak sınıflandır.

### B — Handshake

Local HTTP bağlantısını capture et ve SYN, SYN-ACK, ACK paketlerini bul.

### C — Five-tuple

Capture içinden bir TCP connection seçip five-tuple değerlerini yaz.

### D — Connection lifecycle

```bash
ss -tan
```

komutunu local server'a tekrar tekrar request gönderirken çalıştır ve state değişimlerini gözlemle.

## Sorular

1. Portlar hangi problemi çözer?
2. TCP neden handshake kullanır?
3. SYN ve ACK ne işe yarar?
4. UDP, TCP'den nasıl farklıdır?
5. Ephemeral/client source port nedir?
6. Five-tuple hangi beş değerden oluşur?
7. Open/listening port otomatik olarak vulnerability anlamına gelir mi?
8. Capture içinde neden retransmission veya reset görülebilir?

## Ana çıkarım

```text
application
    ↓
TCP/UDP + portlar
    ↓
IP + routing
    ↓
local link delivery
```

Bir flow'un yönünü ve TCP state'ini tanıyabilmek ileride firewall, IDS/IPS ve packet-analysis lablarının temelini oluşturur.
