# Gün 4 — ICMP, Traceroute, TTL ve Ağ Sorun Giderme

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç
ICMP, TTL/Hop Limit, ping ve traceroute mantığını öğrenmek; bunları defensive troubleshooting ve packet analysis ile bağlamak.

## 1. ICMP, TCP veya UDP değildir
ICMP network layer'da kontrol ve diagnostic bilgi taşır. TCP/UDP portu kullanmaz.

Echo Request/Reply ve teslimat sırasında oluşan bazı hata mesajları yaygın örneklerdir.

## 2. Ping
```bash
ping -c 4 1.1.1.1
```
Ping genellikle ICMP Echo Request/Reply kullanır. Reply gelmesi o anda IP reachability olduğunu gösterir. Reply gelmemesi ise host kesin offline demek değildir; ICMP filtrelenmiş veya rate-limit uygulanmış olabilir.

## 3. TTL
IPv4 packet içinde Time To Live alanı vardır. Packet'i forward eden her router değeri azaltır. Sıfıra ulaştığında router packet'i normalde drop eder ve ICMP Time Exceeded döndürebilir.

Amaç routing loop oluştuğunda packet'in sonsuza kadar dolaşmasını önlemektir.

## 4. Traceroute
Traceroute hop-limit davranışını kullanarak ara routing hop'larını gözlemlemeye çalışır.

```bash
traceroute 1.1.1.1
```

Implementation ve option'a göre UDP, ICMP veya TCP probe kullanılabilir. Eksik hop, router yok veya down demek değildir; response filtrelenebilir/deprioritize edilebilir.

## 5. Packet capture labı
Sadece kendi oluşturduğun diagnostic trafiği yakala:
```bash
sudo tcpdump -n -i any icmp
```
Başka terminal:
```bash
ping -c 4 1.1.1.1
```

Wireshark:
```text
icmp
icmp.type == 8
icmp.type == 0
```

Source/destination IP, ICMP type/code ve TTL alanlarını incele.

## 6. Layer layer troubleshooting
```text
interface up mı?
   ↓
IP var mı?
   ↓
local gateway reachable mı?
   ↓
route var mı?
   ↓
remote IP reachable mı?
   ↓
DNS resolve ediyor mu?
   ↓
application/service çalışıyor mu?
```

Komutlar:
```bash
ip addr
ip route
ip neigh
ping -c 2 <gateway>
ping -c 2 1.1.1.1
getent hosts example.com
ss -tuln
```

## 7. IP çalışıyor, domain çalışmıyor
IP reachable olduğu halde hostname resolve olmuyorsa routing'i suçlamadan önce DNS'i incele.

```text
routing/reachability != name resolution
```

## 8. Güvenlik bağlantısı
ICMP ve route gözlemleri defender'ların network path ve arızaları anlamasına yardım eder. Aynı mekanizmalar reconnaissance sırasında da görülebileceği için bazı ağlar diagnostic trafiği filtreler. Ancak ICMP meşru network operasyonları için de önemlidir.

## Alıştırmalar
1. `ip route` ile default route'u bul.
2. Kendi gateway'ine ping atıp ICMP packet'lerini incele.
3. İletişim kurmana izin verilen public IP'ye ping at ve TTL gözlemlerini karşılaştır.
4. Traceroute çalıştır; yalnızca hop sayısını/gözlemini kaydet ve gizli hop'ları down kabul etme.
5. `getent hosts` ile hostname resolution test et.
6. Failed ping'in neden host'un offline olduğunu kanıtlamadığını açıkla.

## Sorular
1. ICMP port kullanır mı?
2. TTL neden vardır?
3. TTL sıfıra ulaşınca normalde ne olur?
4. Traceroute hop'ları nasıl keşfedebilir?
5. Traceroute neden `*` gösterebilir?
6. IP reachability ile DNS resolution farkı nedir?
7. Troubleshooting neden layer layer yapılmalıdır?

## Ana çıkarım
```text
ICMP + TTL
    ↓
reachability/path evidence
    ↓
packet capture
    ↓
layer-by-layer troubleshooting
    ↓
daha iyi defensive diagnosis
```
