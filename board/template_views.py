from flask import Flask, Blueprint, request, jsonify, render_template, session, redirect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from .models import *

bcrypt = Bcrypt()
jwt = JWTManager()

class HelloTemplateView:
    hello = Blueprint('hello_t', __name__, url_prefix='/')

    @hello.route('/', methods=['GET'])
    def hello_world():
        content = request.args.get('content')
        return render_template('index.html', content=content)

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
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                session['id'] = user.id
                session['username'] = username
                session['password'] = password
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
                user = User(username=username, password=hashed_password)
                db.session.add(user)
                db.session.commit()
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
        all_posts = Post.query.all()
        result = []
        for post in all_posts:
            post_data = post.serialize()
            result.append(post_data)
        # return jsonify({'posts': result})
        return render_template("post_list.html", posts=result)

    @post.route('/create', methods=['POST', 'GET'])
    def create_post():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            new_post = Post(title=title, description=content, user_id=session['id']) # token
            db.session.add(new_post)
            db.session.commit()
            return redirect('/post/')
        elif request.method == 'GET':
                return render_template('post_create.html')

    @post.route('/<int:id>/', methods=['GET'])
    def retrieve_post(id):
        post = Post.query.get_or_404(id)
        return render_template('post_detail.html', post=post)

    @post.route('/<int:id>/edit/', methods=['GET', 'POST'])
    def update_post(id):
        if request.method == 'GET':
            post = Post.query.get_or_404(id)
            return render_template('post_edit.html', post=post)
        elif request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            post = Post.query.get_or_404(id)
            post.title = title
            post.description = content
            db.session.commit()
            return redirect('/post/')

    @post.route('/<int:id>/delete/', methods=['GET'])
    def delete_post(id):
        if request.method == 'GET':
            post = Post.query.get_or_404(id)
            db.session.delete(post)
            db.session.commit()
            return redirect('/post/')