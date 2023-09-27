# -*- coding:utf-8 -*-
from random import choice,randint
from time import sleep
from threading import Thread
from os import system,name


bid = list(range(10001))
su_geçisi = 0
elektrik_yüklenmesi = 0
class Bina:
    def __init__(self,bina_name,kat,her_kattaki_daire_sayisi):
        self.id = choice(bid)
        bid.pop(self.id)
        self.kat = kat
        self.her_kattaki_daire_sayisi = her_kattaki_daire_sayisi
        self.bagli_kanallar = ["first"]
        self.watt = (her_kattaki_daire_sayisi*kat*4700)+200
        self.Litre = len(self.bagli_kanallar)*200
        #(her_kattaki_daire_sayisi*kat*15)+1
        self.bina_name = bina_name
        self.internet_durumu = "Bağlı"
        self.elektrik_durumu = "Var"
        self.kanalizasyon_durumu = "Bağlı"
    def __str__(self):
        return f"""
Bina Adı :{self.bina_name} 
    -İD :{self.id} 
    -Kat Sayısı :{self.kat} 
    -Daire Sayısı :{self.kat*self.her_kattaki_daire_sayisi} 
    -O. Bina Elektrik Kullanımı :{self.watt} Watt
    -O. Bina Su Kullanımı :{self.Litre} Litre
    -Kanalizasyon Durumu :{self.kanalizasyon_durumu} 
    -İnternet Durumu :{self.internet_durumu}
    -Elektrik Sistemi :{self.elektrik_durumu}
    -Bağlı Kanalizasyon Hatları :{self.bagli_kanallar}"""
class Elektrik:
    def __init__(self):
        self.altyapı_ömrü = randint(10,17)
        self.durum = "Açık"
        self.limit = 2000000
    def bakım(self):
        self.altyapı_ömrü = randint(10,17)
        sleep(7.6)
    def altyapı_upgrade(self,watt):
        self.limit += watt
        print("Kapasite Arttırılıyor..")
        sleep(int(watt/100000))
    def kabloları_soğut(self):
        if self.durum != "Açık" and self.durum != "Kablolar Yanmış":
            self.durum = "Açık"
            self.altyapı_ömrü -= 3
    def kabloları_tamir_et(self):
        if self.durum != "Açık" and self.durum != "Kablolar Aşırı Isınmış":
            self.durum = "Açık"
            self.altyapı_ömrü -= 3
    def sistemi_aç(self):
        self.durum = "Açık"
        print("Açıldı.")
        self.altyapı_ömrü -= 1
    def elektrigi_kes(self):
        self.durum = "Kesik."
        print("Kesildi.")
        self.altyapı_ömrü -= 1
    def __str__(self):
        return """
Elektrik Altyapısı
    -Elektrik Altyapısı Durumu :{} 
    -Altyapı Watt Limiti :{} 
    -Yüklenme :{} Watt 
    -Kalan Altyapı Ömrü :{}""".format(self.durum,self.limit,elektrik_yüklenmesi,self.altyapı_ömrü)

class Kanalizasyon:
    def __init__(self):
        self.durum = "Açık"
        self.altyapı_ömrü = randint(14,21)
        self.limit = 10000
        self.kanallar = []
        self.kanal_sayisi = len(self.kanallar)
    def bakım(self):
        self.altyapı_ömrü = randint(14,21)
        self.durum = "Kapalı"
        sleep(7.6)
    def altyapı_upgrade(self,litre):
        self.limit += litre
        print("Kapasite Arttırılıyor..")
        sleep(int(litre/1000))
    def aç(self):
        if randint(0,20) != 7:
            self.durum = "Açık"
            print("Açıldı.")
            self.altyapı_ömrü -= 1
        else:
            self.durum = "Kapaklar Kırıldı"
    def kapat(self):
        if randint(0,20) != 7:
            self.durum = "Kapalı"
            print("Kapatıldı.")
            self.altyapı_ömrü -= 1
        else:
            self.durum = "Kapaklar Kırıldı"
    def kanal_ekle(self, kanal, bina):
        self.kanallar.append(kanal)
        bina.bagli_kanallar.append(kanal.kanal_id)
        print(f"Kanalizasyona yeni bir kanal eklendi: {kanal} (Bina: {bina.id})")
        self.altyapı_ömrü -= 1
    def __str__(self):
        return """
Kanalizasyon Altyapısı
    -Kanalizasyon Altyapısı Durumu :{}
    -Altyapı Su Limiti :{}
    -Su geçişi :{} 
    -Kalan Altyapı Ömrü :{}""".format(self.durum,self.limit,su_geçisi,self.altyapı_ömrü)

