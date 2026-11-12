# Gün 41 — IPv6 DAD Adres Çakışması ve Kanıt Korelasyonu

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](dad_conflicts_demo.py)

## Önceki günün devamı
40. günde IPv6 komşu önbelleğindeki değişikliklerin başka verilerle doğrulanması gerektiğini öğrendik. Bugün **DAD (Duplicate Address Detection)** kavramını inceliyoruz: cihazın seçtiği IPv6 adresinin başka yerde kullanılıp kullanılmadığını kontrol etmesi.

**Neighbor Discovery (ND):** IPv6 ağında komşu adreslerinin ve yönlendiricilerin bulunması için kullanılan mekanizmalar.
**DAD failure:** adresin çakışma şüphesi doğurduğu bir olay.
**Corroboration:** ikinci, mümkünse bağımsız kanıt kaynağıyla destekleme.

DAD hatası **tek başına saldırı kanıtı değildir**.

## Modelde ne var?
Hayalî olaylar; IPv6 adresi, MAC adresi, olay türü ve zaman içerir. Ayrı bir listede komşu önbelleği gözlemleri bulunur. Kod yalnızca `2001:db8:10::/64` belgeleme ağını kullanır.

Olası çakışma için adreslerin eşit, MAC'lerin farklı ve zamanların beş saniye içinde olması beklenir. Geç gelen bir kayıt **UNCONFIRMED** kalır. Bu eşleşme gerçek cihaz kimliğini kanıtlamaz.

## Sonuçlar
- **CORROBORATED_CONFLICT:** farklı MAC'li yakın zamanlı gözlem var.
- **UNCONFIRMED:** DAD hatası var ama destekleyici kayıt yok.
- **NO_FAILURE:** hata olayı yok.
- **INVALID / OUT_OF_SCOPE:** geçersiz veya deney kapsamı dışındaki adres.

## Çalıştır
~~~bash
python3 labs/41-ipv6-dad-conflicts-and-evidence-correlation/dad_conflicts_demo.py
~~~

## Sorular
1. DAD ile ND'nin farkı nedir?
2. Eski önbellek kaydı analizi nasıl yanıltır?
3. Aynı IPv6 adresinin iki MAC ile görünmesinin saldırı dışı nedenleri neler?
4. Saat kayması sonuçları nasıl etkiler?
5. Bağımsız doğrulama için hangi switch veya host kayıtları gerekir?

## Güvenlik
Kod ağa paket göndermez, bir arayüzü sorgulamaz. Tamamı hayalî kayıtlarla çalışan yerel bir alıştırmadır.
