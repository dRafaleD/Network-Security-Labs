# Gün 36 — DNS Yanıtı TTL ve Önbellek Süresinin Korelasyonu

[English](notes.md) · [Türkçe](notes.tr.md) · [Uygulama](dns_ttl_demo.py)

## Öğrenme amacı

Zararsız yerel veriyle **DNS Yanıtı TTL ve Önbellek Süresinin Korelasyonu** konusunun güven sınırlarını ve kanıt değerlendirmesini öğren.

## Temel kavramlar

1. DNS TTL, yanıtın ne kadar süre önbellekte tutulabileceğini belirtir; çözücü politikası ve doğrulama sonucu değiştirebilir.

2. Süresi dolmuş kayıt mutlaka saldırı değildir; yorumdan önce zaman damgası ve önbellek durumunu karşılaştır.

3. Ağ olaylarını ilişkilendirirken tutarlı zaman damgaları ve kaynak bilgisi gerekir.

## Güvenli pratik

Önce kaynak kodunu oku ve sonucu tahmin et:

```bash
python dns_ttl_demo.py
```

Çıktı sentetiktir; gerçek sisteme komut gönderilmez.

## Görevler

1. Girdi verisini ve güvenilmeyen alanları belirle.
2. Bir negatif ya da sınır örneği ekleyip test et.
3. Gözlem ve yorum farkını açıkla.
4. Gerçek ortamda hangi doğrulamaların gerektiğini yaz.

## Kontrol soruları

- Tek gösterge yeterli mi?
- Yanlış pozitif veya eksik kayıt nasıl oluşabilir?
- Sonucu tekrar üretmek için hangi girdileri saklamalısın?

## Güvenlik ve sınırlamalar

Bu çalışma gerçek malware, bulut hesabı, sistem müdahalesi veya dış ağ gerektirmez. Modelin basitliği gerçek platformla birebir eşitlik iddiası taşımaz.
