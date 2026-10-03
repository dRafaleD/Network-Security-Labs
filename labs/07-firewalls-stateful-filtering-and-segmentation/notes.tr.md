# Gün 7 — Firewall, Stateful Filtering ve Network Segmentation

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Firewall'ın gerçekte neye karar verdiğini, stateful filtering'in yalnızca “port açık/kapalı” düşüncesinden nasıl farklı olduğunu ve network segmentation'ın gereksiz iletişimi neden sınırladığını anlamak.

Bu lab tamamen local ve savunma odaklıdır. Loopback üzerinde küçük bir TCP service çalıştıracak, connection state'i gözlemleyecek, host firewall'ı inceleyecek ve üçüncü taraf sistemlere dokunmadan allow/deny policy mantığı kuracaksın.

## 1. Firewall ağın neresinde?

Basit model:

```text
application
    ↓
TCP / UDP
    ↓
IP
    ↓
firewall policy
    ↓
network interface / route
```

Firewall; source/destination address, protocol, port, interface, direction ve connection state gibi özelliklere göre trafik hakkında karar verebilir.

Firewall bir application'ın güvenli olduğunu otomatik olarak kanıtlamaz. Görevi policy'ye göre trafiği kontrol etmektir.

## 2. Packet filtering mantığı

Bir rule'u şöyle düşün:

```text
match conditions
      ↓
decision
      ↓
allow / drop / reject / log
```

Plain-language örnek:

> Established trafiğe izin ver, gerekli local service'e izin ver, açıkça gerekli olmayan trafiği kabul etme.

Exact implementation platforma göre değişir.

## 3. Stateless vs stateful filtering

Stateless filter çoğunlukla her packet içindeki field'lara/rule'a bakar.

Stateful firewall ise connection state'i de takip eder.

```text
client ---- SYN ----> server
       <--- SYN/ACK --
       ---- ACK ---->
            ↓
      ESTABLISHED state
```

Sonraki packet'lerin mevcut flow'a ait olduğu anlaşılabilir.

Bu, Day 5'te packet seviyesinde gördüğümüz TCP state ve flag konularının firewall tarafındaki devamıdır.

## 4. Connection tracking

Linux'ta modern firewall workflow'larının altında connection tracking yaygın kullanılır.

Kavramsal state'ler:

- NEW
- ESTABLISHED
- RELATED
- INVALID

Bunlar firewall/connection-tracking kavramlarıdır; `ss` ile gördüğün bütün TCP state'leriyle birebir aynı şey değildir.

Örneğin firewall rule içindeki `ESTABLISHED`, tracked connection durumunu anlatırken TCP'nin kendi ayrı state machine'i vardır.

## 5. Allowlist düşüncesi

Savunma policy'sinde önce şu soruyu sor:

> Hangi iletişim gerçekten gerekli?

Sonra:

```text
gerekli traffic -> explicit allow
gereksiz traffic -> expose etme
unexpected traffic -> policy'ye göre deny/log
```

“Belki lazım olur” diye çok sayıda service açmaktan daha anlaşılırdır.

## 6. DROP vs REJECT

### DROP

Packet sessizce discard edilir. Sender timeout bekleyebilir.

### REJECT

Traffic reddedilir ve implementation/protocol'e göre ICMP error veya TCP reset gibi cevap dönebilir.

Biri her durumda diğerinden “daha güvenli” değildir. Operational requirement, troubleshooting ve policy önemlidir.

## 7. Host firewall vs network firewall

**Host firewall**, tek endpoint üzerinde/önünde policy uygular.

**Network firewall**, network veya zone'lar arasındaki trafiği kontrol eder.

Birlikte kullanılabilir:

```text
Internet
   ↓
network firewall
   ↓
internal network
   ↓
host firewall
   ↓
application
```

Defense in depth, bir layer'ın diğerlerini gereksiz kılması demek değildir.

## 8. Local training service

Sadece loopback'e bind edilmiş zararsız service:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Listener:

