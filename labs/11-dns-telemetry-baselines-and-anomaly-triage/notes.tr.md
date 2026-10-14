# Gün 11 — DNS Telemetri, NXDOMAIN Baseline ve Anomaly Triage

[English](notes.md) · [Türkçe](notes.tr.md)

**Amaç:** Gün 6 DNS temellerini ve Gün 10 monitoring mantığını birleştirerek savunma odaklı DNS telemetry yorumlamak.

**Güvenli kapsam:** İnternete DNS isteği gönderilmez. Bütün client IP/domain ve zamanlar sentetiktir.

## 1. DNS telemetri alanları

Resolver loglarında zaman, istemci, sorgu adı, record türü ve response code bulunabilir. Gözlem noktası önemlidir: recursive resolver çok istemciyi, endpoint ise çoğunlukla kendisini görür.

## 2. NXDOMAIN ve hata oranı

NXDOMAIN sorgulanan alan adının bulunamadığı anlamına gelir. Çok görülmesi typo, yanlış yapılandırma, retry veya farklı yazılımlardan kaynaklanabilir. Tek başına malware kanıtı değildir.

## 3. Baseline için payda önemli

Bir istemcinin NXDOMAIN sayısını toplam sorguya ve zaman aralığına böl. 12 sorgudaki 10 hata ile 10.000 sorgudaki 10 hata aynı anlama gelmez. Varlık türü ve iş yükü de baseline'ı değiştirir.

## 4. Burst tespiti

Sliding window günlük toplamda kaybolan kısa süreli yoğunluğu görmeye yarar. Labda iki dakikalık penceredeki NXDOMAIN kayıtları sayılır. Burst görmek otomatik saldırgan ataması değildir.

## 5. Periyodik trafik ve meşru işler

Düzenli aralıklarla sorgu görünmesi beaconing'i akla getirebilir; ama update veya health check de aynı paterni üretir. Process, asset owner ve destination bilgisi olmadan karar verme.

## 6. DNS cache ve resolver gözlemi

Cache yüzünden her application lookup upstream log üretmeyebilir. Resolver forwarding, NAT ve ortak çıkış adresi client attribution'ı zorlaştırır. Bir DNS kaydı = bir insan işlemi değildir.

## 7. Encrypted DNS görünürlüğü

DoH/DoT client ile resolver arasındaki DNS içeriğini şifreler. Passive sensor isimleri görmeyebilir; izinli endpoint/resolver logları yardımcı olabilir. Eksik PCAP'tan tam görünürlük iddia etme.

## 8. Mahremiyet

DNS logları ziyaret edilen kaynakları ve özel uygulamaları açığa çıkarabilir. Saklama süresini ve erişimi sınırla. Burada sentetik .example.test domain'leri kullan; gerçek kullanıcı DNS loglarını repoya yükleme.

## 9. Triage ve farklı kaynakları ilişkilendirme

Sensor coverage ve timezone'u doğrula. Gerekirse izinli DHCP lease/asset kayıtlarıyla client IP'yi ilişkilendir. DNS zamanlarını proxy, flow ve endpoint ile karşılaştır; observation ile hypothesis'i ayır.

## 10. Açıklanabilir threshold

Eğitim eşikleri küçük sentetik veri için seçildi. Production detection olarak kullanma. Gerçek dünyada representative baseline ile false positive ölç ve değişen yazılım/ağ ortamında yeniden değerlendir.

## Uygulama akışı

Lab klasöründe Python 3 ile:

```bash
python3 generate_dns_events.py
python3 analyze_dns_events.py
```

Generator timestamp+UTC offset içeren JSONL kayıtları üretir. Analyzer client başına query count, NXDOMAIN oranı ve 2 dakikalık en yoğun pencereyi hesaplar. Kod gerçek ağ verisi toplamaz.

Beklenen gruplar:
- `10.10.0.10`: normal iş yükü ve tek typo.
- `10.10.0.20`: çoğunlukla başarılı resolver trafiği.
- `10.10.0.30`: iki dakika içinde çok sayıda NXDOMAIN (triage sinyali).
- `10.10.0.40`: periyodik ama benign olarak kurgulanmış heartbeat.

Bu adresler sentetik training etiketleridir. Tool “zararlı” kararı vermez.

### Wireshark/tcpdump bağlantısı

Yalnız **kendi izinli ve yerel** DNS capture'larında paket başlıkları için şu Wireshark filtrelerini inceleyebilirsin:

```text
dns
dns.flags.rcode == 3
udp.port == 53
```

DNS port 53 üzerindeki bütün trafiği görebileceğin anlamına gelmez; DoH/DoT ve cache gözlem farkı oluşturabilir.

### Mini challenge

1. İki dakika yerine bir dakika burst penceresi kullan; hangi işaretlerin değiştiğini açıkla.
2. Yeni bir client için 100 başarılı ve 3 başarısız sorgu ekle; oran ile ham count karşılaştır.
3. `10.10.0.40` periyodik sorgularını analiz edip neden otomatik beaconing verdict olmayacağını yaz.
4. Client IP'nin NAT/lease nedeniyle yanlış attribution'a yol açabileceği bir senaryo çiz.

### Alıştırmalar

1. Log şemasını oku.
2. UTC offset'i tanımla.
3. NXDOMAIN'i açıkla.
4. Client bazında count hesapla.
5. Ratio hesapla.
6. Sliding window yaklaşımını açıkla.
7. En yoğun client'ı bul.
8. False positive senaryosu üret.
9. DNS cache etkisini anlat.
10. DoH visibility farkını anlat.
11. DHCP ve endpoint ile correlation planla.
12. Triage raporu hazırla.

### Tekrar soruları

1. NXDOMAIN nedir?
2. DNS telemetry nereden toplanır?
3. Recursive resolver ne görür?
4. Baseline nedir?
5. Count ve ratio farkı?
6. Sliding window niye kullanılır?
7. False positive ne zaman olur?
8. Periodic query neden otomatik C2 değildir?
9. DNS cache sonucu nasıl etkiler?
10. NAT attribution'ı nasıl zorlaştırır?
11. DoH hangi gözlemi engeller?
12. Timezone neden gerekli?
13. Bir DNS kaydı tek kullanıcı eylemi midir?
14. Triage için hangi loglar yararlı?
15. Production threshold nasıl değerlendirilir?

**Ana çıkarım:** DNS anomaly tespitinde istatistik, gözlem noktası ve ek delil gerekir; yüksek NXDOMAIN tek başına saldırı hükmü değildir.
