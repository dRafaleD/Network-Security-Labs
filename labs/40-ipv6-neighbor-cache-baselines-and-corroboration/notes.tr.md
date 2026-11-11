# Gün 40 — IPv6 Komşu Önbelleği, Normal Durum ve Kanıt Doğrulama

[English](notes.md) · [Türkçe](notes.tr.md) · [Çevrimdışı uygulama](neighbor_cache_demo.py)

## 39. günden devam
Önceki gün IPv6 **Neighbor Solicitation (NS)** ve **Neighbor Advertisement (NA)** mesajlarının yapısını gördük. Şimdi bu mesajlarla bağlantılı bir sonuca bakıyoruz: İşletim sisteminin **neighbor cache (komşu önbelleği)**.

Komşu önbelleğinde IPv6 adresi, buna karşılık gelen MAC adresi ve REACHABLE / STALE gibi durum bilgileri bulunabilir. Bu bilgiler ağda iletişim için kullanılır; ancak bir MAC kaydı **kimlik belgesi değildir**.

## Ne zaman inceleme gerekir?
- **Beklenen eşleşme:** IPv6/MAC/port bilinen durumla tutarlı.
- **STALE:** Daha önce öğrenilen eşleşme yakın zamanda teyit edilmemiş. Bu tek başına saldırı göstergesi değildir.
- **MAC değişimi:** Aynı IPv6 için farklı MAC görüldü. Şüpheli olabileceği gibi sanallaştırma, yeni ağ kartı veya bakım nedeniyle de olabilir.
- **Port hareketi:** Switch üzerinde eşleşme farklı porttan gözlemlendi. Fiziksel taşıma veya ağ topolojisi değişikliği de olabilir.
- **Yeni adres:** Henüz envanterde olmayan bir komşu. Otomatik olarak saldırgan kabul edilmez.

Önemli ayrım: **Anomali ≠ saldırı kanıtı.** Özellikle NDP kaynak alanları ağ içindeki bir gönderici tarafından taklit edilebilir.

## Uygulama
~~~bash
python3 neighbor_cache_demo.py
~~~

Program kurgu IPv6 kayıtları üzerinde eşleşme kontrolü yapar. Normal, STALE, farklı MAC, farklı port ve yeni adres örneklerini değerlendirir. Gerçek ağa paket göndermez, komşu tablosunu okumaz ve ayar değiştirmez.

## Görevler
1. Neighbor cache ile doğrulanmış cihaz envanteri aynı şey midir?
2. STALE kaydı neden normal olabilir?
3. MAC veya port değişimini açıklayan meşru senaryolar yaz.
4. Bakım kapsamında geçici izinli değişiklik nasıl tanımlanır?
5. Switch port kayıtları, PCAP, istemci arayüz geçmişi ve ağ yönetimi kayıtlarıyla hangi iddiaları doğrulayabilirsin?
6. Kaynak MAC taklit edilirse bu basit denetimin hangi sınırı ortaya çıkar?

## Güvenlik ve kapsam
Bu kod gerçek NDP parser'ı veya spoofing tespit sistemi değildir. Yalnızca sentetik veriyi karşılaştırır; kesin aktör/saldırı atfında bulunmaz.
