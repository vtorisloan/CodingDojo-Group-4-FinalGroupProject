import pymysql.cursors


class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db=db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=False)

        self.connection = connection

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print('running query:', query)

                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # Insert queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find('select') >= 0:
                    # select queries will return data from the database as a list of dictionaries

                    result = cursor.fetchall()
                    return result
                else:
                    # update and delete queries will return nothing
                    self.connection.commit()

            except Exception as e:
                # if query faisl the method will return false
                print("Something went wrong", e)
                return False
            finally:
                # close connection
                self.connection.close()

        # connecttomysql receivges teh database were using and uses it to creatte and instance of mysql connection


def connectToMySQL(db):
    return MySQLConnection(db)
