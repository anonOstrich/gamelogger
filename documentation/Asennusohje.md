Asennusohje
===========

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