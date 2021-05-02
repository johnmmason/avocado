from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class submitInsertForm(FlaskForm):
    job_type = StringField('Job Type')
    week_id = StringField('Week Id')
    week = StringField('Week (mm/dd/yy)')
    price = StringField('Price')
    volume = StringField('Volume')
    total_4046 = StringField('Total 4046')
    total_4225 = StringField('Total 4225')
    total_4770 = StringField('Total 4770')
    category = StringField('Category')
    year = StringField('Year')
    region = StringField('Region')
    submit = SubmitField('Submit')

class submitUpdateForm(FlaskForm):
    job_type = StringField('Job Type')
    week_id = StringField('Week Id')
    week = StringField('Week (mm/dd/yy)')
    price = StringField('Price')
    volume = StringField('Volume')
    total_4046 = StringField('Total 4046')
    total_4225 = StringField('Total 4225')
    total_4770 = StringField('Total 4770')
    category = StringField('Category')
    year = StringField('Year')
    region = StringField('Region')
    submit = SubmitField('Submit')

class submitQueryForm(FlaskForm):
    job_type = StringField('Job Type')
    week_id = StringField('Week Id')
    week = StringField('Week (mm/dd/yy)')
    price = StringField('Price')
    volume = StringField('Volume')
    total_4046 = StringField('Total 4046')
    total_4225 = StringField('Total 4225')
    total_4770 = StringField('Total 4770')
    category = StringField('Category')
    year = StringField('Year')
    region = StringField('Region')
    submit = SubmitField('Submit')

class submitDeleteForm(FlaskForm):
    job_type = StringField('Job Type')
    week_id = StringField('Week Id')
    week = StringField('Week (mm/dd/yy)')
    price = StringField('Price')
    volume = StringField('Volume')
    total_4046 = StringField('Total 4046')
    total_4225 = StringField('Total 4225')
    total_4770 = StringField('Total 4770')
    category = StringField('Category')
    year = StringField('Year')
    region = StringField('Region')
    submit = SubmitField('Submit')
