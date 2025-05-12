from app import application, db
from app.models import User, Book, Notification, BookShare, ReadingProgress
from flask import flash, redirect, render_template, g, request, url_for, session, jsonify, abort
from datetime import datetime
from app.forms import LoginForm, SignupForm, AccountSettingsForm, ThemeForm, DeleteAccountForm, BookUploadForm, ProfilePictureForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from sqlalchemy import func, distinct
from werkzeug.utils import secure_filename
import requests
import os


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
    unread_notifications_for_dropdown = [] 
    unread_count = 0
    username = None
    
    if current_user.is_authenticated:
        username = current_user.username
        
        unread_notifications_for_dropdown = Notification.query.filter_by(
            receiver_id=current_user.id,
            is_read=False  
        ).order_by(Notification.timestamp.desc()).limit(8).all() 

        unread_count = Notification.query.filter_by(
            receiver_id=current_user.id,
            is_read=False
        ).count()

    return {
        'unread_notifications_for_dropdown': unread_notifications_for_dropdown, 
        'unread_count': unread_count, 
        'username': username
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
        
        shared_book_objects = []
        
        book_share_entries = BookShare.query.filter_by(shared_with_user_id=current_user.id).all()
        
        shared_book_ids_processed = set() 
        for entry in book_share_entries:
            if entry.book and entry.book.id not in shared_book_ids_processed:
                shared_book_objects.append(entry.book)
                shared_book_ids_processed.add(entry.book.id)
        
        # Limit the number of shared books displayed on the homepage for brevity
        shared_books_for_template = shared_book_objects[:4]

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
        goal_books = 10   
        
        # Get distinct genres from completed books for the genre explorer challenge
        completed_genres = db.session.query(Book.genre).filter(
            Book.creator_id == current_user_id,
            Book.status == 'Completed',
            Book.genre.isnot(None),
            Book.genre != ''
        ).distinct().all()
        
        # Extract genre names from the query result
        completed_genre_list = [genre[0] for genre in completed_genres]
        
        # Define the 5 genres for the challenge
        genre_challenge_list = ['Fiction', 'Fantasy', 'Sci-Fi', 'Biography', 'History']
        
        # Create a dictionary to track completion status
        genre_completion = {genre: genre in completed_genre_list for genre in genre_challenge_list}
        
        # Check if all 5 genres are completed
        all_genres_completed = all(genre_completion.values())
        
        # Check if reading challenge is completed
        reading_challenge_completed = completed_count >= goal_books
        
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
            goal_books=goal_books,
            genre_challenge_list=genre_challenge_list,
            genre_completion=genre_completion,
            all_genres_completed=all_genres_completed,
            reading_challenge_completed=reading_challenge_completed,
            shared_books_with_user=shared_books_for_template
        )
    else:
        # User is not authenticated - show all public books
        public_books = Book.query.filter_by(is_public=True).all()
        
        return render_template(
            'index.html',
            title="Home",
            public_books=public_books,
            shared_books_with_user=[]
        )

@application.route('/signup', methods=['GET', 'POST']) 
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignupForm() 
    if form.validate_on_submit(): 
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
       
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
      
        return redirect(url_for('login')) 

    return render_template('signup.html', title="Sign Up", form=form)


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


