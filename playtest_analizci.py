"""
Playtest Geri Bildirim Analizcisi
GEP1316 Kodlama Okuryazarligi - Ara Degerlendirme Odevi 1
Hazirlayan: Alimert Polat

Ne yapar?
Bir oyun gelistirme ekibi playtest (deneme oturumu) sonrasinda oyunculardan
puan toplar. Bu program puanlari alir, dogrular, ortalamalari ve en zayif
alani hesaplar, sonucu ekrana yazar ve CSV dosyasina kaydeder.
"""

import csv

# Puanlanan alanlar: anahtar -> ekranda gorunen ad
ALANLAR = {
    "eglence": "Eglence",
    "zorluk": "Zorluk dengesi",
    "kontroller": "Kontroller",
}


def metin_al(mesaj):
    """Bos olmayan ve en fazla 30 karakterlik bir metin alir."""
    while True:
        deger = input(mesaj).strip()
        if deger == "":
            print("  ! Bos birakilamaz, tekrar deneyin.")
        elif len(deger) > 30:
            print("  ! En fazla 30 karakter girebilirsiniz.")
        else:
            return deger


def sayi_al(mesaj, en_az, en_cok):
    """Belirtilen aralikta bir tam sayi alir; hatali girdide cokmez."""
    while True:
        try:
            deger = int(input(mesaj))
        except ValueError:
            print("  ! Lutfen bir tam sayi girin.")
            continue
        if deger < en_az or deger > en_cok:
            print(f"  ! Deger {en_az} ile {en_cok} arasinda olmali.")
        else:
            return deger


def geri_bildirim_ekle(kayitlar):
    """Bir oyuncudan geri bildirim alip listeye sozluk olarak ekler."""
    print("\n--- Yeni Geri Bildirim ---")
    kayit = {
        "oyuncu": metin_al("Oyuncu takma adi: "),
        "sure": sayi_al("Oynama suresi (dakika, 1-300): ", 1, 300),
    }
    for anahtar, ad in ALANLAR.items():
        kayit[anahtar] = sayi_al(f"{ad} puani (1-10): ", 1, 10)
    kayitlar.append(kayit)
    print(f"  + {kayit['oyuncu']} kaydedildi. Toplam kayit: {len(kayitlar)}")


def ozet_hesapla(kayitlar):
    """Her alanin ortalamasini, ortalama sureyi ve en zayif alani hesaplar."""
    ortalamalar = {}
    for anahtar in ALANLAR:
        toplam = sum(k[anahtar] for k in kayitlar)
        ortalamalar[anahtar] = round(toplam / len(kayitlar), 1)
    ort_sure = round(sum(k["sure"] for k in kayitlar) / len(kayitlar), 1)
    # DUZELTME: Tum puanlar esitse belirgin bir zayif alan yoktur.
    # (Ilk surumde min() esitlikte hep "eglence"yi seciyordu.)
    if len(set(ortalamalar.values())) == 1:
        en_zayif = None
    else:
        en_zayif = min(ortalamalar, key=ortalamalar.get)
    return ortalamalar, ort_sure, en_zayif


def zayif_alan_adi(en_zayif):
    """En zayif alanin ekranda gorunecek adini dondurur."""
    if en_zayif is None:
        return "Yok (tum alanlar esit)"
    return ALANLAR[en_zayif]


def puan_yorumu(puan):
    """Ortalama puana gore kisa bir yorum dondurur."""
    if puan >= 8:
        return "Guclu"
    elif puan >= 5:
        return "Gelistirilebilir"
    else:
        return "Oncelikli sorun"


def cubuk_ciz(puan):
    """Puani 10 karakterlik bir cubuga cevirir. Ornek: 7.7 -> ########--"""
    # round() 6.5 -> 6 ama 7.5 -> 8 yapiyor (bankaci yuvarlamasi);
    # her zaman yukari yuvarlamak icin int(puan + 0.5) kullaniyoruz.
    dolu = int(puan + 0.5)
    return "#" * dolu + "-" * (10 - dolu)


