from flask import Blueprint, request, render_template, session, redirect, render_template_string
from flask_bcrypt import Bcrypt

from board.models import Sqlite3

db = Sqlite3()
bcrypt = Bcrypt()

class HelloTemplateView:
    hello = Blueprint('hello_t', __name__, url_prefix='/')

    @hello.route('/', methods=['GET'])
    def hello_world():
        content = request.args.get('content')
        return render_template('index.html', content=content)

class QuizTemplateView:
    quiz = Blueprint('quiz_t', __name__, url_prefix='/quiz')

    @quiz.route('/', methods=['GET'])
    def quiz_home():
        content = request.args.get('content') or 'Hello Quiz'
        template = ''' 
        <p> Hello world </p>{}
        '''.format(content)

        return render_template_string(template)

class FileTemplateView:
    file = Blueprint('file_t', __name__, url_prefix='/file')

    @file.route('/', methods=['GET'])
    def file_home():
        return render_template("file_home.html")

class UserTemplateView: # Router
    user = Blueprint('user_t', __name__, url_prefix='/user')

    @user.route('/', methods=['GET'])
    def hello_user():
        return render_template('index.html')

    @user.route('/signin', methods=['POST', 'GET'])
    def signin():
        if request.method == 'GET':
            return render_template('user_signin.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = db.retrieve_user_by_username(username)
            print(user)
            if user != "404" and bcrypt.check_password_hash(user.password, password):
                session['id'] = user.id
                session['username'] = username
                session['password'] = user.password # (secure)
                #session['password'] = password # (vuln)
                print(session)
                return redirect('/post/')
            else:
                return render_template('user_signin_error.html')

    @user.route('/signout', methods=['GET'])
    def signout():
        session.clear()
        return redirect('/')

    @user.route('/signup', methods=['POST', 'GET'])
    def signup():
        if request.method == 'GET':
            return render_template('user_signup.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm']
            if password == confirm:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                db.create_user(username=username, password_hash=hashed_password)
                user = db.retrieve_user_by_username(username)
                session['id'] = user.id
                session['username'] = username
                session['password'] = password
                return redirect('/post/')
            else:
                return render_template('user_signup_error.html')


class PostTemplateView:
    post = Blueprint('post_t', __name__, url_prefix='/post')

    @post.route('/', methods=['GET'])
    def retrieve_posts():
        all_posts = db.retrieve_posts()
        return render_template("post_list.html", posts=all_posts)

    @post.route('/create', methods=['POST', 'GET'])
    def create_post():
        if request.method == 'POST':
            try:
                user_id = session['id']
                title = request.form['title']
                content = request.form['content']
                db.create_post(title=title, content=content, user_id=user_id) # token
            except:
                pass
            return redirect('/post/')
        elif request.method == 'GET':
            try:
                user_id = session['id']
                return render_template('post_create.html')
            except:
                return redirect('/post/')

    @post.route('/<int:id>/', methods=['GET'])
    def retrieve_post(id):
        post = db.retrieve_post_by_id(id)
        return render_template('post_detail.html', post=post)

    @post.route('/<int:id>/edit/', methods=['GET', 'POST'])
    def update_post(id):
        if request.method == 'GET':
            post = db.retrieve_post_by_id(id)
            try:
                if post.user_id == session['id']:
                    return render_template('post_edit.html', post=post)
                else:
                    return redirect('/post/')
            except:
                return redirect('/post/')
        elif request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            db.update_post(id, title, content)
            return redirect('/post/')

    @post.route('/<int:id>/delete/', methods=['GET'])
    def delete_post(id):
        if request.method == 'GET':
            post = db.retrieve_post_by_id(id)
            try:
                if post.user_id == session['id']:
                    db.delete_post(id)
                else:
                    pass
            except:
                pass
        return redirect('/post/')