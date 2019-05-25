from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddBookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    pubdate = StringField('Published Date', validators=[DataRequired()])

    submit = SubmitField('Add Book')


class EditBookForm(FlaskForm):
    isbn = StringField('ISBN', [DataRequired(), Length(min=5, max=20)])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    pubdate = DateTimeField('PublishedDate', format='%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField('Apply Change')
