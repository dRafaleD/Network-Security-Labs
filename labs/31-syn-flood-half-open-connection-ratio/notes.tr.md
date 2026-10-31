# Gün 31 — SYN Flood: Yarı Açık Bağlantı Oranı

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **SYN Flood: Yarı Açık Bağlantı Oranı** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. SYN flood çok sayıda bağlantıyı yarı açık bırakır: SYN'ler gelir ama el sıkışma hiç tamamlanmaz.
2. Hedef başına SYN sayısını tamamlanan el sıkışmalarla karşılaştır; çok düşük tamamlanma oranı bir sinyaldir.
3. SYN cookie'ler ve hız sınırları önlemdir; tespit onları ne zaman uygulayacağını söyler.

## Kavramsal ayrımlar
- Port taramaları da cevapsız SYN üretir ama çok sayıda portta.
- Yük altındaki bir sunucu flood'a benzeyebilir.
- Sahte kaynak adresler atfı güvenilmez kılar.

## Lab uygulaması
Önce `synflood_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 synflood_demo.py
~~~


## Görevler
1. Hangi hedefin işaretleneceğini tahmin et.
2. Demoyu çalıştırıp tamamlanma oranlarını not et.
3. Eşiği düşür ve yanlış pozitifleri anlat.
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
