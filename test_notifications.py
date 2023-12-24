import http.client, urllib
conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "anbech6jzpc6vmkfaa48vi599vnxst",
    "user": "u5wv8nafejdjp2ieihweucuqtzcnq9",
    "message": "Reliance and TCS: 1.5 times volume",
    "title": "1.5 time volume Alert"
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()

# from chump import Application
# app = Application('anbech6jzpc6vmkfaa48vi599vnxst')
# user = app.get_user('u5wv8nafejdjp2ieihweucuqtzcnq9')
# user.create_message(title="1.5 times volume", message= "RIL \n"*100).send()
