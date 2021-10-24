## Paikallinen asennus:

Kloonaa sovellus käyttämällä terminaalissa tätä komentoriviä: 

```
git clone https://github.com/limi96/helpforum.git
```

Siirry terminaalissa projektikansioon 

```
cd helpforum
```

Asenna python -virtuaaliympäristö komennolla: 
```
python3 -m venv venv
```
Ota virtuaaliympäristö käyttöön:
```
source venv/bin/activate
```

Asenna sovelluksen tarvitsemat riippuvuudet:
```
pip install -r requirements.txt
```

Noudata tämän videon ohjeita paikallisen tietokannan asennusta ja käynnistämistä varten: https://www2.helsinki.fi/fi/unitube/video/617d690b-b1ce-44f0-997a-dca01bf7eff0. Muista, että tietokannan on oltava käynnistettynä ennen sovelluksen käynnistämistä. 


Käynnistä ohjelma
```
flask run
```
Pääset nyt testaamaan sovellusta osoitteessa http://127.0.0.1:5000/

## Asentaminen Herokuun

Noudata ylläolevia ohjeita ja luo githubiin repositorio.

Luo käyttäjätili Herokussa. Siirry projektikansioon. 

Kirjaudu Herokuun
```
heroku login
```
Tämän jälkeen voit luoda sovelluksen komennolla
```
heroku apps:create nimi_tahan
```
Kytke paikallinen repositorio Herokuun

```
git remote add heroku https://git.heroku.com/nimi_tahan.git

```

Määrittele palvelin ja vaatimukset Herokulle. Huom! pitää suorittaa virtuaaliympäristössä!

```
pip install gunicorn
pip freeze > requirements.txt
```

Luo Herokun tarvitsema asennustiedosto
```
git add Procfile
```

Luo sovellukselle tietokanta Herokuun:
```
heroku addons:create heroku-postgresql
```

Lisää sovelluksen tietokantakaavio Herokuun: 

```
heroku psql < schema.sql
```
Aseta salainen avain Herokulle: 

```
heroku config:set SECRET_KEY=(kirjoita avain tähän)
```

Lähetä sovellus herokuun 

```
git push heroku main
```