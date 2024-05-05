from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.like import Likes

# may need to change db name
class Likes: 
    _db = "booktok_db"
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.likes_id = data["likes_id"]
        self.watch_status = data["watch_status"]


    @classmethod
    def remove(cls, data):
        """Removes an likes from our watch list."""
        query = """
        DELETE FROM watchlist
        WHERE user_id = %(user_id)s AND likes_id = %(likes_id)s;
        """
        connectToMySQL(Likes._db).query_db(query, data)
        return 
    
    @classmethod
    def add(cls, data):
        """Adds an likes to our watch list."""
        query = """
        INSERT INTO watchlist
        (user_id, likes_id, watch_status)
        VALUES
        (%(user_id)s, %(likes_id)s, %(watch_status)s);
        """
        connectToMySQL(Likes._db).query_db(query, data)
        return


    
    @classmethod
    def get_all_by_id(cls, data):
        """Gets all likes from our watch list."""
        query = """
        select *
        from watchlist w inner join likess a 
        on w.likes_id = a.id
        where w.user_id = %(user_id)s;
        """
        data = {"user_id": data}
        result = connectToMySQL(Likes._db).query_db(query, data)
        watchlist = []
        for dict in result: 
            for key, value in dict.items():
                print(key, "\t\t", value )
            # print(dict)
            likes_data = {
                "id": dict["a.id"],
                "title": dict["title"],
                "studio": dict["studio"],
                "description": dict["description"],
                "stream": dict["stream"],
                "user_id": dict["user_id"],
                "created_at": dict["created_at"],
                "updated_at": dict["updated_at"],
            }
            this_likes = Likes(likes_data)
            watchlist.append(this_likes)
        # print("A", result)
        return watchlist

