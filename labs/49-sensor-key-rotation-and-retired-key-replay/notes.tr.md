# Gün 49 — Sensör Anahtarı Yenileme ve Eski Anahtarlı Replay

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](rotation_replay_demo.py)

## 48. günden devam
Önceki gün sensörün yeni boot dönemini challenge ile doğruladık. Şimdi **HMAC anahtarının yenilenmesi** konusuna geçiyoruz.

**Key rotation:** eski anahtardan yeniye kontrollü geçiş. **Retired key:** artık yetkili olmayan eski anahtar. **Replay:** önceden geçerli olan olayın tekrar gönderilmesi. **Active-key registry:** hangi anahtarın güncel olduğunu tutan güvenilir uygulama kaydı.

Başlangıçta `key-1` geçerli. Güncellemeden sonra `key-2` etkinleşiyor. Eski anahtar hâlâ matematiksel olarak doğru HMAC üretse bile sistem **RETIRED_OR_INACTIVE_KEY** diyerek reddediyor. Yeni anahtarlı olaylarda ise sıra numarası ve zaman kontrolü devam ediyor.

## Çalıştırma
```bash
python3 labs/49-sensor-key-rotation-and-retired-key-replay/rotation_replay_demo.py
```

## Sorular
Doğru HMAC neden tek başına yetki değildir? Aktif anahtar listesi neden mesajın içinden alınmamalı? Sensör yeniden başlarsa hangi kayıtlar korunmalı?

## Sınırlar
Gerçek anahtar, ağ paketi veya sensör kullanılmaz; güvenli anahtar yönetimi simüle edilmez.
