# -*- coding: utf-8 -*-

import sqlite3
import os
from libs.common import Common


class Settings:
    def __init__(self):
        self.dbExists = True
        if not os.path.isfile(Common.config_folder + "settings.db"):
            self.dbExists = False
        self.connection = sqlite3.connect(Common.config_folder + "settings.db")
        if not self.dbExists:
            self.__create_db()

    def __del__(self):
        self.connection.close()

    def __create_db(self):
        cursor = self.connection.cursor()
        sql = "CREATE TABLE settings(" \
              "darkmode INTEGER)"
        cursor.execute(sql)
        self.connection.commit()
        sql = "INSERT INTO settings ('darkmode') VALUES(0)"
        cursor.execute(sql)
        self.connection.commit()

    def set_dark_mode(
            self,
            mode
    ):
        cursor = self.connection.cursor()
        sql = "UPDATE settings SET " \
              "darkmode = {0}".format(mode)
        cursor.execute(sql)
        self.connection.commit()

    def get_data(self, column):
        sql = "SELECT {0} FROM settings".format(column)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        for d in cursor:
            return d[0]
