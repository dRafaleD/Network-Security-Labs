# Gün 51 — Bağımsız Sensörlerin Zaman ve Olay Uyuşması

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](time_correlation_demo.py)

## 50. günden devam
Önceki gün relay üzerinden gelen iki mesajın tek sensörün kanıtı olduğunu gördük. Bugün iki bağımsız sensörün **aynı olayı gerçekten mi anlattığını** karşılaştırıyoruz.

**Time window:** iki olay zamanı arasında kabul edilen tolerans. **Origin conflict:** bir sensörün kendi kayıtlarının çelişmesi. **Cross-sensor conflict:** farklı sensörlerin olay türü veya adres konusunda uyuşmaması.

HMAC ile doğrulanan hayalî IPv6 DAD olaylarında sensör kimliği, olay türü, adres ve zaman karşılaştırılıyor. İki ayrı sensör aynı veriyi **±2 saniyelik tolerans içinde** raporlarsa `CORROBORATED_CONTEXT`. Zaman uzaksa `TIME_DISAGREEMENT`, olay türü farklıysa `CROSS_SENSOR_CONFLICT`.

## Çalıştır
```bash
python3 labs/51-multi-sensor-time-correlation-and-origin-conflicts/time_correlation_demo.py
```

## Sorular
Zamanlar neden tek başına olay eşitliği kanıtı değildir? Sensör saatleri kaymışsa ne olur? Doğru HMAC sensörün söylediğinin doğru olduğunu garanti eder mi?

## Sınır
Gerçek sensör, anahtar veya ağ paketi kullanılmaz.
