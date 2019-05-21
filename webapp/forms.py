from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

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
    # status_tick = SelectField('Status', choices=[('avail', 'Available'), ('unavail', 'Unavailable')])

    # status = BooleanField('Status')
    submit = SubmitField('Add Book')
