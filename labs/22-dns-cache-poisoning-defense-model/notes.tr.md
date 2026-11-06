# Gün 22 — DNS Önbelleği Güven Sınırları ve Zehirlenmeye Karşı Kontroller

[English](notes.md) · [Türkçe](notes.tr.md)

## Amaç
DNS yanıtlarının neden doğrulanması gerektiğini, önbellek ömrünün (**TTL**) ve veri kaynağının güvenlikteki rolünü incelemek. Tüm kayıtlar sentetiktir.

## Kavramlar
- **DNS önbelleği**, önceden çözümlenen adların yanıtlarını saklar; hatalı kayıt da saklanabilir.
- Yanıtın beklenen sorguyla eşleşmesi, süre sınırlaması ve **DNSSEC** doğrulaması farklı kontrol katmanlarıdır.
- **DNSSEC**, uygun şekilde doğrulandığında imzalı DNS verisinin bütünlüğünü ve kaynağını denetler; trafiği şifrelemez.
- **DoH/DoT**, aktarım yolunu korur; kötü niyetli yetkili sunucudan gelen yanlış içeriği tek başına düzeltmez.
- TTL dolması ve eski kayıtlar adli incelemede önemli olabilir.

## Uygulama
```bash
python3 dns_cache_demo.py
```
Program ağ trafiği üretmez. `validated` alanı, gerçek kriptografik kontrol yerine **simüle edilmiş** güvenilir çözücü sonucudur.

## Ödev
1. Uzun TTL içeren doğrulanmamış yanıtın neden reddedildiğini açıkla.
2. Süre dolduktan sonraki davranışı gözlemle.
3. DNSSEC ile DoH farkını anlat.
4. Gerçek DNS altyapısı için hangi loglara ihtiyaç olacağını yaz.

## Güvenlik
Yalnızca çevrimdışı simülasyon; DNS sunucularına saldırı yok.
