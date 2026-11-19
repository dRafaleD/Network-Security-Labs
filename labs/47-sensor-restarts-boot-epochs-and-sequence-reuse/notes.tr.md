# Gün 47 — Sensör Yeniden Başlatma ve Boot Kimliği

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](boot_epoch_demo.py)

## 46. günden devam
Önceki gün HMAC, zaman ve olay sıra numarasıyla replay kontrolü yaptık. Ama gerçek bir sensör yeniden başlatılınca sayaç **tekrar 1'den** başlayabilir.

**Boot ID:** sensörün belirli açılış dönemini gösteren kimlik. **Epoch:** nesil/dönem. **Replay identity:** tekrar kaydını tanımlamak için kullanılan `(sensör, boot ID, sıra numarası)` üçlüsü.

Uygulamanın ayrı ve güvenilir **ACTIVE_BOOT** kaydı hangi açılışın geçerli olduğunu belirler. Sensörün mesajda kafasına göre yazdığı boot ID kabul edilmez; mesaj ayrıca HMAC ile doğrulanır. Eski boot döneminden gelen kayıtlar yeniden oynatılsa reddedilir.

## Çalıştır
```bash
python3 labs/47-sensor-restarts-boot-epochs-and-sequence-reuse/boot_epoch_demo.py
```

## Sorular
Sayaç sıfırlanması neden her zaman saldırı değildir? Boot ID neden güvenilir kayıtla eşleştirilmeli? HMAC anahtarı sızarsa ne olabilir?

## Sınır
Gerçek paket, ağ, sensör veya gizli anahtar yoktur. Tamamen eğitim simülasyonudur.
