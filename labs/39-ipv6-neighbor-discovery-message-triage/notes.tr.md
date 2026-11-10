# Gün 39 — IPv6 Neighbor Discovery: NS, NA ve DAD İncelemesi

[English](notes.md) · [Türkçe](notes.tr.md) · [Yerel doğrulama modeli](ndp_triage_demo.py)

## 38. günden devam
Önceki gün **Router Advertisement (RA / ICMPv6 tip 134)** mesajlarıyla router bilgisinin güven sınırını incelemiştik. Bugün aynı IPv6 Neighbor Discovery Protocol (NDP) ailesindeki iki mesajı öğreneceğiz:

- **Neighbor Solicitation (NS / tip 135):** Bir IPv6 komşusunu veya adresin kullanımda olup olmadığını sorgular.
- **Neighbor Advertisement (NA / tip 136):** Bir IPv6 komşusu hakkında bilgi bildirir.

Bunların doğru işlenmesi yerel ağ iletişimi açısından önemlidir. Ancak şüpheli bir NS/NA görmek, gönderenin gerçek kimliğini veya niyetini tek başına kanıtlamaz.

## Kontrol kuralları
1. NDP mesajlarının IPv6 **Hop Limit** değeri **255** olmalıdır.
2. NS ve NA mesajlarının hedef adresi multicast olmamalıdır.
3. **DAD (Duplicate Address Detection):** Henüz adresini doğrulayan istemci, NS mesajını `::` (belirsiz kaynak) üzerinden gönderebilir. Bu yüzden her `::` gördüğümüzde saldırı demeyiz. Bu özel durumda Source Link-Layer Address seçeneği bulunmamalıdır.
4. NA mesajı belirsiz kaynak adresinden (`::`) gelmemelidir.
5. Multicast hedefe gönderilen bir NA'nın **Solicited** bayrağı açık olmamalıdır.
6. Hop Limit ve alan uyumluluğu **kimlik doğrulama değildir**. Aynı LAN üzerindeki aktörler bazı bilgileri taklit edebilir.

## Çalıştır
```bash
python3 ndp_triage_demo.py
```
Kod gerçek ağa çıkmaz; yalnızca hayalî paket alanlarını içeren sözlükleri kontrol eder. Normal NS, DAD NS, hatalı DAD seçeneği, NA bayrak hatası ve yanlış Hop Limit örneklerini raporlar. `assert` testleri beklenen sonuçları doğrular.

## Alıştırmalar
1. NS, NA ve RA arasındaki farkları birer cümleyle anlat.
2. DAD için `::` neden meşru olabilir?
3. Hop Limit 255 neden LAN içindeki bir taklitçiyi durdurmaz?
4. Geçerli bir NA örneğini kendin oluştur.
5. Olası adres sahteciliğini araştırmak için yetkili PCAP, switch port kaydı ve neighbor tablosunu nasıl ilişkilendirirsin?
6. Bu basitleştirilmiş kontrol listesinde hangi RFC kontrolleri eksik?

## Sınırlar
Bu bir gerçek paket ayrıştırıcısı veya kapsamlı NDP doğrulama motoru değildir; ağ trafiği göndermez, cihaz ayarı değiştirmez. Gerçek inceleme için protokol belgeleri ve bağımsız ağ kayıtları gerekir.
