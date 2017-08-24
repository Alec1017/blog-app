from wtforms import Form, StringField, TextAreaField, PasswordField, validators


# A form for a user to register in the app
# Uses validators to specify required data
class RegisterForm(Form):
    # Name field
    name = StringField('Name', [
        validators.Length(min=1, max=50)])
    # Username field
    username = StringField('Username', [
        validators.Length(min=4, max=25)])
    # Email field
    email = StringField('Email', [
        validators.Length(min=6, max=50)])
    # Password field
    password = PasswordField('Password', [
        validators.DataRequired(),
        # Checks the password with the confirm field
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    # Confirm password field
    confirm = PasswordField('Confirm Password')
