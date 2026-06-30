from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.exceptions import DaaraException, TalibeDejaExistantException, TalibeIntrouvableException
from app.extension import db
from app.forms.talibe import TalibeForm
from app.models.classe import Classe
from app.models.talibe import Talibe
from app.utils.csv_exporter import exporter_csv


bp_talibes = Blueprint("talibes", __name__, url_prefix="/talibes")


def _charger_choix_classes(form):
    form.classe_code.choices = [
        (c.code, c.libelle) for c in Classe.query.order_by(Classe.libelle).all()
    ]


def _query_talibes():
    q = request.args.get("q", "").strip()
    classe_code = request.args.get("classe", "").strip()
    query = Talibe.query
    if classe_code:
        query = query.filter_by(classe_code=classe_code)
    if q:
        query = query.filter(Talibe.nom.ilike(f"%{q}%") | Talibe.prenom.ilike(f"%{q}%"))
    return query.order_by(Talibe.nom), q, classe_code


@bp_talibes.route("/")
def lister():
    query, q, classe_code = _query_talibes()
    classes = Classe.query.order_by(Classe.libelle).all()
    return render_template(
        "talibes/liste.html",
        talibes=query.all(),
        classes=classes,
        q=q,
        classe_code=classe_code,
    )


@bp_talibes.route("/exporter")
def exporter():
    query, _, _ = _query_talibes()
    lignes = [
        [
            t.matricule,
            t.prenom,
            t.nom,
            t.date_naissance.isoformat() if t.date_naissance else "",
            t.classe_code,
        ]
        for t in query.all()
    ]
    return exporter_csv(
        "talibes.csv",
        ["matricule", "prenom", "nom", "dateNaissance", "classe"],
        lignes,
    )


@bp_talibes.route("/nouveau", methods=["GET", "POST"])
def creer():
    form = TalibeForm()
    _charger_choix_classes(form)
    try:
        if form.validate_on_submit():
            if db.session.get(Talibe, form.matricule.data):
                raise TalibeDejaExistantException(form.matricule.data)
            talibe = Talibe(
                matricule=form.matricule.data,
                prenom=form.prenom.data,
                nom=form.nom.data,
                date_naissance=form.date_naissance.data,
                nom_tuteur=form.nom_tuteur.data,
                telephone_tuteur=form.telephone_tuteur.data,
                classe_code=form.classe_code.data,
            )
            db.session.add(talibe)
            db.session.commit()
            flash("Talibé ajouté.", "success")
            return redirect(url_for("talibes.lister"))
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return render_template("talibes/formulaire.html", form=form, talibe=None)


@bp_talibes.route("/<matricule>/modifier", methods=["GET", "POST"])
def modifier(matricule):
    form = TalibeForm()
    _charger_choix_classes(form)
    try:
        talibe = db.session.get(Talibe, matricule)
        if not talibe:
            raise TalibeIntrouvableException(matricule)
        if request.method == "GET":
            form.process(obj=talibe)
        if form.validate_on_submit():
            talibe.prenom = form.prenom.data
            talibe.nom = form.nom.data
            talibe.date_naissance = form.date_naissance.data
            talibe.nom_tuteur = form.nom_tuteur.data
            talibe.telephone_tuteur = form.telephone_tuteur.data
            talibe.classe_code = form.classe_code.data
            db.session.commit()
            flash("Talibé modifié.", "success")
            return redirect(url_for("talibes.lister"))
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
        return redirect(url_for("talibes.lister"))
    return render_template("talibes/formulaire.html", form=form, talibe=talibe)


@bp_talibes.route("/<matricule>/supprimer", methods=["POST"])
def supprimer(matricule):
    try:
        talibe = db.session.get(Talibe, matricule)
        if not talibe:
            raise TalibeIntrouvableException(matricule)
        db.session.delete(talibe)
        db.session.commit()
        flash("Talibé supprimé.", "success")
    except DaaraException as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return redirect(url_for("talibes.lister"))
