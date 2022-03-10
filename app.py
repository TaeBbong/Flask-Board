from flask import Flask
## from flask_sqlalchemy import SQLAlchemy
## from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from board.models import *
from board.views import *

app = Flask (__name__, template_folder='board/templates')
app.debug = True
app.config['SECRET_KEY'] = 'mysecretkey'
## app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://testdb:testdb@localhost:5432/testdb'
## app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

bcrypt.init_app(app)
CORS(app)

# app.register_blueprint(HelloView().hello)
# app.register_blueprint(UserView().user)
# app.register_blueprint(PostView().post)

app.register_blueprint(HelloTemplateView().hello)
app.register_blueprint(UserTemplateView().user)
app.register_blueprint(PostTemplateView().post)
app.register_blueprint(QuizTemplateView().quiz)
app.register_blueprint(FileTemplateView().file)

 
if __name__ == "__main__":
    ## db.create_all()
    app.run(host="0.0.0.0", port=80)