# Gün 42 — IPv6 Çakışma Zaman Çizelgesi ve Saat Belirsizliği

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](clock_correlation_demo.py)

## 41. günden devam
DAD hatası ve aynı adrese ait farklı MAC gözlemi birbirine yakın görünebilir. Ancak cihaz saatleri farklı olabilir. Bu lab, her kayda **zaman belirsizliği** (± saniye) ekler.

**DEFINITELY_NEAR:** olası en büyük saat farkı bile beş saniyeyi aşmıyor.
**POSSIBLY_NEAR:** belirsizlik dikkate alınınca beş saniye içinde olma ihtimali var.
**OUTSIDE_WINDOW:** hiçbir olası zaman farkı pencereye sığmıyor.

Aynı IPv6 adresi, farklı MAC ve DAD_FAIL olayı önce doğrulanır.

## Çalıştır
```bash
python3 labs/42-ipv6-conflict-timeline-and-clock-uncertainty/clock_correlation_demo.py
```

## Sorular
Saat kayması hangi eşleşmeleri belirsiz kılar? NTP ve cihaz logları hangi noktada faydalı? Bu kayıtlar neden saldırgan kimliği kanıtlamaz?

## Güvenlik
Sekiz hayalî test kullanır; ağ paketi göndermez veya gerçek arayüzleri sorgulamaz.
