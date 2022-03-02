# -*- coding: utf-8 -*-

import sqlite3
import os
import base64
from libs.common import Common


class Smtp:
    def __init__(self, root):
        self.dbExists = True
        if not os.path.isfile(Common.config_folder + "smtp.db"):
            self.dbExists = False
        self.connection = sqlite3.connect(Common.config_folder + "smtp.db")
        self.root = root
        if not self.dbExists:
            self.__create_db()

    def __del__(self):
        self.connection.close()

    def __create_db(self):
        cursor = self.connection.cursor()
        sql = "CREATE TABLE smtp(" \
              "address TEXT, " \
              "smtpserver TEXT, " \
              "smtpusername TEXT, " \
              "smtppassword TEXT)"
        cursor.execute(sql)
        self.connection.commit()

        smtppassword_utf = "password".encode('UTF-8')
        smtppassword_b64decoded = base64.b64encode(smtppassword_utf)
        smtppassword_utf8decoded = smtppassword_b64decoded.decode('UTF-8')

        sql = "INSERT INTO smtp VALUES('{0}', '{1}', '{2}', '{3}')" \
            .format("name@email-server.com", "smtp.email-server.com", "name@email-server.com", smtppassword_utf8decoded)
        cursor.execute(sql)
        self.connection.commit()

    def insert_to_db(
            self,
            emailaddress,
            smtpserver,
            smtpusername,
            smtppassword
    ):
        cursor = self.connection.cursor()

        smtppassword_utf = smtppassword.encode('UTF-8')
        smtppassword_b64decoded = base64.b64encode(smtppassword_utf)
        smtppassword_utf8decoded = smtppassword_b64decoded.decode('UTF-8')

        sql = "UPDATE smtp SET " \
              "address = '{0}', " \
              "smtpserver = '{1}', " \
              "smtpusername = '{2}', " \
              "smtppassword = '{3}'".format(emailaddress, smtpserver, smtpusername, smtppassword_utf8decoded)
        cursor.execute(sql)
        self.connection.commit()

    def get_data(self, value):
        sql = "SELECT {0} FROM smtp".format(value)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        for d in cursor:
            return d[0]