@application.route('/upload_book', methods=['GET', 'POST'])
@login_required
def upload_book():
    form = BookUploadForm()
    
    if form.validate_on_submit():
        # Handle status-specific validation and data
        if form.status.data == 'Completed':
            # For completed books: ensure current page equals total pages
            if form.total_pages.data:
                form.current_page.data = form.total_pages.data
                
        else:
            # For "In Progress" or "Dropped": ignore end date regardless of what's in the field
            form.end_date.data = None
            
        # Handle book cover image
        cover_image = url_for('static', filename='images/default_cover.png', _external=True)
        
        # If OpenLibrary ID is provided, verify it and get the cover image (so users cannot upload malicious URLs)
        if form.openlibrary_id.data and form.openlibrary_id.data.strip():
            openlibrary_id = form.openlibrary_id.data.strip()
            try:
                # Fetch book data from OpenLibrary API
                if openlibrary_id.startswith('ISBN:'):
                    # Handle ISBN format
                    isbn = openlibrary_id.split(':')[1]
                    api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
                    response = requests.get(api_url)
                    if response.ok:
                        data = response.json()
                        book_data = data.get(f"ISBN:{isbn}")
                        if book_data and book_data.get('cover') and book_data['cover'].get('medium'):
                            cover_image = book_data['cover']['medium']
                else:
                    # Handle standard OpenLibrary format (/works/OL...)
                    api_url = f"https://openlibrary.org{openlibrary_id}.json"
                    response = requests.get(api_url)
                    if response.ok:
                        data = response.json()
                        if data.get('covers') and len(data['covers']) > 0:
                            cover_id = data['covers'][0]
                            cover_image = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            except Exception as e:
                # Log the error but continue with default cover
                application.logger.warning(f"Error fetching OpenLibrary data for '{openlibrary_id}': {str(e)}")
                # We'll use the default cover image if there's an error
        
        # Create new book
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            genre=form.genre.data,
            cover_image=cover_image,
            creator_id=current_user.id,
            status=form.status.data,
            current_page=form.current_page.data or 0,
            total_pages=form.total_pages.data or 0,
            is_favorite=form.is_favorite.data,
            is_public=form.is_public.data,
            rating=form.rating.data or 0,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
        )
        
        try:
            db.session.add(new_book)
            db.session.commit()
            
            # Add a reading progress entry if current_page > 0
            if new_book.current_page > 0:
                initial_progress = ReadingProgress(
                    book_id=new_book.id,
                    user_id=current_user.id,
                    pages_read=new_book.current_page,
                    notes="Initial progress added when the book was created."
                )
                db.session.add(initial_progress)
                db.session.commit()  # Commit the reading progress entry for current page

            flash('Book added successfully!', 'success')

            try:
                application.logger.debug(f"Calling milestone check for user {current_user.id} after adding book.")
                check_and_create_milestone_notifications(current_user)
            except Exception as milestone_e:
                application.logger.error(f"Error during milestone check after adding book for user {current_user.id}: {milestone_e}", exc_info=True)

            return redirect(url_for('my_books')) 

        except Exception as e:
            db.session.rollback() 
            flash(f"Error adding book: {str(e)}", "danger")
            application.logger.error(f"Error adding book for user {current_user.id}: {e}", exc_info=True)
   
    return render_template('upload_book.html', title='Add Book', form=form)

@application.route('/my_books')
@login_required
def my_books():
    favourites_filter = request.args.get('favourites', type=int, default=0) == 1
    shared_filter = request.args.get('shared_with_me', type=int, default=0) == 1

    page_title = "My Books"  # Default page title
    active_filter_type = "all" # Default active filter identifier
    books_to_display = [] # Initialize list to hold books for display

    if favourites_filter:
        books_to_display = Book.query.filter_by(creator_id=current_user.id, is_favorite=True).order_by(Book.title).all()
        page_title = "My Favorite Books"
        active_filter_type = "favourites"
       
        status_order = {'In Progress': 0, 'Completed': 1, 'Dropped': 2}
        books_to_display.sort(key=lambda b: (status_order.get(b.status, 3), b.title.lower()))

    elif shared_filter:
        book_share_entries = BookShare.query.filter_by(shared_with_user_id=current_user.id).all()
        processed_book_ids = set()
        for entry in book_share_entries:
            if entry.book and entry.book.id not in processed_book_ids:
                books_to_display.append(entry.book)
                processed_book_ids.add(entry.book.id)
        # Sort shared books by title
        books_to_display.sort(key=lambda book: book.title.lower())
        page_title = "Books Shared With Me"
        active_filter_type = "shared"

    else:  
        books_to_display = Book.query.filter_by(creator_id=current_user.id).all()
        # Sort user's own books by status, then by title
        status_order = {'In Progress': 0, 'Completed': 1, 'Dropped': 2}
        books_to_display.sort(key=lambda b: (status_order.get(b.status, 3), b.title.lower()))

    view_mode = request.args.get('view', 'card')
    if view_mode not in ['card', 'row']:
        view_mode = 'card'

    return render_template('my_books.html',
                           title=page_title,  
                           current_books=books_to_display, 
                           view_mode=view_mode,
                           active_filter=active_filter_type, 
                           filter_favourites=favourites_filter, 
                           filter_shared=shared_filter  
                           )

