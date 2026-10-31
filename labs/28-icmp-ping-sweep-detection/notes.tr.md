# Gün 28 — ICMP Ping Sweep Tespiti

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **ICMP Ping Sweep Tespiti** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Ping sweep, tek bir kaynağın kısa sürede çok sayıda farklı hosta echo isteği göndermesidir.
2. Kayan bir zaman penceresi içinde kaynak başına farklı hedef sayısını say.
3. İzleme sistemleri de çok sayıda hostu pingler; sahibi etiketli bir izin listesi tut.

## Kavramsal ayrımlar
- Tek hosta tekrarlanan ping başka bir desendir (erişilebilirlik kontrolü).
- Sweep ağa ilgi gösterir, tek başına bir saldırı değildir.
- Pencere uzunluğu yavaş sweep'lerin yakalanıp yakalanmayacağını belirler.

## Lab uygulaması
Önce `sweep_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 sweep_demo.py
~~~


## Görevler
1. Hangi kaynakların işaretleneceğini tahmin et.
2. Demoyu çalıştırıp farklı hedef sayılarını not et.
3. Sweep'i daha uzun sürece yay ve tespitin ne zaman durduğuna bak.
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
