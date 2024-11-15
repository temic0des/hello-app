import enum
from typing import Literal

from slugify import slugify
from app import db
from uuid import uuid4
from sqlalchemy.sql import func
from datetime import datetime
import sqlalchemy.orm as so
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Table, Text

ArticleType = Literal["normal", "breaking", "top"]


class Tag(db.Model):
    __tablename__ = "tags"
    id = Column(String, primary_key=True, default=str(uuid4()))
    name: so.Mapped[str] = so.mapped_column(String(255), unique=True, index=True)
    articles: so.WriteOnlyMapped["Article"] = so.relationship(
        secondary="article_tag", back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Article type {self.name}>"


article_tag = Table(
    "article_tag",
    db.metadata,
    Column("article_id", String, ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", String, ForeignKey("tags.id"), primary_key=True),
)


class Article(db.Model):
    __tablename__ = "articles"
    id = Column(String, primary_key=True, default=str(uuid4()))
    title: so.Mapped[str] = so.mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    slug: so.Mapped[str] = so.mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    description: so.Mapped[str] = so.mapped_column(Text, nullable=False)
    image_url: so.Mapped[str] = so.mapped_column(String(255), nullable=True)
    is_published: so.Mapped[bool] = so.mapped_column(Boolean, default=False)
    article_type: so.Mapped[ArticleType] = so.mapped_column(
        Enum("normal", "breaking", "top", name="article_type"),
        default="normal",
        server_default="normal",
    )
    date_published: so.Mapped[datetime] = so.mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_updated: so.Mapped[datetime] = so.mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    source_id: so.Mapped[str] = so.mapped_column(
        ForeignKey("article_sources.id"), index=True, nullable=True
    )
    source = so.relationship("ArticleSource", back_populates="sources")
    user_id: so.Mapped[str] = so.mapped_column(ForeignKey("users.id"))
    author = so.relationship("User", back_populates="articles")
    tags: so.WriteOnlyMapped[Tag] = so.relationship(
        secondary=article_tag,
        primaryjoin=(article_tag.c.article_id == id),
        secondaryjoin=(article_tag.c.article_id == id),
        passive_deletes=True,
        back_populates="articles",
    )

    def __repr__(self) -> str:
        return f"<Article {self.title}>"


class ArticleSource(db.Model):

    __tablename__ = "article_sources"
    id = Column(String, primary_key=True, default=str(uuid4()))
    name: so.Mapped[str] = so.mapped_column(String(255), unique=True)
    link: so.Mapped[str] = so.mapped_column(String, nullable=True)
    sources: so.WriteOnlyMapped[Article] = so.relationship(back_populates="source")
