from flask_restful import Resource
from flask import request, redirect, url_for, flash, render_template, make_response
from .list_dir import list_in_file

class Download(Resource):  # /download
    def get(self, filename):
        if request.method == 'GET':
            print('get Download')
        return redirect(url_for('static', filename='img/'+filename))
class list_download(Resource):
    def get(self):
        if request.method =='GET':
            print('get list_download')
            file=list_in_file()
            all=file[0]
            one=file[1]
            count=len(all)
            response = make_response(render_template('list_download.html', files=all, one=one, count=count, foo=42))
            response.headers['X-Parachutes'] = 'parachutes are cool'
            return response