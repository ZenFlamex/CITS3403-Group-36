from app import application
from flask import flash, redirect, render_template, g, request, url_for
from app.data import USER, BOOKS  # Import the data from data.py

@application.before_request
def load_current_user():
    if USER and USER.get('is_authenticated', False):
        g.current_user = USER
        g.username = USER['username']
    else:
        g.current_user = None
        g.username = None

@application.context_processor
def inject_user():
    return {
        'current_user': getattr(g, 'current_user', None),
        'username': getattr(g, 'username', None)
    }


@application.route('/')
def index():
    current_username = g.username 
    
    # Filter books for different sections based on the consolidated list
    if current_username:
        favorite_books = [book for book in BOOKS if book['creator'] == current_username and book['is_favorite']]
        current_books = [book for book in BOOKS if book['creator'] == current_username]

        # Sort by In Progress → Completed → Dropped
        status_order = {'In Progress': 0, 'Completed': 1, 'Dropped': 2}
        current_books.sort(key=lambda b: status_order.get(b['status'], 3))

        public_books = [book for book in BOOKS if book['is_public'] and book['creator'] != current_username] 
        
        # Calculate reading statistics
        reading_count = len([b for b in current_books if b['status'] == 'In Progress'])
        completed_count = len([b for b in current_books if b['status'] == 'Completed'])
        pages_read = sum(min(b['current_page'], b['total_pages']) for b in current_books)
        hours_read = 145 # Placeholder for hours read, to be calculated later     
        completed_books = len([b for b in current_books if b['status'] == 'Completed'])
        goal_books = 50  # Will be set by the user in the future     
        
        return render_template(
            'index.html',
            favorite_books=favorite_books,
            current_books=current_books,
            public_books=public_books,
            reading_count=reading_count,
            completed_count=completed_count,
            pages_read=pages_read,
            hours_read=hours_read,
            completed_books=completed_books,
            goal_books=goal_books
        )
    else:
        # User is not authenticated - show all public books
        public_books = [book for book in BOOKS if book['is_public']]
        
        return render_template(
            'index.html',
            current_user=None,
            public_books=public_books
        )

@application.route('/signup') 
def signup():
    return render_template('signup.html')

@application.route('/login')
def login():
    message = request.args.get('message')
    return render_template('login.html', message=message)


@application.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@application.route('/stats')
def stats():
    return render_template('stats.html')

@application.route('/upload_book')
def upload_book():
    return render_template('upload_book.html')

# New routes for future functionality
@application.route('/add_book')
def add_book():
    return "Add Book Page - Coming Soon"


@application.route('/my_books')
def my_books():
    current_username = g.username 

    if current_username:
        user_books = [book for book in BOOKS if book.get('creator') == current_username]

        status_order = {'In Progress': 0, 'Completed': 1, 'Dropped': 2}
        user_books.sort(key=lambda b: status_order.get(b.get('status'), 3))

        view_mode = request.args.get('view', 'card')
        if view_mode not in ['card', 'row']:
            view_mode = 'card'

        return render_template('my_books.html',
                               title="My Books",
                               current_books=user_books,
                               view_mode=view_mode)
    else:
        return redirect(url_for('login', message='Please log in to view your books.'))




@application.route('/profile')
def profile():
    return "Profile Page - Coming Soon"