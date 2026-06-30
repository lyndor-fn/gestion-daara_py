from app.extension import db
from .base import BaseModel


class Maitre(BaseModel):
    __tablename__ = "maitres"

    matricule = db.Column(db.String(50), primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))

    classes = db.relationship("Classe", back_populates="maitre")

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
