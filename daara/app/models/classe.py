from app.extension import db
from .base import BaseModel


class Classe(BaseModel):
    __tablename__ = "classes"

    code = db.Column(db.String(50), primary_key=True)
    libelle = db.Column(db.String(150), nullable=False)
    niveau = db.Column(db.String(100), nullable=False)
    maitre_matricule = db.Column(
        db.String(50),
        db.ForeignKey("maitres.matricule"),
        nullable=False,
    )

    maitre = db.relationship("Maitre", back_populates="classes")
    talibes = db.relationship("Talibe", back_populates="classe")
