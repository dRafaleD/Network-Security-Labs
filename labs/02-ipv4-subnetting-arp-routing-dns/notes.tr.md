# Gün 2 — IPv4, Subnetting, ARP, Routing ve DNS

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Bir hostun trafiği nereye göndereceğine nasıl karar verdiğini daha güçlü bir zihinsel modelle anlamak. Bu lab IPv4 adresleme, subnet mask, local/remote ağ kararı, ARP, default gateway, routing ve DNS konularını birbirine bağlar.

Lab sonunda bir pakete bakıp neden doğrudan yerel hosta veya router'a gönderildiğini açıklayabilmelisin.

## 1. IPv4 adresleri

IPv4 adresi 32 bittir ve genellikle dört decimal octet olarak yazılır:

```text
192.168.1.25
```

Adres tek başına network kısmını belirlemek için yeterli değildir. Prefix uzunluğuna da ihtiyacımız vardır.

```text
192.168.1.25/24
```

`/24`, ilk 24 bitin network'ü, kalan 8 bitin ise o network içindeki hostları tanımladığını söyler.

Tipik `192.168.1.0/24` için:

```text
Network address : 192.168.1.0
Host aralığı    : 192.168.1.1 - 192.168.1.254
Broadcast       : 192.168.1.255
Subnet mask     : 255.255.255.0
```

## 2. CIDR ve subnet mask

| CIDR | Subnet mask | Subnet başına adres |
| --- | --- | ---: |
| /24 | 255.255.255.0 | 256 |
| /25 | 255.255.255.128 | 128 |
| /26 | 255.255.255.192 | 64 |
| /27 | 255.255.255.224 | 32 |
| /28 | 255.255.255.240 | 16 |

Toplam adres sayısına normal IPv4 subnetlerinde network ve broadcast adresleri de dahildir.

Örnek:

```text
10.0.0.205/28
```

`/28` 16'lık bloklara ayrılır. 205'in bulunduğu blok:

```text
192 - 207
```

Dolayısıyla:

```text
Network   : 10.0.0.192
Hostlar   : 10.0.0.193 - 10.0.0.206
Broadcast : 10.0.0.207
```

## 3. Local mı remote mu?

Host:

```text
192.168.1.20/24
```

Hedef A:

```text
192.168.1.50
```

Aynı `/24` içindedir. Ethernet frame yerel ağda doğrudan hedefe gönderilebilir.

Hedef B:

```text
1.1.1.1
```

Yerel network'ün dışındadır. Host frame'i default gateway'e yollar.

Önemli ayrım:

```text
Destination IP  -> uzaktaki sunucunun IP'si olabilir
Destination MAC -> yerel router'ın MAC adresi olabilir
```

Layer 2 ve Layer 3 teslimat probleminin farklı kısımlarını çözer.

## 4. ARP

ARP, yerel ağda bir IPv4 adresini MAC adresiyle eşleştirmeye yarar.

```bash
ip neigh
```

Şuna benzer kayıt görebilirsin:

```text
192.168.1.1 dev wlan0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
```

Gateway'e trafik oluşturup tekrar bak:

```bash
ping -c 1 <gateway-ip>
ip neigh
```

## 5. tcpdump ile ARP gözlemleme

Yalnızca kendi/izinli local ağında uygula.

```bash
sudo tcpdump -n -e -i <interface> arp
```

Başka terminalde çözümleme gerektiren yerel bir adrese trafik oluştur.

ARP mantıksal olarak şunu sorar:

```text
192.168.1.1 kimde?
192.168.1.20'ye söyle.
```

Adrese sahip cihaz MAC adresiyle cevap verir.

`-e`, link-layer bilgisini göstermesi nedeniyle burada faydalıdır.

## 6. Routing table

```bash
ip route
```

Örnek:

```text
default via 192.168.1.1 dev wlan0
192.168.1.0/24 dev wlan0 src 192.168.1.20
```

İkinci route local network'ün doğrudan erişilebilir olduğunu söyler.

Daha spesifik bir route eşleşmediğinde default route kullanılır.

