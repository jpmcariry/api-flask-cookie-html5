from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from sql_alchemy import banco as db
from flask_restful import Resource, reqparse
from flask import request, jsonify, render_template, make_response, redirect, url_for, send_file, session
from models.user import UserModel
from models.conta import UserModel as ContaModel
from flask_jwt_extended import jwt_required, get_jwt_claims, get_raw_jwt
from jinja2 import Environment, FileSystemLoader

file_loader=FileSystemLoader('templates')
import uuid
import random

respo= {'message': 'definindo'}

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
            conta=ContaModel.seach_by_login(session['user_id'])
            response = make_response(render_template('user_get.html', ins=UserModel,admin=conta.admin, foo=42))
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


    def post(self):
        print('post_user')
        if request.method == 'POST':
            print(session['user_id'])
            print("request.method == 'POST'")
        else:
            print("failed")
        conta=ContaModel.seach_by_login(session['user_id'])
        print(conta.admin)
        if(conta.admin==True):
            try:
                print("user claims: ", session['user_id'])
                print('form get')
                user = ContaModel.seach_by_login(session['user_id'])
                if user:
                    print(user.login, user.password, user.admin)
                    if(user.admin==True):
                        dados = self.argumentos.parse_args()
                        hashed_password = generate_password_hash(request.form.get('senha'), method='sha256')
                        id = random.randint(45, 805787)
                        new_user = UserModel(id, public_id=str(uuid.uuid4()), name=request.form.get('login'), password=hashed_password,
                                             classe='sem mudanca')
                        try:
                            new_user.save_user()
                        except:
                            return {'message': 'error no User_post'}, 500  # codigo: 500=ao tentar salvar
                        return new_user.json()
                    else:
                        return {'message': 'Admin privilege is required'}
                else:
                    return {'message': 'user not find'}
            except:
                print("error ao printar")
        else:
            return {'message': 'you need admin privelegius'}

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

    def post(self, public_id, delete=False, put=False):
        global respo
        print('post')
        print("DELETE", request.form.get('delete'))
        print("PUT",request.form.get('put'))
        if(delete==False and request.form.get('delete')!=None):
            self.delete(public_id)
            print("primeiro post delete")
            resp=respo
        elif (put == False and request.form.get('put')!=None):
            self.put(public_id);
            print("primeiro post put")
            resp = respo
        print('post')
        print(delete, put)
        if(delete==True):
            print('resp delete')
            respo = resp
            print(type(resp), type(respo))
            print(respo)
        elif(put!=False):
            print('resp put')
            respo = resp
        return resp

    def put(self, public_id):
        print('put_to_admin')
        try:
            conta= ContaModel.seach_by_login(session['user_id'])
            if conta:
                print(conta.login, conta.password, conta.admin)
                if(conta.admin==True):
                    user = UserModel.seach(public_id)
                    if user:
                        print('user_updated')
                        classes = ['guerreiro', 'paladino', 'mago', 'espadachim', 'trevors']
                        user.update_user(classe=random.choice(classes))
                        try:
                            user.save_user()
                        except:
                            return {'message': 'error internal value promote_user.save'}, 500
                        global respo
                        respo={'messege': 'usuario promovido: {}'.format(user.name)}
                        return self.post(public_id, delete=False,put=user.name)
                    return {'message': "User id '{}' do not existis.".format(public_id)}, 400
                else:
                    return {'message': 'Admin privilege is required'}
            else:
                return {'message': 'user deleted while token did not expires'}
        except:
            print("error ao printar")


    def delete(self, public_id):
        print('delete chamado')
        conta = ContaModel.seach_by_login(session['user_id'])
        if conta:
            print(conta.login, conta.password, conta.admin)
            try:
                user = ContaModel.seach_by_login(session['user_id'])
                if user:
                    print(user.login, user.password, user.admin)
                    if(user.admin==True):
                        print("é admin")
                        user = UserModel.seach(public_id)
                        print(user.name)
                        if not user:
                            print('user nao encontrado')
                            return {'message': 'Usuario não encontrado'}, 404
                        user.delete_user()  # deletar usuario do db pelo method delete  /ID
                        print('user deletado')
                        global respo
                        respo={"message": 'usuario deletado'}
                        self.post(public_id, delete=True, put=False)
                    else:
                        return {'message': 'Admin privilege is required'}
                else:
                    return {'message': 'user deleted while token did not expires'}
            except:
                print("error ao printar")
        else:
            return {'message': 'you need admin privelegius'}
