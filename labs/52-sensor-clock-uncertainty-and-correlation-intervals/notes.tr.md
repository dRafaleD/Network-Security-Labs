# Gün 52 — Sensör Saat Belirsizliği ve Korelasyon Aralıkları

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](clock_intervals.py)

51. günde sensörlerin zaman damgalarını karşılaştırdık. Bugün saat belirsizliğini kapalı zaman aralıklarıyla ifade ediyoruz. Farklı kaynakların aralıkları ortak bir zaman noktasını içermelidir. Aynı sensörün kopyaları tek kaynak olarak sayılır. Ayrık aralıklar veya olay çelişkisi varsa eşleşme yapılmaz. Örtüşme yalnızca POSSIBLE_TIME_MATCH sonucunu verir.

**Sorular:** Saat belirsizliği ile mesaj gecikmesi arasındaki fark ne? Ortak kesişim neden önemli? Zaman uyumu neden aynı olayın kesin kanıtı değildir?

Kaynak kimliklerinin güvenilir bir kolektörden geldiği varsayılır. Gerçek paket yakalama, tarama veya ağ erişimi yoktur.

## Çalıştır
```bash
python3 labs/52-sensor-clock-uncertainty-and-correlation-intervals/clock_intervals.py
```
