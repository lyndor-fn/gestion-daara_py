from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class TalibeForm(FlaskForm):
    matricule = StringField("Matricule", validators=[DataRequired(), Length(max=50)])
    prenom = StringField("Prénom", validators=[DataRequired(), Length(max=100)])
    nom = StringField("Nom", validators=[DataRequired(), Length(max=100)])
    date_naissance = DateField("Date de naissance", validators=[Optional()])
    nom_tuteur = StringField("Nom du tuteur", validators=[Optional(), Length(max=200)])
    telephone_tuteur = StringField(
        "Téléphone tuteur",
        validators=[Optional(), Length(max=20)],
    )
    classe_code = SelectField("Classe", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")