```bash
ss -ltnp | grep 8000
```

Beklenen fikir:

```text
127.0.0.1:8000
```

`127.0.0.1` bind, service'in local host üzerinden erişilmesi için tasarlandığını gösterir.

Test:

```bash
curl -I http://127.0.0.1:8000/
```

## 9. Trafiği gözlemle

Sadece local lab flow:

```bash
sudo tcpdump -n -i lo 'tcp port 8000'
```

Başka terminal:

```bash
curl http://127.0.0.1:8000/ > /dev/null
```

Önceki günlerle bağlantı:

- Day 3: port ve flow
- Day 5: TCP handshake/state
- Day 6: DNS resolution ile sonraki connection farkı
- Day 7: hangi flow'un izinli olması gerektiğine policy karar verir

## 10. Firewall configuration'ı güvenli incele

nftables:

```bash
sudo nft list ruleset
```

UFW varsa:

```bash
sudo ufw status verbose
```

Bu labda önce **sadece incele**. Firewall modification komutlarını remote machine'e veya bağlantısına ihtiyaç duyduğun sisteme körlemesine kopyalama.

Firewall değiştirmeden önce:

- sisteme nasıl bağlı olduğunu,
- hangi service'in erişilebilir kalması gerektiğini,
- kendini kilitlersen recovery yöntemini,
- rule'ları başka firewall manager'ın yönetip yönetmediğini

bil.

## 11. nftables kavramları

```text
table
  ↓
chain
  ↓
rule
  ↓
verdict
```

Chain input/output/forward gibi hook'lara bağlanabilir.

### INPUT benzeri traffic
Local host'a gelen traffic.

### OUTPUT benzeri traffic
Local host'un ürettiği traffic.

### FORWARD benzeri traffic
Host üzerinden başka yere geçen traffic.

Normal workstation'da input/output daha belirgin olabilir; router/firewall sistemlerinde forwarding de kritik hale gelir.

## 12. Rule yazmadan önce oku

Rule'u plain language'e çevir.

Kavramsal rule:

```text
protocol = tcp
destination port = 8000
input interface = loopback
action = accept
```

Şöyle okunur:

> Loopback interface üzerinden port 8000'e gelen TCP traffic'i kabul et.

Bu alışkanlık, anlamadan command ezberlemeyi engeller.

## 13. Rule order önemlidir

Birçok firewall ruleset chain/order semantics ile işlenir.

```text
rule 1: established allow
rule 2: gerekli service allow
rule 3: kalan input deny
```

Broad deny, specific allow'dan önce gelirse outcome değişebilir.

Tek rule'u izole yorumlama; tüm policy context'ine bak.

## 14. Segmentation

Segmentation sistemleri farklı network/security zone'lara ayırır.

```text
User network
     |
  firewall
     |
Server network
     |
  firewall
     |
Management network
```

Amaç yalnızca “daha fazla subnet” değildir. Hangi sistemin hangi sistemle hangi amaçla iletişim kurabileceğini kontrol etmektir.

## 15. Segmentation neden önemli?

Zayıf segmentation:

```text
bir endpoint compromise
        ↓
çok sayıda gereksiz reachable system
```

Daha kontrollü segmentation:

```text
bir endpoint
    ↓
yalnızca gerekli communication path
    ↓
daha küçük reachable surface
```

Segmentation güvenliği garanti etmez ama gereksiz exposure ve zone'lar arası hareket alanını azaltabilir.

## 16. VLAN tek başına security policy değildir

VLAN, Layer-2 broadcast domain'leri ayırabilir. Fakat network'ler arası trafiğin nasıl route/filter edildiği security açısından önemlidir.

```text
VLAN / subnet -> separation
firewall / ACL -> communication policy
```

Gerçek architecture bunları birlikte kullanabilir.

## 17. Ingress ve egress

### Ingress filtering
Host/network/zone içine gelen traffic'i kontrol eder.

### Egress filtering
Dışarı çıkan traffic'i kontrol eder.

