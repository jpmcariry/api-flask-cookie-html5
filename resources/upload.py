from flask_restful import Resource
from flask import request, redirect, url_for, flash, render_template, make_response
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'C:\\Users\\capit\\PycharmProjects\\flask\\static\\img'


class Upload(Resource):  # /upload
    def get(self):
        response = make_response(render_template('upload.html', foo=42))
        response.headers['X-Parachutes'] = 'parachutes are cool'
        return response

    def post(self):
        if request.method == 'POST':
            print('upload post')
            f = request.files['json']
            json = request.files['json']
            print(json.filename, f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            json.save(os.path.join(UPLOAD_FOLDER, json.filename))
            return {'resutado': 'file uploaded successfully', 'file': '{}'.format(f.filename)}