def get_favorite_genre(user_id):
    """
    Calculate a user's favorite genre based on the books they've added.
    If multiple genres have the same count, choose the one with the most recent book.
    """
    try:
        # Query to get genres with their counts and newest book date
        genre_stats = db.session.query(
            Book.genre,
            func.count(Book.id).label('count'),
            func.max(Book.id).label('newest_book_id')  # Higher ID = more recent book
        ).filter(
            Book.creator_id == user_id
        ).group_by(
            Book.genre
        ).order_by(
            func.count(Book.id).desc(),  # First order by count
            func.max(Book.id).desc()     # Then by newest book ID
        ).first()
        
        if genre_stats:
            return genre_stats.genre
        return "No favorite yet"
    except Exception as e:
        application.logger.error(f"Error calculating favorite genre for user {user_id}: {e}")
        return "Unknown"


@application.route('/profile')
@login_required
def profile():
    recent_books = Book.query.filter_by(creator_id=current_user.id).limit(4).all() 
    favorite_genre = get_favorite_genre(current_user.id)
    return render_template( 
        'profile.html',
        title='My Profile',
        recent_books=recent_books,
        favorite_genre=favorite_genre
    )

## Set up the upload folder and allowed file extensions for profile pictures
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def sanitize_filename(filename):
    return ''.join(c for c in filename if c.isalnum() or c in '._-')

@application.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    form = ProfilePictureForm()
    if form.validate_on_submit():
        file = form.file.data
        if not allowed_file(file.filename):  # Check if file type is allowed
            flash('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.', 'danger')
            return redirect(url_for('profile'))

        # Sanitize and save the filename
        filename = datetime.now().strftime('%Y%m%d%H%M%S_') + secure_filename(file.filename)
        upload_path = os.path.join(application.root_path, 'static', 'images')

        os.makedirs(upload_path, exist_ok=True)

        file_path = os.path.join(upload_path, filename)
        file.save(file_path)

        old_picture = current_user.profile_picture
        if old_picture and old_picture != 'default_pfp.png':
            old_path = os.path.join(upload_path, old_picture)
            if os.path.exists(old_path):
                os.remove(old_path)

        current_user.profile_picture = filename
        db.session.commit()

        flash('Profile picture updated successfully.', 'success')
        return redirect(url_for('profile'))

    flash('Error uploading profile picture.', 'danger')
    return redirect(url_for('profile'))

@application.route('/remove-profile-picture', methods=['POST'])
def remove_profile_picture():
    if current_user.profile_picture == 'default_pfp.png':
        flash('You cannot remove the default profile picture.', 'warning')
        return redirect(url_for('profile'))
    
    upload_path = os.path.join(application.root_path, 'static', 'images')
    old_picture = current_user.profile_picture
    if old_picture and old_picture != 'default_pfp.png':
        old_path = os.path.join(upload_path, old_picture)
        if os.path.exists(old_path):
            os.remove(old_path)

    current_user.profile_picture = 'default_pfp.png'
    db.session.commit()
    flash("Profile picture reset to default.", "info")
    return redirect(url_for('profile'))

