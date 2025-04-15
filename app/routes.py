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

<<<<<<< HEAD

@application.route('/upload_book.html')
def upload_book():
    return render_template('upload_book.html')
=======
@application.route('/stats.html')
def stats():
    return render_template('stats.html')
>>>>>>> 595dbd6de4d7f731a8274d0e5f578b99a0c39341