Defender'lar ingress'e çok odaklanır fakat egress policy de önemlidir.

Örneğin:

> Bu server'ın arbitrary outbound connection başlatması gerekiyor mu?

Cevap server'ın görevine bağlıdır.

## 18. Network least privilege

Least privilege communication için de geçerlidir.

```text
any source -> any destination -> any port
```

yerine gerçek requirement'tan türetilen:

```text
specific source/zone
        ↓
specific destination/service
        ↓
required protocol/port
```

policy daha anlamlıdır.

Rule'u sadece “dar görünsün” diye daraltma; gerçek application requirement'ını yansıtmalı.

## 19. Logging ve visibility

Firewall log şu sorulara yardım edebilir:

- ne deny edildi?
- source/destination neydi?
- hangi port/protocol?
- ne zaman?
- tekrarlandı mı?

Ama denied packet otomatik saldırı değildir.

Internet background noise, misconfiguration, eski client ve normal hata da denied traffic üretebilir.

Firewall evidence'ı packet capture, service log ve host telemetry ile correlate et.

## 20. Troubleshooting workflow

Service erişilemiyorsa:

```text
application çalışıyor mu?
       ↓
listen ediyor mu?
       ↓
hangi address/port?
       ↓
route doğru mu?
       ↓
firewall path'e izin veriyor mu?
       ↓
packet destination'a ulaşıyor mu?
       ↓
response geri geliyor mu?
```

Araçlar:

```bash
ss -ltnp
ip addr
ip route
sudo nft list ruleset
sudo tcpdump -n -i any 'tcp port 8000'
curl -v http://127.0.0.1:8000/
```

Service listen etmiyorken direkt “firewall bozdu” dememeyi öğren.

## 21. Design exercise

Bunları command olarak uygulama; plain-language policy yaz.

Scenario:

- User network: `10.10.10.0/24`
- Web server zone: `10.10.20.0/24`
- Management zone: `10.10.30.0/24`
- User'ların web server'a HTTPS erişmesi gerekiyor.
- SSH administration yalnızca management zone'dan gelmeli.
- Bu simplified scenario'da diğer inbound path'ler gerekli değil.

Dört statement yaz:

1. user neye erişebilir?
2. management neye erişebilir?
3. ne deny edilmeli?
4. ne loglanmalı?

Amaç production firewall deploy etmek değil, policy reasoning geliştirmek.

## 22. Savunma analizi bağlantısı

Önceki konuları birleştir:

```text
DNS query
   ↓
TCP connection attempt
   ↓
firewall decision
   ↓
service response
   ↓
host/application log
```

Artık isolated packet okumaktan correlation'a doğru geçiyoruz.

## Alıştırmalar

1. Loopback HTTP server başlat.
2. `ss` ile listening address/port doğrula.
3. Loopback'te bir request capture et.
4. Local firewall rule'larını değiştirmeden incele.
5. Firewall tool'unda input/output/forward kavramlarını bul.
6. DROP vs REJECT farkını açıkla.
7. Connection-tracking ESTABLISHED ile TCP ESTABLISHED farkını açıkla.
8. Üç zone'lu segmented network çiz.
9. Design exercise için least-privilege policy yaz.
10. “Port 8000 erişilemiyor” için troubleshooting checklist oluştur.

## Sorular

1. Firewall neye karar verir?
2. Stateless ve stateful filtering farkı?
3. Connection tracking nedir?
4. Rule order neden önemlidir?
5. Host firewall ve network firewall farkı?
6. Segmentation'ın amacı nedir?
7. VLAN neden tek başına complete security policy değildir?
8. Ingress ve egress filtering nedir?
9. Denied packet neden otomatik malicious değildir?
10. Firewall'ı suçlamadan önce service state neden kontrol edilmelidir?

## Ana çıkarım

```text
gerekli communication
        ↓
state + source + destination + service
        ↓
firewall policy
        ↓
allow / deny / log
        ↓
segmentation + least privilege
        ↓
daha küçük ve anlaşılır network exposure
```