@application.route('/settings', methods=['GET', 'POST']) 
@login_required
def settings():
    account_form = AccountSettingsForm(prefix='account') 
    theme_form = ThemeForm(prefix='theme')
    delete_form = DeleteAccountForm(prefix='delete')

    if request.method == 'POST':
        if account_form.submit_account.data and account_form.validate_on_submit():
            if current_user.username != account_form.username.data:
                 existing_user = User.query.filter(User.username == account_form.username.data, User.id != current_user.id).first()
                 if existing_user:
                     flash('Username already taken.', 'danger')
                     return redirect(url_for('settings'))
                 current_user.username = account_form.username.data
                 flash('Username updated.', 'success')

            if current_user.email != account_form.email.data:
                 existing_user = User.query.filter(User.email == account_form.email.data, User.id != current_user.id).first()
                 if existing_user:
                     flash('Email already registered.', 'danger')
                     return redirect(url_for('settings'))
                 current_user.email = account_form.email.data
                 flash('Email updated.', 'success')

            if account_form.password.data:
                current_user.set_password(account_form.password.data)
                flash('Password updated.', 'success')

            db.session.commit()
            return redirect(url_for('settings')) 

        elif theme_form.submit_theme.data and theme_form.validate_on_submit():
            current_user.theme = theme_form.theme.data
            db.session.commit()
            flash('Theme updated successfully!', 'success')
            return redirect(url_for('settings'))

        elif delete_form.submit_delete.data and delete_form.validate_on_submit():
            user_id_to_delete = current_user.id
            logout_user() 
            user_to_delete = db.session.get(User, user_id_to_delete)
            if user_to_delete:
                # First delete all notifications associated with this user
                Notification.query.filter_by(receiver_id=user_id_to_delete).delete()
                # Now delete the user (books will be deleted by cascade)
                db.session.delete(user_to_delete)
                db.session.commit()
                flash('Your account has been permanently deleted.', 'success')
                return redirect(url_for('index'))
            flash('Error deleting account.', 'danger')
            return redirect(url_for('settings')) 
        else:
             if account_form.errors:
                 for field, errors in account_form.errors.items():
                     for error in errors:
                         flash(f"Account Setting Error in {getattr(account_form, field).label.text}: {error}", 'danger')
             if theme_form.errors:
                  for field, errors in theme_form.errors.items():
                     for error in errors:
                         flash(f"Theme Setting Error in {getattr(theme_form, field).label.text}: {error}", 'danger')
             if delete_form.errors:
                  for field, errors in delete_form.errors.items():
                     for error in errors:
                         flash(f"Delete Account Error in {getattr(delete_form, field).label.text}: {error}", 'danger')

    account_form.username.data = current_user.username
    account_form.email.data = current_user.email

    theme_form.theme.data = current_user.theme 

    return render_template('settings.html', title='Settings',
                           account_form=account_form,
                           theme_form=theme_form,
                           delete_form=delete_form)
                           

@application.route('/notifications')
@login_required 
def notifications():
    user_notifications = Notification.query.filter_by(
        receiver_id=current_user.id
    ).order_by(Notification.timestamp.desc()).all()

    return render_template('notifications.html',
                           title="Notifications",
                           notifications=user_notifications) 
    

# --- Route to Display Book Details ---
@application.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)

    is_owner = False
    has_shared_access = False
    can_view = False
    shared_with_list = []
    reading_progress_data = []

    if book.is_public:
        can_view = True
        if current_user.is_authenticated:
            is_owner = (book.creator_id == current_user.id)
    elif current_user.is_authenticated:
        is_owner = (book.creator_id == current_user.id)
        if is_owner:
            can_view = True
        else:
            share = BookShare.query.filter_by(book_id=book.id, shared_with_user_id=current_user.id).first()
            if share:
                has_shared_access = True
                can_view = True

    if not can_view:
        flash("You don't have permission to view this private book.", "danger")
        if current_user.is_authenticated:
            return redirect(url_for('my_books'))
        else:
            return redirect(url_for('login', next=request.url))

    try:
        if hasattr(book, 'reading_progress') and book.reading_progress:
            reading_progress_data = [
                {
                    "pages_read": progress.pages_read,
                    "timestamp": progress.timestamp.isoformat()  # Convert timestamp to ISO 8601 format
                }
                for progress in book.reading_progress
            ]

            # Calculate total pages read by summing all pages in the reading history
            total_pages_read = sum(item['pages_read'] for item in reading_progress_data)

            # Calculate average pages read
            total_entries = len(reading_progress_data)
            average_pages_read = total_pages_read / total_entries if total_entries > 0 else 0
        else:
            reading_progress_data = []
            total_pages_read = 0
            average_pages_read = 0
    except Exception as e:
        application.logger.error(f"Error calculating reading progress for book {book_id}: {e}")
        reading_progress_data = []
        total_pages_read = 0
        average_pages_read = 0

    if is_owner:
        shares_info = db.session.query(
            BookShare.id.label('share_id'),
            User.id.label('user_id'),
            User.username
        ).join(User, BookShare.shared_with_user_id == User.id).filter(BookShare.book_id == book.id).all()
        shared_with_list = [row._asdict() for row in shares_info]

    return render_template(
        'book_detail.html',
        title=book.title,
        book=book,
        is_owner=is_owner,
        has_shared_access=has_shared_access,
        shared_with_list=shared_with_list,
        reading_progress_data=reading_progress_data,
        total_pages_read=total_pages_read,  # Pass total pages read to the template
        average_pages_read=average_pages_read
    )

