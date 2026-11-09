# Gün 38 — IPv6 Router Advertisement ve Güven Sınırları

[English](notes.md) · [Türkçe](notes.tr.md) · [Çevrimdışı Python lab](ra_guard_demo.py)

## 37. günden devam
Önceki gün IPv6 kaynak adresleriyle izin listesi kontrolü yaptık. Ancak IPv6 ağında yalnızca sunucuya erişim değil, **istemcinin ağ bilgilerini nereden öğrendiği** de önemlidir. Neighbor Discovery Protocol (NDP) içindeki **Router Advertisement (RA)** mesajları bir istemcinin yönlendirici ve ağ öneki (prefix) bilgilerini etkileyebilir.

Bilinmeyen bir RA mesajı inceleme gerektirir. Fakat yalnızca şüpheli bir kayıt görmek, bir saldırganın kimliğini veya niyetini kanıtlamaz.

## Bilmen gerekenler
- RA, ICMPv6 **tip 134** mesajıdır.
- Normal kaynak adresi **link-local** IPv6 adresidir (`fe80::/10` aralığından).
- NDP mesajlarının IPv6 **Hop Limit** değeri **255** olmalıdır. Bu, uzak ağdan yönlendirilen paketlere karşı bir kontrol sağlar ama **aynı yerel ağdaki sahteciliği engellemez**.
- MAC adresi ve link-local kaynak tek başına kimlik doğrulaması değildir; taklit edilebilir.
- Switch üzerindeki **RA Guard**, doğru port/topoloji politikasıyla riski azaltabilir. Tek başına her tehdidi ortadan kaldırmaz.
- `2001:db8:10::/64` gerçek hedef değil, IPv6 dokümantasyon aralığından örnektir.

## Uygulama
```bash
python3 ra_guard_demo.py
```
Program yalnızca sentetik olay sözlüklerini kontrol eder. Beklenen router adresi, MAC, prefix ve Hop Limit değerlerini karşılaştırır. Bazı olaylar politikaya uygun, bazıları **inceleme gerektiriyor** olarak işaretlenir. Ağ paketi göndermez ve firewall/router ayarı değiştirmez.

## Alıştırmalar
1. Switch, router ve istemci arasındaki güven sınırını çiz.
2. Hop Limit 255 neden gönderenin gerçek router olduğunu ispatlamaz?
3. Meşru router'ın MAC adresi değişirse hangi yanlış alarm oluşabilir?
4. Yedek router eklemek için izin listesini nasıl genişletirdin?
5. Bir olayı doğrulamak için switch port kaydı, PCAP ve istemci yönlendirme tablosundan ne öğrenebilirsin?
6. Kaynak adresi/MAC taklit edilirse bu oyuncak modelin hangi sınırlaması ortaya çıkar?

## Sınırlar
Bu lab gerçek paket ayrıştırıcısı değildir; RA yollamaz veya mevcut ağı test etmez. Gerçek ortamda NDP kuralları, RA Guard, ağ topolojisi ve değişiklik yönetimi birlikte değerlendirilmelidir.
