# Gün 5 — TCP Derinlemesine: Flag'ler, State'ler, Sequence Number ve Retransmission

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

“TCP connection-oriented bir protokoldür” bilgisinin ötesine geçip gerçek packet capture içinde TCP bağlantısının nasıl davrandığını anlamak.

Bu lab:

- TCP flag'leri
- three-way handshake
- sequence ve acknowledgment number
- connection state'leri
- düzgün bağlantı kapatma
- RST paketleri
- retransmission ve packet loss
- Wireshark/Tcpdump analizi
- savunma odaklı yorumlama

konularını bir araya getirir.

Amaç her alanı ezberlemek değil, paketlerden bir bağlantının hikâyesini çıkarabilmektir.

## 1. TCP tekrarı

TCP, iki endpoint arasında sıralı ve güvenilir bir byte stream sağlamaya çalışan transport-layer protokolüdür.

Bir flow'u düşünürken:

```text
source IP
source port
destination IP
destination port
protocol
```

bilgileri önemlidir.

TCP'nin reliable olması ağda packet loss olmayacağı anlamına gelmez. TCP eksik veriyi fark edip yeniden gönderebilir.

## 2. Önemli TCP flag'leri

| Flag | Başlangıç seviyesi anlamı |
| --- | --- |
| SYN | Bağlantıyı başlat/senkronize et |
| ACK | Alınan veri veya state'i onayla |
| FIN | Bağlantının bir yönünü düzgün biçimde kapat |
| RST | Bağlantıyı resetle/ani biçimde sonlandır |
| PSH | Verinin uygulamaya hızlı aktarılmasını iste |
| URG | Urgent-pointer semantics; modern normal trafikte nadir |

Flag'ler birlikte bulunabilir. Örneğin server'ın handshake cevabı genellikle SYN + ACK'tir.

## 3. Three-way handshake

```text
Client                         Server
  |                              |
  | -------- SYN --------------> |
  | <----- SYN, ACK ------------ |
  | -------- ACK --------------> |
  |                              |
  |        ESTABLISHED           |
```

Üç adımın mantığı:

1. Client başlangıç sequence number bilgisini bildirir.
2. Server bunu acknowledge eder ve kendi sequence bilgisini bildirir.
3. Client server'ı acknowledge eder.

Böylece iki taraf da connection state'i senkronize eder.

## 4. Sequence number

TCP yalnızca “paket 1, paket 2” şeklinde numaralandırma yapmaz. Byte stream içindeki konumu takip eder.

```text
SEQ = benim gönderdiğim verinin başladığı konum
ACK = senden beklediğim sonraki byte
```

1000 sequence değerinden başlayan segment 100 byte taşıyorsa receiver sonraki beklenen byte olarak 1100'ü acknowledge edebilir.

Wireshark okumayı kolaylaştırmak için çoğu zaman **relative sequence numbers** gösterir. Bu nedenle ekranda 0 veya 1 gibi küçük değerler görebilirsin.

## 5. ACK uygulamanın başarılı olduğu anlamına gelmez

TCP ACK yalnızca TCP seviyesindeki receipt/state hakkında bilgi verir.

Şunları tek başına kanıtlamaz:

- HTTP request uygulama tarafından kabul edildi,
- login başarılı oldu,
- database transaction tamamlandı,
- kullanıcı beklenen sonucu gördü.

```text
TCP success != application success
```

Katmanları birbirine karıştırma.

## 6. TCP state'leri

`ss` ile görebileceğin yaygın state'ler:

- `LISTEN` — incoming connection bekliyor
- `SYN-SENT` — SYN gönderildi, cevap bekleniyor
- `SYN-RECV` — SYN alındı, handshake tamamlanmadı
- `ESTAB` / `ESTABLISHED` — bağlantı kuruldu
- `FIN-WAIT-1` / `FIN-WAIT-2` — local taraf kapanıyor
- `CLOSE-WAIT` — peer kapattı, local application'ın kapatması bekleniyor
- `LAST-ACK` — kapanıştaki son ACK bekleniyor
- `TIME-WAIT` — yeni kapanmış bağlantı geçici olarak tutuluyor
- `CLOSED` — aktif connection state yok

Bugün bütün TCP state machine'i ezberlemene gerek yok. Yaygın state'lerin ne anlattığını öğren.

## 7. Graceful teardown

TCP full-duplex olduğu için iki yön ayrı ayrı kapanabilir.

Basitleştirilmiş akış:

```text
Client                         Server
  | -------- FIN -------------> |
  | <------- ACK -------------- |
  | <------- FIN -------------- |
  | -------- ACK -------------> |
```

Timing'e göre gerçek capture biraz farklı görünebilir.

## 8. TIME-WAIT neden var?

Connection'ı aktif olarak kapatan endpoint bir süre `TIME-WAIT` durumunda kalabilir.

Bu:

- eski connection'dan gecikmiş paketlerin yeni connection ile karışmasını önlemeye,
- gerekirse final ACK'in tekrar gönderilebilmesine

yardım eder.

Dolayısıyla TIME-WAIT görmek otomatik olarak problem değildir.

## 9. RST

RST, graceful close yerine connection'ın resetlendiğini gösterir.

Zararsız local örnek:

