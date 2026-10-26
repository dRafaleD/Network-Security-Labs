# Gün 24 — Port Tarama Tespiti: Fan-Out ve Eşikler

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Port Tarama Tespiti: Fan-Out ve Eşikler** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Port taraması, tek kaynağın bir hedefte çok sayıda porta bağlanması; sweep ise tek kaynağın çok sayıda hedefte tek porta bağlanmasıdır.
2. Ham bağlantı sayısı yerine kaynak başına farklı hedef ve port sayısını say.
3. Eşikler, yavaş taramaları kaçırma riski ile tarayıcı ve izleme araçlarından gelen yanlış alarmlar arasında bir denge kurar.

## Kavramsal ayrımlar
- Tek porta çok sayıda bağlantı tekrar eden trafiktir, tarama değildir.
- Yavaş bir tarama kısa pencere eşiğinin altında kalır; pencere uzunluğu önemlidir.
- Yetkili zafiyet tarayıcıları aynı deseni üretir; sahibi belli bir izin listesi gerekir.

## Lab uygulaması
Önce `scan_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 scan_demo.py
~~~


## Görevler
1. Üç kaynak makineden hangilerinin alarm üreteceğini tahmin et.
2. Demoyu çalıştırıp her alarmı not et.
3. `port_threshold` değerini 5'e düşür ve ortaya çıkabilecek yeni yanlış pozitifleri anlat.
4. Tam 19 porta bağlanan kaynağın varsayılan eşikte işaretlenmediğini doğrulayan bir assertion ekle.
5. Yavaş bir taramanın demoyu nasıl atlatabileceğini ve zaman penceresinin nasıl yardımcı olduğunu anlat.
6. Alarmı doğrulamak için bağımsız bir veri kaynağı öner (firewall deny logları, IDS).

## Kısa sınav
1. Girdi nereden geliyor ve onu kim kontrol ediyor?
2. Doğrudan gözlenen ile çıkarım yapılan arasındaki fark nedir?
3. Hangi varsayımlar gerçek sistemde geçerli olmayabilir?
4. Hangi kanıt tek başına yetersiz kalır?
5. Bir otomatik test neyi kontrol etmeli?

## Etik ve sınırlamalar
Yalnızca izinli sistemlerde ve sentetik verilerle çalış. Bu örnek tam bir tespit veya koruma ürünü değildir.
