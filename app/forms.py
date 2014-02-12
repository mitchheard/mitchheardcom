from flask.ext.wtf import Form
from wtforms import TextField, validators, PasswordField, TextAreaField, SubmitField
from models import Person

strip_filter = lambda x: x.strip() if x else None

class ArticleCreateForm(Form):
    title = TextField('Title', [validators.Required("Please enter title.")],
                      filters=[strip_filter] )
    body = TextAreaField('Body', [validators.Required("Please enter body.")],
                         filters=[strip_filter])

class SignupForm(Form):
    firstname = TextField("First name", [validators.Required("Please enter your first name.")])
    lastname = TextField("Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        person = Person.query.filter_by(email=self.email.data.lower()).first()
        if person:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True

class SigninForm(Form):
    email = TextField("email", [validators.Required("Please enter your email")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        person = Person.query.filter_by(email=self.email.data.lower()).first()
        if person and person.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid username")
            return False