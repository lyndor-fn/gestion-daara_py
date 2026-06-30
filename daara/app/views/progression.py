from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.exceptions import DaaraException, ProgressionIntrouvableException, ProgressionInvalideException
from app.extension import db
from app.forms.progression import ProgressionForm
from app.models.progression import Progression
from app.models.talibe import Talibe
from app.utils.csv_exporter import exporter_csv


bp_progressions = Blueprint("progressions", __name__, url_prefix="/progressions")


def _charger_choix_talibes(form):
    form.talibe_matricule.choices = [
        (t.matricule, f"{t.prenom} {t.nom}") for t in Talibe.query.order_by(Talibe.nom).all()
    ]


def _query_progressions():
    q = request.args.get("q", "").strip()
    talibe_matricule = request.args.get("talibe", "").strip()
    query = Progression.query
    if talibe_matricule:
        query = query.filter_by(talibe_matricule=talibe_matricule)
    if q:
        query = query.filter(Progression.sourate.ilike(f"%{q}%"))
    return query.order_by(Progression.date_evaluation.desc()), q, talibe_matricule


def _valider_progression(form):
    if not form.sourate.data or not form.sourate.data.strip():
        raise ProgressionInvalideException("Progression invalide : sourate obligatoire.")
    if form.nombre_versets.data is None or form.nombre_versets.data < 0:
        raise ProgressionInvalideException(
            "Progression invalide : le nombre de versets doit être positif ou nul."
        )
    if not form.talibe_matricule.data:
        raise ProgressionInvalideException("Progression invalide : talibé obligatoire.")


@bp_progressions.route("/")
def lister():
    query, q, talibe_matricule = _query_progressions()
    talibes = Talibe.query.order_by(Talibe.nom).all()
    return render_template(
        "progressions/liste.html",
        progressions=query.all(),
        talibes=talibes,
        q=q,
        talibe_matricule=talibe_matricule,
    )


@bp_progressions.route("/exporter")
def exporter():
    query, _, _ = _query_progressions()
    lignes = [
        [
            p.id,
            p.talibe_matricule,
            p.sourate,
            p.nombre_versets,
            p.date_evaluation.isoformat() if p.date_evaluation else "",
            p.observations or "",
        ]
        for p in query.all()
    ]
    return exporter_csv(
        "progressions.csv",
        ["id", "talibe", "sourate", "nombreVersets", "dateEvaluation", "observations"],
        lignes,
    )


@bp_progressions.route("/nouveau", methods=["GET", "POST"])
def creer():
    form = ProgressionForm()
    _charger_choix_talibes(form)
    try:
        if form.validate_on_submit():
            _valider_progression(form)
            progression = Progression(
                sourate=form.sourate.data.strip(),
                nombre_versets=form.nombre_versets.data,
                date_evaluation=form.date_evaluation.data,
                observations=form.observations.data,
                talibe_matricule=form.talibe_matricule.data,
            )
            db.session.add(progression)
            db.session.commit()
            flash("Progression ajoutée.", "success")
            return redirect(url_for("progressions.lister"))
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return render_template("progressions/formulaire.html", form=form, progression=None)


@bp_progressions.route("/<int:progression_id>/modifier", methods=["GET", "POST"])
def modifier(progression_id):
    form = ProgressionForm()
    _charger_choix_talibes(form)
    try:
        progression = db.session.get(Progression, progression_id)
        if not progression:
            raise ProgressionIntrouvableException(progression_id)
        if request.method == "GET":
            form.process(obj=progression)
        if form.validate_on_submit():
            _valider_progression(form)
            progression.sourate = form.sourate.data.strip()
            progression.nombre_versets = form.nombre_versets.data
            progression.date_evaluation = form.date_evaluation.data
            progression.observations = form.observations.data
            progression.talibe_matricule = form.talibe_matricule.data
            db.session.commit()
            flash("Progression modifiée.", "success")
            return redirect(url_for("progressions.lister"))
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
        return redirect(url_for("progressions.lister"))
    return render_template("progressions/formulaire.html", form=form, progression=progression)


@bp_progressions.route("/<int:progression_id>/supprimer", methods=["POST"])
def supprimer(progression_id):
    try:
        progression = db.session.get(Progression, progression_id)
        if not progression:
            raise ProgressionIntrouvableException(progression_id)
        db.session.delete(progression)
        db.session.commit()
        flash("Progression supprimée.", "success")
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return redirect(url_for("progressions.lister"))
