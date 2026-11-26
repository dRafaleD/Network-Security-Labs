# Gün 55 — Akış Hızı Normalizasyonu ve Eksik Aralıklar

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](rate_review.py)

54. günde sayaç farkları ve yeniden başlatma belirsizliğini inceledik. Bugün hayalî sayaçlarda bayt farkını geçen süreye bölerek tam kesirli ortalama hız hesaplıyoruz. Aynı 100 bayt iki ve beş saniyede farklı hız verir. Boot değişmişse, sayaç gerilemişse veya 10 eğitim saniyesinden uzun boşluk varsa hız hesaplanmaz. 11 sonucu tahmin et ve kesirli bir hız örneği ekle. Eşik eğitim amaçlıdır; ortalama hız anlık sıçramayı veya veri sızıntısını kanıtlamaz. Gerçek ağ erişimi yoktur.

## Çalıştır
```bash
python3 labs/55-flow-rate-normalization-and-missing-intervals/rate_review.py
```
