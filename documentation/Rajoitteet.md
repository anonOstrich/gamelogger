Sovelluksen rajoitteet
======================

* Indeksejä on itse toteutettuna vain yksi. Suurilla tietomäärillä haut saattavat olla välillä tästä johtuen melko hitaita. 

* Tällä hetkellä käyttäjillä on kahdenlaisia rooleja: on yksi admin, ja muut ovat normaaleja käyttäjiä. Jos käyttäjiä olisi paljon, olisi tiedon asiallisuuden tarkastaminen yhdelle adminille hyvin aikaavievää. Moderaattori-roolin lisäyksellä voitaisiin antaa oikeus muokata/poistaa käyttäjien arvosteluja monelle moderaattorille, jolloin sisällön laadun tarkkailu olisi helpompaa. Adminilla voisi moderaattorien oikeuksien lisäksi olla ainakin mahdollisuus antaa/poistaa moderaattorirooli tai poistaa käyttäjätili kokonaan. 

* Suuri osa tietokannan tiedoista esitetään taulukkomuodossa. Vaikka ne ovatkin skrollattavissa sivulle myös mobiililaitteilla, on sivustoa silti vaikeampi käyttää kännykkällä. Vaihtoehtoinen esitystapa voisi mahdollistaa esimerkiksi sen, että tarvittaessa osa pelin tiedoista tulee allekkain. Taulukko vaatii yhden pelin kaikki tiedot aina vierekkäin. 

* Osa ominaisuuksista vaatii epämiellyttävän monta toimintoa. Esimerkkinä uuden tagin luominen ja peliin liittäminen, kun on pelin sivulla:
Muuta pelin tageja -> Hallinnoi tagejasi -> Lisää. Tältä sivulta ei ole helppoa polkua takaisin sen pelin sivulle, jota aiemmin tarkasteli. On siis jotain kautta navigoitava itsensä pelin sivulle ja valittava uudelleen "Muuta pelin tageja". Toinen mahdollisuus on tietenkin selaimen edellinen-toiminto, jolloin sivu on tosin päivitettävä jotta lisätty tagi näkyy mahdollisten tagien joukossa. 

* Hakusivun tulossivujen välillä siirtyminen on toteutettu kenties siten, että se vaatii jokaisella siirtymällä melko paljon tiedonsiirtoa. Selain ja palvelin lähettelevät jatkuvasti edestakaisin käyttäjän täyttämää lomaketta, jotta palvelinohjelma tietää minkä haun tuloksia käyttäjä haluaa nähdä sivulla. 

* Ulkoasu ja asettelu eivät ole kaikilla sivuilla yhtenäisiä, mikä voi vaikuttaa kokemukseen etenkin mobiililaitteilla. 

* Sivuja ei ole testattu esim. screen readerilla, mutta oletettavasti käyttö olisi hyvin haastavaa. Myös melko haaleat värit voivat olla vaikeaa erottaa toisistaan näkörajoitteisille. 

* Tietokantaa ei alusteta valmiiksi kootulla testidatalla jos tietokantaa ei ole olemassa. On hyvin työlästä sijoittaa komentorivilta / nettisivun kautta riittävä määrä dataa sivulle. 


