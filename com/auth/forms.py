from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
# import phonenumbers
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp, Optional
from com.models import User


class RegistrationForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('This username already exists')

    def validate_email_address(self, email_to_check):
        check_email = User.query.filter_by(email=email_to_check.data).first()
        if check_email:
            raise ValidationError('This email is already associated with an account')

    username = StringField(label='username', validators=[Length(min=3, max=30), DataRequired()])
    email = StringField(label='e-mail', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password', validators=[Length(8), DataRequired()])
    password2 = PasswordField(label='confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Insert your username', validators=[DataRequired()])
    password = PasswordField(label='Insert your password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(label='insert your e-mail', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Request Password Reset')


class ResetPasswordForm(FlaskForm):
    email = StringField(label='insert your e-mail', validators=[DataRequired(), Email()])
    new_password1 = PasswordField(label='your new password', validators=[DataRequired()])
    new_password2 = PasswordField(label='confirm password', validators=[DataRequired(), EqualTo(new_password1)])
    submit = SubmitField(label='Submit')

# class PhoneForm(FlaskForm):
#     phone = StringField(label='Insert Your Phone Number', validators=[DataRequired()])
#     submit = SubmitField(label='Registrate Your Business Page')
#
#     def validate_phone(self, phone):
#         try:
#             p = phonenumbers.parse(phone.data)
#             if not phonenumbers.is_valid_number(p):
#                 raise ValueError()
#         except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
#             raise ValidationError('Invalid phone number')


