# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:90:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:111:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:123:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:123:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:153:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:153:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:174:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:183:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:183:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:208:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:208:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:236:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:236:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:260:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:260:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:278:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:303:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:315:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:315:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:335:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:335:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:357:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:378:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.83/10 (previous run: 8.66/10, +0.16)

************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)

------------------------------------------------------------------
Your code has been rated at 6.50/10 (previous run: 6.50/10, +0.00)

************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 7.59/10 (previous run: 7.59/10, +0.00)

************* Module rcps
rcps.py:1:0: C0114: Missing module docstring (missing-module-docstring)
rcps.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:89:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:116:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:134:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:143:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:159:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:167:0: C0116: Missing function or method docstring (missing-function-docstring)
rcps.py:175:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.27/10 (previous run: 8.27/10, +0.00)

```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

## Missing function/module docstring

Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei käytetä docstring-kommentteja; tässä soveluksessa funktiot on nimetty kuvaavasti, eli funktion tarkoitus tulisi käydä selväksi sen nimestä.

## Inconsistent return statements

Nämä ilmoitukset liittyvät tilanteeseen, jossa funktio käsittelee metodit `GET` ja `POST` mutta ei muita metodeja (esim. funktio ```edit_comment(comment_id)``` ). Kysyiset funktiot ei käsittele muita metodeja, koska funktion dekoraattorissa on vaatimus, että metodin tulee olla `GET` tai `POST`.

## Dangerous default value

Tässä sovelluskessa vaarallinen oeltusarvo on tyhjä lsita esim. funktiossa `query(sql, params=[])`. Tyhjä lista ei ole tässä sovelluksesa varallista käyttää, koska funktiot, jtoka käyttää tämä oletusarvo, eivät muokkaa sitä, vaan lukevat sen.
