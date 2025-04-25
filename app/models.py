from datetime import datetime
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_authenticated: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    
    # Relationships
    books: so.Mapped[List["Book"]] = so.relationship(back_populates="creator")
    notifications_received: so.Mapped[List["Notification"]] = so.relationship(back_populates="receiver")
    
    def __repr__(self):
        return f'{self.username}'

class Book(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(200), index=True)
    author: so.Mapped[str] = so.mapped_column(sa.String(200), index=True)
    cover_image: so.Mapped[str] = so.mapped_column(sa.String(500))
    creator_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'))
    rating: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    status: so.Mapped[str] = so.mapped_column(sa.String(20))
    current_page: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    total_pages: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    is_favorite: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    start_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True)
    end_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True)
    
    # Relationships
    creator: so.Mapped[User] = so.relationship(back_populates="books")
    
    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

class Notification(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    receiver_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'))
    sender_name: so.Mapped[str] = so.mapped_column(sa.String(64))  # Keep as string for non-user senders (system, etc)
    type: so.Mapped[str] = so.mapped_column(sa.String(20))
    is_read: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    text: so.Mapped[str] = so.mapped_column(sa.String(500))
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.utcnow)
    link: so.Mapped[str] = so.mapped_column(sa.String(200), default='#')
    
    # Relationships
    receiver: so.Mapped[User] = so.relationship(back_populates="notifications_received")
    
    def __repr__(self):
        return f'<Notification {self.id} for {self.receiver_id}>'