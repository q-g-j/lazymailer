# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import smtplib
import base64
from email.mime.text import MIMEText
from libs.common import Common
from libs.fonts import Fonts


class SendMail:
    def __init__(self, root, main_window, db_email, db_contacts):
        self.root = root
        self.mainWindow = main_window
        self.dbSMTP = db_email
        self.dbContacts = db_contacts

        self.SMTPport = 587
        self.text_subtype = "plain"

    def send_email(self, button):
        button.configure(style="Normal.TButton")
        checked_contacts = self.mainWindow.get_checked_contacts()
        contact_succeeded = []
        contact_failed = []
        authentification_failed = False
        unknown_error = False

        for i in range(len(checked_contacts)):
            msg = MIMEText(self.dbContacts.get_data(checked_contacts[i], "emailbody"), self.text_subtype)
            msg['Subject'] = self.dbContacts.get_data(checked_contacts[i], "subject")
            msg['From'] = self.dbSMTP.get_data("address")

            try:
                conn = smtplib.SMTP(self.dbSMTP.get_data("smtpserver"))
                conn.connect(self.dbSMTP.get_data("smtpserver"), self.SMTPport)
                conn.ehlo()
                conn.starttls()
                conn.ehlo()
                conn.set_debuglevel(False)
            except:
                unknown_error = True
            else:
                smtppassword_b64 = self.dbSMTP.get_data("smtppassword")
                smtppassword_utf = smtppassword_b64.encode('UTF-8')
                smtppassword_b64decoded = base64.b64decode(smtppassword_utf)
                smtppassword_utf8decoded = smtppassword_b64decoded.decode('UTF-8')
                try:
                    conn.login(
                        self.dbSMTP.get_data("smtpusername"),
                        smtppassword_utf8decoded
                    )
                except:
                    authentification_failed = True
                else:
                    try:
                        conn.sendmail(
                            self.dbSMTP.get_data("address"),
                            self.dbContacts.get_data(checked_contacts[i], "emailaddress"),
                            msg.as_string()
                        )
                    except:
                        contact_failed.append(self.mainWindow.get_checked_contacts()[i])
                    else:
                        contact_succeeded.append(self.mainWindow.get_checked_contacts()[i])
                finally:
                    conn.quit()

        if authentification_failed:
            w = tk.Toplevel(self.root, width=100, height=50)
            w.wm_transient(self.root)
            w.grab_set()
            w.config(padx=2, pady=2)
            w.title("Fehler")
            label_title = ttk.Label(w,
                                    text="Versand fehlgeschlagen:",
                                    anchor="w"
                                    )
            label_title.configure(style="TLabel", font=Fonts.font_title, foreground="red")
            label_title.pack(anchor="w", padx=2, pady=2)
            label_1 = ttk.Label(w,
                                text="Bitte die Anmeldedaten für den SMTP-Server",
                                anchor="w"
                                )
            label_2 = ttk.Label(w,
                                text="unter \"Einstellungen\" überprüfen.",
                                anchor="w"
                                )
            label_1.pack(anchor="w", padx=2)
            label_2.pack(anchor="w", padx=2)

            Common.center(w)

        elif len(contact_succeeded) != 0 or len(contact_failed) != 0:
            w = tk.Toplevel(self.root, width=100, height=50)
            w.wm_transient(self.root)
            w.grab_set()
            w.config(padx=2, pady=2)
            w.title("Zusammenfassung")

            if len(contact_succeeded) != 0:
                label_title = ttk.Label(w,
                                        text="Versand an folgende Adressen erfolgreich:",
                                        anchor="w"
                                        )
                label_title.configure(style="TLabel", font=Fonts.font_title)
                label_title.pack(anchor="w", padx=2, pady=2)
                for s in range(len(contact_succeeded)):
                    label = ttk.Label(w,
                                      text=self.dbContacts.get_data(
                                          contact_succeeded[s],
                                          "emailaddress"
                                      ),
                                      anchor="w",
                                      font=Fonts.font_main
                                      )
                    label.pack(anchor="w", padx=2, pady=2)

            if len(contact_failed) != 0:
                label_title = ttk.Label(w,
                                        text="Versand an folgende Adressen fehlgeschlagen:",
                                        anchor="w"
                                        )
                label_title.configure(style="TLabel", font=Fonts.font_title, foreground="red")
                label_title.pack(anchor="w", padx=2, pady=2)
                for s in range(len(contact_failed)):
                    label = ttk.Label(w,
                                      text=self.dbContacts.get_data(
                                          contact_failed[s],
                                          "emailaddress"
                                      ),
                                      anchor="w",
                                      font=Fonts.font_main
                                      )
                    label.pack(anchor="w", padx=2, pady=2)

            button_ok = ttk.Button(w,
                                   text="OK",
                                   command=w.destroy
                                   )
            button_ok.pack(anchor="e", padx=3, pady=3)

            button_ok.bind(
                "<Enter>",
                lambda event, b=button_ok: Common.hover_button(event, b)
            )
            button_ok.bind(
                "<Leave>",
                lambda event, b=button_ok: Common.leave_button(event, b)
            )

            Common.center(w)

        elif unknown_error:
            w = tk.Toplevel(self.root, width=100, height=50)
            w.wm_transient(self.root)
            w.grab_set()
            w.config(padx=2, pady=2)
            w.title("Fehler")
            label_title = ttk.Label(w,
                                    text="Unbekannter Fehler:",
                                    anchor="w"
                                    )
            label_title.configure(style="TLabel", font=Fonts.font_title, foreground="red")
            label_title.pack(anchor="w", padx=2, pady=2)
            label_1 = ttk.Label(w,
                                text="Etwas ist schiefgelaufen.",
                                anchor="w",
                                      font=Fonts.font_main
                                )
            label_2 = ttk.Label(w,
                                text="Bitte die Kontakte und Einstellungen überprüfen.",
                                anchor="w",
                                      font=Fonts.font_main
                                )
            label_1.pack(anchor="w", padx=2)
            label_2.pack(anchor="w", padx=2)
            
            Common.center(w)
