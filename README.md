# Reseptisovellus

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen reseptia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään reseptia.
- Käyttäjä näkee sovellukseen lisätyt reseptit. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät reseptit.
- Käyttäjä pystyy etsimään reseptit hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä reseptit.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät reseptit.
- Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. onko resepti vegaaninen).
- Sovelluksessa on pääasiallisen tietokohteen lisäksi toissijainen tietokohde, joka täydentää pääasiallista tietokohdetta. käyttäjä pystyy lisäämään toissijaisia tietokohteita omiin ja muiden käyttäjien tietokohteisiin liittyen.
- Käyttäjä voi "tykätä" resepteistä

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ APP_SECRET_KEY="sinun salainen avain" flask run
```
## Suuri tietomäärä

Sovellusta on testattu suurella tietomäärällä. Testi suoritettiin seed.py-tiedostolla. Sovellus toimii hyvin, vaikka tietomäärä on suuri. Home-, käyttäjä-, resepti- sekä hakusivuilla on sivutus. Se huomattavasti helpottaa sovelluksen käyttöä.