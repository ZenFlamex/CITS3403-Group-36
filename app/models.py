from datetime import datetime, timezone
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager

class User(UserMixin,db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    theme: so.Mapped[str] = so.mapped_column(sa.String(10), default='light', nullable=False)
    profile_picture: so.Mapped[str] = so.mapped_column(sa.String(256), default='default_pfp.png')
    join_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now())

    # Relationships
    books: so.Mapped[List["Book"]] = so.relationship(back_populates="creator", cascade="all, delete-orphan")
    notifications_received: so.Mapped[List["Notification"]] = so.relationship(
        "Notification", 
        foreign_keys='Notification.receiver_id',
        back_populates="receiver",
        cascade="all, delete-orphan" 
    )
    
    shares_received_access: so.Mapped[List["BookShare"]] = so.relationship(
        back_populates="shared_with_user",
        cascade="all, delete-orphan" 
    )
    reading_progress: so.Mapped[List["ReadingProgress"]] = so.relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


@login.user_loader
def load_user(id):
   return db.session.get(User, int(id))

class Book(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(200), index=True)
    author: so.Mapped[str] = so.mapped_column(sa.String(200), index=True)
    genre: so.Mapped[str] = so.mapped_column(sa.String(50), default="Other")  # Add genre field
    cover_image: so.Mapped[str] = so.mapped_column(sa.String(500))
    creator_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'))
    rating: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    status: so.Mapped[str] = so.mapped_column(sa.String(20), default="In Progress")
    current_page: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    total_pages: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    is_favorite: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    start_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True)
    end_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True)
    
    # Relationships
    
    creator: so.Mapped["User"] = so.relationship(back_populates="books")
    shares_granted: so.Mapped[List["BookShare"]] = so.relationship(
        back_populates="book",
        cascade="all, delete-orphan" 
    )
    reading_progress: so.Mapped[List["ReadingProgress"]] = so.relationship(
        back_populates="book",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

class Notification(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    receiver_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'))
    sender_name: so.Mapped[str] = so.mapped_column(sa.String(64))  # Keep as string for non-user senders (system, etc)
    type: so.Mapped[str] = so.mapped_column(sa.String(20))
    is_read: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    text: so.Mapped[str] = so.mapped_column(sa.String(500))
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now())
    link: so.Mapped[str] = so.mapped_column(sa.String(200), default='#')
    
    # Relationships
    receiver: so.Mapped[User] = so.relationship(back_populates="notifications_received")
    
    def __repr__(self):
        return f'<Notification {self.id} for {self.receiver_id}>'


class BookShare(db.Model):
    __tablename__ = 'book_shares' 

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    book_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('book.id', ondelete='CASCADE'), index=True)
    shared_with_user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id', ondelete='CASCADE'), index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now())
    book: so.Mapped["Book"] = so.relationship(back_populates="shares_granted")
    shared_with_user: so.Mapped["User"] = so.relationship(back_populates="shares_received_access")

    # Define a unique constraint to ensure that a user can only share a book with another user once
    __table_args__ = (sa.UniqueConstraint('book_id', 'shared_with_user_id', name='uq_book_share'),)

    def __repr__(self):
        return f'<BookShare book_id={self.book_id} user_id={self.shared_with_user_id}>'
    

class ReadingProgress(db.Model):
    __tablename__ = 'reading_progress'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    book_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    pages_read: so.Mapped[int] = so.mapped_column(nullable=False)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.utcnow())

    # Relationships
    book: so.Mapped["Book"] = so.relationship(back_populates="reading_progress")
    user: so.Mapped["User"] = so.relationship(back_populates="reading_progress")

    def __repr__(self):
        return f'<ReadingProgress book_id={self.book_id} user_id={self.user_id} pages_read={self.pages_read}>'