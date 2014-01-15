#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import getopt
import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate

use_tls = False
smtp_host = 'localhost'
smtp_port = 25
smtp_user = None
smtp_pass = None

msg_sender = None
msg_receipients = []
msg_subject = None
msg_body = None

try:
	opts, args = getopt.getopt(sys.argv[1:], '', ['tls', 'host=', 'port=', 'user=', 'pass=', 'from=', 'to=', 'subject='])
	for opt, arg in opts:
		if opt == '--tls':
			use_tls = True
		elif opt == '--host':
			smtp_host = arg
		elif opt == '--port':
			smtp_port = arg
		elif opt == '--user':
			smtp_user = arg
		elif opt == '--pass':
			smtp_pass = arg
	
		elif opt == '--from':
			msg_sender = arg
		elif opt == '--to':
			msg_receipients.append(arg)
		elif opt == '--subject':
			msg_subject = arg

except Exception, e:
	print e
	sys.exit(-1)
	
# 標準入力から読み込み
msg_body = sys.stdin.read()

message = MIMEText(msg_body)
message['Subject'] = '日本語メッセージ'
message['From'] = msg_sender
message['To'] = ', '.join(msg_receipients)
message['Date'] = formatdate()

try:
	smtp = smtplib.SMTP(smtp_host, smtp_port)
	smtp.ehlo()
	
	if use_tls:
		smtp.starttls()
	
	smtp.ehlo()
	if smtp_user and smtp_pass:
		smtp.login(smtp_user, smtp_pass)
	
	smtp.sendmail(msg_sender, msg_receipients, message.as_string())
	smtp.close()

except Exception, e:
	print e
