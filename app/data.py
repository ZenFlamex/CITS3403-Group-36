# Simulated user data - in a real application this would come from a database
# To simulate logging out, comment out this USER variable or set is_authenticated to False
USER = {

    'username': 'bookworm',
    'email': 'bookworm@example.com',
    'is_authenticated': True
}
# Uncomment this line to simulate being logged out
# USER = None

# If USER is commented out, make sure it exists but is None
try:
    USER
except NameError:
    USER = None

# Consolidated book list with all properties
BOOKS = [
    {
        'title': 'Red Queen',
        'author': 'Victoria Aveyard',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780062310637-L.jpg',
        'creator': 'bookworm',
        'rating': 5,
        'status': 'Completed',
        'current_page': 400,
        'total_pages': 400,
        'is_favorite': True,
        'is_public': True
    },
    {
        'title': 'Glass Sword',
        'author': 'Victoria Aveyard',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780062310668-L.jpg',
        'creator': 'bookworm',
        'rating': 3,
        'status': 'Completed',
        'current_page': 350,
        'total_pages': 350,
        'is_favorite': True,
        'is_public': False
    },
    {
        'title': 'King\'s Cage',
        'author': 'Victoria Aveyard',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780062310712-L.jpg',
        'creator': 'bookworm',
        'rating': 4,
        'status': 'Completed',
        'current_page': 380,
        'total_pages': 380,
        'is_favorite': True,
        'is_public': False
    },
    {
        'title': 'War Storm',
        'author': 'Victoria Aveyard',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780062842718-L.jpg',
        'creator': 'bookworm',
        'rating': 0,  # Not rated yet
        'status': 'In Progress',
        'current_page': 235,
        'total_pages': 502,
        'is_favorite': False,
        'is_public': False
    },
    {
        'title': 'Broken Throne',
        'author': 'Victoria Aveyard',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780062423023-L.jpg',
        'creator': 'bookworm',
        'rating': 3,
        'status': 'Completed',
        'current_page': 400,
        'total_pages': 400,
        'is_favorite': False,
        'is_public': True
    },
    {
        'title': 'Cruel Crown',
        'author': 'Victoria Aveyard',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780062435347-L.jpg',
        'creator': 'bookworm',
        'rating': 2,
        'status': 'Dropped',
        'current_page': 45,
        'total_pages': 208,
        'is_favorite': False,
        'is_public': False
    },
    # Books from other users
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J.K. Rowling',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg',
        'creator': 'wizardfan01',
        'rating': 5,
        'status': 'Completed',
        'current_page': 223,
        'total_pages': 223,
        'is_favorite': True,
        'is_public': True
    },
    {
        'title': 'The Martian',
        'author': 'Andy Weir',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780804139021-L.jpg',
        'creator': 'scifibro',
        'rating': 5,
        'status': 'Completed',
        'current_page': 387,
        'total_pages': 387,
        'is_favorite': True,
        'is_public': True
    },
    {
        'title': 'The Hunger Games',
        'author': 'Suzanne Collins',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg',
        'creator': 'readingjourney',
        'rating': 5,
        'status': 'Completed',
        'current_page': 384,
        'total_pages': 384,
        'is_favorite': True,
        'is_public': True
    },
    {
        'title': 'A Court of Thorns and Roses',
        'author': 'Sarah J. Maas',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9781619634442-L.jpg',
        'creator': 'galactic42',
        'rating': 5,
        'status': 'Completed',
        'current_page': 416,
        'total_pages': 416,
        'is_favorite': True,
        'is_public': True
    },
    {
        'title': 'Throne of Glass',
        'author': 'Sarah J. Maas',
        'cover_image': 'https://covers.openlibrary.org/b/isbn/9781619630345-L.jpg',
        'creator': 'literarylion',
        'rating': 4,
        'status': 'Completed',
        'current_page': 404,
        'total_pages': 404,
        'is_favorite': True,
        'is_public': True
    }
]

NOTIFICATIONS_DATA = [
    {
        'id': 101, 'receiver_username': 'bookworm', 'sender': 'system', 'type': 'goal', 'is_read': False,
        'text': 'You updated your annual goal to 50 books!', 
        'timestamp': '2025-04-20 10:00:00', 'link': '#'
    },
    {
        'id': 102, 'receiver_username': 'bookworm', 'sender': 'ZenFlame', 'type': 'friend', 'is_read': False,
        'text': "added 'Red Queen' to their shelf.", 
        'timestamp': '2025-04-21 09:30:0', 'link': '#'
    },
    {
        'id': 103, 'receiver_username': 'bookworm', 'sender': 'bre', 'type': 'comment', 'is_read': True,
        'text': "commented on your review of 'War Storm'.", 
        'timestamp': '2025-04-19 15:00:00', 'link': '#'
    },
    {
        'id': 104, 'receiver_username': 'bookworm', 'sender': 'Jake', 'type': 'friend', 'is_read': False,
        'text': "finished reading 'Glass Sword'.",
        'timestamp': '2025-04-22 14:15:00', 'link': '#'
    },
    {
        'id': 105, 'receiver_username': 'bookworm', 'sender': 'system', 'type': 'goal', 'is_read': False,
        'text': 'You are halfway towards your reading goal this month!', 
        'timestamp': '2025-04-23 08:00:00', 'link': '#'
    },
    {
        'id': 106, 'receiver_username': 'bookworm', 'sender': 'Andy', 'type': 'comment', 'is_read': False,
        'text': "replied to your comment on 'King's Cage'.",
        'timestamp': '2025-04-23 11:20:00', 'link': '#'
    },
    {
        'id': 107, 'receiver_username': 'bookworm', 'sender': 'Sarah', 'type': 'friend', 'is_read': True,
        'text': "liked your review of 'A Court of Thorns and Roses'.", 
        'timestamp': '2025-04-24 09:00:00', 'link': '#'
    },
    {
        'id': 108, 'receiver_username': 'bookworm', 'sender': 'system', 'type': 'goal', 'is_read': False,
        'text': "You finished reading 5 books this month!", 
        'timestamp': '2025-04-25 10:00:00', 'link': '#'
    },
    {
        'id': 109, 'receiver_username': 'wizardfan01', 'sender': 'admin', 'type': 'announcement', 'is_read': False, 
        'text': 'The site will undergo maintenance early Sunday morning.',
        'timestamp': '2025-04-22 12:00:00', 'link': '#' 
    },
    {
        'id': 111, 'receiver_username': 'wizardfan01', 'sender': 'system', 'type': 'welcome', 'is_read': False, 
        'text': 'Welcome to BookGraph, wizardfan01! Start tracking your reading.',
        'timestamp': '2025-04-25 11:00:00', 'link': '#' 
    },
    {
        'id': 112, 'receiver_username': 'wizardfan01', 'sender': 'bookworm', 'type': 'comment', 'is_read': False, 
        'text': 'commented on your profile.',
        'timestamp': '2025-04-25 11:30:00', 'link': '#'
    }
]
    

