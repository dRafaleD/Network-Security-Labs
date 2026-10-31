# Gün 27 — DNS Tünelleme Sezgileri: Etiket Uzunluğu ve Entropi

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **DNS Tünelleme Sezgileri: Etiket Uzunluğu ve Entropi** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. DNS tünelleri veriyi uzun ve yüksek entropili alt alan adı etiketlerine yerleştirir; bu yüzden uzunluk ve karakter rastgeleliği ilk sinyallerdir.
2. Her sorgu adını etiket uzunluğu ve Shannon entropisi ile puanla, sonra kayıtlı alan adı başına topla.
3. İçerik dağıtım ağları ve bazı güvenlik ürünleri de uzun rastgele etiketler kullanır; bilinen servisleri izin listesine al.

## Kavramsal ayrımlar
- Tek bir uzun ad zayıf bir kanıttır; tek alan adı altında çok sayıda farklı uzun ad daha güçlüdür.
- Eşikler kendi trafik taban çizginde ayarlanmalıdır.
- Şifreli DNS, adları bu kontrolden tamamen gizler.

## Lab uygulaması
Önce `dns_tunnel_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 dns_tunnel_demo.py
~~~


## Görevler
1. Hangi alan adlarının şüpheli tünel olarak işaretleneceğini tahmin et.
2. Demoyu çalıştırıp her alan adı için entropi ve etiket uzunluğunu not et.
3. Entropi eşiğini düşür ve ortaya çıkan yeni yanlış pozitifleri anlat.
4. `www.example.test` adının işaretlenmediğini doğrulayan bir assertion ekle.
5. Saldırganın kontrolü atlatmak için etiketleri nasıl kısa ve düşük entropili tutabileceğini anlat.
6. Bağımsız bir sinyal öner (alan adı başına sorgu hacmi veya TXT kaydı kullanımı gibi).

## Kısa sınav
1. Girdi nereden geliyor ve onu kim kontrol ediyor?
2. Doğrudan gözlenen ile çıkarım yapılan arasındaki fark nedir?
3. Hangi varsayımlar gerçek sistemde geçerli olmayabilir?
4. Hangi kanıt tek başına yetersiz kalır?
5. Bir otomatik test neyi kontrol etmeli?

## Etik ve sınırlamalar
Yalnızca izinli sistemlerde ve sentetik verilerle çalış. Bu örnek tam bir tespit veya koruma ürünü değildir.
