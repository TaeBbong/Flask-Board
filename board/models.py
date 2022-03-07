import sqlite3 as sql

class Sqlite3:
    def __init__(self):
        self.con = sql.connect('sqlite3.db')
        self.cur = self.con.cursor()
        self.create_users()
        self.create_posts()
    
    def create_users(self):
        query = 'create table if not exists users (id integer primary key autoincrement, username text, password text)'
        self.cur.execute(query)

    def create_posts(self):
        query = 'create table if not exists posts (id integer primary key autoincrement, title text, content text, created_at datetime default current_timestamp, user_id integer, foreign key(user_id) references users(id))'
        self.cur.execute(query)

    