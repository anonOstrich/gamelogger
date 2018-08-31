User storyt
===========

Käyttötapaukset eritelty käyttäjäroolikohtaisesti. jokaisen käyttötapauksen alla on jokin SQL-kysely. Joko kyselyä käytetään sellaisenaan sovelluksessa, tai sitten kyselyllä voitaisiin saavuttaa haluttu toiminnallisuus. SQL-kyselyissä ... viittaa että valitaan halutut sarakkeet tulokseen. 


Vierailija (ei-kirjautunut selailija)
-------------------------------------

* Vierailijana haluan nähdä äskettäin lisättyjä arvosteluja, jotta huomaan uusia mahdollisesti itseäni kiinnostavia mielipiteitä.  
`katsotaan toteutetaanko...`
* Vierailijana haluan nähdä kaikki pelit valitsemallani rajauksella, jotta löydän haluamani kaltaisia pelejä 
   Esim. kaikki kauhupelit: 

   ```
   SELECT Game.id, ... , Game.description  FROM Game JOIN Game_genre ON Game.id = Game_genre JOIN Genre ON Game_genre.genre_id = Genre.id WHERE Genre.name = "Kauhu"; 
   ```

* Vierailijana haluan hakea peliä nimen perusteella, jotta voin lukea muiden mielipiteitä itseäni miellyttävästä pelistä. 
    Esim. pelit, joiden nimessä esiintyy annettu merkkijono
    ```
    SELECT Game.id, ..., Game.description FROM Game WHERE Game.name LIKE '%esimerkki_nimi%';
    ```
* Vierailijana haluan voida avata yksittäisen pelin sivun, jotta voin lukea sen kuvauksen ja muiden arvostelut.  
    Esim. Joitakin pelin , arvostelun ja arvostelun kirjoittajan tietoja yhdellä kyselyllä. Pelin tiedot haetaan vaikka arvosteluja ei olisikaan. 

    ```
    SELECT Game.name, Game.description, Review.text, Review.points, Account.username FROM Game LEFT JOIN  Review ON Game.id = Review.game_id
    JOIN Account ON Account.id = Review.account_id; 
    ```
* Vierailijana haluan nähdä pelin keskiarvoisen tähtiarvion, jotta voin muodostaa yleiskuvan siitä, kuinka pidetty peli on. 
    `SELECT AVG(Review.points) FROM Review WHERE Review.game_id = esimerkki_id;` (pelin id:n perusteella)
    tai 
    `SELECT AVG(Review.points) FROM Review JOIN Game ON Review.game_id = Game.id WHERE Game.name = 'esimerkki_nimi';` (pelin nimen perusteella)

* Vierailijana haluan nähdä listan valitsemani käyttäjän arvioista, jotta voin lukea kiinnostavan henkilön kaikki näkemykset. 

    ```
    SELECT Game.name, Review.text, Review.points FROM Game JOIN Review ON Game.id = Review.game_id JOIN Account ON Account.id = Review.account_id
    WHERE Account.name = 'esimerkki_nimi'
    ```
* Vierailijana haluan voida rekisteröityä, jotta voin tuottaa sivulle sisältöä. 
    `INSERT INTO Account(name, username, password_hash) VALUES('Matti Meikäläinen', 'nuuskakissa', hashed_and_salted('kissa2'));`

* Vierailijana haluan järjestää pelit haluamani ominaisuuden mukaan 
    esim. arvostelujen lukumäärän mukaan laskevasti 
    `SELECT Game.name, COUNT(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id GROUP BY Game.name ORDER BY COUNT(review.points) DESC`

Käyttäjä (kirjautunut selailija)
--------------------------------

* Käyttäjänä haluan luoda itsestäni kuvauksen, jotta muut käyttäjät voivat kiinnostuani tuottamastani sisällöstä 
   `UPDATE Account SET description = 'uusi kuvaus itsestäni' WHERE username = 'nuuskakissa';`

* Käyttäjänä haluan lisätä uuden pelin, jotta voin merkitä sille arvostelun.  
    `INSERT INTO Game(name, description, developer, year) VALUES('Overwatch', 'hittipeli', 'Blizzard', 2017);`

* Käyttäjänä haluan kirjautua ulos, jotta muut saman koneen käyttäjät eivät näe tietojani 
    ei liity tietokannan käyttöä 

* Käyttäjänä haluan jättää arvostelun, jotta voin kirjata pelin pelatuksi ja tallentaa ajatukseni. 
    `INSERT INTO Review(text, points, account_id, game_id) VALUES('Hyvä peli', 9, arvostelijan_id, arvosteltavan_pelin_id);` 

* Käyttäjänä haluan muokata arvosteluani, jotta voin korjata vahingossa sattuneen virheeni  
    `UPDATE Review SET text = 'muokattu teksti', points = muokattu_pistemäärä WHERE Review.account_id = arvostelijan_id;`
    tai 
    `UPDATE Review SET text = 'muokattu teksti', points = muokattu_pistemäärä WHERE Review.account_id IN (SELECT id FROM Account WHERE username = arvostelijan_käyttäjätunnus);`

* Käyttäjänä haluan reagoida muiden arvosteluihin, jotta voin auttaa hyvin kirjoitettuja arvioita näkymään huonoja paremmin.  
   `INSERT INTO Reaction(positive, account_id, review_id) VALUES(true, reagoijan_id, reagoitavan_arvostelun_id);`


* Käyttäjänä haluan luoda omia tagejani, jotta voin liittää niitä peleihin
    `INSERT INTO Tag(name) VALUES('Parhaat pelit);`

* Käyttäjänä haluan liittää omia tagejani peleihin, jotta voin luoda haluamiani pelilistoja.  
   `INSERT INTO Game_tag(game_id, tag_id) VALUES(liitettävän_pelin_id, liitettävän_tagin_id);`


Ylläpitäjä
----------

* Ylläpitäjänä haluan muokata minkä tahansa pelin tietoja, jotta varmistan tekstien asiallisuuden ja paikkansapitävyyden.
   `UPDATE Game SET name = 'muokattu nimi', ..., developer = 'muokattu kehittäjä' WHERE Game.id = muokattavan_pelin_id; `  

* Ylläpitäjänä haluan voida poistaa/muokata arvosteluja, jotta voin poistaa asiatonta sisältöä. 
   muokkaaminen: 
   `UPDATE Review SET text = 'muokkasin t:admin', points = 1 WHERE id = muokattavan_arvostelun_id;`

   poistaminen (poistetaan ensin turhaksi jäävät arvostelun reaktiot):  
  
  ```
  DELETE FROM Reaction WHERE review_id = poistettavan_arvostelun_id;
  DELETE FROM Review WHERE id = poistettavan_arvostelun_id;
  ```

* Ylläpitäjänä haluan lisätä genrejä, jotta käyttäjät voivat kuvata mahdollisimman tarkasti lisäämiään pelejä
    `INSERT INTO Genre(name) VALUES('Kauhu')`

* Ylläpitäjänä haluan poistaa genrejä, jotta pääsen eroon huonoista genrevalinnoista
    `DELETE FROM Genre WHERE id = poistettavan_genren_id;`
* Ylläpitäjänä haluan muokata käyttäjien omia kuvauksia, jotta voin poistaa asiattoman sisällön
    `UPDATE Account SET description = 'muokkasin t:admin' WHERE id = muokattavan_tekstin_alkuperäisen_kirjoittajan_id;`

* Ylläpitäjänä haluan poistaa käyttäjän tageja, jotta voin poistaa asiattoman sisällön
    `DELETE FROM Tag WHERE id = poistettavan_tagin_id;`


