from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, Regexp, Optional


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
    description = StringField(label='Tell about your business in a few words', validators=[Optional(), Length(max=120)])
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




