# Gün 43 — IPv6 Kanıt Kayıtlarını Tekilleştirme ve Kaynak Bağımsızlığı

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](evidence_dedup_demo.py)

## 42. günden devam
Önceki gün saat belirsizliğiyle olayları eşleştirdik. Şimdi **aynı olayın kopya loglarla birden fazla kez sayılmaması** gerektiğini öğreniyoruz.

**Deduplication (tekilleştirme):** tekrar kayıtlarını ayırmak. **Provenance (kaynak kökeni):** kaydın nereden geldiğini bilmek. **Independent evidence (bağımsız kanıt):** gerçekten ayrı gözlem kaynaklarından gelen veri.

Kod DAD_FAIL, IPv6 adresi, MAC farkı ve zaman aralığını kontrol eder; sonra kayıt sayısı yerine benzersiz `origin` değerlerini sayar. Aynı kaydın kopyası ikinci doğrulama sayılmaz.

## Çalıştırma
~~~bash
python3 labs/43-ipv6-evidence-deduplication-and-source-independence/evidence_dedup_demo.py
~~~

## Sorular
Aynı log iki kez gönderilince neden iki kanıt olmaz? Farklı log kaynağı isimleri niçin tam bağımsızlık ispatlamaz? İki gözlem saldırganı tanımlar mı?

## Sınırlar
Yalnızca hayalî IPv6 olay kayıtları içerir; ağa paket göndermez. Sonuçlar olay atfı veya saldırı kanıtı değildir.
