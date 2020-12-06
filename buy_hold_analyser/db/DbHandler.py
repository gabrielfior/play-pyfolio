import sqlite3

class DbHandler:

    def __init__(self, dbname= 'mydatabase.db'):
        self.con = sqlite3.connect(dbname)
