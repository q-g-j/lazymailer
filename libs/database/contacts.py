# -*- coding: utf-8 -*-

import sqlite3
import os
from libs.common import Common


class Contacts:
    def __init__(self):
        if not os.path.isfile(Common.config_folder + "contacts.db"):
            self.connection = sqlite3.connect(Common.config_folder + "contacts.db")
            self.__create_table()
        else:
            self.connection = sqlite3.connect(Common.config_folder + "contacts.db")

    def __del__(self):
        self.connection.close()

    def __create_table(self):
        cursor = self.connection.cursor()
        sql = "DROP TABLE IF EXISTS contacts"
        cursor.execute(sql)
        self.connection.commit()
        sql = "CREATE TABLE contacts(" \
              "title TEXT, " \
              "name TEXT, " \
              "emailaddress TEXT, " \
              "emailbody TEXT, " \
              "subject)"
        cursor.execute(sql)
        self.connection.commit()

    def insert_to_db(self, title, name, emailaddress, emailbody, subject):
        sql = "INSERT INTO contacts VALUES('{0}', '{1}', '{2}', '{3}', '{4}')" \
            .format(title, name, emailaddress, emailbody, subject)

        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

    def edit_entry(self, index, title, name, emailaddress, emailbody, subject):
        sql = "UPDATE contacts SET " \
                "title = '{0}', " \
                "name = '{1}', " \
                "emailaddress = '{2}', " \
                "emailbody = '{3}', " \
                "subject = '{4}' " \
                "WHERE rowid = {5}".format(title, name, emailaddress, emailbody, subject, index + 1)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

    def delete_from_db(self, index):
        sql = "DELETE FROM contacts WHERE rowid={0}".format(index + 1)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        sql = "PRAGMA auto_vacuum = FULL"
        cursor.execute(sql)
        self.connection.commit()
        sql = "VACUUM"
        cursor.execute(sql)
        self.connection.commit()

    def get_num_entries(self):
        sql = "SELECT name FROM contacts"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        num = 0
        for _ in cursor:
            num += 1
        return num

    def get_data(self, index, value):
        sql = "SELECT {0} FROM contacts WHERE rowid={1}".format(value, index + 1)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        for d in cursor:
            return d[0]
