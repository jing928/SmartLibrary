"""
This module provides functionality for website frontend.
It mainly define routings and associated methods of the website
"""
import json
from datetime import datetime
import requests
from flask import Blueprint, render_template, flash, redirect, session
from config import Config
from forms import LoginForm, AddBookForm, EditBookForm

site = Blueprint("site", __name__)
base_url = 'http://' + Config.HOST_IP + ':' + Config.PORT
headers = {"Content-type": "application/json"}


# Web site page routing
@site.route('/')
def home():
    """ Guard the root path of the URL to make sure it goes to login page.

    Returns:
        Redirect to login page.

    """
    return redirect('/login')


@site.route('/index')
def index():
    """ Presenting the main book page which displays all the book's info.

    Returns:
        The rendered html page for book page with all book data passed to it.

    """

    # Check if the user already logged in
    if session.get('username') is None:
        flash('Please log in first!')
        return redirect('/login')

    response = requests.get(base_url + '/book')
    data = json.loads(response.text)

    return render_template("book.html", books=data)


# website routing for add book function
@site.route('/addbook', methods=['GET', 'POST'])
def addbook():
    """ Provides functionality of the Addbook page.

    Note:
        GET method responds when first time this route is called.
        POST method responds when user already in Addbook page and click the 
        "add book" button

    Returns:
        If added successful, redirect to the main book page (index)
        Otherwise return back to this Add book page

    """
    addbookform = AddBookForm()
    # Check if the user already logged in
    if session.get('username') is None:
        return redirect('/login')

    if addbookform.validate_on_submit():
        # data to be sent to api 
        data = {'isbn': addbookform.isbn.data,
                'title': addbookform.title.data,
                'author': addbookform.author.data,
                'pubDate': addbookform.pubdate.data.strftime("%Y-%m-%d")}
        # API call to add a book with filled data
        requests.post(base_url + '/book', data=json.dumps(data), headers=headers)

        flash('Book added successfully')
        return redirect('/index')

    return render_template("addbook.html", form=addbookform)


# website routing for display book details in Edit page - GET method
@site.route('/editbook/<id>', methods=['GET'])
def getbook(id):
    """ Provides functionality to initialize the Edit Book page with prefilled data.

    Note:
        GET method used when first time edit button is clicked on Book page.

    Returns:
        Render the Edit Book html page with pre-filled page

    """
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
    """ Provides functionality to update book table using filled book information.

    Note:
        POST method responds when user in Editbook page and try to save the updates

    Returns:
        If updated successful, redirect to the main book page (index)
        Otherwise return back to same Edit book page
    """
    editbookform = EditBookForm()

    # Check if the user already logged in
    if session.get('username') is None:
        return redirect('/login')

    # This validation will be Always false for the first time open the page
    if editbookform.validate_on_submit():
        # data to be sent to api 
        data = {'isbn': editbookform.isbn.data,
                'title': editbookform.title.data,
                'author': editbookform.author.data,
                'pubDate': editbookform.pubdate.data.strftime("%Y-%m-%d")}

        requests.put(base_url + '/book/' + id, data=json.dumps(data), headers=headers)

        flash('Book Edited successfully')
        return redirect('/index')

    return render_template("editbook.html", form=editbookform)


# website routing for delete book function
@site.route("/book/<id>", methods=['POST'])
def deletebook(id):
    """ Provides functionality to delete a book with specific book id.
        Call the delete API.

    Returns:
        Redirect to the main book page (index)
    """

    response = requests.delete(base_url + '/book/' + id)
    if response.status_code == 200:
        data = json.loads(response.text)
        flash('Book "{}" is deleted successfully!'.format(data['Title']))
    else:
        flash(u'Book cannot be deleted! Data exists in other tables!')
    return redirect('/index')


@site.route('/login', methods=['GET', 'POST'])
def login():
    """Provide functionaliy of login an existing user

    Note:
        GET method renders the login page when first time this route is called.
        POST method responds when user input his credentials and submit the login form

    Returns:
        If added successful, redirect to the main book page (index)
        Otherwise return back to this Add book page
    Returns:
        Redirect to login page
    """
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == Config.USER['username'] and form.password.data == Config.USER['password']:
            session["username"] = form.username.data
            return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


@site.route('/logout', methods=['GET', 'POST'])
def logout():
    """Provide functionaliy of log out a logged in user

    Returns:
        Redirect to login page
    """
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect('/login')


@site.route('/lending')
def render_lending():
    """Render the statistics page of the website

    Returns:
        Render the statistics page of the website

    """
    # Check if the user already logged in
    if session.get('username') is None:
        flash('Please log in first!')
        return redirect('/login')
    return render_template('lending.html', title='Statistics', url=Config.STAT_URL)
