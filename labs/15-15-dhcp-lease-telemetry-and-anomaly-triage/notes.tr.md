# Gün 15 — DHCP Lease Telemetrisi, Adres Değişiklikleri ve Alarm İncelemesi

[English](notes.md) · [Türkçe](notes.tr.md)

## Hedef
DHCP Lease Telemetrisi, Adres Değişiklikleri ve Alarm İncelemesi konusunu tamamen yerel ve zararsız örneklerle öğrenmek. Gözlemlenen bulguyu yorumdan ayırmak ve kesin olmayan sonuçları abartmamak.

## Temel kavramlar
1. **DHCP discover/offer/request/ack:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
2. **lease lifetimes:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
3. **client identifiers and MAC addresses:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
4. **address reuse and legitimate churn:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
5. **rogue server detection concepts:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
6. **baseline and anomaly triage:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.

## Uygulama
Lab klasöründe `lease_triage.py` dosyasını inceleyin ve şu komutları sırasıyla uygulayın:

```bash
python3 lease_triage.py
```

```bash
ip address show
```

```bash
ip route
```

**Beklenen sonuç:** Repeated MAC/IP offered by two server labels is flagged for review, not declared malicious.

## Analiz defteri
Kullandığınız araç sürümünü, komutu, girdiyi, gördüğünüz çıktıyı, beklenmeyen olayları ve olası açıklamaları kaydedin. Ölçülen veri ile çıkarımı ayrı başlıklar altında yazın.

## Uygulama görevleri
1. Orijinal örneği çalıştırıp çıktıyı kaydedin.
2. Zararsız bir girdiyi değiştirerek sonucu önceden tahmin edin.
3. Bir negatif test ekleyin ve gerçekten hangi kontrolün başarısız olduğunu belirleyin.
4. Başlangıç dosyasına dönüp regresyon testi yapın.
5. İki olası yanlış pozitif açıklaması üretin.
6. Sonucu doğrulayacak bağımsız bir kanıt kaynağı önerin.
7. Belirsizlikleri açıkça yazan kısa bir rapor hazırlayın.

## Tekrar soruları
1. DHCP discover/offer/request/ack nedir, ne işe yarar, neyi garanti etmez?
2. lease lifetimes nedir, ne işe yarar, neyi garanti etmez?
3. client identifiers and MAC addresses nedir, ne işe yarar, neyi garanti etmez?
4. address reuse and legitimate churn nedir, ne işe yarar, neyi garanti etmez?
5. rogue server detection concepts nedir, ne işe yarar, neyi garanti etmez?
6. baseline and anomaly triage nedir, ne işe yarar, neyi garanti etmez?
7. Sonucun güvenilirliğini nasıl artırırsınız?
8. Hangi kontrolü otomatik regresyon testine dönüştürürsünüz?

## Kapsam
Bu lab yalnızca izinli, sentetik veriler içindir. Tek bir bulguyu kesin saldırı kanıtı saymayın.
