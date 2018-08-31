Tietokantakaavio
================

![Tietokantakaavio joka näyttää luokkien yhteydet ja lukumäärärajoitteet](/documentation/images/Tietokantakaavio.png "Tietokantakaavio")





CREATE TABLE -lauseet
---------------------

* 
```
CREATE TABLE Account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(100) NOT NULL, 
	username VARCHAR(100) NOT NULL, 
	password_hash BLOB NOT NULL, 
	description VARCHAR(1000), 
	PRIMARY KEY (id), 
	UNIQUE (username)
   );
```

* 
```
CREATE TABLE Role (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(64) NOT NULL, 
	PRIMARY KEY (id)
   );
``` 

* 
```
CREATE TABLE User_role (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	account_id INTEGER NOT NULL, 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (account_id, role_id), 
	FOREIGN KEY(account_id) REFERENCES Account (id), 
	FOREIGN KEY(role_id) REFERENCES Role (id)
   );
```

* 
```
CREATE TABLE Genre (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(128) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
   );
```

* 
```CREATE TABLE Game (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(200) NOT NULL, 
	developer VARCHAR(100) NOT NULL, 
	description VARCHAR(1000) NOT NULL, 
	year INTEGER NOT NULL, 
	PRIMARY KEY (id)
   );
```

* 
```
CREATE TABLE Game_genre (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	game_id INTEGER NOT NULL, 
	genre_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (game_id, genre_id), 
	FOREIGN KEY(game_id) REFERENCES game (id), 
	FOREIGN KEY(genre_id) REFERENCES genre (id)
   );
```

* 
```
CREATE TABLE tag (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(200) NOT NULL, 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name, account_id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
   );
```

* 
```
CREATE TABLE game_tag (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	tag_id INTEGER NOT NULL, 
	game_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (tag_id, game_id), 
	FOREIGN KEY(tag_id) REFERENCES tag (id), 
	FOREIGN KEY(game_id) REFERENCES game (id)
   );
```

* 
```
CREATE TABLE review (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	text VARCHAR(2000) NOT NULL, 
	points INTEGER NOT NULL, 
	account_id INTEGER NOT NULL, 
	game_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (account_id, game_id), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(game_id) REFERENCES game (id)
   );
```

*
```
CREATE TABLE reaction (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	positive BOOLEAN NOT NULL, 
	account_id INTEGER NOT NULL, 
	review_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (account_id, review_id), 
	CHECK (positive IN (0, 1)), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(review_id) REFERENCES review (id)
   );
```


   Indeksin luominen
   -----------------

   * `CREATE INDEX ix_game_developer ON Game (developer);`