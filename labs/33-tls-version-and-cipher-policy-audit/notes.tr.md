# Gün 33 — TLS Sürümü ve Cipher Politikası Denetimi

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **TLS Sürümü ve Cipher Politikası Denetimi** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. TLS 1.2 ve 1.3'e izin ver; SSLv3, TLS 1.0 ve 1.1'i reddet.
2. RC4, 3DES ve export sınıfı gibi zayıf cipher'ları reddet ve forward secrecy'yi tercih et.
3. Yalnızca dokümantasyonu değil, her uç noktanın gerçekte sunduklarını denetle.

## Kavramsal ayrımlar
- Eski bir sürümü desteklemek yalnızca istemciler ona düşürülebiliyorsa risktir.
- Politika denetimi sertifikaları veya host adlarını doğrulamaz.
- Eski istemciler son kullanma tarihli belgelenmiş bir istisna isteyebilir.

## Lab uygulaması
Önce `tls_policy_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 tls_policy_demo.py
~~~


## Görevler
1. Hangi uç noktaların politikayı geçemeyeceğini tahmin et.
2. Demoyu çalıştırıp nedenleri not et.
3. Son kullanma tarihli bir istisna ekle ve dikkate alındığını göster.
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
