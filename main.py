import web
import hashlib, uuid
from web import form
from register import *
render = web.template.render('templates/')
urls = (
  '/', 'Login',
  '/login', 'Login',
  '/reset', 'Reset',
  '/register', 'Register',
)
app = web.application(urls, locals())
db = web.database(dbn='mysql', db='pythontest', user='genohm', pw='genohm')

web.config.debug = False
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0})

def session_atr(atr_name):
    return session._initializer.get(atr_name)
def set_session_atr(atr_name, value):
    session._initializer[atr_name] = value
def logged():
    if session_atr('login')==1:
        return True
    else:
        return False
def create_render(privilege):
    if logged():
        if privilege == 0:
            render = web.template.render('templates/reader')
        elif privilege == 1:
            render = web.template.render('templates/user')
        elif privilege == 2:
            render = web.template.render('templates/admin')
        else:
            render = web.template.render('templates/communs')
    else:
        render = web.template.render('templates/communs')
    return render
class Login:

    def GET(self):
        if logged():
            render = create_render(session_atr('privilege'))
            return '%s' % render.login_double()
        else:
            render = create_render(session_atr('privilege'))
            return '%s' % render.login('')
    def POST(self):
        name, passwd = web.input().user, web.input().passwd
        ident = db.select('example_users', where='user=$name', vars=locals())[0]
        try:
            if hashlib.sha1("sAlT754-"+passwd).hexdigest() == ident['user_password']:
                set_session_atr('login', 1)
                set_session_atr('privilege', ident['privilege'])
                render = create_render(session_atr('privilege'))
                return render.login_ok()
            else:
                set_session_atr('login', 0)
                set_session_atr('privilege', 0)
                render = create_render(session_atr('privilege'))
                return render.login_error()
        except:
            set_session_atr('login', 0)
            set_session_atr('privilege', 0)
            render = create_render(session_atr('privilege'))
            error = 'User not found, try again'
            return render.login(error)

class Reset:

    def GET(self):
        set_session_atr('login', 0)
        session.kill
        render = create_render(session_atr('privilege'))
        return render.logout()
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
