from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    login = db.Column(db.String(128), unique=True)


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    recipient = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False, server_default=func.now())
    is_read = db.Column(db.Boolean(), nullable=False, default=False)
    content = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.UniqueConstraint(sender, recipient, timestamp),
        db.Index('timestamp_index', timestamp)
    )
