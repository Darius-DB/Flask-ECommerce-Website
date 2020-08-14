from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddItemForm(FlaskForm):
    category = StringField('Add Category', validators=[DataRequired()])
    sub_category = StringField('Add SubCategory', validators=[DataRequired()])
    title = StringField('Add Title', validators=[DataRequired()])
    price = IntegerField('Add Price', validators=[DataRequired()])
    stock = IntegerField('Add Stock', validators=[DataRequired()])
    description = TextAreaField('Add Description', validators=[DataRequired()])
    size = SelectField('Add Size',
                       choices=[
                           ('XS', 'XS'),
                           ('S', 'S'),
                           ('M', 'M'),
                           ('L', 'L'),
                           ('XL', 'XL'),
                           ('XXL', 'XXL'),
                           ('XXXL', 'XXXL')
                       ])

    picture_1 = FileField('Add Picture',
                          validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_2 = FileField('Add Picture',
                          validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_3 = FileField('Add Picture',
                          validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Add Item')
