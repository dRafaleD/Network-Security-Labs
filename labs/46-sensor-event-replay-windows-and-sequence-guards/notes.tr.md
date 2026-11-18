# Gün 46 — Sensör Olaylarında Replay Penceresi ve Sıra Numarası

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](replay_guard_demo.py)

## 45. günden devam
HMAC geçerli bir logun değiştirilmediğini kontrol etmeye yardım eder. Ancak aynı geçerli olay **ikinci kez gönderilebilir**. Buna **replay** denir.

**Replay cache:** daha önce görülen olay kimliklerinin kayıt edildiği alan. **Sequence number:** sensörün olay sıra numarası. **Freshness window:** bir olayın zaman bakımından ne kadar eski veya ileri olabileceğini belirleyen süre.

Kod HMAC'i doğrular, olay zamanını ±10 saniye içinde arar ve `(sensor, sequence)` ikilisinin daha önce kaydedilip kaydedilmediğini kontrol eder. Aynı sıra numarası farklı sensörlerde kullanılabilir. HMAC doğru olsa bile tekrar olaylar reddedilir.

## Çalıştır
~~~bash
python3 labs/46-sensor-event-replay-windows-and-sequence-guards/replay_guard_demo.py
~~~

## Sorular
HMAC neden replay'i tek başına durdurmaz? Saat kayması doğrulamayı nasıl etkiler? Collector kapanıp açılınca bellekteki geçmiş sıfırlanırsa ne olur?

## Sınır
IPv6 adresleri belgeleme amaçlıdır; gerçek ağ paketi veya sensör anahtarı kullanılmaz.