# --- API Route to Search Users ---
@application.route('/users/search')
@login_required
def search_users():
    query = request.args.get('q', '', type=str).strip()
    book_id_str = request.args.get('book_id', '') 

    if not query:
        return jsonify([])

    user_query = User.query.filter(
        User.username.ilike(f'%{query}%'),
        User.id != current_user.id
    )

    # Try to exclude book owner and already shared users if book_id is provided
    exclude_ids = {current_user.id}
    if book_id_str.isdigit():
        book_id = int(book_id_str)
        book = db.session.get(Book, book_id)
   
        if book and book.creator_id == current_user.id:
            exclude_ids.add(book.creator_id) 
            
            shared_user_ids = db.session.query(BookShare.shared_with_user_id).filter_by(book_id=book_id).all()
            exclude_ids.update([uid for uid, in shared_user_ids]) 

    if exclude_ids:
        user_query = user_query.filter(User.id.notin_(exclude_ids))

    users = user_query.limit(10).all()
    results = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(results)

# --- Route to Handle Sharing Action ---
@application.route('/book/<int:book_id>/share', methods=['POST'])
@login_required
def share_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        abort(404)

    if book.creator_id != current_user.id:
        abort(403)

    user_id_to_share_with = request.form.get('user_id', type=int)
    if not user_id_to_share_with:
        flash('No user selected.', 'warning')
        return redirect(url_for('book_detail', book_id=book_id))

    user_to_share = db.session.get(User, user_id_to_share_with)
    if not user_to_share:
        flash('Selected user not found.', 'danger')
        return redirect(url_for('book_detail', book_id=book_id))

    if user_id_to_share_with == current_user.id:
        flash('You cannot share a book with yourself.', 'warning')
        return redirect(url_for('book_detail', book_id=book_id))

    existing_share = BookShare.query.filter_by(book_id=book.id, shared_with_user_id=user_id_to_share_with).first()
    if existing_share:
        flash(f'Book already shared with {user_to_share.username}.', 'info')
        return redirect(url_for('book_detail', book_id=book_id))

    try:
        new_share = BookShare(book_id=book.id, shared_with_user_id=user_to_share.id)
        db.session.add(new_share)

        notification_text = f"{current_user.username} shared the book '{book.title}' with you."
        notification_link = url_for('book_detail', book_id=book.id, _external=True)
        direct_share_notification = Notification(
            receiver_id=user_to_share.id,
            sender_name=current_user.username,
            type='share', 
            text=notification_text,
            link=notification_link
        )
        db.session.add(direct_share_notification)
        db.session.commit()
        flash(f'Book successfully shared with {user_to_share.username}!', 'success')

        try:
            application.logger.debug(f"Calling milestone check for user {current_user.id} (sharer) after sharing a book.")
            check_and_create_milestone_notifications(current_user)
        except Exception as milestone_e_sharer: 
            application.logger.error(f"Error during milestone check for sharer {current_user.id}: {milestone_e_sharer}", exc_info=True)

        if user_to_share: 
            try:
                application.logger.debug(f"Calling milestone check for user {user_to_share.id} (receiver) after being shared a book.")
                check_and_create_milestone_notifications(user_to_share)
            except Exception as milestone_e_receiver:
                application.logger.error(f"Error during milestone check for receiver {user_to_share.id}: {milestone_e_receiver}", exc_info=True)
        else:
            application.logger.warning(f"Could not perform milestone check for receiver; user_to_share object was None for ID {user_id_to_share_with}")
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error sharing book: {str(e)}', 'danger')
        application.logger.error(f"Error sharing book {book_id} by user {current_user.id} to user ID {user_id_to_share_with}: {e}", exc_info=True)

    return redirect(url_for('book_detail', book_id=book_id))

