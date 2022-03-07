from flask import Flask, Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from .models import *

bcrypt = Bcrypt()
jwt = JWTManager()

class HelloView:
    hello = Blueprint('hello', __name__, url_prefix='/hello')

    @hello.route('/', methods=['GET'])
    def hello_world():
        if request.method == "GET":
            return 'Hello, World!'
        return 'Hello, World!'

class UserView: # Router
    user = Blueprint('user', __name__, url_prefix='/user')

    @user.route('/', methods=['GET'])
    def hello_user():
        return 'Hello, User!'

    @user.route('/signin', methods=['POST'])
    def signin():
        if request.is_json:
            data = request.get_json()
            user = User.query.filter_by(username=data['username']).first()
            if user and bcrypt.check_password_hash(user.password, data['password']):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })
            else:
                return {'message': 'Invalid credentials!'}, 401
        else:
            return {'message': 'Request must be JSON!'}, 400

    @user.route('/signup', methods=['POST'])
    def signup():
        if request.is_json:
            data = request.get_json()
            user = User.query.filter_by(username=data['username']).first()
            if user:
                return {'message': 'User already exists!'}, 400
            else:
                new_user = User(username=data['username'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
                db.session.add(new_user)
                db.session.commit()
                return {'message': 'User created!'}
        else:
            return {'message': 'Request must be JSON!'}, 400


class PostView:
    post = Blueprint('post', __name__, url_prefix='/post')

    @post.route('/', methods=['POST', 'GET'])
    def create_or_retrieve_posts():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_post = Post(title=data['title'], description=data['description'], user_id=data['user_id']) # token
                db.session.add(new_post)
                db.session.commit()
                return jsonify({
                    'message': 'Post created!',
                    'post': new_post.id
                })
            else:
                return {'message': 'Request must be JSON!'}, 400
        elif request.method == 'GET':
            all_posts = Post.query.all()
            result = []
            for post in all_posts:
                post_data = post.serialize()
                result.append(post_data)
            return jsonify({'posts': result})

    @post.route('/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
    def get_or_update_or_delete_post(id):
        if request.method == 'GET':
            post = Post.query.get_or_404(id)
            return jsonify(post.serialize())
        elif request.method == 'PUT':
            if request.is_json:
                data = request.get_json()
                post = Post.query.get_or_404(id)
                post.title = data['title']
                post.description = data['description']
                db.session.commit()
                return jsonify(post.serialize())
            else:
                return {'message': 'Request must be JSON!'}, 400
        elif request.method == 'DELETE':
            post = Post.query.get_or_404(id)
            db.session.delete(post)
            db.session.commit()
            return {'message': 'Post deleted!'}