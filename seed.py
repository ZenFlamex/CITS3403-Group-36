from app import create_app, db
from app.models import User, Book, ReadingProgress, BookShare, Notification
from datetime import datetime, timezone, timedelta
from config import Config

application = create_app(Config)

def seed_database():
    print("Seeding database...")
    
    # Clear existing data in reverse dependency order
    print("Clearing existing data...")
    ReadingProgress.query.delete()
    BookShare.query.delete()
    Notification.query.delete()
    Book.query.delete()
    User.query.delete()
    db.session.commit()
    
    # Create users with join_date
    def create_user(username, email, password, join_date=None):
        """Create a user with specified join date"""
        if join_date is None:
            join_date = datetime.now(timezone.utc)
            
        user = User(
            username=username,
            email=email,
            join_date=join_date
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Get ID before committing
        return user
   
    print("Creating users...")
    # Create users with different join dates to test features
    bookworm = create_user(
        'bookworm', 
        'bookworm@example.com', 
        'password123',
        datetime.strptime('2025-01-10 12:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    wizardfan = create_user(
        'wizardfan', 
        'wizardfan@example.com', 
        'passwordabc',
        datetime.strptime('2025-02-15 14:30:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    scifibro = create_user(
        'scifibro', 
        'scifibro@example.com', 
        'simple123',
        datetime.strptime('2025-03-20 09:15:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    literarylion = create_user(
        'literarylion', 
        'literarylion@example.com', 
        'simple123',
        datetime.strptime('2025-04-05 16:45:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    mysterymaven = create_user(
        'mysterymaven', 
        'mysterymaven@example.com', 
        'simple123',
        datetime.strptime('2025-04-20 10:30:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    db.session.commit()
    print("Users created successfully")
    
    # Function to add books - initialize with 0 current page
    def add_book(title, author, cover_image, creator, genre, rating=0, status="In Progress", 
                total_pages=0, is_favorite=False, is_public=False,
                start_date=None, end_date=None):
        """Add a book to the database"""
        book = Book(
            title=title,
            author=author,
            cover_image=cover_image,
            creator_id=creator.id,
            genre=genre,  
            rating=rating,
            status=status,
            current_page=0,  # Initialize all books with current_page = 0
            total_pages=total_pages,
            is_favorite=is_favorite,
            is_public=is_public,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(book)
        db.session.flush()
        return book
    
    # Add reading progress for books
    def add_progress(book, user, pages_read, timestamp=None, notes="Initial progress added when the book was created."):
        if timestamp is None:
            timestamp = datetime.utcnow()
            
        progress = ReadingProgress(
            book_id=book.id,
            user_id=user.id,
            pages_read=pages_read,
            notes=notes,
            timestamp=timestamp
        )
        db.session.add(progress)
        return progress
    
    print("Creating books...")
    
    # 1. Fiction book for bookworm
    book_fiction = add_book(
        'To Kill a Mockingbird', 
        'Harper Lee', 
        'https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg',
        bookworm, 
        genre='Fiction',
        rating=4, 
        status='Completed', 
        total_pages=281, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-01-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-02-05', '%Y-%m-%d')
    )
    # Initial progress
    initial_date = datetime.strptime('2025-01-20', '%Y-%m-%d')
    add_progress(book_fiction, bookworm, 50, initial_date, "Initial progress added when the book was created.")
    
    # Middle progress
    middle_date = initial_date + timedelta(days=8)
    add_progress(book_fiction, bookworm, 100, middle_date, "This book is getting really interesting! Love the character development.")
    
    # Final progress
    final_date = datetime.strptime('2025-02-05', '%Y-%m-%d')
    add_progress(book_fiction, bookworm, 131, final_date, "Finished! The ending was perfect. Adding this to my favorites.")
    book_fiction.current_page = 281
    
    # 2. Fantasy book for bookworm
    book_fantasy = add_book(
        'Red Queen', 
        'Victoria Aveyard', 
        'https://covers.openlibrary.org/b/isbn/9780062310637-L.jpg',
        bookworm, 
        genre='Fantasy',
        rating=5, 
        status='Completed', 
        total_pages=400, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-01-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-02-10', '%Y-%m-%d')
    )
    # Initial progress
    initial_date = datetime.strptime('2025-01-15', '%Y-%m-%d')
    add_progress(book_fantasy, bookworm, 80, initial_date, "Initial progress added when the book was created.")
    
    # Middle progress
    middle_date = initial_date + timedelta(days=15)
    add_progress(book_fantasy, bookworm, 170, middle_date, "The world-building is amazing! Can't stop reading.")
    
    # Final progress
    final_date = datetime.strptime('2025-02-10', '%Y-%m-%d')
    add_progress(book_fantasy, bookworm, 150, final_date, "What a thrilling ending! Definitely one of my favorites this year.")
    book_fantasy.current_page = 400
    
    # 3. Sci-Fi book - in progress, 20 pages from completion
    book_scifi = add_book(
        'The Martian', 
        'Andy Weir', 
        'https://covers.openlibrary.org/b/isbn/9780553418026-L.jpg',
        bookworm, 
        genre='Sci-Fi',
        rating=0, 
        status='In Progress', 
        total_pages=369, 
        is_favorite=False, 
        is_public=False,
        start_date=datetime.strptime('2025-05-01', '%Y-%m-%d')
    )
    # Initial progress
    initial_date = datetime.strptime('2025-05-01', '%Y-%m-%d')
    add_progress(book_scifi, bookworm, 100, initial_date, "Initial progress added when the book was created.")
    
    # Second progress
    second_date = initial_date + timedelta(days=5)
    add_progress(book_scifi, bookworm, 150, second_date, "This is getting interesting! Love the science explanations.")
    
    # Third progress
    third_date = initial_date + timedelta(days=10)
    add_progress(book_scifi, bookworm, 99, third_date, "The humor in this book is fantastic! Almost done.")
    book_scifi.current_page = 349
    
    # 4. Biography book
    book_biography = add_book(
        'Steve Jobs', 
        'Walter Isaacson', 
        'https://covers.openlibrary.org/b/isbn/9781451648539-L.jpg',
        bookworm, 
        genre='Biography',
        rating=3, 
        status='Completed', 
        total_pages=656, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-02-10', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-15', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(book_biography, bookworm, 150, datetime.strptime('2025-02-10', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(book_biography, bookworm, 200, datetime.strptime('2025-02-20', '%Y-%m-%d'), "Such a complex person. Fascinating to learn about his life.")
    add_progress(book_biography, bookworm, 306, datetime.strptime('2025-03-15', '%Y-%m-%d'), "Completed! Insightful but sometimes frustrating biography.")
    book_biography.current_page = 656
    
    # 5. History book
    book_history = add_book(
        'Sapiens: A Brief History of Humankind', 
        'Yuval Noah Harari', 
        'https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg',
        bookworm, 
        genre='History',
        rating=5, 
        status='Completed', 
        total_pages=443, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-03-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-10', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(book_history, bookworm, 100, datetime.strptime('2025-03-20', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(book_history, bookworm, 143, datetime.strptime('2025-03-28', '%Y-%m-%d'), "Mind-blowing concepts about human evolution!")
    add_progress(book_history, bookworm, 200, datetime.strptime('2025-04-10', '%Y-%m-%d'), "Finished and immediately want to read it again. Changed my perspective.")
    book_history.current_page = 443
    
    # 6. Another Fantasy book
    book_fantasy2 = add_book(
        'Six of Crows', 
        'Leigh Bardugo', 
        'https://covers.openlibrary.org/b/isbn/9781627792127-L.jpg',
        bookworm, 
        genre='Fantasy',
        rating=5, 
        status='Completed', 
        total_pages=465, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-04-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-10', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(book_fantasy2, bookworm, 90, datetime.strptime('2025-04-20', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(book_fantasy2, bookworm, 180, datetime.strptime('2025-04-30', '%Y-%m-%d'), "This crew is amazing! The heist planning is so clever.")
    add_progress(book_fantasy2, bookworm, 195, datetime.strptime('2025-05-10', '%Y-%m-%d'), "Finished and immediately ordering the sequel. Best fantasy book this year!")
    book_fantasy2.current_page = 465
    
    # Books for wizardfan - Harry Potter series
    hp1 = add_book(
        'Harry Potter and the Philosopher\'s Stone', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg',
        wizardfan, 
        genre='Fantasy',
        rating=5, 
        status='Completed', 
        total_pages=223, 
        is_favorite=True, 
        is_public=False,
        start_date=datetime.strptime('2025-02-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-01', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(hp1, wizardfan, 75, datetime.strptime('2025-02-20', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(hp1, wizardfan, 148, datetime.strptime('2025-03-01', '%Y-%m-%d'), "Re-reading for the fifth time and still discovering new details!")
    hp1.current_page = 223
    
    hp2 = add_book(
        'Harry Potter and the Chamber of Secrets', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747538486-L.jpg',
        wizardfan, 
        genre='Fantasy',
        rating=4, 
        status='Completed', 
        total_pages=251, 
        is_favorite=False, 
        is_public=False,
        start_date=datetime.strptime('2025-03-05', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-15', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(hp2, wizardfan, 80, datetime.strptime('2025-03-05', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(hp2, wizardfan, 171, datetime.strptime('2025-03-15', '%Y-%m-%d'), "Continuing my re-read marathon. The basilisk scenes are still creepy!")
    hp2.current_page = 251
    
    hp3 = add_book(
        'Harry Potter and the Prisoner of Azkaban', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747546290-L.jpg',
        wizardfan, 
        genre='Fantasy',
        rating=5, 
        status='Completed', 
        total_pages=317, 
        is_favorite=True, 
        is_public=False,
        start_date=datetime.strptime('2025-03-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-05', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(hp3, wizardfan, 100, datetime.strptime('2025-03-20', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(hp3, wizardfan, 217, datetime.strptime('2025-04-05', '%Y-%m-%d'), "My favorite of the series! The time-turner sequence is brilliant writing.")
    hp3.current_page = 317
    
    hp4 = add_book(
        'Harry Potter and the Goblet of Fire', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747550990-L.jpg',
        wizardfan, 
        genre='Fantasy',
        rating=0, 
        status='Completed', 
        total_pages=636, 
        is_favorite=False, 
        is_public=False,
        start_date=datetime.strptime('2025-05-01', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-15', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(hp4, wizardfan, 200, datetime.strptime('2025-05-01', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(hp4, wizardfan, 250, datetime.strptime('2025-05-08', '%Y-%m-%d'), "This is where the series gets darker. The tournament tasks are so exciting!")
    add_progress(hp4, wizardfan, 186, datetime.strptime('2025-05-15', '%Y-%m-%d'), "That ending... even knowing what happens, it still hits hard.")
    hp4.current_page = 636
    
    # Books for scifibro
    scifi1 = add_book(
        'Dune', 
        'Frank Herbert', 
        'https://covers.openlibrary.org/b/isbn/9780441172719-L.jpg',
        scifibro, 
        genre='Sci-Fi',
        rating=5, 
        status='Completed', 
        total_pages=658, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-03-25', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-20', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(scifi1, scifibro, 150, datetime.strptime('2025-03-25', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(scifi1, scifibro, 258, datetime.strptime('2025-04-05', '%Y-%m-%d'), "This is getting interesting! The world-building is unmatched.")
    add_progress(scifi1, scifibro, 250, datetime.strptime('2025-04-20', '%Y-%m-%d'), "Masterpiece! The political intrigue combined with ecological themes is brilliant.")
    scifi1.current_page = 658
    
    scifi2 = add_book(
        'Foundation', 
        'Isaac Asimov', 
        'https://covers.openlibrary.org/b/isbn/9780553293357-L.jpg',
        scifibro, 
        genre='Sci-Fi',
        rating=4, 
        status='Completed', 
        total_pages=244, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-04-25', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-05', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(scifi2, scifibro, 80, datetime.strptime('2025-04-25', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(scifi2, scifibro, 164, datetime.strptime('2025-05-05', '%Y-%m-%d'), "Love how Asimov tackles the concept of psychohistory. Classic sci-fi at its best!")
    scifi2.current_page = 244
    
    scifi3 = add_book(
        'Neuromancer', 
        'William Gibson', 
        'https://covers.openlibrary.org/b/isbn/9780441569595-L.jpg',
        scifibro, 
        genre='Sci-Fi',
        rating=0, 
        status='Completed', 
        total_pages=271, 
        is_favorite=False, 
        is_public=False,
        start_date=datetime.strptime('2025-05-07', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-15', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(scifi3, scifibro, 90, datetime.strptime('2025-05-07', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(scifi3, scifibro, 181, datetime.strptime('2025-05-15', '%Y-%m-%d'), "The cyberpunk genre starts here! Still feels relevant even though it was written in the 80s.")
    scifi3.current_page = 271
    
    # Books for literarylion
    lit1 = add_book(
        'Pride and Prejudice', 
        'Jane Austen', 
        'https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg',
        literarylion, 
        genre='Classic',
        rating=5, 
        status='Completed', 
        total_pages=432, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-04-10', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-30', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(lit1, literarylion, 100, datetime.strptime('2025-04-10', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(lit1, literarylion, 150, datetime.strptime('2025-04-20', '%Y-%m-%d'), "This is getting interesting! Elizabeth and Darcy's relationship is so well-written.")
    add_progress(lit1, literarylion, 182, datetime.strptime('2025-04-30', '%Y-%m-%d'), "Annual re-read complete! Still perfect after all these years.")
    lit1.current_page = 432
    
    lit2 = add_book(
        'Jane Eyre', 
        'Charlotte Brontë', 
        'https://covers.openlibrary.org/b/isbn/9780141441146-L.jpg',
        literarylion, 
        genre='Classic',
        rating=4, 
        status='Completed', 
        total_pages=507, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-03-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-05', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(lit2, literarylion, 150, datetime.strptime('2025-03-15', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(lit2, literarylion, 357, datetime.strptime('2025-04-05', '%Y-%m-%d'), "Jane's independence and moral compass are so inspiring. Beautiful writing.")
    lit2.current_page = 507
    
    lit3 = add_book(
        'The Great Gatsby', 
        'F. Scott Fitzgerald', 
        'https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg',
        literarylion, 
        genre='Classic',
        rating=0, 
        status='Completed', 
        total_pages=180, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-05-05', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-10', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(lit3, literarylion, 50, datetime.strptime('2025-05-05', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(lit3, literarylion, 130, datetime.strptime('2025-05-10', '%Y-%m-%d'), "The symbolism and prose are exquisite. Fitzgerald captured the Jazz Age perfectly.")
    lit3.current_page = 180
    
    # Books for mysterymaven
    mys1 = add_book(
        'The Girl with the Dragon Tattoo', 
        'Stieg Larsson', 
        'https://covers.openlibrary.org/b/isbn/9780307269751-L.jpg',
        mysterymaven, 
        genre='Mystery',
        rating=4, 
        status='Completed', 
        total_pages=672, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-04-25', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-15', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(mys1, mysterymaven, 150, datetime.strptime('2025-04-25', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(mys1, mysterymaven, 252, datetime.strptime('2025-05-05', '%Y-%m-%d'), "This is getting interesting! Lisbeth is such a complex and fascinating character.")
    add_progress(mys1, mysterymaven, 270, datetime.strptime('2025-05-15', '%Y-%m-%d'), "The mystery plot is intricate and kept me guessing. Can't wait to read the sequel!")
    mys1.current_page = 672
    
    mys2 = add_book(
        'Gone Girl', 
        'Gillian Flynn', 
        'https://covers.openlibrary.org/b/isbn/9780307588371-L.jpg',
        mysterymaven, 
        genre='Mystery',
        rating=5, 
        status='Completed', 
        total_pages=432, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-03-10', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-25', '%Y-%m-%d')
    )
    # Add multiple progress entries
    add_progress(mys2, mysterymaven, 100, datetime.strptime('2025-03-10', '%Y-%m-%d'), "Initial progress added when the book was created.")
    add_progress(mys2, mysterymaven, 150, datetime.strptime('2025-03-18', '%Y-%m-%d'), "This is getting interesting! The unreliable narration is brilliantly executed.")
    add_progress(mys2, mysterymaven, 182, datetime.strptime('2025-03-25', '%Y-%m-%d'), "What a twisted psychological thriller. The plot twist floored me!")
    mys2.current_page = 432
    
    # Share wizardfan's books with bookworm
    print("Creating book shares...")
    
    # Function to create a book share
    def share_book(book, shared_with_user):
        book_share = BookShare(
            book_id=book.id,
            shared_with_user_id=shared_with_user.id,
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(book_share)
        return book_share
    
    # Share all wizardfan's books with bookworm
    share_book(hp1, bookworm)
    share_book(hp2, bookworm)
    share_book(hp3, bookworm)
    share_book(hp4, bookworm)
    
    db.session.commit()
    print("Books created successfully")
    print("Reading progress entries created successfully")
    print("Book shares created successfully")
    
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    with application.app_context():
        seed_database()