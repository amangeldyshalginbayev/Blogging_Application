from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                     SelectField)
from wtforms.validators import (DataRequired, Length, Email, EqualTo, Regexp,
                                ValidationError)
from flask_login import current_user
from flaskblog.models import User
from flaskblog.users.utils import is_password_valid, is_mobile_phone_valid


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. '
                                  'Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. '
                                  'Please choose a different one.')

    def validate_password(self, password):
        if not is_password_valid(password.data):
            message = ('Password must contain uppcercase and lowercase '
                       'letters, number and symbol')
            raise ValidationError(message)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. '
                                      'Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. '
                                      'Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. '
                                  'You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_password(self, password):
        if not is_password_valid(password.data):
            message = ('Password must contain uppcercase and lowercase '
                       'letters, number and symbol')
            raise ValidationError(message)


class MobilePhoneEntryForm(FlaskForm):
    country_code = SelectField('Select your country: ',
                               choices=[('+372', 'Estonia'),
                                        ('+7', 'Kazakhstan'),
                                        ('+44', 'United Kingdom')])
    phone_number = StringField('Enter your mobile number: ',
                               validators=[DataRequired()])
    submit = SubmitField('Link my number')

    def validate_phone_number(self, phone_number):
        full_number = self.country_code.data + self.phone_number.data
        if not is_mobile_phone_valid(full_number):
            raise ValidationError('Invalid mobile phone number.')


class ConfirmMobilePhoneForm(FlaskForm):
    pin_code = StringField('Enter PIN code: ',
                           validators=[DataRequired(),
                                       Regexp(regex=r'^[1-9][0-9]{3}$',
                                              message='Invalid PIN')])
    submit = SubmitField('Submit')