def oneri_uret(en_zayif, ort_sure):
    """En zayif alana ve oynama suresine gore ekibe oneri yazar."""
    if en_zayif is None:
        oneri = "Tum alanlar dengeli; daha fazla oyuncuyla test edin."
    elif en_zayif == "eglence":
        oneri = "Cekirdek oynanisi ve odul dongusunu gozden gecirin."
    elif en_zayif == "zorluk":
        oneri = "Zorluk egrisini yumusatin, ilk bolumlere ipucu ekleyin."
    else:
        oneri = "Tus atamalarini ve kontrol hissini yeniden test edin."
    if ort_sure < 10:
        oneri += " Oyuncular cabuk birakiyor; ilk 10 dakikaya odaklanin."
    return oneri


def rapor_yazdir(kayitlar):
    """Kayitlari ve ozeti tablo halinde ekrana yazar."""
    if not kayitlar:
        print("\n  ! Henuz kayit yok. Once geri bildirim ekleyin.")
        return
    # DUZELTME: Isim 30 karaktere kadar olabildigi icin sutun 31 karakter.
    # (Ilk surumde 15 karakterdi; uzun isimler tabloyu kaydiriyordu.)
    print("\n" + "=" * 66)
    print(f"{'Oyuncu':<31}{'Sure':>5}{'Eglence':>10}{'Zorluk':>9}{'Kontrol':>10}")
    print("-" * 66)
    for k in kayitlar:
        print(f"{k['oyuncu']:<31}{k['sure']:>5}{k['eglence']:>10}"
              f"{k['zorluk']:>9}{k['kontroller']:>10}")
    print("-" * 66)
    ortalamalar, ort_sure, en_zayif = ozet_hesapla(kayitlar)
    for anahtar, ad in ALANLAR.items():
        puan = ortalamalar[anahtar]
        print(f"{ad:<18}: {puan:>4} / 10  {cubuk_ciz(puan)}  {puan_yorumu(puan)}")
    print(f"{'Ortalama sure':<18}: {ort_sure} dk")
    print(f"En zayif alan     : {zayif_alan_adi(en_zayif)}")
    print(f"Oneri             : {oneri_uret(en_zayif, ort_sure)}")
    print("=" * 66)


def csv_kaydet(kayitlar, dosya_adi="playtest_sonuclari.csv"):
    """Kayitlari ve ozet satirini CSV dosyasina yazar."""
    if not kayitlar:
        print("\n  ! Kaydedilecek veri yok.")
        return
    ortalamalar, ort_sure, en_zayif = ozet_hesapla(kayitlar)
    # utf-8-sig: Excel'de Turkce karakterler duzgun gorunsun diye
    with open(dosya_adi, "w", newline="", encoding="utf-8-sig") as dosya:
        yazici = csv.writer(dosya, delimiter=";")
        yazici.writerow(["Oyuncu", "Sure (dk)", "Eglence", "Zorluk", "Kontroller"])
        for k in kayitlar:
            yazici.writerow([k["oyuncu"], k["sure"], k["eglence"],
                             k["zorluk"], k["kontroller"]])
        yazici.writerow([])
        yazici.writerow(["ORTALAMA", ort_sure, ortalamalar["eglence"],
                         ortalamalar["zorluk"], ortalamalar["kontroller"]])
        yazici.writerow(["En zayif alan", zayif_alan_adi(en_zayif)])
        yazici.writerow(["Oneri", oneri_uret(en_zayif, ort_sure)])
    print(f"\n  + Sonuclar '{dosya_adi}' dosyasina kaydedildi.")


def ana_menu():
    """Programin ana dongusu: kullanici cikis secene kadar menu doner."""
    kayitlar = []
    while True:
        print("\n=== PLAYTEST GERI BILDIRIM ANALIZCISI ===")
        print("1) Geri bildirim ekle")
        print("2) Raporu goster")
        print("3) CSV'ye kaydet")
        print("4) Cikis")
        secim = input("Seciminiz: ").strip()
        if secim == "1":
            geri_bildirim_ekle(kayitlar)
        elif secim == "2":
            rapor_yazdir(kayitlar)
        elif secim == "3":
            csv_kaydet(kayitlar)
        elif secim == "4":
            print("Gorusmek uzere!")
            break
        else:
            print("  ! Gecersiz secim. 1-4 arasi bir sayi girin.")


if __name__ == "__main__":
    ana_menu()
