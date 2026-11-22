# Gün 50 — Sensör Anahtar Yenileme Sonrası Kanıt Bağımsızlığı

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](sensor_provenance_demo.py)

## 49. günden devam
Önceki gün eski sensör anahtarını iptal ettik. Şimdi başka bir durum var: sensör A'nın olayı iki ayrı relay'den gelirse **iki bağımsız tanık** sayılır mı? Hayır.

**Provenance:** mesajın asıl kaynağı. **Relay fanout:** aynı mesajın birden çok aktarıcıdan ulaşması. **Corroboration:** bağımsız kaynakların aynı iddiayı desteklemesi.

Uygulama, relay'in hangi sensöre ait olduğunu kendi güvenilir listesinde tutuyor. Sensör A'nın iki kopyası `SINGLE_SENSOR`; A ve B aynı olayı destekliyorsa `CORROBORATED` oluyor. Sensörler çelişirse ayrı hata veriliyor. A emekliye ayrılınca eski geçerli HMAC de ona yeniden yetki sağlamıyor.

## Çalıştır
```bash
python3 labs/50-sensor-provenance-after-key-rotation-and-relay-fanout/sensor_provenance_demo.py
```

## Sorular
Geçerli HMAC neden iki bağımsız kanıt anlamına gelmez? Eski sensör kaydı neden hâlâ geçerli HMAC içerse bile reddedilmeli? Farklı sensörler ortak bir hataya sahip olabilir mi?

## Sınır
Gerçek ağ trafiği ve anahtar kullanılmaz; veriler tamamen sentetiktir.
