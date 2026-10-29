# Gün 26 — IP Planlarında CIDR Çakışması Tespiti

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **IP Planlarında CIDR Çakışması Tespiti** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. İki CIDR bloğundan biri diğerinin herhangi bir adresini içeriyorsa çakışırlar.
2. Yanlışlıkla oluşan çakışma yönlendirmeyi bozar ve güvenlik duvarı kurallarını belirsizleştirir.
3. Bilinçli alt dağıtım sessizce kabul edilmek yerine belgelenmelidir.

## Kavramsal ayrımlar
- Bir verinin bulunması, o veriye dayanarak kurulan bütün iddiaları doğrulamaz.
- Önce güven sınırını ve hangi girdiye kimin hükmettiğini belirle.
- Pozitif ve negatif kontrolleri birlikte çalıştır; bir ölçümün sınırlarını kaydet.

## Lab uygulaması
Önce `overlap_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 overlap_demo.py
~~~

## Görevler
1. Kodu inceleyerek beklediğin çıktıyı tahmin et.
2. Çalıştırıp girdileri ve gerçek çıktıları not et.
3. Zararsız bir girdiyi değiştir; farkı ve sebebini açıkla.
4. İlk güvenlik özelliği için assertion ekle.
5. Bir negatif senaryo ve bir yanlış pozitif ihtimali yaz.
6. İkinci bir bağımsız doğrulama yöntemi öner.

## Kısa sınav
1. Bu örnekte giriş verisi nereden geliyor?
2. Hangi davranış doğrudan gözlendi?
3. Hangi varsayımlar gerçek sistemde geçerli olmayabilir?
4. Hangi kanıt yetersiz kalır?
5. Bir otomatik test neyi kontrol etmeli?

## Etik ve sınırlamalar
Yalnızca izinli sistemlerde ve sentetik verilerle çalış. Bu örnek tam bir tespit veya koruma ürünü değildir.
