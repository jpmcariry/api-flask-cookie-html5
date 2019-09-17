from flask_restful import Resource
from flask import request, redirect, url_for, flash, render_template, make_response
from werkzeug.utils import secure_filename

class Main_page(Resource):
    def get(self):
        response = make_response(render_template('main_page.html', foo=42))
        response.headers['X-Parachutes'] = 'parachutes are cool'
        return response