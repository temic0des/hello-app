from flask_wtf import FlaskForm
from app import db
from sqlalchemy import select
from wtforms import BooleanField, EmailField, StringField, TextAreaField, \
    PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired

from app.models.user import User

class LoginForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "main@example.com"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In', render_kw={"class": "button"})

class SignUpForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "main@example.com"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign Up', render_kw={"class": "button"})

    def validate_email(self, email):
        user = db.session.scalar(
            select(User).where(User.email == email.data)
        )
        if user is not None:
            raise ValidationError('Email address is invalid')
        
class CreateArticleForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Title"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Description"})
    published = BooleanField('Published?')
    submit = SubmitField('Create Article', render_kw={"class": "button"})