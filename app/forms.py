from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, PasswordField, BooleanField, SubmitField, RadioField, FileField
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


# --- Upload Book Forms ---
class BookUploadForm(FlaskForm):
    submission_token = StringField('Submission Token', validators=[Optional()])
    # Auto-fill fields (hidden when using API search)
    openlibrary_id = StringField('OpenLibrary ID', validators=[Optional()])
    cover_image = StringField('Cover Image URL', validators=[Optional()])
    
    # Visible form fields
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    
    # Using SelectField for dropdown
    genre = SelectField('Genre', choices=[
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Thriller', 'Thriller'),
        ('Biography', 'Biography'),
        ('History', 'History'),
        ('Self-Help', 'Self-Help'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    
    status = SelectField('Reading Status', choices=[
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Dropped', 'Dropped')
    ], validators=[DataRequired()])
    
    current_page = IntegerField('Current Page', validators=[Optional()])
    total_pages = IntegerField('Total Pages', validators=[DataRequired()])
    rating = SelectField('Rating (Stars)', choices=[
        ('', 'Select rating'),
        ('1', '1 - Poor'),
        ('2', '2 - Fair'),
        ('3', '3 - Good'),
        ('4', '4 - Very Good'),
        ('5', '5 - Excellent')
    ], validators=[Optional()])
    start_date = DateField('Date Started Reading', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Date Finished Reading', format='%Y-%m-%d', validators=[Optional()])
    
    is_public = BooleanField('Make this book public')
    is_favorite = BooleanField('Add to favorites')
    
    submit = SubmitField('Add Book')
    
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        
        # Check if current page equals total pages but status is "In Progress"
        if (self.status.data == 'In Progress' and self.current_page.data and self.total_pages.data and self.current_page.data == self.total_pages.data):
            self.status.data = 'Completed'
            if not self.rating.data or self.rating.data == '':
                self.rating.errors = ['Status has been changed to "Completed" because current page equals total pages. Please provide a rating.']
                return False
        
        # Status-specific validations
        if self.status.data == 'Completed' and not self.end_date.data:
            self.end_date.errors = ['End date is required for completed books']
            return False
        
        if self.status.data in ['In Progress', 'Dropped'] and not self.current_page.data:
            self.current_page.errors = ['Current page is required']
            return False
            
        if self.current_page.data and self.total_pages.data and self.current_page.data > self.total_pages.data:
            self.current_page.errors = ['Current page cannot be greater than total pages']
            return False
        
        if self.start_date.data and self.end_date.data and self.end_date.data < self.start_date.data:
            self.end_date.errors = ['End date cannot be before start date']
            return False
        
        # Handle rating based on status
        if self.status.data == 'In Progress':
            self.rating.data = '0'  # Force rating to 0 for In Progress
        else:
            if not self.rating.data:
                self.rating.errors = ['Rating is required for completed or dropped books']
                return False
        
        return True

# --- Profile Picture Upload Form ---
class ProfilePictureForm(FlaskForm):
    file = FileField('Profile Picture', validators=[DataRequired()])
    submit = SubmitField('Upload Picture')