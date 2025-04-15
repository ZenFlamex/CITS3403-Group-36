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