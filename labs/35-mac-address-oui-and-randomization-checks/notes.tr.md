# Gün 35 — MAC Adresi OUI ve Rastgeleleştirme Kontrolleri

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **MAC Adresi OUI ve Rastgeleleştirme Kontrolleri** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. MAC adresinin ilk üç baytı (OUI) üreticiyi belirtir ve bir arama tablosu cihazları etiketleyebilir.
2. İlk baytın ikinci en düşük anlamlı biti yerel olarak atanmış adresi işaretler; bu, rastgeleleştirilmiş MAC'lerde tipiktir.
3. MAC'ini değiştiren cihaz birçok cihaz gibi görünür; envanterler bunu hesaba katmalıdır.

## Kavramsal ayrımlar
- MAC adresi elle kolayca ayarlanır; kimliğin kanıtı değil etiket olarak ele al.
- Bilinmeyen bir OUI yeni bir üreticiyi veya rastgeleleştirilmiş adresi gösterebilir.
- Lab örneklerinde dokümantasyon tarzı adresler kullan.

## Lab uygulaması
Önce `mac_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 mac_demo.py
~~~


## Görevler
1. Hangi adreslerin yerel olarak atanmış olduğunu tahmin et.
2. Demoyu çalıştırıp her adres için üretici etiketini not et.
3. Bir multicast adres ekle ve bit testinin onu nasıl ele aldığına bak.
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
