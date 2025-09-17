import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, Enum

db = SQLAlchemy()

# ---- Tablas del Blog StarWars ----

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    posts = db.relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="author", cascade="all, delete-orphan")

class Follower(db.Model):
    """
    Relación de seguidores entre usuarios: user_from sigue a user_to.
    """
    __tablename__ = "follower"
    id = db.Column(db.Integer, primary_key=True)
    user_from_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_to_id   = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_from_id", "user_to_id", name="uq_follow_pair"),)

    user_from = db.relationship("User", foreign_keys=[user_from_id])
    user_to   = db.relationship("User", foreign_keys=[user_to_id])

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(140), nullable=True)
    body  = db.Column(db.Text, nullable=True)

    author = db.relationship("User", back_populates="posts")
    media  = db.relationship("Media", back_populates="post", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="post", cascade="all, delete-orphan")

class MediaType(enum.Enum):
    image = "image"
    video = "video"

class Media(db.Model):
    __tablename__ = "media"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(Enum(MediaType), nullable=False)
    url  = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    post = db.relationship("Post", back_populates="media")

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id   = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    author = db.relationship("User", back_populates="comments")
    post   = db.relationship("Post", back_populates="comments")

# ---- Diagrama (no tocar) ----
# Si tu plantilla incluye render_er, déjalo así:
try:
    from eralchemy2 import render_er
    render_er(db.Model, "diagram.png")
except Exception:
    pass
