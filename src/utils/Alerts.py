#!/usr/bin/python

import platform
import smtplib
import Config
from utils import Logger


class Alerts:
   def __init__(self):
      global file
      self.logger = Logger.Logger(self.__class__.__name__).get()

   config = Config.Config()
   sender = 'debabrat_panda@apple.com'
   emailTo = config.getEmail()
   receivers = [emailTo]
   hostname = platform.node()
   # message = """From: hostname <hostname@apple.com>
   # To: emailTo <emailTo>
   # Subject: e-mail test
   #
   # This is a test e-mail message.
   #"""
   def sendEmail(self, text):

      try:
         smtpObj = smtplib.SMTP('localhost')
         smtpObj.sendmail(self.sender, self.receivers, text)
         self.logger.info("Successfully sent email")
      except BaseException:
         self.logger.error("Error: unable to send email")
         #raise "ERROR"
   def raiseAlert(self):
       pass