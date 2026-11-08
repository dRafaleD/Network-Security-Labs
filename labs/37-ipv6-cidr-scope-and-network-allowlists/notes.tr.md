# Gün 37 — IPv6 CIDR Kapsamı ve Ağ İzin Listeleri

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](ipv6_policy_demo.py)

## IPv6 neden güvenlik açısından önemli?
Bir kurum IPv4 firewall kurallarını ayrıntılı yapılandırırken IPv6 üzerinden açık kalan ayrı bir bağlantı yolunu unutabilir. **IPv4 ve IPv6 farklı adres aileleridir.** Birisi için yazılmış politika diğerini kendiliğinden korumaz. Sunucunun dinlediği tüm adres aileleri için açık kurallar gerekir.

## CIDR ve adres kapsamı
`2001:db8:10::/64`, ilk 64 bit ile tanımlanan IPv6 alt ağını gösterir. Bu adresler dokümantasyon amaçlıdır; gerçek hedef olarak kullanılmaz. `fe80::/10` bağlantı-yerel (link-local) adresler için ayrılmıştır; arayüz/scope bağlamı dikkate alınmadan global ağ kaynağı gibi yorumlanmamalıdır.

## Güven sınırları
Örnekte yalnızca `2001:db8:10::/64` kaynağından TCP/443 kabul edilir. Tanımlanmayan her kaynak ve port **varsayılan olarak reddedilir**. Kod gerçek firewall değiştirmez ve paket göndermez.

```bash
python3 ipv6_policy_demo.py
```

## Beklenen gözlemler
- İzinli alt ağdan TCP/443: kabul.
- Farklı IPv6 alt ağından, `fe80::1` adresinden veya TCP/22: ret.
- IPv4 adresi: IPv6 kuralıyla eşleşmez.

## Görevler
1. Çıktıyı önceden tahmin et; her ret kararını açıkla.
2. `/64` yerine `/48` yaz; kapsanan adresler nasıl değişir?
3. IPv6 kuralını bozmadan ayrı IPv4 kuralı ekle.
4. IP/CIDR denetiminin neden kullanıcı kimlik doğrulaması olmadığını açıkla.
5. Gerçek ağ politikalarında stateful izleme, routing, egress ve dual-stack dinleme eksiklerini tartış.

## Güvenlik
Yalnız Python standart kütüphanesi ve dokümantasyon IP'leri kullanılır. Gerçek sisteme veya ağa müdahale edilmez.
