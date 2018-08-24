peliloki
========

Rekisteröityneet käyttäjät voivat kirjata pelaamiaan pelejä ja antaa näille tähti- ja tekstiarvion (vertaa elokuvien Letterboxd). He voivat myös lisätä peleille omia henkilökohtaisia tagejaan , joiden perusteella he voivat tehdä omia pelilistojaan (esim. “Keskiajalle sijoittuvat”). Kirjautuneet käyttäjät voivat myös lisätä järjestelmään uusia pelejä ja näiden kuvauksia. Kirjautuneena pystyy myös reagoimaan muiden arvioihin: niistä voi näyttää pitävänsä tai päinvastoin. Reagointien määrä näkyy kaikille arvostelun yhteydessä.   

Kaikki sivuston käyttäjät pystyvät selaamaan tietokannassa olevia pelejä ja niihin liittyviä arvosteluja. Oletuksena etusivulla näytetään äskettäin lisättyjä arvosteluja. Pelejä voi etsiä esimerkiksi kehittäjän, nimen tai julkaisuvuoden mukaan. Klikkaamalla käyttäjätunnusta pääsee tutkailemaan tämän käyttäjän arvioimia pelejä ja tagien perusteella luotuja listoja.

Järjestelmällä on myös ylläpitäjä, joka pystyy ainakin poistamaan käyttäjätunnuksia ja muokkaamaan mitä tahansa sivulla olevaa tietoa. Mahdollisesti myös elokuvien tietojen syöttäminen järjestelmään voisi olla ylläpitäjän vastuulla.

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
  * Muiden arvioiden kommentoiminen (mahdollinen toteutettava ajan salliessa)
  * Muiden käyttäjien seuraaminen(mahdollinen toteutettava ajan salliessa) 

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

Käyttöohje:
-----------

Etusivulla näet perustietoja sivusta ja käyttäjät, jotka eivät ole vielä arvioineet pelejä. Kirjautuneille on näkyvillä myös lista peleistä, joita he eivät ole arvioineet; listasta voi siirtyä suoraan pelin sivulle. Yläpalkki pysyy pääpiirteiltään samanlaisena kaikkialla sivustossa. Vasemmanpuolimmaista "Peliloki"-tekstiä painamalla pääset aina palaamaan etusivulle. 
Halutessasi rekisteröityä paina oikealta ylhäältä "rekisteröidy", täytä tietosi ja valitse "Rekisteröidy". Nyt käytössäsi on kirjautumismahdollisuus, jota voit hyödyntää painamalla yläpalkin oikeammaisinta linkkiä, "Kirjaudu".  

Ilmankin kirjautumista pystyy selaamaan tietokannan tietoja. Valitsemalla yläpalkista "Genret" saa näkyviin lisätyt genret ja niihin liittyvien pelien lukumäärät. Jos olet kirjautunut admin-tunnuksella, pystyt samalta sivulta myös lisäämään uuden genren. Klikkaamalla genreä saat näkyviin sivun, jolla on lueteltu kaikki kyseisen genren pelit. Pelistä on lueteltu perustiedot ja lisäksi sen arvioiden lukumäärä ja keskiarvo.  
Hyvin samanlaisen näkymän saa painamalla yläpalkin "Kaikki pelit"-linkkiä; samat tiedot näytetään vain kaikista peleistä, eikä ainoastaan yhden genren. Kummasta tahansa listauksesta voi klikata pelin nimeä, jolloin pääsee kyseisen pelin omalle sivulle. Siellä näytetään pidempi kuvaus ja kaikki pelin arviot. Rekisteröityneet käyttäjät voivat tykätä tai olla pitämättä muiden arvioisa, ja kaikille sivun vierailijoille näytetään tiedot arvion saamista reaktioista arvion yhteydessä.  

Rekisteröityneet käyttäjät pystyvät pelin omalla sivulla reagoimaan arvioihin painamalla taulukossa oikealla olevaa "tykkään"/"en tykkää"-painiketta. Reagointimahdollisuus poistuu yhden kerran jälkeen. He voivat myös kirjoittaa oman arvostelun painamalla pelin tietojen oikealla puolella olevaa arviointinäppäintä. Arvio kirjoitetaan omalla sivullaan, ja se koostuu tekstistä ja numeroarviosta 1-10. Arvion kirjoittamisen jälkeen käyttäjä palautetaan arviota koskeneen pelin omalle sivulle. Arvion yhteydessä näkyy muokkauslinkki sen kirjoittajalle tunnin verran kirjoittamisen jälkeen. Myös admineilla on mahdollisuus muokkaamiseen. 

