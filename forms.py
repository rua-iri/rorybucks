import wtforms

class RegisterForm(wtforms.Form):

    name = wtforms.StringField("Full Name", [wtforms.validators.Length(min=1, max=50)])
    username = wtforms.StringField("Username", [wtforms.validators.Length(min=4, max=25)])
    email = wtforms.StringField("Email", [wtforms.validators.Length(min=6, max=50)])
    password = wtforms.PasswordField('Password', [wtforms.validators.DataRequired(), wtforms.validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = wtforms.PasswordField("Confirm Password")


class SendMoneyForm(wtforms.Form):
    username = wtforms.StringField("Username", [wtforms.validators.Length(min=4, max=25)])
    amount = wtforms.StringField("Amount", [wtforms.validators.Length(min=1, max=50)])









