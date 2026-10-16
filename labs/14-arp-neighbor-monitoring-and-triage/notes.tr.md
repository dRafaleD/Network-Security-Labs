# Gün 14 — ARP Komşu İzleme ve Katman-2 Alarm İncelemesi

[English](notes.md) | [Türkçe](notes.tr.md)

## Amaç

ARP Komşu İzleme ve Katman-2 Alarm İncelemesi konusunu gerçek sistemlere dokunmadan, yerel ve zararsız örneklerle çalışmak. Hedef yalnızca komutları ezberlemek değil; ölçümün neyi gösterdiğini ve neyi kanıtlamadığını anlamaktır.

## Birbiriyle bağlantılı konular

1. **ARP basics**: Bu kavramın hangi problemi çözdüğünü, veri akışını ve sınırlamalarını açıklayın.
2. **IPv6 Neighbor Discovery**: Bu kavramın hangi problemi çözdüğünü, veri akışını ve sınırlamalarını açıklayın.
3. **IP/MAC baseline**: Bu kavramın hangi problemi çözdüğünü, veri akışını ve sınırlamalarını açıklayın.
4. **mapping anomalies**: Bu kavramın hangi problemi çözdüğünü, veri akışını ve sınırlamalarını açıklayın.
5. **false positives**: Bu kavramın hangi problemi çözdüğünü, veri akışını ve sınırlamalarını açıklayın.
6. **passive monitoring**: Bu kavramın hangi problemi çözdüğünü, veri akışını ve sınırlamalarını açıklayın.

## Ortamın hazırlanması ve çalışma

`arp_triage.py` dosyası sentetik eğitim örneğidir. İlgili lab klasöründe çalıştırın:

``bash
python3 arp_triage.py
```

``bash
ip neigh show
```

## Adım adım analiz

1. Çalıştırmadan önce beklediğiniz sonucu not edin.
2. Gerçek çıktıyı ve kullandığınız aracın sürümünü kaydedin.
3. Gözlediğiniz olgular ile tahminlerinizi ayrı yazın.
4. Bir zararsız negatif test ekleyin; sonucu yeniden ölçün.
5. Yanlış pozitif, yanlış negatif ve eksik bağlam ihtimallerini düşünün.
6. Delil niteliğindeki örneği değiştirmeden önce kopyasını alın ve hash kaydedin.
7. Konfigürasyondaki bilgi ile çalışma zamanı sonucunu karşılaştırın.
8. Kesin bildikleriniz, belirsizlikler ve sonraki kontroller için kısa rapor yazın.

## Mini görevler

- **Başlangıç ölçümü:** örneği çalıştırıp çıktı, varsayım ve sınırlamaları belgeleyin.
- **Tek değişken:** zararsız bir işaretçi, log alanı veya ayarı değiştirip etkisini gözleyin.
- **Regresyon:** ilk ayara dönün ve beklenen sonucun korunduğunu doğrulayın.
- **Kanıt yorumu:** tek bir eşleşmenin ya da alarmın neden saldırı kanıtı olmadığını tartışın.

## Tekrar soruları

1. ARP basics nedir, ne sağlar ve tek başına neyi kanıtlamaz?
2. IPv6 Neighbor Discovery nedir, ne sağlar ve tek başına neyi kanıtlamaz?
3. IP/MAC baseline nedir, ne sağlar ve tek başına neyi kanıtlamaz?
4. mapping anomalies nedir, ne sağlar ve tek başına neyi kanıtlamaz?
5. false positives nedir, ne sağlar ve tek başına neyi kanıtlamaz?
6. passive monitoring nedir, ne sağlar ve tek başına neyi kanıtlamaz?
7. Analizin güvenilirliği için hangi ikinci kanıta ihtiyacınız var?
8. Aynı ölçümü başka bir makinede nasıl tekrarlarsınız?

## Güvenlik

Yalnızca kendi örnekleriniz ve açık izinli ortamlar üzerinde çalışın. Sentetik sonuçları gerçek vaka bulgusu gibi sunmayın.