# Gün 32 — SNMP Community String ve Maruziyet Denetimi

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **SNMP Community String ve Maruziyet Denetimi** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. SNMP v1 ve v2c düz bir community string ile kimlik doğrular; `public` ve `private` gibi varsayılanlar iyi bilinir.
2. Kimlik doğrulama ve şifreleme içeren SNMPv3'ü tercih et ve servise kimin erişebileceğini kısıtla.
3. Cihaz konfigürasyonlarını varsayılanlar, yazma erişimi ve geniş kaynak aralıkları için denetle.

## Kavramsal ayrımlar
- Salt okunur erişim bile ağ yerleşimini sızdırır.
- Güçlü bir community string bile v2c ile açık metin gönderilir.
- Konfigürasyon denetimi portun erişilebilir olup olmadığını göstermez; ikisini de doğrula.

## Lab uygulaması
Önce `snmp_audit_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 snmp_audit_demo.py
~~~


## Görevler
1. Hangi cihazların bulgu içereceğini tahmin et.
2. Demoyu çalıştırıp her bulguyu not et.
3. Bir v3 cihaz ekle ve bulgu üretmediğini doğrula.
4. Bir güvenlik özelliği için assertion ekle.
5. Bir negatif senaryo ve bir yanlış pozitif ihtimali yaz.
6. Bağımsız bir doğrulama yöntemi öner.

## Kısa sınav
1. Girdi nereden geliyor ve onu kim kontrol ediyor?
2. Doğrudan gözlenen ile çıkarım yapılan arasındaki fark nedir?
3. Hangi varsayımlar gerçek sistemde geçerli olmayabilir?
4. Hangi kanıt tek başına yetersiz kalır?
5. Bir otomatik test neyi kontrol etmeli?

## Etik ve sınırlamalar
Yalnızca izinli sistemlerde ve sentetik verilerle çalış. Bu örnek tam bir tespit veya koruma ürünü değildir.