```bash
nc -v 127.0.0.1 65000
```

O portta hiçbir şey dinlemiyorsa bağlantı genellikle refused olur ve local capture içinde reset görebilirsin.

RST'nin birçok normal nedeni olabilir. Tek başına malicious activity göstergesi değildir.

## 10. Local handshake labı

Terminal 1:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Terminal 2:

```bash
sudo tcpdump -n -i lo 'tcp port 8000'
```

Terminal 3:

```bash
curl http://127.0.0.1:8000/
```

Şunları bul:

1. SYN
2. SYN/ACK
3. ACK
4. TCP içindeki HTTP data
5. ACK'ler
6. connection close

Her şey loopback üzerinde kaldığı için güvenli ve tekrar üretilebilir bir labdır.

## 11. Connection state inceleme

Server çalışırken:

```bash
ss -ltn
```

8000 portunu bul.

Aktif bağlantı sırasında:

```bash
ss -tn
```

kullanabilirsin.

Kendine sor:

- Hangi endpoint listen ediyor?
- Server port hangisi?
- Client tarafındaki ephemeral port hangisi?

## 12. Wireshark filter'ları

```text
tcp
tcp.port == 8000
tcp.flags.syn == 1
tcp.flags.reset == 1
tcp.analysis.retransmission
tcp.analysis.fast_retransmission
tcp.analysis.duplicate_ack
```

Bir TCP packet seçip şunları incele:

- source/destination
- source/destination port
- flags
- sequence number
- acknowledgment number
- TCP payload length
- window size

## 13. Follow TCP Stream

Wireshark'taki **Follow TCP Stream**, aynı TCP conversation'a ait application byte'larını birlikte gösterir.

Local HTTP labında request ve response'u tek conversation olarak görmeyi kolaylaştırır.

Fakat timing, flag, retransmission gibi packet-level detaylar için tekrar packet listesine dön.

## 14. Retransmission

Sender beklenen acknowledgment'ı alamazsa data yeniden gönderilebilir.

```text
sender ---- segment A ----> receiver
             X kayıp

sender ---- segment A ----> receiver
          retransmission
```

Olası nedenler:

- packet loss
- congestion
- overloaded system
- wireless interference
- routing problemi
- capture artifact

Retransmission, TCP'nin recovery davranışının kanıtıdır; tek başına root cause'u söylemez.

## 15. Duplicate ACK

Receiver daha sonraki data'yı alıp daha önceki bir bölüm eksik olduğunda aynı beklenen sequence position'ı tekrar tekrar acknowledge edebilir.

Duplicate ACK'ler packet loss veya out-of-order delivery için ipucu olabilir.

Yine context gerekir.

## 16. Capture sınırlamaları

Packet'i nerede capture ettiğin önemlidir.

Örneğin checksum offloading yüzünden local capture'da outgoing packet checksum'u yanlış görünebilir; NIC gerçek gönderimden önce checksum'u hesaplıyor olabilir.

Bir endpoint'teki capture, yol üzerindeki başka cihazın gördüğüyle birebir aynı olmak zorunda değildir.

Packet capture belirli bir observation point'ten alınmış delildir.

## 17. Savunma bağlantısı

TCP analizi defender'a şunları incelemede yardım eder:

- service availability problemi
- refused connection
- beklenmedik reset
- packet loss
- unusual connection pattern
- tamamlanmayan handshake
- scanning benzeri davranış
- overloaded service

Örneğin çok sayıda SYN görmek tek başına saldırı kanıtı değildir. Rate, source dağılımı, server state ve diğer telemetry ile birlikte değerlendirilmelidir.

## 18. Mini investigation workflow

```text
flow'u belirle
    ↓
handshake'i bul
    ↓
flag'leri kontrol et
    ↓
SEQ/ACK ilerleyişini takip et
    ↓
application data'yı incele
    ↓
retransmission/reset ara
    ↓
teardown'u incele
    ↓
host/service evidence ile correlate et
```

## Alıştırmalar

1. Local HTTP server'ı başlat.
2. Tek bir `curl` request capture et.
3. SYN, SYN/ACK ve ACK'i bul.
4. Client/server portlarını yaz.
5. Application data taşıyan ilk packet'i bul.
6. Follow TCP Stream kullan.
7. Connection'ın nasıl kapandığını belirle.
8. `ss -ltn` ile listening socket'i bul.
9. Kullanılmayan local port örneğini deneyip RST ara.
10. Retransmission'ın neden tek başına root cause göstermediğini açıkla.

## Sorular

1. SYN'in görevi nedir?
2. ACK number kavramsal olarak neyi gösterir?
3. TCP neden sequence number kullanır?
4. FIN ve RST arasındaki fark nedir?
5. TIME-WAIT neden normal olabilir?
6. Retransmission nedir?
7. Duplicate ACK neye işaret edebilir?
8. TCP ACK application işleminin tamamlandığını kanıtlar mı?
9. Capture location neden önemlidir?
10. Unusual SYN trafiği neden context ile yorumlanmalıdır?

## Ana çıkarım

```text
flags + states + sequence numbers
             ↓
      connection'ı yeniden kur
             ↓
 retransmission / reset / close
             ↓
       gözlemi açıkla
             ↓
 savunma odaklı network analysis
```
