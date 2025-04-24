# CITS3403-Group-36 Book Reading Tracker

## Purpose of the Application

The **Personal Book Reading Tracker** application allows users to track their reading progress, set goals, and analyze reading habits. Users can log book details, track reading sessions, write reviews, and store quotes. The app calculates insightful statistics such as reading pace, monthly progress, and comparisons between different book genres. Additionally, users can make their profiles and books public or private, add friends, and share progress with a private group.

## Key Features

- **Track Book Information**: Add book title, author, genre, and the date you started/finished reading.
- **Log Reading Sessions**: Input the number of pages read and the duration of each reading session.
- **Rating and Review**: Rate books and leave detailed reviews.
- **Reading Goals**: Set personal reading goals for pages, books, or genres to stay motivated.
- **Quotes**: Save memorable quotes from books for later reference.
- **Reading Stats**: Get statistics like average pages read per day, reading speed comparison between fiction and non-fiction, and month-over-month progress.
- **Privacy Settings**: Toggle the visibility of books (public/private) and make your entire account public or private.
- **Share your books to your friends**: Look up friends and share specific books with them

The application also provides insightful statistics such as:

- Average pages read per day.
- Comparison of reading speed between fiction and non-fiction books.
- Progress updates on reading goals, with year-over-year comparisons.

To maintain user privacy, books can be toggled between public and private visibility, and users can make their entire account either public or private. Users can also add friends to share progress and private content with specific groups.

## Design and Use

The design focuses on user-friendliness with a clean, responsive interface. The user can add details about books, track reading sessions, rate books, and save quotes. It offers a dashboard for easy access to reading statistics, monthly progress, and comparisons between genres. Privacy is emphasized with options for toggling book visibility and making accounts public or private. The system supports friend interactions for sharing progress and accessing private content.

## Group Members

| **UWA ID** | **Name**        | **GitHub Username** |
| ---------- | --------------- | ------------------- |
| 23840745   | Alton Wong      | ZenFlamex           |
| 23838888   | Andy Nguyen     | thisisandyn         |
| 23782618   | Jake Blackburne | Jakewidow           |
| 23152493   | Bowen Guo       | breg11              |

1. **Clone the repo**

   ```bash
   git clone https://github.com/ZenFlamex/CITS3403-Group-36.git
   ```

2. **Install dependencies**:
   Ensure you have Python 3.x and `pip` installed on your machine. Then, install the required dependencies by running the following command in the project directory:

   If on windows:

   ```bash
   wsl
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   If on linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set SECRET_KEY in Environemnt**

   ```bash
   SECRET_KEY=your_secure_secret_key
   ```

4. **Setup Datbase**

   ```bash
   flask db upgrade
   ```

5. **\*Seed the Database with Initial Data**

   ```bash
   python seed.py
   ```

6. **Run Flask server using**

   ```bash
   python run.py
   ```

7. **_Open in browser visit http://127.0.0.1:5000 to view homepage_**
