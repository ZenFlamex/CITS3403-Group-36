from app import db, application
from app.models import User, Book, Notification
from datetime import datetime

def seed_database():
    print("Seeding database...")
    
    # Clear existing data
    Notification.query.delete()
    Book.query.delete()
    User.query.delete()
    db.session.commit()
    
    # Create users - Simulates user signup process
    def create_user(username, email, password):
        """Simulate user creation through signup form"""
        # This would normally include password hashing
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Get ID before committing
        return user
    
    # Main user (logged in) .To simulate logged out make is_authenticated=False
    bookworm = create_user('bookworm', 'bookworm@example.com', 'password123')
    
    # Additional users
    wizardfan01 = create_user('wizardfan01', 'wizardfan01@example.com', 'password456')
    scifibro = create_user('scifibro', 'scifibro@example.com', 'password789')
    readingjourney = create_user('readingjourney', 'readingjourney@example.com', 'passwordabc')
    galactic42 = create_user('galactic42', 'galactic42@example.com', 'passworddef')
    literarylion = create_user('literarylion', 'literarylion@example.com', 'passwordghi')
    
    db.session.commit()
    print("Users created successfully")
    
    # Function to simulate adding a book through a form
    def add_book(title, author, cover_image, creator, rating=0, status="In Progress", 
                 current_page=0, total_pages=0, is_favorite=False, is_public=False,
                 start_date=None, end_date=None):
        """Simulate adding a book through a form submission"""
        book = Book(
            title=title,
            author=author,
            cover_image=cover_image,
            creator_id=creator.id,
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
        return book
    
    # Add books for bookworm user
    add_book(
        'Red Queen', 
        'Victoria Aveyard', 
        'https://covers.openlibrary.org/b/isbn/9780062310637-L.jpg',
        bookworm, 
        rating=5, 
        status='Completed', 
        current_page=400, 
        total_pages=400, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-01-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-02-10', '%Y-%m-%d')
    )
    
    add_book(
        'Glass Sword', 
        'Victoria Aveyard', 
        'https://covers.openlibrary.org/b/isbn/9780062310668-L.jpg',
        bookworm, 
        rating=3, 
        status='Completed', 
        current_page=350, 
        total_pages=350, 
        is_favorite=True, 
        is_public=False,
        start_date=datetime.strptime('2025-02-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-10', '%Y-%m-%d')
    )
    
    add_book(
        'King\'s Cage', 
        'Victoria Aveyard', 
        'https://covers.openlibrary.org/b/isbn/9780062310712-L.jpg',
        bookworm, 
        rating=4, 
        status='Completed', 
        current_page=380, 
        total_pages=380, 
        is_favorite=True, 
        is_public=False,
        start_date=datetime.strptime('2025-03-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-10', '%Y-%m-%d')
    )
    
    add_book(
        'War Storm', 
        'Victoria Aveyard', 
        'https://covers.openlibrary.org/b/isbn/9780062842718-L.jpg',
        bookworm, 
        rating=0,  # Not rated yet
        status='In Progress', 
        current_page=235, 
        total_pages=502, 
        is_favorite=False, 
        is_public=False,
        start_date=datetime.strptime('2025-04-15', '%Y-%m-%d')
    )
    
    add_book(
        'Broken Throne', 
        'Victoria Aveyard', 
        'https://covers.openlibrary.org/b/isbn/9780062423023-L.jpg',
        bookworm, 
        rating=3, 
        status='Completed', 
        current_page=400, 
        total_pages=400, 
        is_favorite=False, 
        is_public=True,
        start_date=datetime.strptime('2025-05-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-06-10', '%Y-%m-%d')
    )
    
    add_book(
        'Cruel Crown', 
        'Victoria Aveyard', 
        'https://covers.openlibrary.org/b/isbn/9780062435347-L.jpg',
        bookworm, 
        rating=2, 
        status='Dropped', 
        current_page=45, 
        total_pages=208, 
        is_favorite=False, 
        is_public=False,
        start_date=datetime.strptime('2025-06-15', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-07-10', '%Y-%m-%d')
    )
    
    # Add books for other users
    add_book(
        'Harry Potter and the Philosopher\'s Stone', 
        'J.K. Rowling', 
        'https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg',
        wizardfan01, 
        rating=5, 
        status='Completed', 
        current_page=223, 
        total_pages=223, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-01-01', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-01-20', '%Y-%m-%d')
    )
    
    add_book(
        'The Martian', 
        'Andy Weir', 
        'https://covers.openlibrary.org/b/isbn/9780804139021-L.jpg',
        scifibro, 
        rating=5, 
        status='Completed', 
        current_page=387, 
        total_pages=387, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-02-01', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-02-20', '%Y-%m-%d')
    )
    
    add_book(
        'The Hunger Games', 
        'Suzanne Collins', 
        'https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg',
        readingjourney, 
        rating=5, 
        status='Completed', 
        current_page=384, 
        total_pages=384, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-03-01', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-03-20', '%Y-%m-%d')
    )
    
    add_book(
        'A Court of Thorns and Roses', 
        'Sarah J. Maas', 
        'https://covers.openlibrary.org/b/isbn/9781619634442-L.jpg',
        galactic42, 
        rating=5, 
        status='Completed', 
        current_page=416, 
        total_pages=416, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-04-01', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-04-20', '%Y-%m-%d')
    )
    
    add_book(
        'Throne of Glass', 
        'Sarah J. Maas', 
        'https://covers.openlibrary.org/b/isbn/9781619630345-L.jpg',
        literarylion, 
        rating=4, 
        status='Completed', 
        current_page=404, 
        total_pages=404, 
        is_favorite=True, 
        is_public=True,
        start_date=datetime.strptime('2025-05-01', '%Y-%m-%d'),
        end_date=datetime.strptime('2025-05-20', '%Y-%m-%d')
    )
    
    db.session.commit()
    print("Books created successfully")
    
    # Function to simulate notification creation
    def create_notification(receiver, sender_name, notification_type, text, timestamp=None, is_read=False, link='#'):
        """Simulate creating a notification as would happen in the application"""
        if timestamp is None:
            timestamp = datetime.utcnow()
            
        notification = Notification(
            receiver_id=receiver.id,
            sender_name=sender_name,
            type=notification_type,
            text=text,
            timestamp=timestamp,
            is_read=is_read,
            link=link
        )
        db.session.add(notification)
        return notification
    
    # Create notifications for bookworm
    create_notification(
        bookworm, 'system', 'goal', 'You updated your annual goal to 50 books!',
        datetime.strptime('2025-04-20 10:00:00', '%Y-%m-%d %H:%M:%S')
    )
    
    create_notification(
        bookworm, 'ZenFlame', 'friend', "added 'Red Queen' to their shelf.",
        datetime.strptime('2025-04-21 09:30:00', '%Y-%m-%d %H:%M:%S')
    )
    
    create_notification(
        bookworm, 'bre', 'comment', "commented on your review of 'War Storm'.",
        datetime.strptime('2025-04-19 15:00:00', '%Y-%m-%d %H:%M:%S'),
        is_read=True
    )
    
    create_notification(
        bookworm, 'Jake', 'friend', "finished reading 'Glass Sword'.",
        datetime.strptime('2025-04-22 14:15:00', '%Y-%m-%d %H:%M:%S')
    )
    
    create_notification(
        bookworm, 'system', 'goal', 'You are halfway towards your reading goal this month!',
        datetime.strptime('2025-04-23 08:00:00', '%Y-%m-%d %H:%M:%S')
    )
    
    create_notification(
        bookworm, 'Andy', 'comment', "replied to your comment on 'King's Cage'.",
        datetime.strptime('2025-04-23 11:20:00', '%Y-%m-%d %H:%M:%S')
    )
    
    create_notification(
        bookworm, 'Sarah', 'friend', "liked your review of 'A Court of Thorns and Roses'.",
        datetime.strptime('2025-04-24 09:00:00', '%Y-%m-%d %H:%M:%S'),
        is_read=True
    )
    
    create_notification(
        bookworm, 'system', 'goal', "You finished reading 5 books this month!",
        datetime.strptime('2025-04-25 10:00:00', '%Y-%m-%d %H:%M:%S')
    )
    
    # Create notifications for wizardfan01
    create_notification(
        wizardfan01, 'admin', 'announcement', 'The site will undergo maintenance early Sunday morning.',
        datetime.strptime('2025-04-22 12:00:00', '%Y-%m-%d %H:%M:%S')
    )
    
    create_notification(
        wizardfan01, 'system', 'welcome', 'Welcome to BookGraph, wizardfan01! Start tracking your reading.',
        datetime.strptime('2025-04-25 11:00:00', '%Y-%m-%d %H:%M:%S')
    )
    
    create_notification(
        wizardfan01, 'bookworm', 'comment', 'commented on your profile.',
        datetime.strptime('2025-04-25 11:30:00', '%Y-%m-%d %H:%M:%S')
    )
    
    db.session.commit()
    print("Notifications created successfully")
    
    print("Database seeding completed successfully")

if __name__ == '__main__':
    with application.app_context():
        seed_database()