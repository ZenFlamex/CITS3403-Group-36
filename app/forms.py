from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

    # Custom validator to check if username already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken. Please choose a different one.')

    # Custom validator to check if email already exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already registered.')


# --- Settings Forms ---

class AccountSettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    # Password fields are optional - only validate if user enters something
    password = PasswordField('New Password', validators=[Optional(), Length(min=6, message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[Optional(),
                                                 EqualTo('password', message='New passwords must match.')])
    submit_account = SubmitField('Save Changes') 

    # Validate username uniqueness (only if changed)
    def validate_username(self, username):
        if username.data != current_user.username: 
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Username already taken. Please choose a different one.')

    # Validate email uniqueness (only if changed)
    def validate_email(self, email):
        if email.data != current_user.email: 
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Email address already registered.')

class ThemeForm(FlaskForm):
    # Use RadioField for theme selection
    theme = RadioField('Theme', choices=[('light', 'Light Mode'), ('dark', 'Dark Mode')],
                       validators=[DataRequired()])
    submit_theme = SubmitField('Save Theme') 

class DeleteAccountForm(FlaskForm):
    password = PasswordField('Confirm Password to Delete Account', validators=[DataRequired()])
    submit_delete = SubmitField('Delete Account') 

    def validate_password(self, password):
      if not current_user.check_password(password.data):
        raise ValidationError('Incorrect password.')
