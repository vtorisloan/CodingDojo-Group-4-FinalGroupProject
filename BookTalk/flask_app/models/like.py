from flask_app.config.mysqlconnection import connectToMySQL

class Like: 
    # _db = "booktok" change the DB name to correct schema

    @classmethod
    def create(cls, form_data):
        """This method creates a new like or dislike"""

        query = """
        INSERT INTO likes
        (rating, user_id, book_id)
        VALUES
        (%(rating)s, %(user_id)s, %(book_id)s);
        """
        connectToMySQL(Like._db).query_db(query, form_data)
        return
