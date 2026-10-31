# Gün 30 — Beaconing Düzenliliği ve Jitter Analizi

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Beaconing Düzenliliği ve Jitter Analizi** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Otomatik check-in'ler neredeyse sabit aralıklarla tekrarlanır; insan gezinmesi düzensizdir.
2. Aralıkların varyasyon katsayısı (standart sapma bölü ortalama) düzenliliği ölçer.
3. Saldırganlar jitter ekler; düzenliliği hedef nadirliği ve bayt boyutlarıyla birleştir.

## Kavramsal ayrımlar
- Güncelleyiciler, posta istemcileri ve izleme ajanları da düzenlidir.
- Az örnek güvenilmez istatistik verir; asgari bir sayı iste.
- Düşük varyasyon bir ipucudur, kötü niyetli faaliyetin kanıtı değil.

## Lab uygulaması
Önce `beacon_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 beacon_demo.py
~~~


## Görevler
1. Hangi serinin işaretleneceğini tahmin et.
2. Demoyu çalıştırıp her serinin varyasyonunu not et.
3. Düzenli seriye %30 jitter ekle ve hâlâ işaretlenip işaretlenmediğine bak.
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
