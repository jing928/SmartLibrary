"""
This module implements forms on different pages to faciliate user input.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """
    LoginForm class handles user login process and its validation.

    """
    username = StringField('Username', [DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddBookForm(FlaskForm):
    """
    AddBookForm class handles user add book process and its validation.

    Note: It's used on Addbook page
    """
    isbn = StringField('ISBN', [DataRequired(), Length(min=5, max=20)])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    pubdate = DateTimeField('Published Date', format='%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField('Add Book')


class EditBookForm(FlaskForm):
    """
    EditBookForm class handles user edit book process and its validation.

    Note: It's used on Editbook page
    """    
    isbn = StringField('ISBN', [DataRequired(), Length(min=5, max=20)])
    title = StringField('Title', [DataRequired()])
    author = StringField('Author', [DataRequired()])
    pubdate = DateTimeField('PublishedDate', format='%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField('Apply Change')
