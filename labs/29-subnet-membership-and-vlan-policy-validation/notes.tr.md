# Gün 29 — Alt Ağ Üyeliği ve VLAN Politikası Doğrulama

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Alt Ağ Üyeliği ve VLAN Politikası Doğrulama** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Her VLAN bir alt ağa karşılık gelir; adresi dışında kalan host yanlış yapılandırma veya sahte adres işaretidir.
2. Dize öneklerini kullanmak yerine gerçek bir IP kütüphanesi kullan; `10.0.1.5` ve `10.0.10.5` aynı öneki paylaşır.
3. Beklenen eşlemeyi doğruluk kaynağından dışa aktar ve düzenli kontrol et.

## Kavramsal ayrımlar
- Statik eşleme tabloları eskir; kontrol niyeti değil drift'i bulur.
- Birden çok arayüzlü hostlar her arayüz için bir kayıt ister.
- Geçen bir kontrol VLAN'lar arası firewall kuralları hakkında bir şey söylemez.

## Lab uygulaması
Önce `vlan_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 vlan_demo.py
~~~


## Görevler
1. Hangi hostların eşlemeyi ihlal ettiğini tahmin et.
2. Demoyu çalıştırıp her ihlali not et.
3. Farklı VLAN'larda iki arayüzü olan bir host ekle.
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
