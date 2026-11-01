from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    DecimalField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange
)
class RegistrationForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")



class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Login")



class DonationForm(FlaskForm):

    amount = DecimalField(
        "Donation Amount",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    submit = SubmitField("Donate")




class CharityForm(FlaskForm):

    name = StringField(
        "Charity Name",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )

    category = StringField(
        "Category",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Charity")