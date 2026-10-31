# Yapay Zekâ ile Çalışma Günlüğü

Araç: Claude (Anthropic), claude.ai
Aşağıdaki prompt'ları sohbette aynen bu şekilde gönderdim. Her birinde YZ'nin ne yaptığını ve benim kararımı yazdım.

---

### Prompt 1
> Ödevin gereksinim listesini çıkar ve kodumun her maddeyi nerede karşıladığını tablo halinde göster.

**YZ ne yaptı:** 8 gereksinimi tabloya döktü, her birinin kodda hangi fonksiyonda ve satırda karşılandığını gösterdi. Ayrıca bir zayıf nokta buldu: `csv_kaydet()` her seferinde aynı dosyanın üzerine yazıyor, program ikinci kez çalıştırılırsa önceki oturumun sonuçları siliniyor. Dosya adına tarih eklemeyi önerdi.
**Kararım: Red (B).** Uygulama tek bir playtest oturumunu analiz etmek için tasarlandı. Her oturumdan sonra dosya zaten ekiple paylaşılıyor, bu kullanım için yeterli.

---

### Prompt 2
> Kodu hatalı ve uç girdilerle test et, bulduğun hataları ve nasıl düzelttiğini açıkla.

**YZ ne yaptı:** 9 senaryo test etti (ondalık, negatif, boşluklu sayı, sadece boşluktan oluşan isim, `;` içeren isim, kısa süre, eşit puanlar, uzun isim, Ctrl+C/Ctrl+D). İlk test turunda kendi kodunda bulup düzelttiği iki hatayı açıkladı (aşağıda). Yeni olarak, girdi beklenirken Ctrl+C/Ctrl+D'ye basılırsa programın `EOFError` ile çöktüğünü buldu.
**Kararım: Red (B).** Normal kullanımda bu tuşlara basılmıyor. Bunu bilinen bir sınırlama olarak test tablosuna yazdım.

---

### Prompt 3
> Hatalı girdiyi yakalayan sayi_al fonksiyonunu satır satır, basitçe açıkla.

**YZ ne yaptı:** `while True` döngüsünü, `try/except ValueError` ile harf ve ondalık girdinin yakalanmasını, `if` ile aralık kontrolünü ve `return` ile döngüden çıkışı satır satır açıkladı.
**Kararım: Kabul.** Özet: Önce "sayı mı?", sonra "aralıkta mı?" diye kontrol ediliyor; ikisinden de geçene kadar soru tekrar soruluyor.

---

### Prompt 4
> Ekrandaki raporu daha okunur hale getir, bana iki seçenek sun.

**YZ ne yaptı:** İki seçenek sundu: A) ortalamaların yanına `#` ile çubuk grafik, B) en üstte özet kutusu. Windows komut ekranında bozulmaması için sadece basit karakterler kullanmayı önerdi.
**Kararım: Kabul (A).** Zayıf alan tek bakışta görünüyor. `cubuk_ciz()` fonksiyonu eklendi. Testte yuvarlama hatası çıktı (aşağıda), o da düzeltildi.

---

### Prompt 5
> Program gereksiz kişisel veri topluyor mu, kontrol et.

**YZ ne yaptı:** Sadece takma ad, süre ve puanların toplandığını; gerçek ad, e-posta, telefon gibi verilerin hiç sorulmadığını ve verinin sadece yerel CSV dosyasına yazıldığını doğruladı. Kullanıcının takma ad yerine gerçek ad yazabileceği riskini belirtip soruya uyarı eklemeyi önerdi.
**Kararım: Red (B).** Soru zaten "takma ad" istiyor. Programı oturumu yöneten kişi kullanıyor ve bunu biliyor.

---

## YZ'nin hataları ve düzeltmeleri

YZ'nin ürettiği kod ilk bakışta çalışıyordu ama testlerde üç hata çıktı:

1. **Eşitlik hatası:** En zayıf alan `min()` ile bulunuyordu. `min()` eşitlikte ilk anahtarı döndürdüğü için tüm puanlar 6-6-6 iken program "En zayıf alan: Eğlence" diyordu. Düzeltme: Ortalamalar eşitse "Yok (tüm alanlar eşit)" yazılıyor.
2. **Tablo hizası:** İsim 30 karaktere kadar kabul ediliyordu ama sütun 15 karakterdi, uzun isimler tabloyu kaydırıyordu. Düzeltme: Sütun 31 karakter yapıldı.
3. **Yuvarlama tutarsızlığı:** Çubuk grafikte `round()` kullanılmıştı. Python 6.5'i 6'ya, 7.5'i 8'e yuvarlıyor (bankacı yuvarlaması), bu yüzden çubuk uzunlukları tutarsızdı. Düzeltme: `int(puan + 0.5)`.

Düzeltilen satırlar kodda yorumlarla açıklanmıştır.
