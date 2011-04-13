from google.appengine.ext import db

#model to store every received SMS messages
class SMS(db.Model):
	phone =  db.StringProperty()
	msg = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now=True)
	
	name =  db.StringProperty()
	location  =  db.StringProperty()
	need  =  db.StringProperty()
	
	status = db.StringProperty(default="active")
	

