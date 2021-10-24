# helpforum

Sovellusta pääsee testaamaan Herokussa osoitteessa http://tsoha-helpforum.herokuapp.com/

Tietokanta on toteutettu PostgreSQL-tietokannalla. 

Sovelluksen ideana on, että käyttäjät voivat luoda oman keskustelualueen, jossa ensimmäinen postaus on käyttäjän luoma kysymys ja muut käyttäjät voivat vastata kysymykseen kommentoimalla alkuperäistä postausta.

Samalla jokainen käyttäjä voi äänestää, mistä kommenteista oli eniten apua. Kommentit voidaan laittaa joko niiden äänestyspisteiden tai laatimisajankohdan mukaisesti. Alkuperäinen postaaja voi valita parhaimman vastauksen kysymykseensä, jolloin kysymys luokitellaan ratkaistuksi eikä uusia vastauksia sallita enää.

Kaikilla käyttäjillä on “omat kysymykset” -näkymä, josta he voivat seurata, minkälaisia vastauksia heidän kysymyksensä ovat saaneet. 

## Puutteet:

* Hakutuloksien näkymässä ei ole mahdollista muuttaa tuloksien järjestyksiä.
* Routes-tiedostojen järjestäminen omaan kansioon ei onnistunut, koska Heroku aina herjasi tämän, eikä löytänyt enää tiedostoja.
* Paikallisesti testattuna näitä ongelmia ei ollut.
* Sama koskee myös fetch.py, queries.py, users.py ja thread_functions.py. Ideaalitapauksessa nämä olisivat voineet olla omassa "functions"-kansiossa.

## Toteutetut toiminnallisuudet: 

### Yleiset käyttäjätoiminnot:
* Käyttäjä voi luoda oman tunnuksen ja kirjautua sillä sisään
* Jokaisella käyttäjänimellä on vain yksi tunnus
* Jokaisella käyttäjällä on oma profiili, jossa näkyvät hänen viimeisimmät kysymykset ja vastaukset.

### Kysymyksien etsiminen ja tarkastelu: 
* Etusivulla näkyy 5 kysymystä, joilla on viimeisimmät vastaukset. 
* Yksittäinen kysymys näkyy vain kerran etusivulla
* Browse-sivulta saa listan muiden käyttäjien, omista tai kaikkien käyttäjien kysymyksistä.
* Ratkaistut kysymykset tallennetaan solved-tauluun ja käyttäjät voivat etsiä näitä solved-sivulta
* Listatuille kysymyksille on monia vaihtoehtoja niiden järjestysnäkymille.
* Jos kysymyksellä ei ole vastauksia ja järjestys valitaan vastauksien ajankohdan mukaan, kysymys sijoitetaan aina listan perään.

### Kysymysketjun toiminnallisuudet:
* Käyttäjä voi luoda kysymysketjun asettamalla otsikon ja antamalla lisätietoja kysymyksestä
* Käyttäjät voivat myös kirjoittaa vastauksia kyseiselle kysymyksille.
* Käyttäjät voivat editoida tai poistaa vain omia kysymyksiä ja vastauksia. Poikkeuksena ovat adminit.
* Käyttäjät voivat myös antaa pisteitä vastauksille. Jokainen käyttäjä saa vain **yhden äänen**
* Alkuperäinen kirjoittaja voi valita parhaimman vastauksen kysymysketjussa. Tällöin ketju suljetaan (ei enää uusia vastuaksia) ja paras vastaus tuodaan näkyvästi esille. Kysymys luokitellaan nyt ratkaistuksi ja otsikoon laitetaan ”[SOLVED]"-merkintä
* Listatuille vastauksille on monia vaihtoehtoja niiden järjestysnäkymille.

### Hakutoiminto:
* Sivustosta voi etsiä käyttäjänimiä, kysymyksiä ja vastauksia  Search-sivulta käyttämällä avainsanaa.
* Kysymysten hausa tulokset etsitään kysymyksen otsikosta tai sen lisätiedoista.
* Kysymyksiä ja vastauksia etsiessä haun voi myös rajata siten, että etsitään tietyn käyttäjänimen postauksia.
* Haku on CASE INSENSITIVE.

### Tietoturva:
* SQL-injektio, XXS -ja CSRF-haavoittuvuudet käsitelty
* Käyttäjien salasanat tallennetaan SECRET_KEY:n avulla tietokantaan
* Syötteiden tarkastus implementoitu. Käyttäjä näkee tekstikentissä, onko hänen syötteensä sopivan pituinen.
* Käyttäjä ei pääse muokkaamaan muiden käyttäjien kysymyksiä/vastauksia.






