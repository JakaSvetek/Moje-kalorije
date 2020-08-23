import json
from datetime import date
import os
import hashlib

TIPI_OBROKOV = [
    "Zajtrk",
    "Dopoldanska malica",
    "Kosilo",
    "Popoldanska malica",
    "Večerja"
]

CILJI = [
    "Hitro pridobiti",
    "Pridobiti",
    "Počasi pridobiti",
    "Hitro izgubiti",
    "Izgubiti",
    "Počasi izgubiti"
]

SPOLI = [
    "Moški",
    "Ženski"
]

MAPA_Z_UPORABNIKI = "uporabniki"

class Uporabnik:

    def __init__(self, uporabnisko_ime, zasifrirano_geslo, postava, cilj):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.postava = postava
        self.cilj = cilj
        self.obroki = []
        self.vadbe = []

    def priporocen_dnevni_vnos(self):

        if self.postava.spol == "Moški":

            if self.cilj == "Hitro pridobiti":
                return 85 + 6.3 * int(self.postava.visina) + 15.5 * int(self.postava.teza) - 5.6 * int(self.postava.starost)

            elif self.cilj == "Pridobiti":
                return 80 + 6 * int(self.postava.visina) + 15 * int(self.postava.teza) - 6 * int(self.postava.starost)

            elif self.cilj == "Počasi pridobiti":
                return 75 + 5.7 * int(self.postava.visina) + 14.5 * int(self.postava.teza) - 6.4 * int(self.postava.starost)

            elif self.cilj == "Počasi izgubiti":
                return 70 + 5.3 * int(self.postava.visina) + 14 * int(self.postava.teza) - 6.8 * int(self.postava.starost)

            elif self.cilj == "Izgubiti":
                return 65 + 5 * int(self.postava.visina) + 13.5 * int(self.postava.teza) - 7.1 * int(self.postava.starost)

            elif self.cilj == "Hitro izgubiti":
                return 60 + 4.7 * int(self.postava.visina) + 13 * int(self.postava.teza) - 7.4 * int(self.postava.starost)

        elif self.postava.spol == "Ženski":

            if self.cilj == "Hitro pridobiti":
                return 830 + 3.4 * int(self.postava.visina) + 11.3 * int(self.postava.teza) - 3.5 * int(self.postava.starost)

            elif self.cilj == "Pridobiti":
                return 805 + 3.2 * int(self.postava.visina) + 11 * int(self.postava.teza) - 3.7 * int(self.postava.starost)

            elif self.cilj == "Počasi pridobiti":
                return 780 + 3 * int(self.postava.visina) + 10.7 * int(self.postava.teza) - 3.9 * int(self.postava.starost)

            elif self.cilj == "Počasi izgubiti":
                return 730 + 2.4 * int(self.postava.visina) + 9.8 * int(self.postava.teza) - 4.5 * int(self.postava.starost)

            elif self.cilj == "Izgubiti":
                return 705 + 2.2 * int(self.postava.visina) + 9.5 * int(self.postava.teza) - 4.7 * int(self.postava.starost)

            elif self.cilj == "Hitro izgubiti":
                return 680 + 2 * int(self.postava.visina) + 9.2 * int(self.postava.teza) - 4.9 * int(self.postava.starost)

    def nov_obrok(self, tip_obroka, kalorije, datum):
        obrok = Obrok(tip_obroka, kalorije, datum)
        if tip_obroka in self.tipi_obrokov_za_datum(datum):
            raise ValueError("Za ta dan ste že vpisali {}.".format(tip_obroka.lower()))
        self.obroki.append(obrok)

    def nova_vadba(self, tip_vadbe, kalorije, datum):
        vadba = Vadba(tip_vadbe, kalorije, datum)
        self.vadbe.append(vadba)

    def pridobi_obroke_za_datum(self, datum):
        obroki_tega_datuma = []
        for obrok in self.obroki:
            if obrok.datum == str(datum):
                obroki_tega_datuma.append(obrok)
        return obroki_tega_datuma

    def tipi_obrokov_za_datum(self, datum):
        tipi_obrokov_tega_datuma = []
        for obrok in self.obroki:
            if obrok.datum == str(datum):
                tipi_obrokov_tega_datuma.append(obrok.tip_obroka)
        return tipi_obrokov_tega_datuma

    def pridobi_vadbe_za_datum(self, datum):
        vadbe_tega_datuma = []
        for vadba in self.vadbe:
            if vadba.datum == str(datum):
                vadbe_tega_datuma.append(vadba)
        return vadbe_tega_datuma
    
    def dnevne_kalorije(self, datum):
        vsota_kalorij = 0
        for obrok in self.obroki:
            if obrok.datum == str(datum):
                vsota_kalorij += int(obrok.kalorije)
        for vadba in self.vadbe:
            if vadba.datum == str(datum):
                vsota_kalorij -= int(vadba.kalorije)
        return vsota_kalorij

    def dnevne_preostale_kalorije(self, datum):
        presotanek_kalorij = self.priporocen_dnevni_vnos() - self.dnevne_kalorije(datum)
        return presotanek_kalorij

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "postava": self.postava.v_slovar(),
            "cilj": self.cilj,
            "obroki": [obrok.v_slovar() for obrok in self.obroki],
            "vadbe": [vadba.v_slovar() for vadba in self.vadbe]
        }

    def shrani_slovar(self):
        ime_datoteke = Uporabnik.pridobi_ime_datoteke_uporabnika(self.uporabnisko_ime)
        with open(ime_datoteke, 'w', encoding='utf8') as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)  

    @staticmethod
    def pridobi_ime_datoteke_uporabnika(uporabnisko_ime):
        return os.path.join(MAPA_Z_UPORABNIKI, uporabnisko_ime + ".json")
        
    @classmethod
    def pridobi_podatke_uporabnika(cls, uporabnisko_ime):
        ime_datoteke = cls.pridobi_ime_datoteke_uporabnika(uporabnisko_ime)
        with open(ime_datoteke, encoding='utf8') as datoteka:
            podatki_uporabnika = json.load(datoteka)
        uporabnisko_ime = podatki_uporabnika['uporabnisko_ime']
        zasifrirano_geslo = podatki_uporabnika['zasifrirano_geslo']
        postava = Postava(
            podatki_uporabnika['postava']['spol'], 
            podatki_uporabnika['postava']['visina'], 
            podatki_uporabnika['postava']['teza'], 
            podatki_uporabnika['postava']['starost']
            )
        cilj = podatki_uporabnika['cilj']
        uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, postava, cilj)
        for obrok in podatki_uporabnika['obroki']:
            uporabnik.nov_obrok(
                obrok['tip_obroka'], 
                obrok['kalorije'], 
                obrok['datum']
                )
        for vadba in podatki_uporabnika['vadbe']:
            uporabnik.nova_vadba(
                vadba['tip_vadbe'], 
                vadba['kalorije'], 
                vadba['datum']
                )
        return uporabnik

    @staticmethod
    def sifriraj_geslo(geslo):
        hasher = hashlib.blake2b()
        hasher.update(geslo.encode(encoding='utf-8'))
        return hasher.hexdigest()

    @staticmethod
    def ali_uporabnik_ze_obstaja(uporabnisko_ime):
        return (uporabnisko_ime + ".json") in os.listdir(MAPA_Z_UPORABNIKI)


class Postava:
    def __init__(self, spol, visina, teza, starost):
        self.spol = spol
        self.visina = visina
        self.teza = teza
        self.starost = starost

    def v_slovar(self):
        return {
            "spol": self.spol,
            "visina": self.visina,
            "teza": self.teza,
            "starost": self.starost
        }


class Obrok:
    def __init__(self, tip_obroka, kalorije, datum):
        self.tip_obroka = tip_obroka
        self.kalorije = kalorije
        self.datum = datum

    def v_slovar(self):
        return {
            "tip_obroka": self.tip_obroka,
            "kalorije": self.kalorije,
            "datum": str(self.datum)
        }


class Vadba:
    def __init__(self, tip_vadbe, kalorije, datum):
        self.tip_vadbe = tip_vadbe
        self.kalorije = kalorije
        self.datum = datum

    def v_slovar(self):
        return {
            "tip_vadbe": self.tip_vadbe,
            "kalorije": self.kalorije,
            "datum": str(self.datum)
        }