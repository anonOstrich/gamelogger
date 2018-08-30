from application import db
from application.genres.models import GameGenre
from application.tags.models import GameTag
from application.models import Base
from application.utilities import page_query, shorten_if_longer_than, format_average
from application.constants import GAME_RESULTS_PER_PAGE
from sqlalchemy.sql import text
from sqlalchemy import bindparam
import os


class Game(Base):
    name = db.Column(db.String(200), nullable=False)
    developer = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    reviews = db.relationship("Review", backref="game", lazy=True)
    game_genres = db.relationship("GameGenre", backref="game", lazy=True)
    game_tags = db.relationship("GameTag", backref="game", lazy=True)

    def __init__(self, name, developer, description, year):
        self.name = name
        self.developer = developer
        self.description = description
        self.year = year

    def average(self):
        stmt = text("SELECT AVG(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id "
        " WHERE Game.id = :game_id GROUP BY Game.id;").params(game_id = self.id)

        res = db.engine.execute(stmt)

        for row in res: 
            return row[0]
            
        return None

    def update_genres(self, genre_ids):
        # voisiko tehdä vähemmällä tietokannan käytöllä kuin poistamalla aina kaikki?
        GameGenre.query.filter(GameGenre.game_id == self.id).delete()
        db.session.commit()
        self.add_genres(genre_ids)

    def add_genres(self, genre_ids):
        def create_game_genre(genre_id):
            result = GameGenre()
            result.game_id = self.id
            result.genre_id = genre_id
            return result

        g_genres = map(create_game_genre, genre_ids)
        db.session.add_all(g_genres)
        db.session.commit()

    def modify_tags(self, tag_ids):
        GameTag.query.filter_by(game_id=self.id).delete()
        self.add_tags(tag_ids)

    def add_tags(self, tag_ids):
        def create_game_tag(tag_id):
            result = GameTag()
            result.game_id = self.id
            result.tag_id = tag_id
            return result

        game_tags = map(create_game_tag, tag_ids)
        db.session.add_all(game_tags)
        db.session.commit()




    @staticmethod
    def find_all_unreviewed_games(user_id):
        stmt = text("SELECT DISTINCT Game.id, Game.name FROM Game"
                    " WHERE Game.id NOT IN (SELECT Game.id FROM Game JOIN Review ON Game.id = Review.game_id"
                    " WHERE Review.account_id = :user_id); "
                    ).params(user_id=user_id)

        res = db.engine.execute(stmt)
        return [{"id": row[0], "name":row[1]} for row in res]

    # dictionary with keyes being strings, e.g. "min_year":2000

    @staticmethod
    def find_all_info(parameters={}, page_number = 1):
        name_query = ""
        if "name" in parameters:
            # || on tapa liittää merkkijonoja yhteen sqlitessä ja postgresql:ssä
            name_query = "LOWER(Game.name) LIKE '%' || :name ||'%'"

        year_query = ""
        if "min_year" in parameters or "max_year" in parameters:
            first = ":min_year" if parameters["min_year"] else 0
            last = ":max_year" if parameters["max_year"] else 3000
            year_query = "Game.year BETWEEN " + \
                str(first) + "  AND " + str(last)

        developer_query = ""
        if "developer" in parameters:

            # Voidaan vaihtaa: LIKE, jolloin ei tarvitse tästämä täysin 
            # ja lowercase, jolloin kirjotusasulla ei väliä
            developer_query = "Game.developer LIKE :developer "

    

        average_query = ""
        if "min_average" in parameters or "max_average" in parameters:
            lowest_average = ":min_average" if "min_average" in parameters else 0
            highest_average = ":max_average" if "max_average" in parameters else 10
            no_average_addendum = "" if "min_average" in parameters else " OR AVG(Review.points) IS NULL"
            average_query = "AVG(Review.points) BETWEEN " + str(lowest_average) + \
                " AND " + str(highest_average) + no_average_addendum

        count_query = ""
        if "min_count" in parameters or "max_count" in parameters:
            lowest_count = ":min_count" if "min_count" in parameters else 0
            # ainakin postgreSQL:n integerin suurin arvo. Jos missään tulee vastaan niin herokussa, jossa ko tkhj käytössä
            highest_count = ":max_count" if "max_count" in parameters else 2147483647
            no_count_addendum = "" if "min_count" in parameters else " OR COUNT(Review.points) IS NULL"
            count_query = "COUNT(Review.points) BETWEEN " + str(lowest_count) + \
                " AND " + str(highest_count) + no_count_addendum



                

        genre_where_query = ""
        if "genres" in parameters:
            genre_where_query = " Game_genre.genre_id IN ("

            genre_parameter_names = []
            for genre_id in parameters["genres"]:
                genre_parameter_names.append(":genre_id" + str(genre_id))
                parameters.update({"genre_id" + str(genre_id): genre_id})
            
            genre_where_query = genre_where_query + ", ".join(genre_parameter_names)
            genre_where_query  = genre_where_query + " ) "


        genre_having_query = ""
        if "genres" in parameters:
            genre_having_query = genre_having_query + " COUNT(Game_genre.id) >= :number_of_genres"
            parameters.update({"number_of_genres": len(parameters["genres"])})


        tag_where_query = ""
        if "tags" in parameters:
            tag_where_query = "Game_tag.tag_id IN ("

            tag_parameter_names = []
            for tag_id in parameters["tags"]: 
                tag_parameter_names.append(":tag_id" + str(tag_id))
                parameters.update({"tag_id" + str(tag_id): tag_id})

            tag_where_query = tag_where_query + ", ".join(tag_parameter_names) + ") "

 
        
        tag_having_query = ""
        if "tags" in parameters:
            tag_having_query = tag_having_query + " COUNT(Game_tag.id) >= :number_of_tags"
            parameters.update({"number_of_tags": len(parameters["tags"])})


        



        where_filters = [name_query, year_query, developer_query, genre_where_query, tag_where_query]
        where_filters = [q for q in where_filters if q != ""]
        having_filters = [average_query, count_query, genre_having_query, tag_having_query]
        having_filters = [q for q in having_filters if q != ""]

        query = "SELECT Game.id, Game.name, Game.year, Game.developer, COUNT(Review.points), AVG(Review.points)"

        if "genres" in parameters:
            query = query + ", COUNT(Game_Genre.id)"

        if "tags"in parameters:
            query = query + ", COUNT(Game_Tag.id)"

        query = query + " From Game LEFT JOIN Review ON Game.id=Review.game_id "
        
        if "genres" in parameters:
            query = query +  "LEFT JOIN Game_genre ON Game_genre.game_id=Game.id "
        if "tags" in parameters:
            query = query + " LEFT JOIN Game_tag ON Game_tag.game_id = Game.id "

        if len("".join(where_filters)) > 0:
            query = query + " WHERE ("
            query = query + " AND ".join(where_filters)
            query = query + ") "

        query = query + " GROUP BY Game.id "

        if len("".join(having_filters)) > 0:
            query = query + "HAVING ("
            query = query + " AND ".join(having_filters)
            query = query + ")"

        query = query + " ORDER BY Game.name"

        res = page_query(query, parameters, limit = GAME_RESULTS_PER_PAGE, page_number = page_number)
        games_info = []

        for row in res:
            game_info = {}
            game_info.update({"id": row[0], "name": shorten_if_longer_than(row[1]), "year": row[2], "developer": shorten_if_longer_than(row[3], max=20),
                              "number_of_reviews": row[4], "average_of_reviews": format_average(row[5])})
            games_info.append(game_info)

        return games_info


    @staticmethod
    def find_general_details(): 
        stmt = text("SELECT COUNT(Game.id), COUNT(Review.id) FROM Game LEFT JOIN Review ON Game.id = Review.game_id;")
        res = db.engine.execute(stmt)
        for row in res: 
            return [row[0], row[1]]
        return None