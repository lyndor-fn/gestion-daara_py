from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProgressionForm(FlaskForm):
    sourate = StringField("Sourate", validators=[DataRequired(), Length(max=150)])
    nombre_versets = IntegerField(
        "Nombre de versets",
        validators=[DataRequired(), NumberRange(min=0)],
    )
    date_evaluation = DateField("Date d'évaluation", validators=[DataRequired()])
    observations = TextAreaField("Observations", validators=[Optional()])
    talibe_matricule = SelectField("Talibé", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")
