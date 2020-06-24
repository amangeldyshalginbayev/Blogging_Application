from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Comment')


class UpdateCommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    update = SubmitField('Update')
    delete = SubmitField('Delete')
