from app.extension import db
from .base import BaseModel


class Progression(BaseModel):
    __tablename__ = "progressions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sourate = db.Column(db.String(150), nullable=False)
    nombre_versets = db.Column(db.Integer, nullable=False, default=0)
    date_evaluation = db.Column(db.Date, nullable=False)
    observations = db.Column(db.Text)
    talibe_matricule = db.Column(
        db.String(50),
        db.ForeignKey("talibes.matricule"),
        nullable=False,
    )

    talibe = db.relationship("Talibe", back_populates="progressions")
