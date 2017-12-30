
# SendEmail.py - by Luna Winters
# Quick and dirty python script to send an email to a gmail address
# Also works with google apps domains
#
#The MIT License (MIT)
#
#Copyright (c) 2014 Luna Winters
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
import smtplib

SERVER = "smtp.gmail.com:587"
FROM = "LPBot9000"
TO = "" #Your email goes here
gmailUsername = "" #Bots email goes here
gmailPassword = "" #Bots password goes here

def sendemail(subject, text):
	message = "From: %s\n" % FROM
	message += "To: %s\n" % TO
	message += "Subject: %s\n\n" % subject
	message += text

	server = smtplib.SMTP(SERVER)
	server.starttls()
	server.login(gmailUsername,gmailPassword)
	server.sendmail(FROM,TO,message)
	server.quit()
