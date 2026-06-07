# reseptisovellus

## sovelluksen toiminnot

- käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- käyttäjä pystyy lisäämään sovellukseen reseptia. lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään reseptia.
- käyttäjä näkee sovellukseen lisätyt reseptit. käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät reseptit.
- käyttäjä pystyy etsimään reseptit hakusanalla tai muulla perusteella. käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä reseptit.
- sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät reseptit.
- käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. onko resepti vegaaninen).
- sovelluksessa on pääasiallisen tietokohteen lisäksi toissijainen tietokohde, joka täydentää pääasiallista tietokohdetta. käyttäjä pystyy lisäämään toissijaisia tietokohteita omiin ja muiden käyttäjien tietokohteisiin liittyen.
- käyttäjä voi "tykätä" resepteistä

## sovelluksen asennus

asenna `flask`-kirjasto:

```
$ pip install flask
```

luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

voit käynnistää sovelluksen näin:

```
$ flask run
```
