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


class BusinessForm(FlaskForm):
    business_name = StringField(label='Insert your business name', validators=[DataRequired()])
    category = SelectField(label="Choose your business category", choices=[
        ('accounting_bookkeeping', 'Accounting & Bookkeeping'),
        ('agriculture_farming', 'Agriculture & Farming'),
        ('apparel_fashion', 'Apparel & Fashion'),
        ('auto', 'Auto'),
        ('beauty_personalcare', 'Beauty & Personal Care'),
        ('business_consulting', 'Business Consulting'),
        ('cleaning_services', 'Cleaning Services'),
        ('construction_renovation', 'Construction & Renovation'),
        ('education_training', 'Education & Training'),
        ('entertainment_media', 'Entertainment & Media'),
        ('environmental_services', 'Environmental Services'),
        ('eventplanning_services', 'Event Planning & Services'),
        ('financial_services', 'Financial Services'),
        ('food_beverage', 'Food & Beverage'),
        ('graphicdesign_printing', 'Graphic Design & Printing'),
        ('health_wellness', 'Health & Wellness'),
        ('home_garden', 'Home & Garden'),
        ('hospitality_tourism', 'Hospitality & Tourism'),
        ('humanresources', 'Human Resources'),
        ('informationtechnology', 'Information Technology (IT)'),
        ('insurance_medical_healthcare', 'Insurance, Medical & Healthcare'),  # Fixed here
        ('legal_services', 'Legal Services'),
        ('marketing_advertising', 'Marketing & Advertising'),
        ('nonprofit_philanthropy', 'Nonprofit & Philanthropy'),
        ('photography_videography', 'Photography & Videography'),
        ('realestate', 'Real Estate'),
        ('retail', 'Retail'),
        ('sports_recreation', 'Sports & Recreation'),
        ('technology_software', 'Technology & Software'),
        ('transportation_logistics', 'Transportation & Logistics'),
        ('travel_leisure', 'Travel & Leisure'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = StringField(label='Tell about your business in a few words', validators=[Optional()])
    owner_name = StringField(label='Insert your name as business owner', validators=[DataRequired()])
    phone = StringField(label='Insert your phone number',
                        validators=[Optional(),
                                    Length(min=10, max=13), Regexp(regex='^[+-]?[0-9]+')])
    address = StringField(label='Insert your business address', validators=[Optional(), Length(min=3, max=120)])

    # def validate_address(form, field):
    #    if form.data and (len(form.data) < 3 or len(form.data) > 120):
    #        raise ValidationError('Address must be between 3 and 120 characters long')
    web_page = StringField(label='If you have a web-site, insert the link', validators=[Optional()])
    submit = SubmitField(label='Create your business page')


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


