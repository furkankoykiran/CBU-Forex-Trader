import requests
from bs4 import BeautifulSoup
import time

tl_kasa = 1000
dolar_kasa = 0
son_islem_turu = ""
son_islem_fiyati = 0
tetikleyici = 0.001

def dolar_fiyati():
    response = requests.get("https://www.doviz.com/")
    soup = BeautifulSoup(response.content, "html.parser")
    dolar = soup.find("span", {"data-socket-key": "USD"}).text
    return float(dolar.replace(",", "."))

baslangic_zamani = time.time()

while True:
    if time.time() - baslangic_zamani > 3600:
        break

    dolar = float(dolar_fiyati())
    print(f"Dolar Fiyatı: {dolar}")

    # Son işlem türü "Alış" ise ve (dolar_fiyati > son_islem_fiyati + tetikleyici) ise satış yapacağız.
    if son_islem_turu == "Alış" and dolar > son_islem_fiyati + tetikleyici:
        tl_kasa += dolar * dolar_kasa
        dolar_kasa = 0
        son_islem_turu = "Satış"
        son_islem_fiyati = dolar
        print(f"Satış Yapıldı. TL: {tl_kasa}, Dolar: {dolar_kasa}")

    # Son işlem türü "Satış" ise ve (dolar_fiyati < son_islem_fiyati - tetikleyici) ise alış yapacağız.
    elif son_islem_turu == "Satış" and dolar < son_islem_fiyati - tetikleyici:
        dolar_kasa += tl_kasa / dolar
        tl_kasa = 0
        son_islem_turu = "Alış"
        son_islem_fiyati = dolar
        print(f"Alış Yapıldı. TL: {tl_kasa}, Dolar: {dolar_kasa}")

    # İlk işlem
    elif son_islem_turu == "":
        son_islem_turu = "Alış"
        son_islem_fiyati = dolar
        dolar_kasa += tl_kasa / dolar
        tl_kasa = 0
        print(f"Alış Yapıldı. TL: {tl_kasa}, Dolar: {dolar_kasa}")

    time.sleep(3)

print(f"Son Durum: TL: {tl_kasa}, Dolar: {dolar_kasa}")
print(f"Kâr/Zarar: {tl_kasa + (dolar_kasa * dolar) - 1000}")