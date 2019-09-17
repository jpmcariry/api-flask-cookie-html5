from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt, get_jwt_claims, unset_jwt_cookies,set_access_cookies, unset_access_cookies
from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from models.conta import UserModel
from blacklist import BLACKLIST
from flask import render_template, make_response, jsonify, redirect, url_for, session, flash, request, g
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
import jwt
import warnings

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="o campo 'login' nao deve estar vazio")
atributos.add_argument('password', type=str, required=True, help="o campo 'password' nao deve estar vazio")
atributos.add_argument('admin', type=str, required=False)

class User(Resource):
    def get(self, user_id):
        user = UserModel.seach(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404# not found

    @jwt_required
    def delete(self, user_id):
        user = UserModel.seach(user_id)
        if user:
            try:
                user.delete_hotel()
            except:
                return {'message': 'error nos valores internos no delete_user.delete'}, 500
            return {'messsage': 'User deleted.'}
        return {'message': 'User not found'}, 404
class UserRegister(Resource):

    def get(self):
        response = make_response(render_template('cadastro.html', foo=42))
        response.headers['X-Parachutes'] = 'parachutes are cool'
        return response

    def post(self):
        global atributos
        dados = atributos.parse_args()
        print("aqui")
        if UserModel.seach_by_login(dados['login']):
            return {'message': 'Conta already exists'}, 409
        print("dados: ", dados['login'], dados['password'], dados['admin'])
        if(dados['admin']==None or dados['admin']=="False" or dados['admin']=="false" or dados['admin']=="0"):
            admin=False
            user = UserModel(dados['login'], dados['password'], admin)
            user.save_user()
            return {'message': 'Conta {} created'.format(dados['login'])}, 201
        elif(dados['admin']=="True" or dados['admin']=="true" or dados['admin']=="1" or dados['admin'=="on"]):
            print("true")
            admin=True
            user = UserModel(dados['login'], dados['password'], admin)
            user.save_user()
            return {'message': 'Conta {} created, admin: {}'.format(dados['login'], admin)}, 201
        else:
            print("error")
            return {'message': 'error no post'}, 500


class UserLogin(Resource):
    def get(self):
        response = make_response(render_template('login.html', foo=42))
        response.headers['X-Parachutes'] = 'parachutes are cool'
        return response
    @classmethod
    def post(cls):
        global atributos
        min = timedelta(seconds=10)
        print(min)
        dados = atributos.parse_args()

        user = UserModel.seach_by_login(dados['login'])
        if user and safe_str_cmp(user.password, dados['password']):
            token_de_acesso = create_access_token(identity=user.user_id, user_claims=user.login, expires_delta=min)
            resp = jsonify({'refresh': True})
            set_access_cookies(resp, token_de_acesso)
            session['login'] = request.form['login']
            return redirect('/user')
        response = make_response(render_template('login.html', foo=42))
        response.headers['X-Parachutes'] = 'parachutes are cool'
        return response


class UserLogout(Resource):
    def get(self):
        response = make_response(render_template('logout.html', foo=42))
        response.headers['X-Parachutes'] = 'parachutes are cool'
        self.post()
        return response


    def post(self):
        print('logout')
        resp = jsonify({'logout': True})
        session=None
        unset_jwt_cookies(resp)
        #jwt_id = get_raw_jwt()['jti']
        #print(jwt_id)# JWT token identify
        #BLACKLIST.add(jwt_id)
        return resp, 200