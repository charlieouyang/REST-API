import smtplib

from flask import Flask, url_for
from flask import request, json
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'This is a REST API built by Charlie Ou Yang. Please visit www.charlieouyang.com to contact him.'

@app.route('/data', methods = ['GET', 'POST'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
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