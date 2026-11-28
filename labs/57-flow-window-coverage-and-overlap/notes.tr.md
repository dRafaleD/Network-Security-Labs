# Gün 57 — Akış Penceresi Kapsaması ve Örtüşme

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](window_coverage.py)

56. günde ağırlıklı akış hızları ve kapsama vardı. Bugün yarı açık gözlem aralıklarının birleşimini hesaplıyoruz. [0,6) ve [4,10) toplam 12 değil 10 saniyeyi kapsar. Örtüşen sayaçların baytlarını doğrudan toplamayız; inceleme gerekir. On örneği tahmin et, sırasız aralıklar ekle ve boş gözlemi tam kapsamla karşılaştır. Zaman kapsamı her paketin kaydedildiğini kanıtlamaz. Gerçek ağ erişimi yoktur.

## Çalıştır
```bash
python3 labs/57-flow-window-coverage-and-overlap/window_coverage.py
```
