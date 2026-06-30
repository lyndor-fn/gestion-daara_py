from datetime import datetime

from app.extension import db


class BaseModel(db.Model):
    __abstract__ = True

    cree_le = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    maj_le = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
