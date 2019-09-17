from flask_restful import Resource
from flask import request, redirect, url_for, flash, render_template, make_response
from .list_dir import list_in_file

class Admin(Resource):  # /download
    def get(self):
        response = make_response(render_template('admin.html', foo=42))
        response.headers['X-Parachutes'] = 'parachutes are cool'
        return response