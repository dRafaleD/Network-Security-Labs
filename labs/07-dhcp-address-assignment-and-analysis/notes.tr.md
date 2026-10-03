# Gün 7 — DHCP, Adres Atama ve Paket Analizi

## Hedefler
Bu lab sonunda bir cihazın IPv4 yapılandırmasını nasıl aldığını açıklayabilmeli; DHCP'yi DNS ve ARP'den ayırabilmeli; paket yakalamada DORA akışını okuyabilmeli; önemli DHCP alanlarını tanıyabilmeli ve protokolü savunma açısından yorumlayabilmelisin.

## 1. DHCP neden var?
Bir cihazın normal iletişim kurabilmesi için çoğunlukla IP adresi, prefix/subnet mask, default gateway ve DNS resolver bilgilerine ihtiyacı vardır. DHCP bu yapılandırmayı otomatik dağıtır.

DHCP bir **yapılandırma protokolüdür**. DNS isimleri IP gibi verilere çözer; ARP ise aynı yerel ağdaki IPv4 next-hop adresinin MAC adresini bulmaya yardım eder.

## 2. Portlar
DHCPv4 normalde UDP kullanır:
- sunucu: UDP 67
- istemci: UDP 68

Yeni bağlanan istemci henüz kendi IP adresini ve DHCP sunucusunun adresini bilmeyebileceği için ilk aşamalarda broadcast önemlidir.

## 3. DORA akışı
Normal ilk lease sürecini öğrenmek için dört adım:
1. **DHCPDISCOVER** — istemci DHCP sunucusu arar.
2. **DHCPOFFER** — sunucu bir yapılandırma teklif eder.
3. **DHCPREQUEST** — istemci teklif edilen adresi ister/kabul eder.
4. **DHCPACK** — sunucu lease'i onaylar.

DORA temel modeldir. Gerçek capture'da retransmission, birden fazla OFFER, NAK veya renewal paketleri görebilirsin.

## 4. Lease yaşam döngüsü
Adres genellikle sınırlı süreliğine kiralanır. İstemci süre bitmeden yenilemeye çalışır. **T1 (renewal)** ve **T2 (rebinding)** önemli iki kavramdır. İlk yenileme bilinen sunucuya daha doğrudan yapılabilir; başarısız olursa istemci daha geniş şekilde sunucu arayabilir.

DHCPNAK, DHCPDECLINE, DHCPRELEASE ve DHCPINFORM gibi başka mesajlar da vardır.

## 5. Wireshark'ta bakılacak alanlar
- transaction ID (xid)
- client hardware/MAC address
- client/your IP alanları
- teklif edilen IP
- server identifier
- lease time
- subnet mask
- router/default gateway option
- DNS server option
- DHCP message type

Özellikle **options** bölümüne dikkat et: DHCP yalnızca IP dağıtmaz.

## 6. DHCP Relay
Broadcast trafik normalde router üzerinden diğer subnet'e geçmez. Büyük ağlarda DHCP relay kullanılarak farklı subnet'teki istemcilerin merkezi DHCP sunucusuna ulaşması sağlanabilir. Bu nedenle DHCP analizinde topolojiyi bilmek önemlidir.

## 7. Savunma açısından güvenlik
Yetkisiz/rogue bir DHCP sunucusu istemcilere yanlış gateway veya DNS bilgisi dağıtabilir. Savunmada DHCP snooping gibi switch özellikleri, trusted/untrusted port tasarımı, segmentasyon, beklenmeyen DHCP sunucularının izlenmesi ve sıra dışı lease davranışlarının takibi kullanılabilir.

Paylaşılan ağlarda rogue DHCP denemesi yapma. Aktif deneyleri yalnızca kendi izole VM/lab ağında gerçekleştir.

## 8. Lab A — Mevcut yapılandırmayı incele
Linux:
```bash
ip addr
ip route
cat /etc/resolv.conf
resolvectl status 2>/dev/null
```
Şunları kaydet:
- interface
- IPv4/prefix
- default gateway
- DNS resolver

Her değerin DHCP'den geldiğini varsayma; statik yapılandırma veya local resolver stub olabilir.

## 9. Lab B — DHCP paketlerini güvenli şekilde yakala
Tercihen izole VM ağı kullan. Wireshark display filter:
```text
dhcp
```
UDP 67/68 trafiğini de filtreleyebilirsin.

Disposable bir lab VM'de lease yenilemek trafik oluşturabilir; komut kullandığın NetworkManager/systemd-networkd/dhclient yapısına göre değişir. Uzak bağlantını veya yönetmediğin bir ağı bozacak işlem yapma.

Gördüğün paketleri tabloya yaz:
| Mesaj | Kaynak | Hedef | Broadcast? | Önemli options |
|---|---|---|---|---|
| Discover | | | | |
| Offer | | | | |
| Request | | | | |
| ACK | | | | |

ACK içindeki gateway/DNS bilgilerini host üzerindeki route ve resolver bilgileriyle karşılaştır.

## 10. Lab C — tcpdump
Interface'i bul:
```bash
ip link
```
DHCPv4 trafiğini izle:
```bash
sudo tcpdump -i <interface> -nn -vvv 'udp port 67 or udp port 68'
```
`-nn` seçeneğinin analizde neden yararlı olduğunu açıkla ve client/server portlarını belirle.

## 11. Tekrar soruları
1. İstemci henüz IPv4 adresine sahip değilken broadcast neden işe yarar?
2. OFFER ile ACK arasındaki fark nedir?
3. Default gateway hangi tür DHCP option ile verilir?
4. DHCP üzerinden kötü niyetli DNS ayarı dağıtılması neden önemlidir?
5. Farklı subnet'lerde relay neden gerekebilir?
6. Capture'da DHCP ile DNS'i nasıl ayırırsın?
7. Birden fazla DHCP sunucusunun cevap verdiğini hangi kanıt gösterebilir?
8. Paket capture'ını host yapılandırmasıyla neden karşılaştırmalıyız?

## 12. Mini challenge
Kısa bir analiz raporu oluştur:
- ortam/topoloji
- yakalayabildiysen dört DORA mesajı
- transaction ID
- teklif/atanan IP
- gateway ve DNS options
- lease süresi
- bir savunma gözlemi
- capture'ın sınırlamaları

## Günün özeti
DHCP yalnızca “IP veren protokol” değildir; cihazın ağa katılabilmesi için temel yapılandırmayı bootstrap eder. Broadcast mantığını, UDP 67/68'i, options yapısını, lease yaşam döngüsünü ve güven varsayımlarını anlamak; ileride segmentasyon, NAC, monitoring ve incident analysis konularını kolaylaştırır.
