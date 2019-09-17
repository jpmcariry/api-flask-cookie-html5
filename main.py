from flask import Flask, jsonify, session, request, redirect, url_for, g
from flask_restful import Api
from resources.main_page import Main_page
from resources.git_res import User, User_public
from resources.cadastro import UserRegister, UserLogin, UserLogout
from resources.download import Download, list_download
from resources.upload import Upload
from resources.admin import Admin
from resources.logout import Logout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from datetime import timedelta
import os
import cgi
import jinja2
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'])
UPLOAD_FOLDER='C:\\Users\\capit\\PycharmProjects\\flask\\static'
#UPLOAD_FOLDER = '/path/to/the/uploads'
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
template_dir= os.path.join(os.path.dirname(__file__), 'templates')

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = 'C://Users//Nutes//PycharmProjects//data_science//static//img//'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['SECRET_KEY'] = 'dawdwadwa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DonTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=10)


api = Api(app)
jwt = JWTManager(app)

api.add_resource(Main_page, '/home')
api.add_resource(User, '/user')
api.add_resource(User_public, '/user/<string:public_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Download, '/download/<string:filename>')
api.add_resource(list_download, '/download')
api.add_resource(Upload, '/upload')
api.add_resource(Admin, '/admin')
api.add_resource(Logout, '/out')


# @app.route('/login')
# fazer a autenticaçao = request autorizado
@app.before_first_request
def cria_banco():
    banco.create_all()

@app.before_request
def require_login():
    allowed_routes=['userlogin','userregister', 'main_page']
    print(session)
    if request.endpoint not in allowed_routes and 'login' not in session:
        return redirect(url_for('main_page'))

@jwt.token_in_blacklist_loader
def verify_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message': 'You have been logged out'})
def cadastro():
    pass
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
