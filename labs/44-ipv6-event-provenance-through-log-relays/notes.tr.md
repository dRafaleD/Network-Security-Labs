# Gün 44 — IPv6 Log Aktarıcılarında Olay Kaynağını İzleme

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](relay_provenance_demo.py)

## 43. günden devam
Önceki gün aynı olayın kopya loglar nedeniyle iki kez sayılmaması gerektiğini öğrendik. Şimdi **log relay (aktarıcı)** kavramını ekliyoruz. Bir sensör aynı kaydı iki farklı log toplayıcısına gönderebilir.

**Upstream source:** gözlemi ilk üreten kaynak. **Collector:** kaydı alan/toplayan sistem. **Provenance:** kaydın nereden geldiği.

İki farklı toplayıcıda aynı `upstream` varsa kod bunu **tek kaynak** olarak sayıyor. İkinci sensörden kayıt gelirse `MULTI_ORIGIN` diyor. Ancak sensör isimleri de sahte olabilir; bu sonuç saldırganın kimliğini veya fiziksel kaynakların bağımsızlığını kanıtlamaz.

Önce DAD_FAIL, aynı IPv6 adresi, farklı MAC ve belirsizlikli 5 saniye penceresi kontrol edilir. Kaynağı bilinmeyen loglar bağımsız kanıt olarak sayılmaz.

## Çalıştırma
~~~bash
python3 labs/44-ipv6-event-provenance-through-log-relays/relay_provenance_demo.py
~~~

## Sorular
Log toplayıcısı ile olayın asıl kaynağı arasındaki fark nedir? Tek kayıt iki toplayıcıya ulaşırsa neden iki kanıt sayılmaz? Sahte upstream ID analizi nasıl yanıltabilir?

## Güvenlik
Gerçek IPv6 ağına erişmez; yalnızca hayalî kayıtlarla çalışır.
