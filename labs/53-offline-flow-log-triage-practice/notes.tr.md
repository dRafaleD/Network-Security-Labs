# Gün 53 — Uygulama Günü: Çevrimdışı Akış Logu İncelemesi

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](flow_triage.py)

RFC 5737 dokümantasyon adresleri ile oluşturulmuş 12 hayalî akış kaydını incele. IP, protokol ve sayaçları doğrulayıp trafiğin laboratuvar ağına göre yönünü belirle. Yalnızca geçerli ve boş olmayan kayıtların baytlarını topla.

| Örnek | Beklenen |
|---|---|
| Lab → lab | LAB_INTERNAL |
| Lab → peer | LAB_OUTBOUND |
| Peer → lab | LAB_INBOUND |
| Peer → peer | PEER_INTERNAL |
| Sıfır paket ve bayt | EMPTY_FLOW |
| Negatif bayt | INVALID_COUNTER |

**Alıştırmalar:** 12 satırı elle sınıflandır. Bayt toplamlarını karşılaştır. 60 baytlık geçerli inbound akış ekleyip beklenen toplamı güncelle. Geçersiz IP ekleyip toplamdan çıkarıldığını doğrula. Outbound akış neden tek başına veri sızıntısı kanıtı değildir?

Orijinal toplamlar: internal 100, outbound 200, inbound 150, peer 80 bayt. Gerçek ağ bağlantısı veya paket yakalama yoktur.

## Çalıştır
```bash
python3 labs/53-offline-flow-log-triage-practice/flow_triage.py
```
