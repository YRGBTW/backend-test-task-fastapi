from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.database import Base

# User
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")
    posts = relationship("Post", back_populates="author")

# User roles
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique= True)

    users = relationship("User", back_populates="role")

# Post
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id =  Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")

# Post category
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)

    posts = relationship("Post", back_populates="category")


