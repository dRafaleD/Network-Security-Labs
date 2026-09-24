# Gün 1 — Ağ Temelleri ve Paket Gözlemleme

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Bilgisayarınız ağ üzerinden iletişim kurarken devreye giren temel parçaları anlamak ve kendi makinenizin oluşturduğu gerçek trafiği gözlemlemek.

## Temel kavramlar

- **IP adresi:** IP ağı üzerindeki bir host/interface'i tanımlar.
- **MAC adresi:** yerel ağ iletişiminde kullanılan link-layer adresidir.
- **Default gateway:** hedef yerel ağın dışındaysa hostun trafiği normalde gönderdiği router'dır.
- **Paket:** ağ üzerinden taşınan veri birimidir.

Basitleştirilmiş faydalı bir model:

```text
Application
    ↓
TCP / UDP
    ↓
IP
    ↓
Ethernet / Wi-Fi
```

## Lab 1 — Interface'lerini incele

Linux'ta:

```bash
ip addr
```

Şunları bul:

- interface isimleri
- IPv4/IPv6 adresleri
- MAC adresleri
- loopback interface (`lo`)

Ardından route'ları incele:

```bash
ip route
```

`default via` ile başlayan satırı bul. Sonrasındaki adres normalde default gateway'idir.

## Lab 2 — Basit trafik oluştur

Public bir resolver'a bağlantıyı test et:

```bash
ping -c 4 1.1.1.1
```

Ardından bir hostname dene:

```bash
ping -c 4 example.com
```

İkinci komutta hedef IP'ye paket gönderilmeden önce isim çözümleme işlemi de gerekir.

## Lab 3 — Kendi paketlerini gözlemle

Interface'leri listele:

```bash
sudo tcpdump -D
```

Uygun interface üzerindeki ICMP trafiğini yakala:

```bash
sudo tcpdump -n -i <interface> icmp
```

Başka bir terminalde:

```bash
ping -c 4 1.1.1.1
```

Request/reply çiftlerini gözlemle.

`-n` seçeneği adresleri sayısal halde tutar; bu da ilk alıştırmayı takip etmeyi kolaylaştırır.

## Wireshark alternatifi

Aktif interface üzerinde capture başlat ve şu display filter'ı kullan:

```text
icmp
```

Ping'i tekrar çalıştır ve şunları incele:

- Source
- Destination
- Protocol
- Echo request
- Echo reply

## Sorular

1. Aktif network interface'in hangisi?
2. Private IP adresi ne?
3. Default gateway'in ne?
4. ICMP request içinde hangi source ve destination IP'leri görüyorsun?
5. IP adresi yerine hostname pinglediğinde ne değişiyor?

## Ana çıkarım

Ağ iletişimini görünmez bir sihir gibi düşünme. `ping` gibi basit bir komut bile source, destination, protocol ve yön bilgileri görülebilen trafik üretir.

Ağ güvenliğinde bu trafiği okumayı öğrenmek, araç komutlarını ezberlemekten daha önemlidir.
