import sqlite3 as sql

class Sqlite3:
    def __init__(self):
        self.con = sql.connect('sqlite3.db', check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_tables()
    
    def create_tables(self):
        query = 'create table if not exists users (id integer primary key autoincrement, username text, password text)'
        self.cur.execute(query)
        query = 'create table if not exists posts (id integer primary key autoincrement, title text, content text, created_at datetime default current_timestamp, user_id integer, foreign key(user_id) references users(id))'
        self.cur.execute(query)

    def create_user(self, username, password_hash):
        query = 'insert into users values (NULL, ?, ?)'
        self.cur.execute(query, (username, password_hash))
        self.con.commit()

    def retrieve_user_by_username(self, username):
        query = 'select * from users where username = ?'
        self.cur.execute(query, (username, ))
        try:
            user = self.cur.fetchone()
            return User(user)
        except:
            return "404"

    def retrieve_user_by_id(self, id):
        query = 'select * from users where id = ?'
        self.cur.execute(query, (str(id), ))
        try:
            user = self.cur.fetchone()
            return User(user)
        except:
            return "404"

    def create_post(self, title, content, user_id):
        query = 'insert into posts values (NULL, ?, ?, NULL, ?)'
        self.cur.execute(query, (title, content, str(user_id)))
        self.con.commit()

    def retrieve_posts(self):
        query = 'select * from posts'
        self.cur.execute(query)
        posts = self.cur.fetchall()
        return list(map(Post, posts))
    
    def retrieve_post_by_id(self, id):
        query = 'select * from posts where id = ?'
        self.cur.execute(query, (str(id), ))
        try:
            post = self.cur.fetchone()
            return Post(post)
        except:
            return "404"

    def retrieve_post_by_userid(self, user_id):
        query = 'select * from posts where user_id = ?'
        self.cur.execute(query, (str(user_id), ))
        try:
            posts = self.cur.fetchall()
            return list(map(Post, posts))
        except:
            return "404"

    def update_post(self, id, title, content):
        query = 'update posts set title = ?, content = ? where id = ?'
        self.cur.execute(query, (title, content, str(id), ))
        self.con.commit()

    def delete_post(self, id):
        query = 'delete from posts where id = ?'
        self.cur.execute(query, (str(id), ))
        self.con.commit()

class User:
    def __init__(self, row):
        id = row[0]
        username = row[1]
        password = row[2]
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id: {0}, username: {1})".format(str(self.id), self.username)


class Post:
    def __init__(self, row):
        id = row[0]
        title = row[1]
        content = row[2]
        created_at = row[3]
        user_id = row[4]
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.user_id = user_id
    
    def __repr__(self):
        return "Post(id: {0}, title: {1}, created_at: {2}, user_id: {3}".format(str(self.id), self.title, self.created_at, str(self.user_id))
