from flask import Flask, Blueprint, request, jsonify, render_template, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

from config import Config
from forms import LoginForm

site = Blueprint("site", __name__)

# Client webpage routing
@site.route('/index')
def index():
    # Check if the user already logged in
    if(session.get('username') is None):
        return redirect('/login')
   
    # response = requests.get("http://192.168.1.7:5000/book")
    url = 'http://' + Config.HOST_IP + ':'  + Config.PORT
    response = requests.get(url + '/book')
    print(Config.HOST_IP)
    data = json.loads(response.text)

    return render_template("index_book.html", books = data)


@site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, pass {}, remember_me={}'.format(
            form.username.data, form.password.data, form.remember_me.data))
        if form.username.data == Config.USER['username'] and form.password.data == Config.USER['password']:
            session["username"] = form.username.data
            return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


@site.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it is there
   session.pop('username', None)
    # return redirect('url_for(''index'))
   return redirect('/login')

# @site.route('/index', methods=['GET'])
# def index():
#     return render_template('index.html', title='Home')