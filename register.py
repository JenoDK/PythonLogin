import web
import hashlib, uuid
from web import form
from main import *

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")
vNotNull = form.notnull

register_form = form.Form(
    form.Textbox("firstName", vNotNull, description="First name"),
    form.Textbox("lastName", vNotNull, description="Last name"),
    form.Textbox("email", vemail, vNotNull, description="E-Mail"),
    form.Password("password", vpass, vNotNull, description="Password"),
    form.Password("password2", vNotNull, description="Repeat password"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)

class Register:
    def GET(self):
        # do $:f.render() in the template
        f = register_form()
        return render.register(f)

    def POST(self):
        f = register_form()
        if not f.validates():
            render = web.template.render('templates/')
            return render.register(f)
        else:
            user, email, password = web.input().username, web.input().email, web.input().password
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha1("sAlT754-"+password).hexdigest()
            db.insert('example_users', user=user,user_password=hashed_password,email=email,privilege=0)
            render = create_render(0)
            return render.login('')
