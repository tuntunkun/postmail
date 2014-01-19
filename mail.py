#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import getopt
import getpass
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE
from email.Utils import formatdate
from email import Encoders

class App(object):
	class Option(object):
		def __init__(self, sopt, lopt, type, desc):
			self.sopt = sopt
			self.lopt = lopt
			self.type = type
			self.desc = desc

	__options = []

	def __init__(self, argv):
		self._init(argv)

	def _pre_init(self):
		pass

	def _post_init(self, args):
		pass

	def _parse(self, opt, arg):
		return False

	def _short_opts(self):
		return map(lambda x: x.sopt, filter(lambda x: not x.sopt is None, self.__options))

	def _long_opts(self):
		return map(lambda x: x.lopt, filter(lambda x: not x.lopt is None, self.__options))

	def _append_option(self, sopt, lopt, type=None, desc=None):
		self.__options.append(App.Option(sopt, lopt, type, desc))

	def _init(self, argv):
		self._pre_init()

		opts, args = getopt.getopt(argv, ''.join(self._short_opts()), self._long_opts())
		for opt, arg in opts:
			self._parse(opt, arg)

		self._post_init(args)

	def run(self):
		pass


class SMTPApp(App):
	_use_tls = False

	_smtp_host = 'localhost'
	_smtp_port = 25
	_smtp_user = None
	_smtp_pass = None
	_smtp_auth = False

	_msg_sender = None
	_msg_recipients = []
	_msg_copies = []
	_msg_attachments = []
	_msg_subject = None
	_msg_body = sys.stdin

	def _pre_init(self):
		super(SMTPApp, self)._pre_init()

		self._append_option(None, 'tls')

		# smtp
		self._append_option(None, 'host=', 'host')
		self._append_option(None, 'port=', 'port')
		self._append_option(None, 'user=', 'user')
		self._append_option(None, 'pass=', 'password')

		# message
		self._append_option(None, 'from=', 'email')
		self._append_option(None, 'to=', 'email')
		self._append_option(None, 'cc=', 'email')
		self._append_option(None, 'subject=', 'text')
		self._append_option(None, 'body=', 'file')
		self._append_option(None, 'attach=', 'file')

		# service
		self._append_option(None, 'gmail')
		self._append_option(None, 'o365')

	def _parse(self, opt, arg):
		result = True

		if super(SMTPApp, self)._parse(opt, arg):
			return result

		if opt in ('--tls',):
			self._use_tls = True

		elif opt in ('--host',):
			self._smtp_host = arg
		elif opt in ('--port',):
			self._smtp_port = arg
		elif opt in ('--user',):
			self._smtp_auth = True
			self._smtp_user = arg
		elif opt in ('--pass',):
			self._smtp_pass = arg

		elif opt in ('--from',):
			self._msg_sender = arg
		elif opt in ('--to',):
			self._msg_recipients.append(arg)
		elif opt in ('--cc',):
			self._msg_copies.append(arg)
		elif opt in ('--subject',):
			self._msg_subject = arg
		elif opt in ('--body',):
			if not self._msg_body is sys.stdin:
				self._msg_body.close()
			self._msg_body = open(arg, 'rb')
		elif opt in ('--attach',):
			self._msg_attachments.append(arg)

		elif opt in ('--gmail',):
			self._use_tls = True
			self._smtp_auth = True
			self._smtp_host = 'smtp.gmail.com'
			self._smtp_port = 587
		elif opt in ('--o365',):
			self._use_tls = True
			self._smtp_auth = True
			self._smtp_host = 'smtp.office365.com'
			self._smtp_port = 587
		else:
			result = False
		return result

	def _post_init(self, args):
		super(SMTPApp, self)._post_init(args)

		if len(self._msg_recipients) < 1:
			raise Exception('you must specify at least one recipient email address')

		if self._smtp_auth and self._smtp_user is None:
			raise Exception('you must specify smtp user to authenticate')

		if self._smtp_auth and self._smtp_pass is None:
			self._smtp_pass = getpass.getpass('password: ')
		
		
	def _compose_message(self):
		msg = MIMEMultipart()
		msg['Subject'] = self._msg_subject
		msg['From'] = self._msg_sender
		msg['Cc'] = COMMASPACE.join(self._msg_copies)
		msg['To'] = COMMASPACE.join(self._msg_recipients)
		msg['Date'] = formatdate(localtime=True)

		msg.attach(MIMEText(self._msg_body.read()))

		for fname in self._msg_attachments:
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(open(fname, 'rb').read())
			Encoders.encode_base64(part)
			part.add_header(
				'Content-Disposition',
				'attachment; filename="%s"' % os.path.basename(fname))
			msg.attach(part)

		return msg

	def run(self):
		smtp = smtplib.SMTP(self._smtp_host, self._smtp_port)
		smtp.ehlo()
		
		if self._use_tls:
			smtp.starttls()
		
		smtp.ehlo()
		if self._smtp_user and self._smtp_pass:
			smtp.login(self._smtp_user, self._smtp_pass)

		msg = self._compose_message()
		smtp.sendmail(self._msg_sender, self._msg_recipients, msg.as_string())
		smtp.close()
	
	
try:
	app = SMTPApp(sys.argv[1:])
	app.run()
except KeyboardInterrupt:
	pass
except smtplib.SMTPException, e:
	print >>sys.stderr, e.smtp_error
except Exception, e:
	print >>sys.stderr, e
