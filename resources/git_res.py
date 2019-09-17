from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from sql_alchemy import banco as db
from flask_restful import Resource, reqparse
from flask import request, jsonify, render_template, make_response, redirect, url_for, send_file
from models.user import UserModel
from models.conta import UserModel as ContaModel
from flask_jwt_extended import jwt_required, get_jwt_claims, get_raw_jwt
from jinja2 import Environment, FileSystemLoader

file_loader=FileSystemLoader('templates')
import uuid
import random
class User(Resource):#/user
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('public_id')
    argumentos.add_argument('name')
    argumentos.add_argument('password')
    argumentos.add_argument('admin')
    def get(self):
        print('get_all')
        if request.method == 'GET':
            print("request.method == 'GET'")
            #response = send_file(open('C:\\Users\\Nutes\\PycharmProjects\\data_science\\templates\\img\\carro.jpg'))
            #response.set_etag('carro')
            x={'users': [user.json() for user in UserModel.query.all()]}
            response = make_response(render_template('user_get.html', ins=UserModel, foo=42))
            response.headers['X-Parachutes'] = 'parachutes are cool'
            return response#{'users': [user.json() for user in UserModel.query.all()]}#render_template('./carro.jpg', as_attachment=True)
            '''try:
                image = request.files['image']
                nom_image = secure_filename(image.filename)
                image = Image.open(image)
                ...
                image.save('./img/' + nom_image)
                return send_file('/home/modificateurimage/mysite/static/images/' + nom_image, mimetype='image/jpeg',
                                 attachment_filename=nom_image, as_attachment=True), os.remove(
                    '/home/modificateurimage/mysite/static/images/' + nom_image)
            except Exception as e:
                print(e)'''


        return {'users': [user.json() for user in UserModel.query.all()]}#response


    @jwt_required
    def post(self):
        print('post_user')
        if request.method == 'POST':
            print("request.method == 'POST'")
        else:
            print("failed")
        try:
            jwt_id = get_raw_jwt()['jti']
            print(jwt_id)
            print("user claims: ", get_jwt_claims())
            user = ContaModel.seach_by_login(get_jwt_claims())
            if user:
                print(user.login, user.password, user.admin)
                if(user.admin==True):
                    dados = self.argumentos.parse_args()
                    hashed_password = generate_password_hash(dados['password'], method='sha256')
                    id = random.randint(45, 805787)
                    new_user = UserModel(id, public_id=str(uuid.uuid4()), name=dados['name'], password=hashed_password,
                                         classe='sem mudanca')
                    try:
                        new_user.save_user()
                    except:
                        return {'message': 'error no User_post'}, 500  # codigo: 500=ao tentar salvar
                    return new_user.json()
                else:
                    return {'message': 'Admin privilege is required'}
            else:
                return {'message': 'user deleted while token did not expires'}
        except:
            print("error ao printar")

class User_public(Resource):#/user/<string:public_id>
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('id')
    argumentos.add_argument('public_id')
    argumentos.add_argument('admin')
    argumentos.add_argument('name')
    argumentos.add_argument('password')
    def get(self, public_id):
        print("get_one")
        user = UserModel.seach(public_id)
        if user is not None:
            print("dentro do user")
            return user.json()
        return {'message': 'user not found.'}, 404# not found
    @jwt_required
    def post(self, public_id):
        print('post')
    @jwt_required
    def put(self, public_id):
        print('put_to_admin')
        try:
            print("user claims: ", get_jwt_claims())
            user= ContaModel.seach_by_login(get_jwt_claims())
            if user:
                print(user.login, user.password, user.admin)
                if(user.admin==True):
                    user = UserModel.seach(public_id)
                    if user:
                        print('user_updated')
                        classes = ['guerreiro', 'paladino', 'mago', 'espadachim', 'trevors']
                        user.update_user(classe=random.choice(classes))
                        try:
                            user.save_user()
                        except:
                            return {'message': 'error internal value promote_user.save'}, 500
                        return {'messege': 'usuario promovido: {}'.format(user.name)}, 200
                    return {'message': "User id '{}' do not existis.".format(public_id)}, 400
                else:
                    return {'message': 'Admin privilege is required'}
            else:
                return {'message': 'user deleted while token did not expires'}
        except:
            print("error ao printar")

    @jwt_required
    def delete(self, public_id):
        print("delete_user")
        try:
            print("user claims: ", get_jwt_claims())
            user = ContaModel.seach_by_login(get_jwt_claims())
            if user:
                print(user.login, user.password, user.admin)
                if(user.admin==True):
                    user = UserModel.seach(public_id)
                    if not user:
                        return {'message': 'Usuario não encontrado'}, 404

                    user.delete_user()  # deletar usuario do db pelo method delete  /ID
                    return {'message': 'usuario deletado'}, 200
                else:
                    return {'message': 'Admin privilege is required'}
            else:
                return {'message': 'user deleted while token did not expires'}
        except:
            print("error ao printar")