from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class PictureForm(FlaskForm):
    picture1 = FileField('Post a picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')