Kirjautuneet käyttäjät näkevät yläpalkissa uuden linkin, "Lisää peli". Sen painaminen johtaa erilliselle lomakesivulle jossa täydennetään pelin perustiedot. Samassa yhteydessä on mahdollista valita genret, joihin peli kuuluu. Kun uuden pelin on kerran lisännyt, eivät sitä pysty muokkaamaan kuin adminit, joille pelin sivulla näkyy sen tietojen vieressä muokkausnappula. He pystyvät muokkaamaan kaikkia pelin tietoja, joita sivuston kautta voi tarkastella. 


Linkkejä: 
---------

[Sovellus herokussa](https://peliloki.herokuapp.com/)

[Tietokantakaavio](https://github.com/anonOstrich/peliloki/tree/master/documentation/Tietokantakaavio.png)

[Käyttötapaukset](https://github.com/anonOstrich/peliloki/tree/master/documentation/Käyttötapaukset.md)


Asennusohje
-----------

### Paikalliselle tietokoneelle (linux)

Oletetaan, että asennettuina on valmiiksi ajantasainen versio [pythonista](https://www.python.org/), siihen [pip](https://packaging.python.org/key_projects/#pip)-työkalu ja [venv](https://docs.python.org/3/library/venv.html)-kirjasto. 

1. Paina GitHub-sivun oikeassa olevaa vihreää nappulaa "Clone or download" ja valitse "Download zip"
2. Ladattuasi tiedosto pura se haluamaasi sijaintiin. Sijainniksi käy esimerkiksi Documents, eli "/home/username/Documents". 
3. Navigoi kansion Documents/peliloki-master/ sisään ja avaa komentorivi.

   Voit mennä tiedostoselaimella kyseiseen sijaintiin, painaa hiiren oikealla näppäimellä ja valita "Open in Terminal", tai vastaavan komennon.   
   Toinen vaihtoehto on avata komentorivi ja navigoida sillä oikean kansion sisälle.
4. Suorita komento `python3 -m venv venv`
5. Avaa virtuaalinen ympäristö komennolla `source venv/bin/activate`
6. Asenna tarvittavat tiedostot komennolla `pip install -r requirements.txt`
7. Käynnistä sovellus komennolla `python run.py`

Sovellus on nyt käynnissä osoitteessa <http://127.0.0.1:5000/>. Siirry sinne valitsemallasi selaimella, ja olet sovelluksen etusivulla. 


### Erilliselle palvelimelle (heroku)

Oletetaan samat asiat kuin paikallisessa asennuksessa. Lisäksi oletetaan, että asennettuina ovat [git](https://github.com/git/git) ja [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). 
1. Seuraa paikallisia asennuskohtia kunnes olet suorittanut askeleen 3
2. Suorita komento `heroku create sovelluksen_nimi`.

   Voit nimetä sovelluksen haluamaksesi, tai jättää nimen pois komennosta. 
   Jos et ole kirjautunut sisään, syötä kirjautumistietosi niitä kysyttäessä.   
   Jos haluat, että sovelluksessa on käytössä pysyvä tietokanta, suorita muutama lisäaskel:   
   Luo Herokuun ympäristömuuttuja komennolla `heroku config:set HEROKU=1`  
   Luo sovelluksen käyttöön PostgreSQL-tietokanta komennolla `heroku addons:add heroku-postgresql:hobby-dev`  
   
   Tällöin sovellukseen syötetyt tiedot pysyvät tallessa vaikka se käynnistyisi uudellen palvelimella.
3. Suorita `git init`
4. Suorita `git remote add heroku https://git.heroku.com/sovelluksen_nimi.git`. Voit tarkastaa nimen komennolla `heroku apps`
5. Suorita `git add .`
6. Suorita `git commit -m "Ensimmäinen commit"`, tai muulla haluamallasi viestillä
7. Suorita `git push heroku master`, jolloin tiedostot lähetetään Herokun palvelimelle.
8. Sovellus käynnistetään herokussa. 

Käynnistymisen jälkeen se löytyy osoitteesta <https://sovelluksen_nimi.herokuapp.com>