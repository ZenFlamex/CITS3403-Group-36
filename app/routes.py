from app import application, db
from app.models import User, Book, Notification, BookShare, ReadingProgress
from flask import flash, redirect, render_template, g, request, url_for, session, jsonify, abort
from datetime import datetime
from app.forms import LoginForm, SignupForm, AccountSettingsForm, ThemeForm, DeleteAccountForm, BookUploadForm, ProfilePictureForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
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
    recent_notifications = []
    unread_count = 0
    username = None
    
    # Check if the user is logged in using Flask-Login's current_user
    if current_user.is_authenticated:
        username = current_user.username
        
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

@application.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html', title='Forgot Password')

@application.route('/stats')
@login_required
def stats():
    return render_template('stats.html', title='Statistics')

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
                print(f"Error fetching OpenLibrary data: {str(e)}")
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
        
        db.session.add(new_book)
        db.session.commit()
        
        flash('Book added successfully!', 'success')
        return redirect(url_for('my_books'))
        
    return render_template('upload_book.html', title='Add Book', form=form)

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
        filename = datetime.now().strftime('%Y%m%d%H%M%S_') + file.filename
        upload_path = os.path.join(application.root_path, 'static', 'images', 'profile_pictures')

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

    current_user.profile_picture = 'default_pfp.png'
    db.session.commit()
    
    flash('Your profile picture has been removed.', 'success')
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
    

# --- Route to Display Book Details --
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
                 {"pages_read": progress.pages_read}
                 for progress in book.reading_progress
             ]
           
             total_pages_read = sum(item['pages_read'] for item in reading_progress_data) 
             total_entries = len(reading_progress_data)
             average_pages_read = total_pages_read / total_entries if total_entries > 0 else 0
        else:
             reading_progress_data = []
    except Exception as e:
        application.logger.error(f"Error calculating reading progress for book {book_id}: {e}")
        reading_progress_data = [] 

    if is_owner:
        shares_info = db.session.query(
                BookShare.id.label('share_id'),
                User.id.label('user_id'),
                User.username
            ).\
            join(User, BookShare.shared_with_user_id == User.id).\
            filter(BookShare.book_id == book.id).\
            all()
        shared_with_list = [row._asdict() for row in shares_info]

    return render_template(
        'book_detail.html',
        title=book.title,
        book=book,
        is_owner=is_owner,
        has_shared_access=has_shared_access,
        shared_with_list=shared_with_list,
        reading_progress_data=reading_progress_data 
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
        new_share = BookShare(book_id=book.id, shared_with_user_id=user_id_to_share_with)
        db.session.add(new_share)
        db.session.commit()
        flash(f'Book successfully shared with {user_to_share.username}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error sharing book, please try again later.', 'danger')
        application.logger.error(f"Error sharing book {book_id} to user {user_id_to_share_with}: {e}")

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
        db.session.delete(share_to_revoke)
        db.session.commit()
        flash(f'Access revoked for {username}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error revoking access, please try again later.', 'danger')
        application.logger.error(f"Error revoking share {share_id}: {e}")

    return redirect(url_for('book_detail', book_id=book.id))

@application.route('/book/<int:book_id>/add_progress', methods=['POST'])
def add_reading_progress(book_id):
    book = Book.query.get_or_404(book_id)

    # Ensure only the owner can add progress
    if book.creator_id != current_user.id:
        flash("You don't have permission to update this book.", "danger")
        return redirect(url_for('book_detail', book_id=book.id))

    # Get form data
    pages_read = request.form.get('pagesRead', type=int)
    notes = request.form.get('readingNotes', type=str)

    if pages_read is None or pages_read < 0:
        flash("Invalid page number.", "danger")
        return redirect(url_for('book_detail', book_id=book.id))

    total_pages_read = sum(progress.pages_read for progress in book.reading_progress)

    # Ensure the new pages_read does not exceed the remaining pages
    if book.total_pages > 0 and (total_pages_read + pages_read) > book.total_pages:
        remaining_pages = book.total_pages - total_pages_read
        flash(f"You can only add up to {remaining_pages} more pages.", "danger")
        return redirect(url_for('book_detail', book_id=book.id))

    progress = ReadingProgress(
        book_id=book.id,
        user_id=current_user.id,
        pages_read=pages_read,
        notes=notes
    )
    db.session.add(progress)
    db.session.commit()

    flash("Reading progress added successfully!", "success")
    return redirect(url_for('book_detail', book_id=book.id))

@application.route('/book/<int:book_id>/delete_progress/<int:progress_id>', methods=['POST'])
def delete_reading_progress(book_id, progress_id):
    book = Book.query.get_or_404(book_id)
    progress = ReadingProgress.query.get_or_404(progress_id)

    # Ensure only the owner can delete progress
    if book.creator_id != current_user.id:
        flash("You don't have permission to delete this progress entry.", "danger")
        return redirect(url_for('book_detail', book_id=book.id))

    db.session.delete(progress)
    db.session.commit()

    flash("Reading progress entry deleted successfully!", "success")
    return redirect(url_for('book_detail', book_id=book.id))