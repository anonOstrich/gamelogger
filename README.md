Peliloki
========



Aiheen kuvaus
-------------

Helsingin yliopiston tietokantojen harjoitustyö, jossa on toteutettu pelitietokanta jossa on arvostelumahdollisuus. 

Kirjautuneet käyttäjät voivat kirjata pelaamiaan pelejä ja antaa näille tähti- ja tekstiarvion (vertaa elokuvien Letterboxd). He voivat myös lisätä peleille omia henkilökohtaisia tageja , joiden perusteella he voivat tehdä omia pelilistojaan (esim. “Keskiajalle sijoittuvat”). Kirjautuneet käyttäjät voivat myös lisätä järjestelmään uusia pelejä ja näiden kuvauksia. Kirjautuneena pystyy myös reagoimaan muiden arvioihin: niistä voi näyttää pitävänsä tai päinvastoin. Reagointien määrä näkyy kaikille arvostelun yhteydessä.   

Kaikki sivuston käyttäjät pystyvät selaamaan tietokannassa olevia pelejä ja niihin liittyviä arvosteluja. Oletuksena etusivulla näytetään eniten pelattuja/arvosteltuja pelejä. Pelejä voi etsiä esimerkiksi kehittäjän, nimen tai julkaisuvuoden mukaan. Tulokset, jotka näyttävät myös yhteenvetolukuja arvioista,  voi myös järjestää haluamansa sarakkeen perusteella. Pelin omilla siviulla näkyvät sen saamat arviot ja koko kuvaus. Käyttäjälistauksesta voi siirtyä käyttäjän omalle sivulle, jossa pystyy tarkastelemaan käyttäjän omaa kuvausta, sekä tämän tageja ja niihin liittyviä pelejä. 

Järjestelmällä on myös ylläpitäjä, joka pystyy  poistamaan/muokkaamaan pelejä/arvioita tietokannasta. Hän vastaa myös genrejen ylläpitämisestä. Ylläpitäjällä on myös normaalin käyttäjän rooli, eli hän pystyy osallistumaan pelien arviointiin ja lisäämiseen normaalisti. 


Toimintoja
-----------

  * Käyttäjätunnuksen luominen
  * Kirjautuminen
  * Uloskirjautuminen
  * Pelien lisääminen
  * Lisättyjen pelien selaaminen eri tietojen perusteella
  * Pelien muokkaaminen ja poistaminen
  * Arvion kirjoittaminen, muokkaaminen ja poistaminen
  * Tietyn pelin arvioiden tutkiminen 
  * Arvioista “tykkääminen” tai “ei-tykkääminen” 
  * Omien tagien lisääminen järjestelmään
  * Tagien liittäminen peliin 
  * Kenen tahansa tag-listojen selaaminen


Monimutkaiset yhteenvetokyselyt
------------------------------

Arvioinnin vaatimasta monimutkaisemmasta yhteenvetokyselystä esimerkkinä on etusivun listaus eniten arvioiduista peleistä. 
Näkymä tuotetaan seuraavalla SQL-kyselyllä: 

`SELECT Game.id, Game.name, Game.year, Game.developer, COUNT(Review.points), AVG(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id GROUP BY Game.id ORDER BY COUNT(Review.points) LIMIT 5; `

Toinen vaihtoehto on kirjautuneille käyttäjille etusivulla näytettävä lista peleistä, joita he eivät ole arvioneet. Sanotaan, että käyttäjän id on x. Tällöin näkymään tarvittavat tiedot saadaan kyselyllä: 

`SELECT Game.id, Game.name FROM Game LEFT JOIN Review ON Game.id = Review.game_id WHERE Game.id NOT IN (SELECT Review.game_id FROM Review WHERE Review.account_id = x);`

Tunnukset
---------

### Admin-käyttäjä

tunnus: admin
salasana: admin_password

### Normaali käyttäjä

tunnus: testi
salsana: salasana

Voit myös rekisteröidä oman testikäyttäjän, jolla ei ole adminin-roolia. Vaikka sovelluksessa on pyritty huomioimaan salasanojen riittävän turvallinen tallentaminen, suosittelen silti olemaan käyttämättä oikeassa käytössä olevia salasanoja.



Linkkejä: 
---------

[Sovellus herokussa](https://peliloki.herokuapp.com/)

[Tietokantakaavio](https://github.com/anonOstrich/peliloki/tree/master/documentation/Tietokantakaavio.md)

[Käyttötapaukset](https://github.com/anonOstrich/peliloki/tree/master/documentation/Käyttötapaukset.md)

[Rajoitteet](https://github.com/anonOstrich/peliloki/tree/master/documentation/Rajoitteet.md) ja [puuttuvat ominaisuudet](https://github.com/anonOstrich/peliloki/tree/master/documentation/Puuttuvat_ominaisuudet.md)

[Asennusohje](https://github.com/anonOstrich/peliloki/tree/master/documentation/Asennusohje.md)

[Käyttöohje](https://github.com/anonOstrich/peliloki/tree/master/documentation/Käyttöohje.md)

[Omat kokemukset projektista](https://github.com/anonOstrich/peliloki/tree/master/documentation/Omat_kokemukset.md)