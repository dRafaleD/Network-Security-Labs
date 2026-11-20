# Gün 48 — Sensör Boot Kayıt Onayı ve Tek Kullanımlık Challenge

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](enrollment_demo.py)

## 47. günden devam
Önceki gün sensör yeniden başlatılınca farklı **boot ID** ile sıra numarasının tekrar 1 olabileceğini gördük. Ama yeni boot ID'yi sensörün mesajında yazması tek başına yetki değildir.

**Enrollment:** yeni açılış döneminin güvenilir kontrol sistemine kaydedilmesi. **Challenge nonce:** yalnızca bir kez kullanılacak doğrulama değeri. **Replay resistance:** eski mesajları yeniden kabul etmemek.

Modelde kontrol sistemi belirli süresi olan challenge verir. Sensör boot ID ve nonce'u HMAC ile doğrular. Challenge başarılı olunca tek kullanımlık olarak işaretlenir, aktif boot güncellenir. Eski boot'a ait olaylar reddedilir; yeni boot'ta sıra numarası 1 tekrar kullanılabilir.

## Çalıştır
```bash
python3 labs/48-boot-enrollment-challenges-and-replay-resistance/enrollment_demo.py
```

## Sorular
Yeni boot ID neden tek başına yeterli değildir? Challenge neden tahmin edilemez ve tek kullanımlık olmalı? Kontrol sistemindeki kayıtlar kaybolursa ne olur?

## Sınırlar
Gerçek anahtar, rastgele nonce veya ağ paketi kullanılmaz; yalnızca sentetik HMAC örneğidir.
