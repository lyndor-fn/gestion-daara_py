from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.exceptions import (
    DaaraException,
    MaitreDejaExistantException,
    MaitreIntrouvableException,
    SuppressionImpossibleException,
)
from app.extension import db
from app.forms.maitre import MaitreForm
from app.models.maitre import Maitre
from app.utils.csv_exporter import exporter_csv


bp_maitres = Blueprint("maitres", __name__, url_prefix="/maitres")


def _query_maitres():
    q = request.args.get("q", "").strip()
    query = Maitre.query
    if q:
        query = query.filter(Maitre.nom.ilike(f"%{q}%") | Maitre.prenom.ilike(f"%{q}%"))
    return query.order_by(Maitre.nom), q


@bp_maitres.route("/")
def lister():
    query, q = _query_maitres()
    return render_template("maitres/liste.html", maitres=query.all(), q=q)


@bp_maitres.route("/exporter")
def exporter():
    query, _ = _query_maitres()
    lignes = [
        [m.matricule, m.prenom, m.nom, m.telephone or ""]
        for m in query.all()
    ]
    return exporter_csv("maitres.csv", ["matricule", "prenom", "nom", "telephone"], lignes)


@bp_maitres.route("/nouveau", methods=["GET", "POST"])
def creer():
    form = MaitreForm()
    try:
        if form.validate_on_submit():
            if db.session.get(Maitre, form.matricule.data):
                raise MaitreDejaExistantException(form.matricule.data)
            maitre = Maitre(
                matricule=form.matricule.data,
                prenom=form.prenom.data,
                nom=form.nom.data,
                telephone=form.telephone.data,
            )
            db.session.add(maitre)
            db.session.commit()
            flash("Maître ajouté.", "success")
            return redirect(url_for("maitres.lister"))
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return render_template("maitres/formulaire.html", form=form, maitre=None)


@bp_maitres.route("/<matricule>/modifier", methods=["GET", "POST"])
def modifier(matricule):
    form = MaitreForm()
    try:
        maitre = db.session.get(Maitre, matricule)
        if not maitre:
            raise MaitreIntrouvableException(matricule)
        if request.method == "GET":
            form.process(obj=maitre)
        if form.validate_on_submit():
            maitre.prenom = form.prenom.data
            maitre.nom = form.nom.data
            maitre.telephone = form.telephone.data
            db.session.commit()
            flash("Maître modifié.", "success")
            return redirect(url_for("maitres.lister"))
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
        return redirect(url_for("maitres.lister"))
    return render_template("maitres/formulaire.html", form=form, maitre=maitre)


@bp_maitres.route("/<matricule>/supprimer", methods=["POST"])
def supprimer(matricule):
    try:
        maitre = db.session.get(Maitre, matricule)
        if not maitre:
            raise MaitreIntrouvableException(matricule)
        if maitre.classes:
            raise SuppressionImpossibleException(
                "Suppression impossible : ce maître encadre au moins une classe."
            )
        db.session.delete(maitre)
        db.session.commit()
        flash("Maître supprimé.", "success")
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return redirect(url_for("maitres.lister"))
