from app import application
from flask import render_template

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/signup.html') 
def signup():
    return render_template('signup.html')

@application.route('/login.html')
def login():
    return render_template('login.html') 


@application.route('/forgot_password.html')
def forgot_password():
    return render_template('forgot_password.html') 


@application.route('/upload_book.html')
def upload_book():
    return render_template('upload_book.html')