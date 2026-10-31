# Yapay Zekâ ile Çalışma Günlüğü

Araç: Claude (Anthropic), claude.ai
Aşağıdaki prompt'lar sohbette gerçekten gönderdiğim mesajlardır. Ödevle ilgisi olmayan kısımları `[...]` ile kısalttım; kelimelerimi değiştirmedim.

---

### Prompt 1: Ödevi anlamak

> "Bu dersi tekrar aldım çünkü finale girmedim. şimdi bize yeni 2 ödev vermiş. [...] önce bu 2 ödevi sanki bir profmuş gibi çok iyi anla ve bana söyle"

**YZ ne yaptı:** Ödev PDF'ini özetledi. Zorunlu 8 maddeyi kontrol listesi yaptı, rubrikte puanın yarıdan fazlasının belge ve testten geldiğini, sözlü doğrulama olabileceğini söyledi.
**Kararım: Kabul.** Kontrol listesini olduğu gibi kullandım. Sözlü doğrulama yüzünden kodun basit kalmasını (sadece standart kütüphane, sınıf yok) doğru buldum.

---

### Prompt 2: Konu ve yöntem

> "[...] senden sadece ufak tefek soru sorarak bu projeye beni karıştırmadan yapmanı istiyorum. Ama bak bana zorluk çıkarmadan gerekirse kendin görsel oluştur ama onu bana sormadan ekle ve bu ödevi en iyi şekilde teslim et. [...]"

**YZ ne yaptı:** Konu olarak benim bölümüme (Dijital Oyun Tasarımı) uygun "Playtest Geri Bildirim Analizcisi"ni seçti, ilk kodu yazdı.
**Kararım: Kabul.** Oyun tasarımı bölümüne doğrudan bağlı, gerçek bir ihtiyaç olduğu için konuyu değiştirmedim.

---

### Test aşaması: Yakalanan YZ hatası

YZ ilk kodu yazdıktan sonra hatalı ve uç girdilerle test etti. Testte **kendi ürettiği kodda iki hata** çıktı:

1. **Tablo hizası:** Takma ad 30 karaktere kadar kabul ediliyordu ama tablodaki sütun 15 karakterdi. 29 karakterlik isimde bütün tablo sağa kaydı.
2. **Eşitlik durumu:** `min()` fonksiyonu eşitlikte ilk anahtarı döndürüyor. Tüm puanlar 6-6-6 iken program "En zayıf alan: Eğlence" diyordu, oysa zayıf alan yoktu. Ekip yanlış alana odaklanabilirdi.

**Kararım: Düzenleme.** Sütun genişliği 31 yapıldı. Puanlar eşitse "Yok (tüm alanlar eşit)" yazan ve buna göre öneri veren kontrol eklendi. Düzeltilen satırlar kodda `DUZELTME` yorumuyla işaretli. README'deki 7. ve 8. test senaryoları bu iki hata.
**Ders:** YZ'nin kodu "çalışıyor" görünse de uç durumları denemeden doğru olduğunu söyleyemezsin.

---

### Prompt 3: Daha basit anlatım

> "anlamadım bu attığın şeyi napacağım [...] çok daha detaylı anlatılsın github kısmı şuraya tıkla şuraya gir [...]"

**YZ ne yaptı:** İlk anlatımı çok karışıktı. GitHub'da repo açmayı tıklama tıklama, numaralı adımlarla yeniden anlattı.
**Kararım: Red → düzenleme.** İlk açıklamayı reddettim, adım adım halini istedim ve onu kullandım.

---

### Prompt 4: Yansıtma ve teslim

> "Dönem başında kodlama sana ne ifade ediyordu, şimdi ne ifade ediyor? oyun yapmak para kazanmak / YZ ile çalışmak sana ne kazandırdı? hayatımı kolaylaştırdı" + repo linki

**YZ ne yaptı:** Cevaplarımdan yansıtma metnini taslak olarak yazdı, README'yi, ekran görüntülerini (programın gerçek çıktılarından) ve akış şemasını hazırlayıp repoya yükledi.
**Kararım: Kabul.**
