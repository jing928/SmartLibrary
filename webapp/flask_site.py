import os, requests, json, sys
from flask import Flask, Blueprint, request, jsonify, render_template, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config
from forms import LoginForm, AddBookForm

site = Blueprint("site", __name__)

# Client webpage routing
@site.route('/')
def home():
    return redirect('/login')

@site.route('/index')
def index():
    addbookform = AddBookForm()
    # Check if the user already logged in
    if(session.get('username') is None):
        return redirect('/login')
   
    url = 'http://' + Config.HOST_IP + ':'  + Config.PORT
    response = requests.get(url + '/book')
    print(Config.HOST_IP)
    data = json.loads(response.text)

    return render_template("book.html", books = data, form=addbookform)

@site.route('/addbook', methods=['GET', 'POST'])
def addbook():
    addbookform = AddBookForm()
    # Check if the user already logged in
    if(session.get('username') is None):
        return redirect('/login')
   
    if addbookform.validate_on_submit():   
        print('Add book request {}: {}: {}: {}'.format(addbookform.isbn.data, 
            addbookform.title.data, addbookform.author.data, addbookform.pubdate.data))

        url = 'http://' + Config.HOST_IP + ':'  + Config.PORT

        # data to be sent to api 
        # data = {'isbn': addbookform.isbn.data, 
        #         'title': addbookform.title.data, 
        #         'author': addbookform.author.data, 
        #         'pubDate': addbookform.pubdate.data} 
        data = {'isbn': 'addbookform.isbn.data', 
        'title': 'King', 
        'author': 'James', 
        'pubDate': '2018-01-05'} 

        response = requests.post(url + '/book', data=data)

        # data = json.loads(response.text)
        # print('response: ' + data)
        flash('Book added successfully')
        
        return redirect('/index')

    return render_template("addbook.html", form=addbookform)

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