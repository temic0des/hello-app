from app import db
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from datetime import datetime
import sqlalchemy.orm as so
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text

class ArticleType(db.Model):
    __tablename__ = 'article_types'
    id = Column(String, primary_key=True, default=str(uuid4()))
    name: so.Mapped[str] = so.mapped_column(String(255), unique=True, index=True)

    def __repr__(self) -> str:
        return f'<Article type {self.name}>'


class Article(db.Model):
    __tablename__ = 'articles'
    id = Column(String, primary_key=True, default=str(uuid4()))
    title: so.Mapped[str] = so.mapped_column(String(255), unique=True, index=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(Text, nullable=False)
    image_url: so.Mapped[str] = so.mapped_column(String(255), nullable=True)
    is_published: so.Mapped[bool] = so.mapped_column(Boolean, default=False)
    date_published: so.Mapped[datetime] = so.mapped_column(DateTime(timezone=True), server_default=func.now())
    date_updated: so.Mapped[datetime] = so.mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id: so.Mapped[str] = so.mapped_column(ForeignKey('users.id'), index=True)
    author = so.relationship('User', back_populates='articles')
    

    def __repr__(self) -> str:
        return f'<Article {self.title}>'