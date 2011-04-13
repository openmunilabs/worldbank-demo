import os

import logging
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import string

class MainPage(webapp.RequestHandler):
    def get(self):
		#all = db.GqlQuery("SELECT * FROM SMS WHERE active='active' ORDER BY timestamp DESC")

		#for sms in all:
		#	count=count+1
		#	if count<4:
		#		msg=msg+"<b>"+truck.name+" ("+truck.short+") - "+str(truck.counter)+" votes </b><br/> "
		#	else:
		#		msg=msg+truck.name+" ("+truck.short+") - "+str(truck.counter)+" votes <br/> "

		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'main.html')
		self.response.out.write(template.render(path, template_values))

class Json(webapp.RequestHandler):
    def get(self):
		all = db.GqlQuery("SELECT * FROM SMS WHERE status='active' ORDER BY timestamp DESC")

		json='{"messages":['
		for sms in all:
			json=json+'{"phone":"%s", "msg":"%s", "name":"%s", "location":"%s", "need":"%s","timestamp":"%s"},' % (sms.phone, sms.msg, sms.name, sms.location, sms.need, sms.timestamp)
		
		if (json[len(json)-1]==","): json=json[0:len(json)-1]
		json=json+"]}"

		self.response.headers["Content-Type"] = "application/json"
		self.response.out.write(json)


class Sms(webapp.RequestHandler):
    def get(self):
		phone=cgi.escape(self.request.get('From'))
		msg=cgi.escape(self.request.get('Body'))
		msg2=msg.upper()
				
		sms=models.SMS()
		
		sms.phone=phone
		sms.msg=msg;
		
		try:
			if (string.find(msg2,"FROM")<0): raise Exception("FROM keyword is missing")
			if (string.find(msg2,"NEED")<0): raise Exception("NEED keyword is missing")
			
			name=msg[0:string.find(msg2,"FROM")-1]
			location=msg[string.find(msg2,"FROM")+5:string.rfind(msg2,"NEED")-1]
			need=msg[string.rfind(msg2,"NEED")+5:]
		
			sms.name=name
			sms.location=location
			sms.need=need
			response="OK"
		
		except:
			sms.status="error"
			response="format error - use message format: NAME from LOCATION need SOMETHING"
		finally:
			sms.put()

		
		self.response.headers["Content-Type"] = "text/xml"
		self.response.out.write("""<?xml version="1.0" encoding="UTF-8"?>
		<Response>
		    <Sms>%s</Sms>
		</Response>
		""" % (response))


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/json', Json),
                                     ('/sms', Sms)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()