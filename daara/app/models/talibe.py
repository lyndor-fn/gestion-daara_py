from app.extension import db
from .base import BaseModel


class Talibe(BaseModel):
    __tablename__ = "talibes"

    matricule = db.Column(db.String(50), primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date)
    nom_tuteur = db.Column(db.String(200))
    telephone_tuteur = db.Column(db.String(20))
    classe_code = db.Column(
        db.String(50),
        db.ForeignKey("classes.code"),
        nullable=False,
    )

    classe = db.relationship("Classe", back_populates="talibes")
    progressions = db.relationship(
        "Progression",
        back_populates="talibe",
        cascade="all, delete-orphan",
    )

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
