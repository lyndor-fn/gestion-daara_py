from flask import Blueprint, redirect, url_for


bp_main = Blueprint("main", __name__)


@bp_main.route("/")
def accueil():
    return redirect(url_for("talibes.lister"))
