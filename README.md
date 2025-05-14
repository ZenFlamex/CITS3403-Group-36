# CITS3403-Group-36 Book Reading Tracker

## Purpose of the Application

**BookCorner** is a comprehensive book tracking application that helps users manage their reading journey. The platform allows users to track book progress, rate books, log reading sessions, and share books with friends. With insightful statistics and visualizations, users can better understand their reading habits and reach meaningful goals.

## Key Features

- **Book Collection Management**: Add books manually or search via OpenLibrary API to maintain your personal library
- **Progress Tracking**: Record current page numbers and completion status (In Progress, Completed, Dropped)
- **Reading Analytics**: View statistics on reading speed, pages read over time, and genre distribution
- **Reading Goals**: Set and track personal reading challenges based on book count or genres
- **User Connectivity**: Add friends and selectively share books and reading progress
- **Privacy Controls**: Toggle visibility settings for individual books and profile information
- **Book Details**: Store ratings, reviews, and completion dates for each book
- **User Experience**: Toggle between light/dark themes and customize profile settings
- **Book Discovery**: See what friends are reading and explore public shelves

The application provides valuable insights including:

- Visual representations of reading progress over time
- Achievement tracking for completed reading goals and milestones

BookCorner prioritizes user privacy with granular controls for sharing settings. Books can be marked as public or private individually, and users can also choose selected readers to share books with them privately.


## Design and Use

The design focuses on user-friendliness with a clean, responsive interface. The user can add details about books, track reading sessions, rate books, and save quotes. It offers a dashboard for easy access to reading statistics, customizable profile and interactive book details to track your books. Privacy is emphasized with options for toggling book visibility and making accounts public or private. The system supports selective user selection for sharing progress and accessing private content.

## Group Members

| **UWA ID** | **Name**        | **GitHub Username** |
| ---------- | --------------- | ------------------- |
| 23840745   | Alton Wong      | ZenFlamex           |
| 23838888   | Andy Nguyen     | thisisandyn         |
| 23782618   | Jake Blackburne | Jakewidow           |
| 23152493   | Bowen Guo       | breg11              |


## How to run the website
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

3. **Set SECRET_KEY in Environment**

   ```bash
   SECRET_KEY=your_secure_secret_key
   ```

4. **Setup Database**

   ```bash
   flask db upgrade
   ```

5. **Seed the Database with Initial Data**

   ```bash
   python seed.py
   ```

6. **Run Flask server using**

   ```bash
   python run.py
   ```

7. **_Open in browser visit http://127.0.0.1:5000 to view homepage_**




## How to run test

Make sure you are in venv then run 
```
python -m unittest discover tests
```


## Credits and Tools Used

The development of **BookCorner** was supported with the help of the following AI-powered tools:

- ChatGPT by OpenAI
- Claude by Anthropic
- GitHub Copilot

These tools were used as coding assistants, while all design, logic, and implementation choices were made by Group 36.

