from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ClasseForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired(), Length(max=50)])
    libelle = StringField("Libellé", validators=[DataRequired(), Length(max=150)])
    niveau = StringField("Niveau", validators=[DataRequired(), Length(max=100)])
    maitre_matricule = SelectField("Maître", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")