# --- Route to Handle Revoking Share Action ---
@application.route('/book/share/<int:share_id>/revoke', methods=['POST'])
@login_required
def revoke_share(share_id):

    share_to_revoke = db.session.get(BookShare, share_id)
    if not share_to_revoke:
        flash('Share record not found.', 'warning')
        return redirect(url_for('index')) 

    book = db.session.get(Book, share_to_revoke.book_id)
    if not book:
        flash('Associated book not found.', 'danger')
        
        try:
            db.session.delete(share_to_revoke)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            application.logger.error(f"Error deleting orphaned share {share_id} after book not found: {e}")
        return redirect(url_for('index'))

    # Authorization: Only the book owner can revoke
    if book.creator_id != current_user.id:
        abort(403)

    try:
        user_shared_with = db.session.get(User, share_to_revoke.shared_with_user_id)
        username = user_shared_with.username if user_shared_with else "this user" 
        # Create a notification for the user whose access is being revoked
        book_id_of_revoked_share = share_to_revoke.book_id
        receiver_id_of_notification = share_to_revoke.shared_with_user_id

        db.session.delete(share_to_revoke)
        application.logger.info(f"Share record ID {share_id} deleted.")

        expected_link = url_for('book_detail', book_id=book_id_of_revoked_share, _external=True)
        
        related_notification = Notification.query.filter_by(
            receiver_id=receiver_id_of_notification,
            type='share',
            link=expected_link
        ).first() 

        if related_notification:
            application.logger.info(f"Revoking share also deleting related 'share' notification ID: {related_notification.id} for receiver_id: {receiver_id_of_notification}, book_id: {book_id_of_revoked_share}")
            db.session.delete(related_notification)
        else:
            # If no specific notification found, log the event
            application.logger.info(f"No specific 'share' notification found to delete for share revoke targeting: receiver_id={receiver_id_of_notification}, book_id={book_id_of_revoked_share}, expected_link={expected_link}")

        db.session.commit()
        flash(f'Access revoked for {username}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error revoking access, please try again later.', 'danger')
        application.logger.error(f"Error revoking share {share_id}: {e}")

    return redirect(url_for('book_detail', book_id=book.id))


@application.route('/book/<int:book_id>/add_progress', methods=['POST'])
@login_required 
def add_reading_progress(book_id):
    book = Book.query.get_or_404(book_id)
    if book.creator_id != current_user.id:
        abort(403)

    pages_read = request.form.get('pagesRead', type=int)
    notes = request.form.get('readingNotes', '')

    # Calculate total pages already read
    total_pages_read = sum(progress.pages_read for progress in book.reading_progress)

    book_status_changed = False

    # Validate that pages_read does not exceed the remaining pages
    if pages_read is not None:
        remaining_pages = book.total_pages - total_pages_read
        if book.total_pages > 0 and pages_read > remaining_pages:
            flash(f"Cannot add progress. The current page ({pages_read}) exceeds the remaining pages of the book ({remaining_pages}).", "danger")
            return redirect(url_for('book_detail', book_id=book.id))

        if pages_read < 0:
            flash("Cannot add progress. The current page cannot be negative.", "danger")
            return redirect(url_for('book_detail', book_id=book.id))

        # Update the current page
        book.current_page = total_pages_read + pages_read

        # Automatically set status to "In Progress" if it was "Dropped" and pages are added
        if book.status == 'Dropped' and pages_read > 0:
            book.status = 'In Progress'

        # Automatically set status to "Completed" if current page equals total pages
        if book.total_pages > 0 and book.current_page >= book.total_pages:
            book.current_page = book.total_pages
            book.status = 'Completed'

    # Add a new reading progress entry
    progress = ReadingProgress(
        book_id=book.id,
        user_id=current_user.id,
        pages_read=pages_read,
        notes=notes
    )

    try:
        db.session.add(progress)
        if book_status_changed:
            db.session.add(book) 

        db.session.commit() 
        flash("Reading progress added successfully!", "success")

        check_and_create_milestone_notifications(current_user)

    except Exception as e:
        db.session.rollback()
        flash("Error saving reading progress.", "danger")
        application.logger.error(f"Error adding reading progress for book {book_id} by user {current_user.id}: {e}", exc_info=True)


    return redirect(url_for('book_detail', book_id=book.id))

@application.route('/book/<int:book_id>/delete_progress/<int:progress_id>', methods=['POST'])
def delete_reading_progress(book_id, progress_id):
    book = Book.query.get_or_404(book_id)
    progress = ReadingProgress.query.get_or_404(progress_id)

    if book.creator_id != current_user.id:
        flash("You don't have permission to delete this progress entry.", "danger")
        return redirect(url_for('book_detail', book_id=book.id))

    db.session.delete(progress)
    db.session.commit()

    flash("Reading progress entry deleted successfully!", "success")
    return redirect(url_for('book_detail', book_id=book.id))


