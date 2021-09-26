# helpforum

Sovellusta pääsee testaamaan osoitteessa http://tsoha-helpforum.herokuapp.com/

Sovelluksen ideana on, että käyttäjät voivat luoda oman keskustelualueen, jossa ensimmäinen postaus on käyttäjän luoma kysymys ja muut käyttäjät voivat vastata kysymykseen kommentoimalla alkuperäistä postausta.

Samalla jokainen käyttäjä voi äänestää, mistä kommenteista oli eniten apua. Kommentit voidaan laittaa joko niiden äänestyspisteiden tai laatimisajankohdan mukaisesti.

Kaikilla käyttäjillä on “omat kysymykset” -näkymä, josta he voivat seurata, minkälaisia vastauksia heidän kysymyksensä ovat saaneet. 

Kaikki kysymykset postataan yhteiselle seinälle, josta jokainen voi katsoa, minkälaisia kysymyksiä käyttäjillä on ollut. 

Tällä hetkellä sovelluksessa on kaikki perustoiminnot. Sovellukseen ei kuitenkaan ole vielä implementoitu käyttäjänoikeuksien tarkastajaa, lomakesyötteiden tarkastusta, eikä huomioitu CSRF-haavoittuvuutta. Mahdollisia lisätoimintoja olisivat omien kysymysten ja vastauksien poistaminen.

Sovelluksen ulkoasua ei ole varsinaisesti suunniteltu yhtään, joten tämä on heti työn alla sen jälkeen, kun kaikki yllämainitut puutteet saadaan hoidettua pois alta.



