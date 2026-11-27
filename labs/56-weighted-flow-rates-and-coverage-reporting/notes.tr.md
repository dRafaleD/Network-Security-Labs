# Gün 56 — Ağırlıklı Akış Hızları ve Kapsama Raporu

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](weighted_rates.py)

55. günde sayaç farklarını süreye böldük. Bugün tek hayalî akışın geçerli, örtüşmeyen aralıklarını birleştiriyoruz. 2 saniyede 100 ve 8 saniyede 100 bayt için ağırlıklı hız 20 bayt/sn olur; hızların basit ortalaması 31,25 yanlıştır. Boşluklar kapsanan süre / toplam zaman olarak ayrıca raporlanır; eksik kayıt sıfır trafik değildir. Sekiz senaryoyu çalıştır, boşluk ekle ve kapsama oranını karşılaştır. Girdi önceden doğrulanmış tek akış varsayılır; canlı ağ, tarama veya kişi atfı yoktur.

## Çalıştır
```bash
python3 labs/56-weighted-flow-rates-and-coverage-reporting/weighted_rates.py
```
