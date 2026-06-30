class DaaraException(RuntimeError):
    pass


class MaitreIntrouvableException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Aucun maître pour le matricule : {matricule}")


class MaitreDejaExistantException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Un maître existe déjà avec le matricule : {matricule}")


class ClasseIntrouvableException(DaaraException):
    def __init__(self, code: str):
        super().__init__(f"Aucune classe pour le code : {code}")


class ClasseDejaExistanteException(DaaraException):
    def __init__(self, code: str):
        super().__init__(f"Une classe existe déjà avec le code : {code}")


class TalibeIntrouvableException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Aucun talibé pour le matricule : {matricule}")


class TalibeDejaExistantException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Un talibé existe déjà avec le matricule : {matricule}")


class ProgressionIntrouvableException(DaaraException):
    def __init__(self, progression_id: int):
        super().__init__(f"Aucune progression pour l'identifiant : {progression_id}")


class ProgressionInvalideException(DaaraException):
    def __init__(self, message="Progression invalide."):
        super().__init__(message)


class SuppressionImpossibleException(DaaraException):
    def __init__(self, message="Suppression impossible à cause d'une relation existante."):
        super().__init__(message)