Linux'a belirli hedef için hangi route'u kullanacağını sor:

```bash
ip route get 1.1.1.1
```

Sonra local bir IP ile karşılaştır:

```bash
ip route get <başka-local-ip>
```

## 7. DNS

İnsanlar:

```text
example.com
```

gibi isimleri kullanmayı tercih eder; ağ iletişiminde ise adres gerekir.

```bash
getent hosts example.com
```

`dig` kuruluysa:

```bash
dig example.com
```

Tanıman gereken bazı DNS record türleri:

```text
A     -> IPv4 adresi
AAAA  -> IPv6 adresi
CNAME -> alias
MX    -> mail server bilgisi
NS    -> authoritative name server bilgisi
```

## 8. DNS trafiğini gözlemleme

```bash
sudo tcpdump -n -i <interface> port 53
```

Ardından bir DNS sorgusu yap.

Modern sistemlerde encrypted DNS veya local resolver kullanılabildiği için DNS trafiğini her zaman düz port 53 olarak görmeyebilirsin. Hiçbir şey görünmemesi doğrudan komutun bozuk olduğu anlamına gelmez.

Wireshark'ta klasik DNS için:

```text
dns
```

Şunları incele:

- query name
- query type
- response
- dönen adresler
- source ve destination

## 9. Bir bağlantıyı zihninde takip et

Remote bir siteye giderken basitleştirilmiş akış:

```text
hostname
   ↓
DNS resolution
   ↓
destination IP
   ↓
routing kararı
   ↓
hedef remote mu? evet
   ↓
ARP/neighbour cache ile gateway MAC'i bul
   ↓
local frame'i gateway'e gönder
   ↓
router paketi ileri taşır
```

Bu model basitleştirilmiştir ama ayrı ayrı öğrendiğimiz kavramları birbirine bağlar.

## 10. Mini alıştırmalar

### A — Subnet

```text
192.168.10.77/27
```

Bul:

- subnet mask
- network address
- broadcast address
- kullanılabilir host aralığı

### B — Route

```bash
ip route get 1.1.1.1
```

Kaydet:

- seçilen interface
- gateway
- source IP

### C — ARP

```bash
ip neigh
```

Varsa gateway kaydını bul ve IP/MAC ilişkisini incele.

### D — DNS

`example.com` adresini resolve et ve dönen adreslerden en az birini kaydet.

## 11. Güvenlik bağlantısı

Bu temeller güvenlik çalışmalarında sürekli karşına çıkar.

- ARP, yerel Layer-2 kimliğini ve spoofing risklerinin temelini anlamana yardım eder.
- Routing, trafiğin nereye gidebildiğini açıklar.
- DNS logları bir sistemin hangi domainlerle iletişim kurmaya çalıştığını gösterebilir.
- Subnetler network sınırlarını oluşturur ve segmentation için önemlidir.
- Packet capture, ağda gerçekte ne olduğunu doğrulamayı sağlar.

Direkt saldırılara atlama. Önce normal davranışın nasıl göründüğünü öğren.

## Sorular

1. Bir host neden hem IP adresine hem subnet mask/prefix'e ihtiyaç duyar?
2. Remote server'a giderken destination IP ile destination MAC arasındaki fark nedir?
3. ARP hangi problemi çözer?
4. Default gateway ne zaman kullanılır?
5. En spesifik eşleşen route ne anlama gelir?
6. DNS A ve AAAA record arasındaki fark nedir?
7. Bazı sistemlerde neden `port 53` capture'ında DNS göremeyebilirsin?
8. `192.168.10.77/27` için network ve broadcast adresleri nedir?

## Ana çıkarım

```text
Adresim ve subnetim ne?
        ↓
Hedef local mı?
        ↓
Hangi route kullanılacak?
        ↓
Frame hangi local MAC'e gidecek?
        ↓
Önce hostname DNS ile çözülmeli mi?
```

Bu karar sürecini anlamak; ileride packet analysis, firewall kuralları, segmentation ve network security troubleshooting için temel oluşturur.