class Kanal:
    def __init__(self, kanal_id):
        self.kanal_id = kanal_id
    def __str__(self):
        return f"Kanal ID: {self.kanal_id}"

class İnternet:
    def __init__(self):
        self.speed = 16
        self.durum = "Bağlı"
    def upgrade(self,add_mbps):
        print("Hız arttırılıyor..")
        sleep(int(add_mbps/2))
        self.speed += add_mbps
    def kes(self):
        self.durum = "Kesilmiş"
        Bina.internet_durumu = "Kesilmiş"
    def bağla(self):
        self.durum = "Bağlı"
        Bina.internet_durumu = "Bağlı"

def bina_yık(bina):
    if bina.id not in bid:
        bid.append(bina.id)
    bina.id = None
    bina.elektrik_durumu = None
    bina.internet_durumu = None
    bina.kanalizasyon_durumu = None
    bina.bagli_kanallar = None
    print("Bina yıkımı tamamlandı.")

binalar = []
elektrik = Elektrik()
kanalizasyon = Kanalizasyon()
internet = İnternet()
def checker():
    while True:
        sleep(0.2)
        if su_geçisi > kanalizasyon.limit:
            kanalizasyon.durum = "Taşmış"
        if elektrik_yüklenmesi > elektrik.limit:
            elektrik.durum = "Kablolar Yanmış"
            internet.durum = "Kesilmiş"
        if elektrik_yüklenmesi < elektrik.limit and elektrik.limit-elektrik_yüklenmesi < 70001:
            elektrik.durum = "Kablolar Aşırı Isınmış"
            internet.durum = "Yavaş"
checker_thread = Thread(target=checker)
checker_thread.start()

