import smtplib

from flask import Flask, url_for
from flask import request, json

from datetime import timedelta
from flask import make_response, current_app
from functools import update_wrapper
    
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

@app.route('/')
@crossdomain(origin='*')
def api_root():
    return 'This is a REST API built by Charlie Ou Yang. Please visit www.charlieouyang.com to contact him.'

@app.route('/data', methods = ['GET', 'POST'])
@crossdomain(origin='*')
def data():
    # Specifying the from and to addresses
    fromaddr = 'charlieouyangwebsite@gmail.com'
    toaddrs  = 'charlieouyang@gmail.com'
    # Writing the message (this message will appear in the email)
    msg = "\r\n".join([
        "From: charlieouyangwebsite@gmail.com",
        "To: charlieouyang@gmail.com",
        "Subject: Message from your website",
        "",
        json.dumps(request.json)
        ])
    # Gmail Login
    username = 'charlieouyangwebsite@gmail.com'
    password = 'charlieloveswebsites'
    # Sending the mail  
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

    return "Email sent!"

if __name__ == '__main__':
    app.run()