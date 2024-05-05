from flask import flash
from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

# may need to change db name
class Book: 
    _db = "booktok_db"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.review = data["review"]
        self.image = data["image"]
        self.author = data["author"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @staticmethod
    def form_is_valid(form_data):
        is_valid = True
        # text validator
        if len(form_data["title"]) == 0:
            flash("please enter title")
            print("a")
            is_valid = False
        elif len(form_data["title"]) < 3:
            flash("title must be at least 3 characters")
            print("b")
            is_valid = False
        if len(form_data["review"]) == 0:
            flash("please enter review")
            print("c")
            is_valid = False
        elif len(form_data["review"]) < 3:
            flash("review must be at least 3 characters")
            print("d")
            is_valid = False
        if len(form_data["image"]) == 0:
            flash("please enter image")
            print("e")
            is_valid = False
        elif len(form_data["image"]) < 3:
            flash("image must be at least 3 characters")
            print("f")
            is_valid = False
        if len(form_data["author"]) == 0:
            flash("please enter author")
            print("e")
            is_valid = False
        elif len(form_data["author"]) < 3:
            flash("author must be at least 3 characters")
            print("f")
            is_valid = False

        return is_valid



    @classmethod
    def find_all(cls):
        """Finds all books in the database"""

        query = "SELECT * FROM books;"
        list_of_dicts = connectToMySQL(Book._db).query_db(query)

        print("***********************ALL BOOKS****************")
        pprint(list_of_dicts)
        print("***********************ALL BOOKS****************")

        books = []
        for each_dict in list_of_dicts:
            book = Book(each_dict)
            books.append(book)
        return books
        
    @classmethod
    def find_all_with_users(cls):
        """Finds all books with users in the database"""

        query = """
        SELECT * FROM books 
        JOIN users 
        ON books.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Book._db).query_db(query)

        print("***********************ALL BOOKS****************")
        pprint(list_of_dicts)
        print("***********************ALL BOOKS****************")

        books = []
        for each_dict in list_of_dicts:
            book = Book(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            print(each_dict)
            print(book.id)
            user = User(user_data)
            book.user = user
            books.append(book)
        return books

    @classmethod
    def find_by_id(cls, book_id):
        """Finds one book by id in the database"""
        query = "SELECT * FROM books WHERE id = %(book_id)s;"
        data = {"book_id": book_id}
        list_of_dicts = connectToMySQL(Book._db).query_db(query, data)
        
        book = Book(list_of_dicts[0])
        return book
    
    @classmethod
    def find_by_id_with_users(cls, book_id):
        """Finds one book by id and the uploader in the database"""

        query = """
        SELECT * FROM books 
        JOIN users 
        ON books.user_id = users.id
        WHERE books.id = %(book_id)s;
        """
        data = {"book_id": book_id}
        list_of_dicts = connectToMySQL(Book._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        book = Book(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        book.user = User(user_data)
        return book

    @classmethod
    def create(cls, form_data):
        """Creates a new Book from a form"""
        query = """
        INSERT INTO books
        (title, review, image, author, user_id)
        VALUES
        (%(title)s, %(review)s, %(image)s, %(author)s, %(user_id)s);
        """
        book_id = connectToMySQL(Book._db).query_db(query, form_data)
        return book_id
    
    @classmethod
    def update_by_id(cls, form_data):
        """Updates a book by its ID"""
        query = "UPDATE books SET title = %(title)s, review = %(review)s, image = %(image)s, author = %(author)s WHERE id = %(book_id)s;"
        connectToMySQL(Book._db).query_db(query, form_data)
        return
    
    @classmethod
    def delete_by_id(cls, book_id):
        """Deletes an book by its ID"""
        query = "DELETE FROM books WHERE id = %(book_id)s;"
        data = {"book_id": book_id}
        connectToMySQL(Book._db).query_db(query, data)
        return
    
    @classmethod
    def count_by_title(cls, title):
        """This method counts the number of book by title"""
        query = """SELECT COUNT(title) as "count" 
        FROM books 
        WHERE title = %(title)s;
        """
        data = {"title": title}
        list_of_dicts = connectToMySQL(Book._db).query_db(query, data)
        pprint(list_of_dicts)
        return list_of_dicts[0]["count"]
    
    # @classmethod
    # def add_to_watchlist(cls, data):
    #     query = """
    #     INSERT INTO watchlist
    #     (user_id, book_id, watch_status)
    #     VALUES
    #     (%(user_id)s, %(book_id)s, %(watch_status)s);
    #     """
    #     connectToMySQL(Book._db).query_db(query, data)
    #     return
 
