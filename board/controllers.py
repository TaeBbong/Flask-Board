class UserController: # UserService
    def signup(self, user_data, db):
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