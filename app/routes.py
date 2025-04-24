from app import application, db
from app.models import User, Book, Notification
from flask import flash, redirect, render_template, g, request, url_for
from datetime import datetime

#  Format a timestamp string into 'DD MonthName YYYY HH:MM' format.
@application.template_filter('datetimeformat') 
def format_datetime_custom(value, format="%d %B %Y %H:%M"):
    if value is None: return ""
    try:
        if isinstance(value, datetime): dt_object = value
        else: dt_object = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
        return dt_object.strftime(format)
    except (ValueError, TypeError): return str(value)

@application.before_request
def load_current_user():
    # Temporary before password is implemented
    user = User.query.filter_by(is_authenticated=True).first()
    if user:
        g.current_user = user
        g.username = user.username
        g.user_id = user.id
    else:
        g.current_user = None
        g.username = None
        g.user_id = None

@application.context_processor
def inject_user():
    username_from_g = getattr(g, 'username', None)
    current_user_from_g = getattr(g, 'current_user', None)
    user_id_from_g = getattr(g, 'user_id', None)
    is_authenticated_from_g = current_user_from_g is not None

    recent_notifications = []
    unread_count = 0
    
    if is_authenticated_from_g and user_id_from_g:
        user_notifications = Notification.query.filter_by(
            receiver_id=user_id_from_g
        ).order_by(Notification.timestamp.desc()).all()
        
        unread_count = Notification.query.filter_by(
            receiver_id=user_id_from_g,
            is_read=False
        ).count()
      
        recent_notifications = user_notifications[:5]

    return {
        'current_user': current_user_from_g, 
        'username': username_from_g,
        'user_id': user_id_from_g,
        'is_authenticated': is_authenticated_from_g, 
        'recent_notifications': recent_notifications,
        'unread_count': unread_count
    }

@application.route('/')
def index():
    current_user_id = g.user_id
    
    if current_user_id:
        # Query books from the database
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
            current_user=None,
            public_books=public_books
        )

@application.route('/signup') 
def signup():
    return render_template('signup.html', title="Sign Up")

@application.route('/login')
def login():
    message = request.args.get('message')
    return render_template('login.html', title='Login', message=message)

@application.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html', title='Forgot Password')

@application.route('/stats')
def stats():
    return render_template('stats.html', title='Statistics')

@application.route('/upload_book')
def upload_book():
    return render_template('upload_book.html', title='Add Book')

@application.route('/my_books')
def my_books():
    current_user_id = g.user_id

    if current_user_id:
        user_books = Book.query.filter_by(creator_id=current_user_id).all()

        status_order = {'In Progress': 0, 'Completed': 1, 'Dropped': 2}
        user_books.sort(key=lambda b: status_order.get(b.status, 3))

        view_mode = request.args.get('view', 'card')
        if view_mode not in ['card', 'row']:
            view_mode = 'card'

        return render_template('my_books.html',
                               title="My Books",
                               current_books=user_books,
                               view_mode=view_mode)
    else:
        return redirect(url_for('login', title='My Books', message='Please log in to view your books.'))

@application.route('/profile')
def profile():
    if g.current_user:
        recent_books = Book.query.filter_by(
            creator_id=g.current_user.id
        ).limit(4).all()
        
        return render_template(
            'profile.html',
            title='My Profile',
            recent_books=recent_books
        )
    else:
        return redirect(url_for('login', message='Please log in to view your profile.'))

@application.route('/settings')
def settings():
    return "Settings Page - Coming Soon"

@application.route('/notifications')
def notifications():
    current_user_id = g.user_id

    if current_user_id:
        user_notifications = Notification.query.filter_by(
            receiver_id=current_user_id
        ).order_by(Notification.timestamp.desc()).all()

        return render_template('notifications.html',
                               title="Notifications",
                               notifications=user_notifications) 
    else:
        flash('Please log in to view notifications.', 'warning')
        return redirect(url_for('login'))