# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from libs.common import Common
from libs.fonts import Fonts
import base64


class Settings:
    def __init__(self, root, db_smtp, db_settings):
        self.root = root
        self.dbSMTP = db_smtp
        self.dbSettings = db_settings

        self.dark_mode_intvar = tk.IntVar()

    def __switch_dark_mode(self):
        if self.dbSettings.get_data("darkmode") == 1:
            self.dbSettings.set_dark_mode(0)
            self.root.tk.call("set_theme", "light")
        else:
            self.dbSettings.set_dark_mode(1)
            self.root.tk.call("set_theme", "dark")

    def __button_ok(
            self,
            w,
            textbox_emailaddress,
            textbox_smtp_server,
            textbox_smtp_username,
            textbox_smtp_password
    ):

        self.dbSMTP.insert_to_db(
            textbox_emailaddress.get("1.0", 'end-1c').rstrip("\n"),
            textbox_smtp_server.get("1.0", 'end-1c').rstrip("\n"),
            textbox_smtp_username.get("1.0", 'end-1c').rstrip("\n"),
            textbox_smtp_password.get().rstrip("\n")
        )
        w.destroy()

    def open_settings(self, b):
        try:
            b.configure(style="TButton")
        except AttributeError:
            del b
        w = tk.Toplevel(self.root, width=100, height=50)
        w.title("E-Mail-Versand-Einstellungen")
        w.wm_transient(self.root)
        w.grab_set()
        w.resizable(False, False)
        w.config(padx=2, pady=2)

        label_emailaddress = ttk.Label(
            w,
            width=20,
            font=Fonts.font_main,
            text="Deine E-Mail-Adresse:",
            anchor="w"
        )
        text_box_emailaddress = tk.Text(
            w,
            font=Fonts.font_block,
            width=50,
            height=1, relief=tk.SUNKEN, borderwidth=2, highlightthickness=1, padx=2, pady=2
        )
        label_smtp_server = ttk.Label(
            w,
            width=20,
            font=Fonts.font_main,
            text="SMTP-Server:",
            anchor="w"
        )
        text_box_smtp_server = tk.Text(
            w,
            font=Fonts.font_block,
            width=50,
            height=1, relief=tk.SUNKEN, borderwidth=2, highlightthickness=1, padx=2, pady=2
        )
        label_smtp_username = ttk.Label(
            w,
            width=20,
            font=Fonts.font_main,
            text="SMTP-Benutzername:",
            anchor="w"
        )
        text_box_smtp_username = tk.Text(
            w,
            font=Fonts.font_block,
            width=50,
            height=1, relief=tk.SUNKEN, borderwidth=2, highlightthickness=1, padx=2, pady=2
        )
        label_smtp_password = ttk.Label(
            w,
            width=20,
            font=Fonts.font_main,
            text="SMTP-Password:",
            anchor="w"
        )
        text_box_smtp_password = tk.Entry(
            w,
            width=50,
            show="*",
            font=Fonts.font_block, relief=tk.SUNKEN, borderwidth=2, highlightthickness=1
        )

        button_dark_mode = ttk.Checkbutton(
            w,
            text="Dark Mode",
            style="Switch.TCheckbutton",
            variable=self.dark_mode_intvar,
            command=self.__switch_dark_mode
        )

        if self.dbSettings.get_data("darkmode") == 1:
            self.dark_mode_intvar.set(1)
        else:
            self.dark_mode_intvar.set(0)

        frame = tk.Frame(w, height=0)

        button_ok = ttk.Button(
            frame,
            width=15,
            style="Normal.TButton",
            text="OK",
            command=(
                lambda
                widget=w,
                e=text_box_emailaddress,
                s=text_box_smtp_server,
                u=text_box_smtp_username,
                p=text_box_smtp_password: self.__button_ok(widget, e, s, u, p)
            )
        )
        button_cancel = ttk.Button(
            frame,
            width=15,
            style="Normal.TButton",
            text="Abbrechen",
            command=w.destroy
        )
        smtppassword_base64 = self.dbSMTP.get_data("smtppassword")
        smtppassword_utf = smtppassword_base64.encode('UTF-8')
        smtppassword = base64.b64decode(smtppassword_utf)
        smtppassword = smtppassword.decode('UTF-8')
        text_box_emailaddress.insert("1.0", self.dbSMTP.get_data("address"))
        text_box_smtp_server.insert("1.0", self.dbSMTP.get_data("smtpserver"))
        text_box_smtp_username.insert("1.0", self.dbSMTP.get_data("smtpusername"))
        text_box_smtp_password.insert(0, smtppassword)
        label_emailaddress.grid(column=0, row=0, padx=2, pady=2)
        text_box_emailaddress.grid(column=1, row=0, padx=2, pady=2)
        label_smtp_server.grid(column=0, row=1, padx=2, pady=2)
        text_box_smtp_server.grid(column=1, row=1, padx=2, pady=2)
        label_smtp_username.grid(column=0, row=2, padx=2, pady=2)
        text_box_smtp_username.grid(column=1, row=2, padx=2, pady=2)
        label_smtp_password.grid(column=0, row=3, padx=2, pady=2)
        text_box_smtp_password.grid(column=1, row=3, padx=2, pady=2, ipadx=2, ipady=2)
        button_dark_mode.grid(column=1, row=4, padx=2, pady=2, sticky="e")

        frame.grid(column=1, row=5, columnspan=2, sticky="e", padx=0, pady=0)
        button_ok.grid(column=0, row=0, padx=2, pady=2, sticky="w")
        button_cancel.grid(column=1, row=0, padx=2, pady=2, sticky="e")

        text_box_emailaddress.bind("<Tab>", Common.tab_pressed)
        text_box_smtp_server.bind("<Tab>", Common.tab_pressed)
        text_box_smtp_username.bind("<Tab>", Common.tab_pressed)
        text_box_smtp_password.bind("<Tab>", Common.tab_pressed)

        button_ok.bind("<Enter>",
                       lambda event, button=button_ok: Common.hover_button(event, button)
                       )
        button_ok.bind("<Leave>",
                       lambda event, button=button_ok: Common.leave_button(event, button))

        button_cancel.bind("<Enter>",
                           lambda event, button=button_cancel: Common.hover_button(event, button))
        button_cancel.bind("<Leave>",
                           lambda event, button=button_cancel: Common.leave_button(event, button))

        Common.center(w)
