import bottle
from datetime import date
import os

from model import MAPA_Z_UPORABNIKI, TIPI_OBROKOV, CILJI, Uporabnik, Postava, Obrok, Vadba

skrivnost = 'zelo_sem_vesel_da_lahko_programiram'

if not os.path.isdir(MAPA_Z_UPORABNIKI):
    os.mkdir(MAPA_Z_UPORABNIKI)

def nastavi_piskotek(uporabnisko_ime):
    bottle.response.set_cookie('uporabnisko_ime', uporabnisko_ime, path='/', secret=skrivnost)

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=skrivnost)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
    return Uporabnik.pridobi_podatke_uporabnika(uporabnisko_ime)

@bottle.get('/prijava/')
def prijava():
    return bottle.template('prijava.html', cilji = CILJI, error = None)

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    zasifrirano_geslo = Uporabnik.sifriraj_geslo(geslo)
    uporabnik = Uporabnik.pridobi_podatke_uporabnika(uporabnisko_ime)
    if uporabnik is None or zasifrirano_geslo != uporabnik.zasifrirano_geslo:
        return bottle.template('prijava.html', cilji = CILJI, error = "Nepravilno uporabniško ime ali geslo.")
    else:
        nastavi_piskotek(uporabnik.uporabnisko_ime)
        bottle.redirect('/')

@bottle.post('/registracija/')
def registracija():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    zasifrirano_geslo = Uporabnik.sifriraj_geslo(geslo)
    spol = bottle.request.forms.getunicode('spol')
    visina = bottle.request.forms['visina']
    teza = bottle.request.forms['teza']
    starost = bottle.request.forms['starost']
    postava = Postava(spol, visina, teza, starost)
    cilj = bottle.request.forms.getunicode('cilj')
    if Uporabnik.ali_uporabnik_ze_obstaja(uporabnisko_ime):
        return bottle.template('prijava.html', cilji = CILJI, error = "Uporabnik s tem imenom že obstaja")
    uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, postava, cilj)
    uporabnik.shrani_slovar()
    nastavi_piskotek(uporabnik.uporabnisko_ime)
    bottle.redirect('/')

@bottle.get('/')
def zacetna_stran():
    oseba = trenutni_uporabnik()
    return bottle.template('zacetna_stran.html', oseba = oseba, datum = date.today(), tipi_obrokov = TIPI_OBROKOV)

@bottle.post('/dodaj_obrok/')
def dodaj_obrok():
    oseba = trenutni_uporabnik()
    oseba.nov_obrok(
        bottle.request.forms.getunicode('tip_obroka'), 
        bottle.request.forms['kalorije'], 
        bottle.request.forms['datum']
        )
    oseba.shrani_slovar()
    return bottle.redirect('/')

@bottle.post('/dodaj_vadbo/')
def dodaj_vadbo():
    oseba = trenutni_uporabnik()
    oseba.nova_vadba(
        bottle.request.forms.getunicode('vadba'), 
        bottle.request.forms['kalorije'], 
        bottle.request.forms['datum']
        )
    oseba.shrani_slovar()
    return bottle.redirect('/')

@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')


bottle.run(debug=True, reloader=True)