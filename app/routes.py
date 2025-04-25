from app import application, db
from app.models import User, Book, Notification
from flask import flash, redirect, render_template, g, request, url_for, session
from datetime import datetime
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

#  Format a timestamp string into 'DD MonthName YYYY HH:MM' format.
@application.template_filter('datetimeformat') 
def format_datetime_custom(value, format="%d %B %Y %H:%M"):
    if value is None: return ""
    try:
        if isinstance(value, datetime): dt_object = value
        else: dt_object = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
        return dt_object.strftime(format)
    except (ValueError, TypeError): return str(value)


@application.context_processor
def inject_notifications():
    recent_notifications = []
    unread_count = 0
    # Check if the user is logged in using Flask-Login's current_user
    if current_user.is_authenticated:
        user_notifications = Notification.query.filter_by(
            receiver_id=current_user.id 
        ).order_by(Notification.timestamp.desc()).limit(5).all() 

        unread_count = Notification.query.filter_by(
            receiver_id=current_user.id,
            is_read=False
        ).count()
        recent_notifications = user_notifications 

    return {
        'recent_notifications': recent_notifications,
        'unread_count': unread_count
    }

@application.route('/')
def index():
    if current_user.is_authenticated:
        current_user_id = current_user.id

        favorite_books = Book.query.filter_by(
            creator_id=current_user_id, 
            is_favorite=True
        ).all()
        
        current_books = Book.query.filter_by(
            creator_id=current_user_id
        ).all()
        
        # Sort by status
        status_order = {'In Progress': 0, 'Completed': 1, 'Dropped': 2}
        current_books.sort(key=lambda b: status_order.get(b.status, 3))

        public_books = Book.query.filter(
            Book.is_public == True,
            Book.creator_id != current_user_id
        ).all()
        
        # Calculate reading statistics
        reading_count = Book.query.filter_by(
            creator_id=current_user_id,
            status='In Progress'
        ).count()
        
        completed_count = Book.query.filter_by(
            creator_id=current_user_id,
            status='Completed'
        ).count()
        
        # Calculate pages read
        all_user_books = Book.query.filter_by(creator_id=current_user_id).all()
        pages_read = sum(min(b.current_page, b.total_pages) for b in all_user_books)
        
        hours_read = 145  # Placeholder for hours read, to be calculated later     
        goal_books = 50   # Will be set by the user in the future     
        
        return render_template(
            'index.html',
            title="Home",
            favorite_books=favorite_books,
            current_books=current_books,
            public_books=public_books,
            reading_count=reading_count,
            completed_count=completed_count,
            pages_read=pages_read,
            hours_read=hours_read,
            completed_books=completed_count,
            goal_books=goal_books
        )
    else:
        # User is not authenticated - show all public books
        public_books = Book.query.filter_by(is_public=True).all()
        
        return render_template(
            'index.html',
            title="Home",
            public_books=public_books
        )

@application.route('/signup') 
def signup():
    return render_template('signup.html', title="Sign Up")

@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm() 
    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first() 
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password.', 'danger') 
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Login successful!', 'success')

        next_page = request.args.get('next')
 
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index') 
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)

@application.route('/logout')
@login_required
def logout():
    logout_user() 
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@application.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html', title='Forgot Password')

@application.route('/stats')
@login_required
def stats():
    return render_template('stats.html', title='Statistics')

@application.route('/upload_book')
@login_required
def upload_book():
    return render_template('upload_book.html', title='Add Book')

@application.route('/my_books')
@login_required
def my_books():
    user_books = Book.query.filter_by(creator_id=current_user.id).all()

    status_order = {'In Progress': 0, 'Completed': 1, 'Dropped': 2}
    user_books.sort(key=lambda b: status_order.get(b.status, 3))

    view_mode = request.args.get('view', 'card')
    if view_mode not in ['card', 'row']:
        view_mode = 'card'

    return render_template('my_books.html',
                            title="My Books",
                            current_books=user_books,
                            view_mode=view_mode)

@application.route('/profile')
@login_required
def profile():
    recent_books = Book.query.filter_by(creator_id=current_user.id).limit(4).all() 
    return render_template( 
        'profile.html',
        title='My Profile',
        recent_books=recent_books
    )

@application.route('/settings')
@login_required
def settings():
    email = current_user.email
    return render_template('settings.html', title='Settings')

@application.route('/notifications')
@login_required 
def notifications():
    user_notifications = Notification.query.filter_by(
        receiver_id=current_user.id
    ).order_by(Notification.timestamp.desc()).all()

    return render_template('notifications.html',
                           title="Notifications",
                           notifications=user_notifications) 
    
@application.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)

    # If the book is private and the current user is not the creator
    if not book.is_public and (not current_user.is_authenticated or book.creator_id != current_user.id):
        flash("You don't have permission to view this book.", "danger")
        return redirect(url_for('my_books'))

    # If the book is public, allow viewing but only the creator can edit
    can_edit = current_user.is_authenticated and book.creator_id == current_user.id

    return render_template(
        'book_detail.html',
        title=book.title,
        book=book,
        can_edit=can_edit
    )
