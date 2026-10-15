# Gün 12 — Akış Korelasyonu, TCP/TLS Metadata ve PCAP Delili

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

Bu gün önceki labların üzerine inşa edilen, yalnızca yerel ve zararsız eğitim verisi kullanan uygulamalı bir çalışmadır. Kodun her varsayımını incele; çıktıları otomatik güvenlik kanıtı sayma.

## Öğrenme hedefleri

- Five-tuple
- Bidirectional sessions
- TCP context
- TLS observability
- DNS linkage
- NAT vantage points
- Baseline and anomaly
- Evidence language

## Veri akışı ve tehdit modeli

```text
controlled training input
        ↓
parser / evaluator / analyst
        ↓
security or evidence check
        ↓
observable result
        ↓
review assumptions and limits
```

## 1. Five-tuple

Kaynak/hedef IP, port ve protokolü kaydet; akışı kişiyle eşitleme.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 2. Bidirectional sessions

Gidiş/dönüş trafiğini eşleştir; cevapta adres ve portların neden yer değiştirdiğini açıkla.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 3. TCP context

SYN, retransmission, FIN ve RST farklı bağlantı durumu kanıtlarıdır.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 4. TLS observability

Uygulama içeriği şifreli olsa da boyut, uç nokta ve zaman görünür kalabilir.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 5. DNS linkage

DNS cevabı ipucudur; bağlantının kesin tek bir domaine ait olduğu kanıtı değildir.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 6. NAT vantage points

İzleme noktalarına göre özel/çevrilmiş IP farklıdır; arayüz ve yönü kaydet.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 7. Baseline and anomaly

Hedeflere göre sayı/bayt karşılaştır; sıra dışı sıklık karar değil araştırma sinyalidir.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 8. Evidence language

Zaman dilimi, toplama yöntemi, varsayım ve yorum sınırlarını raporla.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## Uygulama

Yalnızca repo içindeki dosyaları kullan. Bu örnek üretim ortamına kurulacak güvenlik servisi değildir.

```bash
python3 flow_summary.py
```

## Test matrisi

| Senaryo | Beklenen | Neden |
|---|---|---|
| Valid training input | Kabul / eşleşme | Baseline |
| Wrong owner or header | Ret / eşleşmeme | Scope / structure |
| Truncated or missing field | Kontrollü hata | Input validation |
| Unrelated benign sample | Yanlış alarm yok | False-positive awareness |

## Alıştırmalar

1. Örneği çalıştır ve çıktıyı kaydet.
2. İlk varsayımını not et.
3. Olumlu senaryoyu doğrula.
4. Bir negatif senaryo ekle.
5. İkinci negatif senaryo ekle.
6. Bir sınır değeri dene.
7. İlgili kontrolü kaynak kodunda bul.
8. Gözlem ve çıkarımı ayrı yaz.
9. Tek bir kontrolü çalışma kopyasında değiştir.
10. Bütün senaryoları tekrar test et.
11. Sonuçların sınırlamalarını yaz.
12. Bir sayfalık kısa analiz raporu hazırla.

## Tekrar soruları

1. Bu labda hangi güven sınırı var?
2. Hangi veri kullanıcı tarafından kontrol ediliyor?
3. Olumlu testin amacı ne?
4. Negatif testin amacı ne?
5. Çıktı neyi gerçekten kanıtlıyor?
6. Çıktı neyi kanıtlamıyor?
7. En kritik input hangisi?
8. Bir sınır değeri örneği ver.
9. Fail-closed davranış nedir?
10. Bu labı prod ortamına doğrudan almak neden riskli?
11. Bir false positive senaryosu düşün.
12. Bir false negative senaryosu düşün.
13. Log hangi alanları taşımalı?
14. Hangi kişisel veri gereksiz?
15. Sürüm bilgisi niçin kaydedilir?
16. Kontrol değişince hangi testler tekrar koşulmalı?

## Mini projeler

1. Bir yeni negatif test ve beklenen çıktı ekle; çalıştırıp belgele.
2. Bir güvenlik varsayımını çalışma kopyasında boz; hangi testin yakaladığını açıkla.
3. Kaynak, hash, araç sürümü, komut, gözlem ve sınırlamalardan oluşan kısa rapor yaz.

## Özet

Kendi aracının gerçek davranışını ölç; sentetik örneği aşırı genelleme. Güvenlik kararı, izin ve adli çıkarım bağımsız doğrulama gerektirir.
