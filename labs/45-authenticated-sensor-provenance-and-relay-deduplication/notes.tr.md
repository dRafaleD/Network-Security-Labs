# Gün 45 — Sensör Kaynağını HMAC ile Doğrulama ve Log Tekilleştirme

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](sensor_auth_demo.py)

## 44. günden devam
Önceki gün logu taşıyan **collector** ile asıl **sensor (üretici)** arasındaki farkı öğrendik. Ancak logdaki `sensor-a` yazısı tek başına gerçek kaynak kanıtı değildir. Bu gün hayalî sensör kayıtlarına **HMAC** doğrulaması ekliyoruz.

Her sensörün farklı bir örnek anahtarı var. HMAC; producer, event ID, IPv6 adresi, MAC ve zamanı kapsıyor. Kayıt değişirse doğrulama başarısız olur. Aynı olay başka bir collector üzerinden gelirse **ikinci bağımsız kanıt olarak sayılmaz**.

**Deduplication:** tekrarlanan aynı olayları birleştirme. **Authenticated provenance:** kayıt kaynağının, önceden güvenilen anahtar ile doğrulanması. HMAC anahtarı ele geçirilirse geçerli görünen sahte olay üretilebilir.

## Çalıştırma
~~~bash
python3 labs/45-authenticated-sensor-provenance-and-relay-deduplication/sensor_auth_demo.py
~~~

## Sorular
Bir log kaynağının adı neden yeterli değil? HMAC geçerli bir kaydın tekrar gönderilmesini tek başına önler mi? Sensör anahtarı çalınırsa nasıl davranılmalı?

## Sınır
Gerçek anahtar, ağ bağlantısı veya saldırı trafiği yoktur. Çoklu doğrulama aktör kimliği kanıtı değildir.
