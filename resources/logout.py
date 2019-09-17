from flask_restful import Resource
from flask import request, redirect, url_for, flash, render_template, make_response

class Logout(Resource):  # /out
    def get(self):
        response = make_response(render_template('index.html', foo=42))
        response.headers['X-Parachutes'] = 'parachutes are cool'
        return response
