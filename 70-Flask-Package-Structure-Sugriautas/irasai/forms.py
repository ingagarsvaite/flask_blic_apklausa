from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    SubmitField,
    BooleanField,
    StringField,
    PasswordField,
    TextAreaField,
    EmailField,
)
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from irasai import app
from .models import Vartotojas
import re

# Šis metodas yra skirtas nustatyti, ar slaptažodis, kurį norime įvesti, yra tinkamas (t.y. ar ne per trumpas, ar
# nėra per lengvas
def utility_password_check(password):
    # calculating the length
        length_error = len(password) < 8

        # searching for digits
        digit_error = re.search(r"\d", password) is None

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None

        # searching for symbols
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

        # overall result
        password_ok = not (
            length_error
            or digit_error
            or uppercase_error
            or lowercase_error
            or symbol_error
        )

        return password_ok



class RegistracijosForma(FlaskForm):
    vardas = StringField("Vardas", [DataRequired()])
    el_pastas = EmailField("El.pastas", [DataRequired()])
    slaptazodis = PasswordField("Slaptazodis", [DataRequired()])
    patvirtintas_slaptazodis = PasswordField(
        "Pakartokite slaptazodi",
        [EqualTo("slaptazodis", "Slaptazodis turi but toks pats")],
    )
    submit = SubmitField("Prisiregistruoti")

    def validate_vardas(self, vardas):
        with app.app_context():
            vartotojas = Vartotojas.query.filter_by(vardas=vardas.data).first()
            if vartotojas:
                raise ValidationError("Sis vardas jau yra musu duomenu bazeje")

    def validate_el_pastas(self, el_pastas):
        with app.app_context():
            vartotojas = Vartotojas.query.filter_by(
                el_pastas=el_pastas.data
            ).first()
            if vartotojas:
                raise ValidationError("Sis vardas jau yra musu duomenu bazeje")

    def validate_password(self, slaptazodis):
        tinkamas_slaptazodis = utility_password_check(slaptazodis.data)

        if not tinkamas_slaptazodis:
            raise ValidationError("Slaptazodis netinkamas")


class PaskyrosAtnaujinimoForma(FlaskForm):
    vardas = StringField("Vardas", [DataRequired()])
    el_pastas = EmailField("El.pastas", [DataRequired()])
    nuotrauka = FileField(
        "Atnaujinti profilio nuotrauka",
        validators=[FileAllowed(["jpg", "jpeg", "png"])],
    )
    submit = SubmitField("Atnaujinti")

    def validate_vardas(self, vardas):
        if current_user.vardas != vardas.data:
            with app.app_context():
                vartotojas = Vartotojas.query.filter_by(vardas=vardas.data).first()
                if vartotojas:
                    raise ValidationError("Sis vardas jau yra musu duomenu bazeje")

    def validate_el_pastas(self, el_pastas):
        if current_user.el_pastas != el_pastas.data:
            with app.app_context():
                vartotojas = Vartotojas.query.filter_by(
                    el_pastas=el_pastas.data
                ).first()
                if vartotojas:
                    raise ValidationError("Sis el pastas jau yra musu duomenu bazeje")


class PrisijungimoForma(FlaskForm):
    el_pastas = EmailField("El.pastas", [DataRequired()])
    slaptazodis = PasswordField("Slaptazodis", [DataRequired()])
    prisiminti = BooleanField("Prisiminti mane")
    submit = SubmitField("Prisijungti")


class IrasasForm(FlaskForm):
    irasas = TextAreaField("Irasas", [DataRequired()])
    submit = SubmitField("Prideti irasa")

class UzklausosAtnaujinimoForma(FlaskForm):
    el_pastas = EmailField("El. pastas", validators=[DataRequired()])
    submit = SubmitField("Gauti")

    def validate_el_pastas(self, el_pastas):
        with app.app_context(): # Ne visai grazu, fix #1
            user = Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
            if user is None:
                raise ValidationError("Nera tokios paskyros")

class SlaptazodzioAtnaujinimoForma(FlaskForm):
    slaptazodis = PasswordField("Slaptazodis", [DataRequired()])
    patvirtintas_slaptazodis = PasswordField(
        "Pakartokite slaptazodi",
        [EqualTo("slaptazodis", "Slaptazodis turi but toks pats")],
    )
    submit = SubmitField("Atnaujinti slaptazodi")
