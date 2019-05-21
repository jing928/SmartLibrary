import os, requests, json, sys
from flask import Flask, Blueprint, request, jsonify, render_template, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config
from forms import LoginForm, AddBookForm

site = Blueprint("site", __name__)

# Web site page routing
@site.route('/')
def home():
    return redirect('/login')

@site.route('/index')
def index():
    addbookform = AddBookForm()
    # Check if the user already logged in
    if(session.get('username') is None):
        flash('Please log in first!')
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
        headers = {"Content-type": "application/json"}

        # data to be sent to api 
        data = {'isbn': addbookform.isbn.data, 
                'title': addbookform.title.data, 
                'author': addbookform.author.data, 
                'pubDate': addbookform.pubdate.data}

        response = requests.post(url + '/book', data=json.dumps(data), headers=headers)

        # data = json.loads(response.text)
        # print('response: ' + data)
        flash('Book added successfully')
        return redirect('/index')

    return render_template("addbook.html", form=addbookform)


@site.route("/book/<id>", methods = ['POST'])
def deleteBook(id):
    url = 'http://' + Config.HOST_IP + ':'  + Config.PORT

    response = requests.delete(url + '/book/' + id)
    data = json.loads(response.text)

    flash('Book "{}" deleted successfully'.format(data['Title']))
    return redirect('/index')


@site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == Config.USER['username'] and form.password.data == Config.USER['password']:
            session["username"] = form.username.data
            return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@site.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(('/login'))


@site.route('/lending')
def render_lending():
    if(session.get('username') is None):
        flash('Please log in first!')
        return redirect('/login')
    return render_template('lending.html', title='Lending', url = Config.LEND_URL)

@site.route('/return')
def render_return():
    if(session.get('username') is None):
        flash('Please log in first!')
        return redirect('/login')
    return render_template('return.html', title='Return', url = Config.RETURN_URL)