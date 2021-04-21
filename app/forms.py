# This file will be used to create the Multiple Choice Form used for the quizzes

# Importing form package from flask_wtf
from flask_wtf import Form
# Importing field packages from wtforms
from wtforms import RadioField, SubmitField, HiddenField, StringField
from wtforms.validators import Email, DataRequired


class MultipleChoiceForm(Form):
    answer = RadioField(coerce=int, choices=[(0, "false"),(1, "true")])
    hidden = HiddenField("questionIndex")  # 19/03/2021 - This field will be used to store the current question ID
    submit = SubmitField(label=('Next Question ->')) # This field will be used to submit the form data back to def quiz() in views.py

# 29/03/2021 - new initializeSessionForm
class initializeSessionForm(Form):
    email = StringField('Email', [Email(message=('Not a valid email address.')), DataRequired()])
    submit = SubmitField(label=('Submit Email Address'))
