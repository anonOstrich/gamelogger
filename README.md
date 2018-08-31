peliloki
========



Aiheen kuvaus
-------------

Rekisteröityneet käyttäjät voivat kirjata pelaamiaan pelejä ja antaa näille tähti- ja tekstiarvion (vertaa elokuvien Letterboxd). He voivat myös lisätä peleille omia henkilökohtaisia tagejaan , joiden perusteella he voivat tehdä omia pelilistojaan (esim. “Keskiajalle sijoittuvat”). Kirjautuneet käyttäjät voivat myös lisätä järjestelmään uusia pelejä ja näiden kuvauksia. Kirjautuneena pystyy myös reagoimaan muiden arvioihin: niistä voi näyttää pitävänsä tai päinvastoin. Reagointien määrä näkyy kaikille arvostelun yhteydessä.   

Kaikki sivuston käyttäjät pystyvät selaamaan tietokannassa olevia pelejä ja niihin liittyviä arvosteluja. Oletuksena etusivulla näytetään äskettäin lisättyjä arvosteluja. Pelejä voi etsiä esimerkiksi kehittäjän, nimen tai julkaisuvuoden mukaan. Klikkaamalla käyttäjätunnusta pääsee tutkailemaan tämän käyttäjän arvioimia pelejä ja tagien perusteella luotuja listoja.

Järjestelmällä on myös ylläpitäjä, joka pystyy ainakin poistamaan käyttäjätunnuksia ja muokkaamaan mitä tahansa sivulla olevaa tietoa. Hän vastaa myös genrejen ylläpitämisestä

Toimintoja: 
-----------

  * Käyttäjätunnuksen luominen
  * Kirjautuminen
  * Pelien lisääminen
  * Lisättyjen pelien selaaminen eri tietojen perusteella
  * Pelien muokkaaminen ja poistaminen
  * Arvion kirjoittaminen, muokkaaminen ja poistaminen
  * Tietyn pelin arvioiden tutkiminen 
  * Arvioista “tykkääminen” tai “ei-tykkääminen” 
  * Omien tagien lisääminen 
  * Tagien perusteella käyttäjän listojen selaaminen



### Huomioita arvosteluun

Sovelluksen monimutkaisempia yhteenvetokyselyitä ovat esimerkiksi etusivun arvioita tekemättömien käyttäjien esittäminen ja myös kirjautuneille käyttäjille näytettävä lista peleistä, joita kyseinen käyttäjä ei ole vielä arvioinut. Myös pelin yksittäisellä sivulla esitettävät arviot saattavat täyttää vaatimukset (/application/reactions/models.py, metodi find_all_reactions_for_reviews_of_game)

Tunnukset
---------

### Admin-käyttäjä: 
tunnus: admin
salasana: admin_password

### Normaali käyttäjä
tunnus: testi
salsana: salasana

Voit myös rekisteröidä oman testikäyttäjän, jolla ei ole adminin roolia. Vaikka sovelluksessa on pyritty huomioimaan salasanojen riittävän turvallinen tallentaminen, suosittelen silti olemaan käyttämättä oikeassa käytössä olevai salasanoja.



Linkkejä: 
---------

[Sovellus herokussa](https://peliloki.herokuapp.com/)

[Tietokantakaavio](https://github.com/anonOstrich/peliloki/tree/master/documentation/Tietokantakaavio.md)

[Käyttötapaukset](https://github.com/anonOstrich/peliloki/tree/master/documentation/Käyttötapaukset.md)

[Rajoitteet](https://github.com/anonOstrich/peliloki/tree/master/documentation/Rajoitteet.md) ja [puuttuvat ominaisuudet](https://github.com/anonOstrich/peliloki/tree/master/documentation/Puuttuvat_ominaisuudet.md)

[Asennusohje](https://github.com/anonOstrich/peliloki/tree/master/documentation/Asennusohje.md)

[Käyttöohje](https://github.com/anonOstrich/peliloki/tree/master/documentation/Käyttöohje.md)

[Omat kokemukset projektista](https://github.com/anonOstrich/peliloki/tree/master/documentation/Omat_kokemukset.md)








