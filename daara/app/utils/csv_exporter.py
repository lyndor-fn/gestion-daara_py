import csv
import io

from flask import make_response


def exporter_csv(nom_fichier: str, entetes: list, lignes: list):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(entetes)
    for ligne in lignes:
        writer.writerow(ligne)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={nom_fichier}"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    return response
