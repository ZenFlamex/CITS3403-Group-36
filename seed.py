from app import db, application
from app.models import User, Book, ReadingProgress
from datetime import datetime, timezone

def seed_database():
    print("Seeding database...")
    
    # Clear existing data in reverse dependency order
    print("Clearing existing data...")
    ReadingProgress.query.delete()
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
        'passwordabc',  # Updated password for wizardfan
        datetime.strptime('2025-02-15 14:30:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    scifibro = create_user(
        'scifibro', 
        'scifibro@example.com', 
        'simple123',  # Simple password
        datetime.strptime('2025-03-20 09:15:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    literarylion = create_user(
        'literarylion', 
        'literarylion@example.com', 
        'simple123',  # Simple password
        datetime.strptime('2025-04-05 16:45:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    mysterymaven = create_user(
        'mysterymaven', 
        'mysterymaven@example.com', 
        'simple123',  # Simple password
        datetime.strptime('2025-04-20 10:30:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    )
    
    db.session.commit()
    print("Users created successfully")
    
    # Function to add books
    def add_book(title, author, cover_image, creator, genre, rating=0, status="In Progress", 
                current_page=0, total_pages=0, is_favorite=False, is_public=False,
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
            current_page=current_page,
            total_pages=total_pages,
            is_favorite=is_favorite,
            is_public=is_public,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(book)
        db.session.flush()
        return book
    
    print("Creating books...")
    
    # Books for bookworm - one for each genre as specified
    # 1. Fiction book
    book_fiction = add_book(
        'To Kill a Mockingbird', 
        'Harper Lee', 
        'https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg',
        bookworm, 
        genre='Fiction',
        rating=4, 
        status='Completed', 
        current_page=281, 
        total_pages=281, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-01-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-02-05', '%Y-%m-%d')
    )
    
    # 2. Fantasy book
    book_fantasy = add_book(
        'Red Queen', 
        'Victoria Aveyard', 
        'https://covers.openlibrary.org/b/isbn/9780062310637-L.jpg',
        bookworm, 
        genre='Fantasy',
        rating=5, 
        status='Completed', 
        current_page=400, 
        total_pages=400, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-01-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-02-10', '%Y-%m-%d')
    )
    
    # 3. Sci-Fi book - in progress, 20 pages from completion
    book_scifi = add_book(
        'The Martian', 
        'Andy Weir', 
        'https://covers.openlibrary.org/b/isbn/9780553418026-L.jpg',
        bookworm, 
        genre='Sci-Fi',
        rating=0, 
        status='In Progress', 
        current_page=349, 
        total_pages=369,  # 20 pages from completion
        is_favorite=False, 
        is_public=False,
        start_date=datetime.strptime('2025-05-01', '%Y-%m-%d')
    )
    
    # 4. Biography book
    book_biography = add_book(
        'Steve Jobs', 
        'Walter Isaacson', 
        'https://covers.openlibrary.org/b/isbn/9781451648539-L.jpg',
        bookworm, 
        genre='Biography',
        rating=3, 
        status='Completed', 
        current_page=656, 
        total_pages=656, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-02-10', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-15', '%Y-%m-%d')
    )
    
    # 5. History book
    book_history = add_book(
        'Sapiens: A Brief History of Humankind', 
        'Yuval Noah Harari', 
        'https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg',
        bookworm, 
        genre='History',
        rating=5, 
        status='Completed', 
        current_page=443, 
        total_pages=443, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-03-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-10', '%Y-%m-%d')
    )
    
    # 6. Another Fantasy book
    book_fantasy2 = add_book(
        'Six of Crows', 
        'Leigh Bardugo', 
        'https://covers.openlibrary.org/b/isbn/9781627792127-L.jpg',
        bookworm, 
        genre='Fantasy',
        rating=5, 
        status='Completed', 
        current_page=465, 
        total_pages=465, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-04-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-10', '%Y-%m-%d')
    )
    
    # Books for wizardfan - Harry Potter series
    hp1 = add_book(
        'Harry Potter and the Philosopher\'s Stone', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg',
        wizardfan, 
        genre='Fantasy',
        rating=5, 
        status='Completed', 
        current_page=223, 
        total_pages=223, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-02-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-01', '%Y-%m-%d')
    )
    
    hp2 = add_book(
        'Harry Potter and the Chamber of Secrets', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747538486-L.jpg',
        wizardfan, 
        genre='Fantasy',
        rating=4, 
        status='Completed', 
        current_page=251, 
        total_pages=251, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-03-05', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-15', '%Y-%m-%d')
    )
    
    hp3 = add_book(
        'Harry Potter and the Prisoner of Azkaban', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747546290-L.jpg',
        wizardfan, 
        genre='Fantasy',
        rating=5, 
        status='Completed', 
        current_page=317, 
        total_pages=317, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-03-20', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-05', '%Y-%m-%d')
    )
    
    hp4 = add_book(
        'Harry Potter and the Goblet of Fire', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747550990-L.jpg',
        wizardfan, 
        genre='Fantasy',
        rating=0, 
        status='In Progress', 
        current_page=300, 
        total_pages=636, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-05-01', '%Y-%m-%d')
    )
    
    # Books for scifibro
    scifi1 = add_book(
        'Dune', 
        'Frank Herbert', 
        'https://covers.openlibrary.org/b/isbn/9780441172719-L.jpg',
        scifibro, 
        genre='Sci-Fi',
        rating=5, 
        status='Completed', 
        current_page=658, 
        total_pages=658, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-03-25', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-20', '%Y-%m-%d')
    )
    
    scifi2 = add_book(
        'Foundation', 
        'Isaac Asimov', 
        'https://covers.openlibrary.org/b/isbn/9780553293357-L.jpg',
        scifibro, 
        genre='Sci-Fi',
        rating=4, 
        status='Completed', 
        current_page=244, 
        total_pages=244, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-04-25', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-05', '%Y-%m-%d')
    )
    
    scifi3 = add_book(
        'Neuromancer', 
        'William Gibson', 
        'https://covers.openlibrary.org/b/isbn/9780441569595-L.jpg',
        scifibro, 
        genre='Sci-Fi',
        rating=0, 
        status='In Progress', 
        current_page=150, 
        total_pages=271, 
        is_favorite=False, 
        is_public=False,
        start_date=datetime.strptime('2025-05-07', '%Y-%m-%d')
    )
    
    # Books for literarylion
    lit1 = add_book(
        'Pride and Prejudice', 
        'Jane Austen', 
        'https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg',
        literarylion, 
        genre='Classic',
        rating=5, 
        status='Completed', 
        current_page=432, 
        total_pages=432, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-04-10', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-30', '%Y-%m-%d')
    )
    
    lit2 = add_book(
        'Jane Eyre', 
        'Charlotte Brontë', 
        'https://covers.openlibrary.org/b/isbn/9780141441146-L.jpg',
        literarylion, 
        genre='Classic',
        rating=4, 
        status='Completed', 
        current_page=507, 
        total_pages=507, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-03-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-05', '%Y-%m-%d')
    )
    
    lit3 = add_book(
        'The Great Gatsby', 
        'F. Scott Fitzgerald', 
        'https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg',
        literarylion, 
        genre='Classic',
        rating=0, 
        status='In Progress', 
        current_page=100, 
        total_pages=180, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-05-05', '%Y-%m-%d')
    )
    
    # Books for mysterymaven
    mys1 = add_book(
        'The Girl with the Dragon Tattoo', 
        'Stieg Larsson', 
        'https://covers.openlibrary.org/b/isbn/9780307269751-L.jpg',
        mysterymaven, 
        genre='Mystery',
        rating=4, 
        status='Completed', 
        current_page=672, 
        total_pages=672, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-04-25', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-15', '%Y-%m-%d')
    )
    
    mys2 = add_book(
        'Gone Girl', 
        'Gillian Flynn', 
        'https://covers.openlibrary.org/b/isbn/9780307588371-L.jpg',
        mysterymaven, 
        genre='Mystery',
        rating=5, 
        status='Completed', 
        current_page=432, 
        total_pages=432, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-03-10', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-25', '%Y-%m-%d')
    )
    
    db.session.commit()
    print("Books created successfully")
    
    # Add reading progress data for milestone tracking
    print("Creating reading progress entries...")
    
    def add_progress(book, user, pages_read, notes=""):
        progress = ReadingProgress(
            book_id=book.id,
            user_id=user.id,
            pages_read=pages_read,
            notes=notes
        )
        db.session.add(progress)
        return progress
    
    # Add reading progress entries for bookworm
    # Fiction book
    add_progress(book_fiction, bookworm, 100, "Classic literature at its best")
    add_progress(book_fiction, bookworm, 181, "Finished this masterpiece")
    
    # Fantasy book (Red Queen)
    add_progress(book_fantasy, bookworm, 150, "Great start to the series!")
    add_progress(book_fantasy, bookworm, 250, "Plot is getting interesting")
    add_progress(book_fantasy, bookworm, 400, "Finished the book!")
    
    # Sci-Fi book (The Martian)
    add_progress(book_scifi, bookworm, 150, "Fascinating survival story on Mars")
    add_progress(book_scifi, bookworm, 349, "Almost done! Can't wait to finish it")
    
    # Biography book
    add_progress(book_biography, bookworm, 200, "Interesting insights into Jobs' life")
    add_progress(book_biography, bookworm, 400, "Learning a lot about Apple's history")
    add_progress(book_biography, bookworm, 656, "Completed the biography")
    
    # History book
    add_progress(book_history, bookworm, 150, "Fascinating perspective on human history")
    add_progress(book_history, bookworm, 300, "The agricultural revolution chapter was eye-opening")
    add_progress(book_history, bookworm, 443, "Finished! One of my favorite non-fiction books")
    
    # Another Fantasy book (Six of Crows)
    add_progress(book_fantasy2, bookworm, 200, "Great characters and world-building")
    add_progress(book_fantasy2, bookworm, 465, "Finished! Can't wait to read the sequel")
    
    # Reading progress for wizardfan
    # HP1 (223 total pages, current page 223)
    add_progress(hp1, wizardfan, 100, "Magical start to the series!")
    add_progress(hp1, wizardfan, 123, "Finished the first book, amazing!")
    
    # HP2 (251 total pages, current page 251)
    add_progress(hp2, wizardfan, 125, "The mystery deepens!")
    add_progress(hp2, wizardfan, 126, "Finished book 2, even better than the first")
    
    # HP3 (317 total pages, current page 317)
    add_progress(hp3, wizardfan, 150, "Love the time-turner plot!")
    add_progress(hp3, wizardfan, 167, "My favorite book in the series so far")
    
    # HP4 (636 total pages, current page 300)
    add_progress(hp4, wizardfan, 150, "The Triwizard Tournament is exciting")
    add_progress(hp4, wizardfan, 150, "The tournament continues to amaze")
    
    # Reading progress for scifibro
    # Dune (658 total pages, current page 658)
    add_progress(scifi1, scifibro, 300, "Epic worldbuilding")
    add_progress(scifi1, scifibro, 358, "Masterpiece of science fiction")
    
    # Foundation (244 total pages, current page 244)
    add_progress(scifi2, scifibro, 120, "Asimov's vision is incredible")
    add_progress(scifi2, scifibro, 124, "Completed the first Foundation book")
    
    # Neuromancer (271 total pages, current page 150)
    add_progress(scifi3, scifibro, 75, "Cyberpunk at its best")
    add_progress(scifi3, scifibro, 75, "Diving deeper into the matrix")
    
    # Reading progress for literarylion
    # Pride and Prejudice (432 total pages, current page 432)
    add_progress(lit1, literarylion, 200, "Elizabeth and Darcy's relationship is fascinating")
    add_progress(lit1, literarylion, 232, "A perfect romance novel")
    
    # Jane Eyre (507 total pages, current page 507)
    add_progress(lit2, literarylion, 250, "Jane's childhood is heartbreaking")
    add_progress(lit2, literarylion, 257, "Such a powerful female protagonist")
    
    # The Great Gatsby (180 total pages, current page 100)
    add_progress(lit3, literarylion, 50, "Gatsby's parties are something else")
    add_progress(lit3, literarylion, 50, "The symbolism is incredible")
    
    # Reading progress for mysterymaven
    # The Girl with the Dragon Tattoo (672 total pages, current page 672)
    add_progress(mys1, mysterymaven, 350, "Lisbeth Salander is such a complex character")
    add_progress(mys1, mysterymaven, 322, "Brilliant mystery, can't wait to read the next one")
    
    # Gone Girl (432 total pages, current page 432)
    add_progress(mys2, mysterymaven, 200, "So many twists already!")
    add_progress(mys2, mysterymaven, 232, "That ending was shocking!")
    
    db.session.commit()
    print("Reading progress entries created successfully")
    
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    with application.app_context():
        seed_database()