# --- API Route to Mark Notification as Read ---
@application.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = db.session.get(Notification, notification_id)

    # Check if notification exists
    if not notification:
        return jsonify({'success': False, 'message': 'Notification not found.'}), 404

    # Check if the notification belongs to the current user
    if notification.receiver_id != current_user.id:
        return jsonify({'success': False, 'message': 'Forbidden.'}), 403

    # Mark as read if it's not already
    if not notification.is_read:
        try:
            notification.is_read = True
            db.session.commit()

            return jsonify({'success': True}), 200
        except Exception as e:
            db.session.rollback()
            application.logger.error(f"Error marking notification {notification_id} as read: {e}")
            return jsonify({'success': False, 'message': 'Database error.'}), 500
    else:
        return jsonify({'success': True}), 200

def check_and_create_milestone_notifications(user):
    if not user or not isinstance(user, User):
        application.logger.warning("Invalid user passed to milestone check.")
        return

    application.logger.debug(f"Checking milestones for user {user.id} ({user.username})")

    milestones = {
        'first_book_added': {
            'condition': lambda u: Book.query.filter_by(creator_id=u.id).count() >= 1,
            'text': 'Bookshelf initiated! You successfully added your first book.',
            'link': lambda: url_for('my_books', _external=True)
        },
        'first_book_completed': {
            'condition': lambda u: Book.query.filter_by(creator_id=u.id, status='Completed').count() >= 1,
            'text': 'First victory! Congratulations on completing your first book!',
            'link': lambda: url_for('my_books', _external=True)
        },

        'completed_5_books': { 
            'condition': lambda u: Book.query.filter_by(creator_id=u.id, status='Completed').count() >= 5,
            'text': 'Reading enthusiast! You have completed 5 books!',
            'link': lambda: url_for('my_books', _external=True)
        },
        'completed_10_books': { 
            'condition': lambda u: Book.query.filter_by(creator_id=u.id, status='Completed').count() >= 10,
            'text': 'Perfect ten! 10 books completed, keep it up!',
            'link': lambda: url_for('my_books', _external=True)
        },
        'completed_25_books': { 
            'condition': lambda u: Book.query.filter_by(creator_id=u.id, status='Completed').count() >= 25,
            'text': 'Reading expert! 25 books completed, awesome!',
            'link': lambda: url_for('my_books', _external=True)
        },
        'completed_50_books': {
            'condition': lambda u: Book.query.filter_by(creator_id=u.id, status='Completed').count() >= 50,
            'text': 'Reading master! 50 books completed, impressive!',
            'link': lambda: url_for('my_books', _external=True)
        },

        'read_100_pages': { 
            'condition': lambda u: (db.session.query(func.sum(ReadingProgress.pages_read))
                                    .filter(ReadingProgress.user_id == u.id).scalar() or 0) >= 100,
            'text': 'A journey of a thousand pages begins with a single step! You\'ve read over 100 pages!',
            'link': lambda: url_for('my_books', _external=True)
        },
        'read_1000_pages': { 
            'condition': lambda u: (db.session.query(func.sum(ReadingProgress.pages_read))
                                    .filter(ReadingProgress.user_id == u.id).scalar() or 0) >= 1000,
            'text': 'Breaking a thousand! You\'ve read over 1000 pages!',
            'link': lambda: url_for('my_books', _external=True)
        },
        'read_5000_pages': {
            'condition': lambda u: (db.session.query(func.sum(ReadingProgress.pages_read))
                                    .filter(ReadingProgress.user_id == u.id).scalar() or 0) >= 5000,
            'text': 'Page conqueror! Your reading volume has exceeded 5000 pages!',
            'link': lambda: url_for('my_books', _external=True)
        },
        'read_10000_pages': { 
            'condition': lambda u: (db.session.query(func.sum(ReadingProgress.pages_read))
                                    .filter(ReadingProgress.user_id == u.id).scalar() or 0) >= 10000,
            'text': 'Breaking ten thousand! Your reading volume has exceeded 10,000 pages!',
            'link': lambda: url_for('my_books', _external=True)
        },

         'diverse_reader_3_genres': { 
             'condition': lambda u: db.session.query(func.count(distinct(Book.genre))).filter(Book.creator_id == u.id).scalar() >= 3,
             'text': 'Broad Tastes! You have added books from at least 3 different genres.',
             'link': lambda: url_for('my_books', _external=True)
    
         },

        'shared_first_book': {
            'condition': lambda u: db.session.query(BookShare.id).join(Book, BookShare.book_id == Book.id).filter(Book.creator_id == u.id).count() >= 1,
            'text': 'Sharing is caring! You shared your first book.',
            'link': lambda: url_for('my_books', _external=True)
        },
         
    }

    for key, config in milestones.items():
        try:
            if config['condition'](user):
                application.logger.debug(f"User {user.id} meets condition for milestone '{key}'")
        
                existing_notification = Notification.query.filter_by(
                    receiver_id=user.id,
                    type=key 
                ).first()

                if not existing_notification:
                    application.logger.info(f"Milestone '{key}' reached by user {user.id} and not yet notified. Creating notification.")
                    notification = Notification(
                        receiver_id=user.id,
                        sender_name='System',
                        type=key,
                        text=config['text'],
                        link=config['link']() 
                    )
                    db.session.add(notification)
                    db.session.commit() 
                    application.logger.info(f"Milestone notification '{key}' successfully created for user {user.id}")

                else:
                     application.logger.debug(f"User {user.id} already notified for milestone '{key}'. Skipping.")

        except Exception as e:
            db.session.rollback()
            application.logger.error(f"Error processing milestone '{key}' for user {user.id}: {e}", exc_info=True)
