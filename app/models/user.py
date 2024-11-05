from datetime import datetime
from typing import Optional
from app import db, login
from flask_login import UserMixin
from sqlalchemy import DateTime, String, Column, func
from uuid import uuid4
import sqlalchemy.orm as so

from werkzeug.security import generate_password_hash, check_password_hash

from app.models.article import Article

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=str(uuid4))
    email: so.Mapped[str] = so.mapped_column(String(255), index=True, unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(String(256))
    date_created: so.Mapped[datetime] = so.mapped_column(DateTime(timezone=True), server_default=func.now())
    articles: so.WriteOnlyMapped[Article] = so.relationship(
        back_populates='author')
    

    def __repr__(self) -> str:
        return f'<User {self.email}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(password=password, pwhash=self.password)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, str(id))