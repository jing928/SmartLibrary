import requests
import json
from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, session
from config import Config
from forms import LoginForm, AddBookForm, EditBookForm

site = Blueprint("site", __name__)
base_url = 'http://' + Config.HOST_IP + ':' + Config.PORT
headers = {"Content-type": "application/json"}

# Web site page routing
@site.route('/')
def home():
    return redirect('/login')


@site.route('/index')
def index():
    addbookform = AddBookForm()
    # Check if the user already logged in
    if session.get('username') is None:
        flash('Please log in first!')
        return redirect('/login')

    url = 'http://' + Config.HOST_IP + ':' + Config.PORT
    response = requests.get(url + '/book')
    print(Config.HOST_IP)
    data = json.loads(response.text)

    return render_template("book.html", books=data, form=addbookform)

# website routing for add book function
@site.route('/addbook', methods=['GET', 'POST'])
def addbook():
    addbookform = AddBookForm()
    # Check if the user already logged in
    if session.get('username') is None:
        return redirect('/login')

    if addbookform.validate_on_submit():
        print('Add book request {}: {}: {}: {}'.format(addbookform.isbn.data,
                                                       addbookform.title.data, addbookform.author.data,
                                                       addbookform.pubdate.data))

        url = 'http://' + Config.HOST_IP + ':' + Config.PORT
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

# website routing for display book details in Edit page - GET method
@site.route('/editbook/<id>', methods=['GET'])
def getbook(id):

    # Check if the user already logged in
    if session.get('username') is None:
        return redirect('/login')

    # Invoke API to get book information for specific book id
    response = requests.get(base_url + '/book/' + id)
    data = json.loads(response.text)
    print(data)

    editbookform = EditBookForm()
    editbookform.isbn.data = data['ISBN']
    editbookform.title.data = data['Title']
    editbookform.author.data = data['Author']
    editbookform.pubdate.data = datetime.strptime(data['PublishedDate'], "%Y-%m-%d")

    return render_template("editbook.html", form=editbookform)

# website routing for edit book details in Edit page - POST method
@site.route('/editbook/<id>', methods=['POST'])
def editbook(id):
    editbookform = EditBookForm()

    # Check if the user already logged in
    if session.get('username') is None:
        return redirect('/login')

    # This validation will be Always false for the first time open the page
    if editbookform.validate_on_submit():
        print('Edit book request {}: {}: {}: {}'.format(editbookform.isbn.data,
                                                       editbookform.title.data, editbookform.author.data,
                                                       editbookform.pubdate.data))

        url = 'http://' + Config.HOST_IP + ':' + Config.PORT
        headers = {"Content-type": "application/json"}

        # data to be sent to api 
        data = {'isbn': editbookform.isbn.data,
                'title': editbookform.title.data,
                'author': editbookform.author.data,
                'pubDate': editbookform.pubdate.data.strftime("%Y-%m-%d")}

        response = requests.put(url + '/book/' + id, data=json.dumps(data), headers=headers)

        # data = json.loads(response.text)
        # print('response: ' + data)
        flash('Book Edited successfully')
        return redirect('/index')

    return render_template("editbook.html", form=editbookform)


# website routing for delete book function
@site.route("/book/<id>", methods=['POST'])
def deletebook(id):
    url = 'http://' + Config.HOST_IP + ':' + Config.PORT

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
    return redirect('/login')


@site.route('/lending')
def render_lending():
    # Check if the user already logged in
    if session.get('username') is None:
        flash('Please log in first!')
        return redirect('/login')
    return render_template('lending.html', title='Lending', url=Config.LEND_URL)
