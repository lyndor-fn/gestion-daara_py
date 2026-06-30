from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.exceptions import (
    ClasseDejaExistanteException,
    ClasseIntrouvableException,
    DaaraException,
    SuppressionImpossibleException,
)
from app.extension import db
from app.forms.classe import ClasseForm
from app.models.classe import Classe
from app.models.maitre import Maitre
from app.utils.csv_exporter import exporter_csv


bp_classes = Blueprint("classes", __name__, url_prefix="/classes")


def _charger_choix_maitres(form):
    form.maitre_matricule.choices = [
        (m.matricule, f"{m.prenom} {m.nom}") for m in Maitre.query.order_by(Maitre.nom).all()
    ]


def _query_classes():
    q = request.args.get("q", "").strip()
    query = Classe.query
    if q:
        query = query.filter(Classe.libelle.ilike(f"%{q}%") | Classe.niveau.ilike(f"%{q}%"))
    return query.order_by(Classe.libelle), q


@bp_classes.route("/")
def lister():
    query, q = _query_classes()
    return render_template("classes/liste.html", classes=query.all(), q=q)


@bp_classes.route("/exporter")
def exporter():
    query, _ = _query_classes()
    lignes = [
        [c.code, c.libelle, c.niveau, c.maitre_matricule]
        for c in query.all()
    ]
    return exporter_csv("classes.csv", ["code", "libelle", "niveau", "maitre"], lignes)


@bp_classes.route("/nouveau", methods=["GET", "POST"])
def creer():
    form = ClasseForm()
    _charger_choix_maitres(form)
    try:
        if form.validate_on_submit():
            if db.session.get(Classe, form.code.data):
                raise ClasseDejaExistanteException(form.code.data)
            classe = Classe(
                code=form.code.data,
                libelle=form.libelle.data,
                niveau=form.niveau.data,
                maitre_matricule=form.maitre_matricule.data,
            )
            db.session.add(classe)
            db.session.commit()
            flash("Classe ajoutée.", "success")
            return redirect(url_for("classes.lister"))
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return render_template("classes/formulaire.html", form=form, classe=None)


@bp_classes.route("/<code>/modifier", methods=["GET", "POST"])
def modifier(code):
    form = ClasseForm()
    _charger_choix_maitres(form)
    try:
        classe = db.session.get(Classe, code)
        if not classe:
            raise ClasseIntrouvableException(code)
        if request.method == "GET":
            form.process(obj=classe)
        if form.validate_on_submit():
            classe.libelle = form.libelle.data
            classe.niveau = form.niveau.data
            classe.maitre_matricule = form.maitre_matricule.data
            db.session.commit()
            flash("Classe modifiée.", "success")
            return redirect(url_for("classes.lister"))
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
        return redirect(url_for("classes.lister"))
    return render_template("classes/formulaire.html", form=form, classe=classe)


@bp_classes.route("/<code>/supprimer", methods=["POST"])
def supprimer(code):
    try:
        classe = db.session.get(Classe, code)
        if not classe:
            raise ClasseIntrouvableException(code)
        if classe.talibes:
            raise SuppressionImpossibleException(
                "Suppression impossible : cette classe contient au moins un talibé."
            )
        db.session.delete(classe)
        db.session.commit()
        flash("Classe supprimée.", "success")
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return redirect(url_for("classes.lister"))
