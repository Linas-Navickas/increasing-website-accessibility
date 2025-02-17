import sqlite3

class DataBase:
    
    def execute_query(self, database, query):
        with sqlite3.connect(database) as conn:
            c = conn.cursor()
            c.execute(query)
            conn.commit()