@application.route('/book/<int:book_id>/change_status', methods=['POST'])
def change_status(book_id):
    book = Book.query.get_or_404(book_id)

    # Ensure only the owner can change the status
    if book.creator_id != current_user.id:
        abort(403)

    new_status = request.form.get('status')

    # Prevent setting "Completed" if current page < total pages
    if new_status == 'Completed' and book.current_page < book.total_pages:
        flash("Cannot mark as 'Completed' because the current page is less than the total pages.", "danger")
        return redirect(url_for('book_detail', book_id=book.id))

    # Prevent changing status if the book is already completed
    if book.status == 'Completed':
        flash("Cannot change status because the book is already completed.", "danger")
        return redirect(url_for('book_detail', book_id=book.id))

    if new_status in ['Completed', 'Dropped', 'In Progress']:
        book.status = new_status
        db.session.commit()
        flash(f"Book status updated to '{new_status}'.", "success")
    else:
        flash("Invalid status.", "danger")

    return redirect(url_for('book_detail', book_id=book.id))


@application.route('/book/<int:book_id>/toggle_favorite', methods=['POST'])
def toggle_favorite(book_id):
    book = Book.query.get_or_404(book_id)

    # Ensure only the owner can toggle favorites
    if book.creator_id != current_user.id:
        abort(403)

    # Toggle the is_favorite attribute
    book.is_favorite = not book.is_favorite
    db.session.commit()

    if book.is_favorite:
        flash("Book added to favorites.", "success")
    else:
        flash("Book removed from favorites.", "success")

    return redirect(url_for('book_detail', book_id=book.id))


@application.route('/book/<int:book_id>/toggle_public', methods=['POST'])
def toggle_public(book_id):
    book = Book.query.get_or_404(book_id)

    # Ensure only the owner can toggle public/private status
    if book.creator_id != current_user.id:
        abort(403)

    book.is_public = not book.is_public
    db.session.commit()

    if book.is_public:
        flash("Book is now public.", "success")
    else:
        flash("Book is now private.", "success")

    return redirect(url_for('book_detail', book_id=book.id))

@application.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    # Ensure only the owner can delete the book
    if book.creator_id != current_user.id:
        abort(403)

    # Delete the book
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully.", "success")

    return redirect(url_for('index'))

@application.route('/book/<int:book_id>/update_rating', methods=['POST'])
def update_rating(book_id):
    book = Book.query.get_or_404(book_id)

    # Ensure only the owner can update the rating
    if book.creator_id != current_user.id:
        abort(403)

    new_rating = request.form.get('rating', type=int)
    if new_rating is not None and 0 <= new_rating <= 5:
        book.rating = new_rating
        db.session.commit()
        flash("Book rating updated successfully.", "success")
    else:
        flash("Invalid rating value.", "danger")

    return redirect(url_for('book_detail', book_id=book.id))
