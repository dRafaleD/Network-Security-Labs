# Gün 54 — Akış Sayaç Farkları ve Sıfırlanma Belirsizliği

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](counter_deltas.py)

53. günde hayalî ağ akış kayıtlarını sınıflandırdık. Bugün birikimli bayt sayacı ile belirli aralıktaki farkı ayırıyoruz. Aynı kaynak ve açılış döneminde artan sayaçlar çıkarılır. Yeni epoch, ters zaman veya sayaç gerilemesinde trafik miktarı uydurulmaz.

Örnek: zaman 10'da 100 bayt, zaman 20'de 160 bayt → 60. 100 → sıfır. 90 → COUNTER_REGRESSION. Farklı boot → RESET_BOUNDARY.

**Alıştırma:** aynı epoch içinde üç kayıt oluşturup geçerli farkları topla. Araya sıfırlanma ekle ve bu sınırdaki bilinmeyen trafiği açıkla. Sayaç taşması ile sıfırlanmayı ayır. On senaryo vardır; gerçek ağ erişimi yoktur.

## Çalıştır
```bash
python3 labs/54-flow-counter-deltas-and-reset-ambiguity/counter_deltas.py
```