# Ana Sistem
while True:
    su_geçisi+=randint(100,400)
    elektrik_yüklenmesi+=randint(10000,25000)
    print("\n--- ŞEHİR ALTYAPI SİMULASYONU ---")
    print("1. İnşaat Sistemine Gir")
    print("2. Elektrik Sistemine Gir")
    print("3. Internet Sistemine Gir")
    print("4. Kanalizasyon Sistemine Gir")
    print("5. Bakım Sistemi")
    print("6. Upgrade Sistemi")
    print("7. Konsolu Temizle")
    print("8. Çıkış\n")
    try:
        req = int(input("İşlemini Seç :"))
        if req == 1:
            print("1. Bina İnşa Et")
            print("2. Binaları Listele")
            print("3. Bina Yık")
            req = int(input("İşlemini Seç :"))
            if req == 1:
                name = input("Bina adını girin: ")
                kat = int(input("Kat sayısını girin: "))
                her_kattaki_daire = int(input("Her kattaki daire sayısını girin :"))
                bina = Bina(name, kat, her_kattaki_daire)
                binalar.append(bina)
                elektrik_yüklenmesi += bina.watt
                su_geçisi += bina.Litre
                print("Bina başarıyla inşa edildi.")
            elif req == 2:
                print("\n--- BİNALAR ---")
                for bina in binalar:
                    print(bina)
                print("\nBina sayısı -->",len(binalar))
                input()
            elif req == 3:
                bina_id = int(input("Yıkılacak bina ID'sini girin: "))
                for bina in binalar:
                    if bina.id == bina_id:
                        su_geçisi-=bina.Litre
                        elektrik_yüklenmesi-=bina.watt
                        bina_yık(bina)
                        binalar.remove(bina)
                        print("Bina başarıyla yıkıldı.")
                        break
                else:
                    print("Bina bulunamadı.")
            else:
                print("Bilinmeyen İstek.")
        elif req == 2:
            print(elektrik,"\n")
            print("1. Elektrik Dağıtımını Başlat")
            print("2. Elektrik Dağıtımını Durdur")
            req = int(input("İşlemini Seç :"))
            if req == 1:
                if elektrik.durum != "Kablolar Yanmış":
                    elektrik.sistemi_aç()
                    for bina in binalar:
                        bina.elektrik_durumu = "Bağlı"
                    print("Elektrik sistemi başlatıldı.")
                else:
                    print("Elektrik Altyapı Kabloları Yanmış. Acilen Upgrade Edin!")
            elif req == 2:
                elektrik.elektrigi_kes()
                for bina in binalar:
                    bina.elektrik_durumu = "Kesik"
                print("Elektrik Dağıtımı Durduruldu")
            else:
                print("Bilinmeyen İstek.")
        elif req == 3:
            print("1. İnterneti Dağıtımını Başlat")
            print("2. İnternet Dağıtımını Kes")
            req = int(input("İşlemini Seç :"))
            if req == 1:
                if elektrik.durum != "Kablolar Yanmış":
                    internet.bağla()
                    for bina in binalar:
                        bina.internet_durumu = "Bağlı"
                    print("Internet Dağıtımı başlatıldı.")
                else:
                    print("Elektrik Altyapı Kabloları Yanmış. Acilen Upgrade Edin!")
            elif req==2:
                internet.kes()
                for bina in binalar:
                    bina.internet_durumu = "Kesilmiş"
                print("Internet Dağıtımı durduruldu.")
            else:
                print("Bilinmeyen İstek.")
        elif req == 4:
            print(kanalizasyon,"\n")
            print("1. Kapakları Aç")
            print("2. Kapakları Kapat")
            print("3. Sisteme Yeni Kanal Ekle")
            req = int(input("İşlemini Seç :"))
            if req == 1:
                if kanalizasyon.durum != "Kapaklar Kırıldı" and kanalizasyon.durum != "Taşmış":
                    kanalizasyon.aç()
                    for bina in binalar:
                        bina.kanalizasyon_durumu = "Bağlı"
                    print("Kanalizasyon sistemi başlatıldı.")
                else:
                    print("Kapaklar Kırık. Acilen altyapıyı upgrade veya tamir edin!")
            elif req == 2:
                if kanalizasyon.durum != "Kapaklar Kırıldı" and kanalizasyon.durum == "Taşmış":
                    kanalizasyon.kapat()
                    for bina in binalar:
                        bina.kanalizasyon_durumu = "Kesik"
                    print("Kanalizasyon sistemi durduruldu.")
                else:
                    print("Kapaklar Kırık. Acilen altyapıyı upgrade veya tamir edin!")
            elif req == 3:
                if kanalizasyon.durum != "Kapaklar Kırıldı" and kanalizasyon.durum != "Taşmış":
                    kanal_id = int(input("Kanal ID'sini girin: "))
                    bina_id = int(input("Kanalı hangi binaya bağlamak istiyorsunuz? Bina ID'sini girin: "))
                    kanal = Kanal(kanal_id)
                    for bina in binalar:
                        if bina.id == bina_id:
                            kanalizasyon.kanal_ekle(kanal, bina)
                            su_geçisi+=200
                            break
                    else:
                        print("Bina bulunamadı.")
                else:
                    print("Kapaklar Kırık veya Taşmış. Acilen altyapıyı upgrade veya tamir edin!")
            else:
                print("Bilinmeyen İstek.")
        elif req == 5:
            print("1. Elektrik Sistemine Bakım Yap")
            print("2. İnternet Sistemine Bakım Yap")
            print("3. Kanalizasyon Sistemine Bakım Yap")
            req = int(input("İşlemini Seç :"))
            if req == 1:
                print("Bakım yapılıyor..")
                elektrik.bakım()
                print("Bakım tamamlandı.")
            elif req == 2:
                print("Bakım yapılıyor..")
                elektrik.bakım()
                print("Bakım tamamlandı.")
            elif req == 3:
                print("Bakım yapılıyor..")
                kanalizasyon.bakım()
                print("Bakım tamamlandı.")
            else:
                print("Bilinmeyen İstek.")
        elif req == 6:
            check_elektrik = elektrik.limit-elektrik_yüklenmesi
            check_su_geçisi = kanalizasyon.limit-su_geçisi
            print("1. Elektrik Sistemini Yükselt. Watt aşımı -->","Yok" if check_elektrik > -1 else check_elektrik)
            print("2. İnternet Sistemini Yükselt. Litre aşımı -->","Yok" if check_su_geçisi > -1 else check_su_geçisi)
            print("3. Kanalizasyon Sistemini Yükselt")
            req = int(input("İşlemini Seç :"))
            if req == 1:
                elektrik.altyapı_upgrade(int(input("Yük kapasitesi kaç watt arttırılsın :")))
            elif req == 2:
                internet.upgrade(int(input("İnternet hızı kaç MBPS arttırılsın :")))
            elif req == 3:
                kanalizasyon.altyapı_upgrade(int(input("Kanalizasyon Litre Kapasitesi Ne Kadar arttırılsın :")))
            else:
                print("Bilinmeyen İstek.")
        elif req == 7:
            system('cls' if name == 'nt' else 'clear')
        elif req == 8:
            print("Sistem Kapatılıyor..")
            #del Elektrik,Bina,Kanalizasyon,Kanal,İnternet,binalar,elektrik_yüklenmesi,su_geçisi,req
            break
        else:
            print("Bilinmeyen İstek.")
    except ValueError:
        print("Sayısal bir değer gir!")
        continue