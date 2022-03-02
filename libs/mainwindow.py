# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import ttk

from libs.common import Common
from libs.database.settings import Settings as DBsettings
from libs.database.contacts import Contacts as DBcontacts
from libs.database.smtp import Smtp as DBsmtp
from libs.settings import Settings
from libs.sendmail import SendMail
from libs.fonts import Fonts


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.varArray = []
        self.checkbuttonArray = []
        self.contactEditButtonArray = []
        self.root.config(padx=2, pady=2)

        exists_settings_db = True
        if not os.path.isfile(Common.config_folder + "settings.db"):
            exists_settings_db = False
        self.dbContacts = DBcontacts()
        self.dbSMTP = DBsmtp(self.root)
        self.dbSettings = DBsettings()

        Common.set_theme(self.root, self.dbSettings)
        Common.set_styles()

        self.settings = Settings(self.root, self.dbSMTP, self.dbSettings)
        self.mail = SendMail(self.root, self, self.dbSMTP, self.dbContacts)

        self.recipientsNum = self.dbContacts.get_num_entries()

        self.__create_contact_entries()
        self.__create_buttons()

        Common.center(self.root)

        if not exists_settings_db:
            self.settings.open_settings("dummy")

    @staticmethod
    def __tab_pressed(event):
        event.widget.tk_focusNext().focus()
        return "break"

    def __check_all(self):
        num_entries = self.dbContacts.get_num_entries()
        check_all_pos = num_entries

        if len(self.get_checked_contacts()) != num_entries:
            for i in range(num_entries):
                self.varArray[i].set(1)
            self.varArray[check_all_pos].set(1)
        else:
            for i in range(num_entries):
                self.varArray[i].set(0)
            self.varArray[check_all_pos].set(0)

    def __change_check_all_label(self):
        num_entries = self.dbContacts.get_num_entries()
        check_all_pos = num_entries

        if num_entries == len(self.get_checked_contacts()):
            self.varArray[check_all_pos].set(1)
        else:
            self.varArray[check_all_pos].set(0)

    def __create_contact_entries(self):
        num_entries = self.dbContacts.get_num_entries()
        for i in self.checkbuttonArray:
            i.destroy()
        for i in self.contactEditButtonArray:
            i.destroy()
        self.checkbuttonArray.clear()
        self.contactEditButtonArray.clear()
        self.varArray.clear()

        for i in range(num_entries):
            self.varArray.append(tk.IntVar())
            self.checkbuttonArray.append(ttk.Checkbutton(
                self.root,
                style="TCheckbutton",
                variable=self.varArray[i])
            )
            self.checkbuttonArray[i].grid(column=0, row=i, sticky="w", padx=2, pady=2)
            self.checkbuttonArray[i].config(
                text=self.dbContacts.get_data(i, "title")
                + " "
                + self.dbContacts.get_data(i, "name"),
                command=self.__change_check_all_label
            )
            self.contactEditButtonArray.append(
                ttk.Button(
                    self.root,
                    style="Normal.TButton",
                    text="bearbeiten",
                    width=12
                )
            )
            self.contactEditButtonArray[i].config(command=lambda index=i: self.__edit_contact(index))
            self.contactEditButtonArray[i].grid(column=3, row=i, sticky="w", padx=2, pady=2)

            self.contactEditButtonArray[i].bind(
                "<Enter>",
                lambda event, button=self.contactEditButtonArray[i]: Common.hover_button(event, button)
            )
            self.contactEditButtonArray[i].bind(
                "<Leave>",
                lambda event, button=self.contactEditButtonArray[i]: Common.leave_button(event, button)
            )

        if num_entries > 0:
            check_all_pos = num_entries
            self.varArray.append(tk.IntVar())
            self.checkbuttonArray.append(ttk.Checkbutton(
                self.root,
                text="Alle",
                style="Switch.TCheckbutton",
                command=self.__check_all,
                variable=self.varArray[check_all_pos])
            )
            self.checkbuttonArray[check_all_pos].grid(column=0, row=check_all_pos, sticky="w")

            self.checkbuttonArray[check_all_pos].configure(
            )
            self.checkbuttonArray[num_entries].grid(columnspan=3, padx=2, pady=2)

    def __add_contact_button_ok(
            self,
            widget,
            title,
            name,
            emailaddress,
            emailbody,
            subject
            ):
        self.dbContacts.insert_to_db(
            title.get("1.0", 'end-1c').rstrip("\n"),
            name.get("1.0", 'end-1c').rstrip("\n"),
            emailaddress.get("1.0", 'end-1c').rstrip("\n"),
            emailbody.get("1.0", 'end-1c'),
            subject.get("1.0", 'end-1c').rstrip("\n")
        )
        self.__create_contact_entries()

        self.button_new_contact.grid(column=0, row=self.dbContacts.get_num_entries() + 2, padx=2, pady=2, sticky="w")
        self.button_ok.grid(column=2, row=self.dbContacts.get_num_entries() + 3, padx=2, pady=2, sticky="w")
        self.button_settings.grid(column=3, row=self.dbContacts.get_num_entries() + 3, padx=2, pady=2, sticky="w")

        widget.destroy()

    def __edit_contact_button_ok(
            self,
            widget,
            index,
            title,
            name,
            emailaddress,
            emailbody,
            subject
            ):
        self.dbContacts.edit_entry(
            index,
            title.get("1.0", 'end-1c').rstrip("\n"),
            name.get("1.0", 'end-1c').rstrip("\n"),
            emailaddress.get("1.0", 'end-1c').rstrip("\n"),
            emailbody.get("1.0", 'end-1c'),
            subject.get("1.0", 'end-1c').rstrip("\n"),
        )

        self.checkbuttonArray[index].config(
            text=self.dbContacts.get_data(index, "title")
            + " "
            + self.dbContacts.get_data(index, "name")
        )

        self.button_new_contact.grid(column=0, row=self.dbContacts.get_num_entries() + 2, padx=2, pady=2, sticky="w")
        self.button_ok.grid(column=2, row=self.dbContacts.get_num_entries() + 3, padx=2, pady=2, sticky="w")
        self.button_settings.grid(column=3, row=self.dbContacts.get_num_entries() + 3, padx=2, pady=2, sticky="w")

        widget.destroy()

    @staticmethod
    def __contact_button_cancel(widget):
        widget.destroy()

    def __create_add_edit_widgets(self, w, mode, index):
        label_title = ttk.Label(w, text="Anrede:", font=Fonts.font_main)
        label_name = ttk.Label(w, text="Nachname:", font=Fonts.font_main)
        label_emailaddress = ttk.Label(w, text="E-Mail-Adresse:", font=Fonts.font_main)
        label_subject = ttk.Label(w, text="Betreff:", font=Fonts.font_main)
        label_emailbody = ttk.Label(w, text="Nachricht:", font=Fonts.font_main)

        textbox_title = tk.Text(
            w,
            font=Fonts.font_block,
            height=0,
            width=50,
            relief=tk.SUNKEN,
            borderwidth=2,
            highlightthickness=1,
            padx=2,
            pady=2
        )
        textbox_name = tk.Text(
            w,
            font=Fonts.font_block,
            height=0,
            width=50,
            relief=tk.SUNKEN,
            borderwidth=2,
            highlightthickness=1,
            padx=2,
            pady=2
        )
        textbox_emailaddress = tk.Text(
            w,
            font=Fonts.font_block,
            height=0,
            width=50,
            relief=tk.SUNKEN,
            borderwidth=2,
            highlightthickness=1,
            padx=2,
            pady=2
        )
        textbox_subject = tk.Text(
            w,
            font=Fonts.font_block,
            height=0,
            width=50,
            relief=tk.SUNKEN,
            borderwidth=2,
            highlightthickness=1,
            padx=2,
            pady=2
        )
        textbox_emailbody = tk.Text(
            w,
            font=Fonts.font_block,
            height=10,
            width=50,
            relief=tk.SUNKEN,
            borderwidth=2,
            highlightthickness=1,
            padx=2,
            pady=2
        )

        label_title.grid(column=0, row=0, sticky="w", padx=2, pady=2, ipadx=2, ipady=2)
        label_name.grid(column=0, row=1, sticky="w", padx=2, pady=2, ipadx=2, ipady=2)
        label_emailaddress.grid(column=0, row=2, sticky="w", padx=2, pady=2, ipadx=2, ipady=2)
        label_subject.grid(column=0, row=3, sticky="w", padx=2, pady=2, ipadx=2, ipady=2)
        label_emailbody.grid(column=0, row=4, sticky="nw", padx=2, pady=2, ipadx=2, ipady=4)

        textbox_title.grid(column=1, row=0, sticky="w", padx=2, pady=2)
        textbox_name.grid(column=1, row=1, sticky="w", padx=2, pady=2)
        textbox_emailaddress.grid(column=1, row=2, sticky="w", padx=2, pady=2)
        textbox_subject.grid(column=1, row=3, sticky="w", padx=2, pady=2)
        textbox_emailbody.grid(column=1, row=4, rowspan=10, sticky="w", padx=2, pady=2)

        frame = tk.Frame(w)

        button_ok = ttk.Button(
            frame,
            style="Normal.TButton",
            text="OK",
            width=12
        )
        if mode == "edit":
            textbox_title.insert("1.0", self.dbContacts.get_data(index, "title"))
            textbox_name.insert("1.0", self.dbContacts.get_data(index, "name"))
            textbox_emailaddress.insert("1.0", self.dbContacts.get_data(index, "emailaddress"))
            textbox_subject.insert("1.0", self.dbContacts.get_data(index, "subject"))
            textbox_emailbody.insert("1.0", self.dbContacts.get_data(index, "emailbody"))

            frame.grid(column=1, row=15, columnspan=1, padx=0, pady=0, sticky="e")
            frame_left = tk.Frame(w, height=0)
            frame_left.grid(column=0, row=15, columnspan=1, padx=0, pady=0, sticky="w")

            button_delete = ttk.Button(
                frame_left,
                style="Normal.TButton",
                text="Kontakt löschen",
                command=lambda widget=w, i=index: self.__delete_contact(widget, i)
            )
            button_delete.grid(column=0, row=0, padx=2, pady=2, sticky="w")
            button_ok.configure(
                command=lambda widget=w: self.__edit_contact_button_ok(
                    widget,
                    index,
                    textbox_title,
                    textbox_name,
                    textbox_emailaddress,
                    textbox_emailbody,
                    textbox_subject
                )
            )
            button_delete.bind(
                "<Enter>",
                lambda event, button=button_delete: Common.hover_button(event, button)
                )
            button_delete.bind(
                "<Leave>",
                lambda event, button=button_delete: Common.leave_button(event, button)
                )

        elif mode == "add":
            frame.grid(column=1, row=15, columnspan=2, sticky="e", padx=0, pady=0)
            button_ok.configure(
                command=lambda widget=w,
                title=textbox_title,
                name=textbox_name,
                emailaddress=textbox_emailaddress,
                emailbody=textbox_emailbody,
                subject=textbox_subject: self.__add_contact_button_ok(
                    widget,
                    title,
                    name,
                    emailaddress,
                    emailbody,
                    subject
                )
            )
        button_cancel = ttk.Button(
            frame,
            style="Normal.TButton",
            text="Abbrechen",
            width=12,
            command=lambda widget=w: self.__contact_button_cancel(widget)
        )

        button_ok.grid(column=0, row=0, padx=2, pady=2, sticky="w")
        button_cancel.grid(column=1, row=0, padx=2, pady=2, sticky="w")

        textbox_title.bind("<Tab>", Common.tab_pressed)
        textbox_name.bind("<Tab>", Common.tab_pressed)
        textbox_emailaddress.bind("<Tab>", Common.tab_pressed)
        textbox_subject.bind("<Tab>", Common.tab_pressed)
        textbox_emailbody.bind("<Tab>", Common.tab_pressed)
    
        button_ok.bind(
            "<Enter>",
            lambda event, button=button_ok: Common.hover_button(event, button)
            )
        button_ok.bind(
            "<Leave>",
            lambda event, button=button_ok: Common.leave_button(event, button)
            )

        button_cancel.bind(
            "<Enter>",
            lambda event, button=button_cancel: Common.hover_button(event, button)
            )
        button_cancel.bind(
            "<Leave>",
            lambda event, button=button_cancel: Common.leave_button(event, button)
            )

    def __add_contact(self):
        w = tk.Toplevel(self.root, width=100, height=50)
        w.wm_transient(self.root)
        w.grab_set()
        w.config(padx=2, pady=2)
        w.title("Kontakt hinzufügen")

        self.button_new_contact.configure(style="Normal.TButton")

        self.__create_add_edit_widgets(w, "add", 0)

        Common.center(w)

    def __edit_contact(self, index):
        w = tk.Toplevel(self.root)
        w.wm_transient(self.root)
        w.grab_set()
        w.config(padx=2, pady=2)
        w.title("Kontakt bearbeiten")

        self.contactEditButtonArray[index].configure(style="Normal.TButton")

        self.__create_add_edit_widgets(w, "edit", index)

        Common.center(w)

    def __delete_contact(self, widget, index):
        self.dbContacts.delete_from_db(index)
        self.checkbuttonArray[index].destroy()
        self.contactEditButtonArray[index].destroy()
        self.__create_contact_entries()

        self.button_new_contact.grid(column=0, row=self.dbContacts.get_num_entries() + 2, padx=2, pady=2, sticky="w")
        self.button_ok.grid(column=2, row=self.dbContacts.get_num_entries() + 3, padx=2, pady=2, sticky="w")
        self.button_settings.grid(column=3, row=self.dbContacts.get_num_entries() + 3, padx=2, pady=2, sticky="w")

        widget.destroy()

    def __create_buttons(self):
        self.button_new_contact = ttk.Button(
            self.root,
            style="Normal.TButton",
            text="neuer Kontakt",
            command=lambda checked_contacts=self.get_checked_contacts: self.__add_contact()
        )
        self.button_ok = ttk.Button(
            self.root,
            style="Normal.TButton",
            text="Senden",
            width=12
        )
        self.button_ok.configure(command=lambda b=self.button_ok: self.mail.send_email(b))

        self.button_settings = ttk.Button(
            self.root,
            style="Normal.TButton",
            text="Einstellungen",
            width=12
        )
        self.button_settings.configure(command=lambda b=self.button_settings: self.settings.open_settings(b))

        self.button_new_contact.grid(column=0, row=self.dbContacts.get_num_entries() + 2, padx=2, pady=2, sticky="w")
        self.button_ok.grid(column=2, row=self.dbContacts.get_num_entries() + 3, padx=2, pady=2, sticky="w")
        self.button_settings.grid(column=3, row=self.dbContacts.get_num_entries() + 3, padx=2, pady=2, sticky="w")

        self.button_ok.bind(
            "<Enter>",
            lambda event, button=self.button_ok: Common.hover_button(event, button)
        )
        self.button_ok.bind(
            "<Leave>",
            lambda event, button=self.button_ok: Common.leave_button(event, button)
        )

        self.button_new_contact.bind(
            "<Enter>",
            lambda event, button=self.button_new_contact: Common.hover_button(event, button)
        )
        self.button_new_contact.bind(
            "<Leave>",
            lambda event, button=self.button_new_contact: Common.leave_button(event, button)
        )

        self.button_settings.bind(
            "<Enter>",
            lambda event, button=self.button_settings: Common.hover_button(event, button)
        )
        self.button_settings.bind(
            "<Leave>",
            lambda event, button=self.button_settings: Common.leave_button(event, button)
        )

    def get_checked_contacts(self):
        checked_contacts = []
        for i in range(len(self.checkbuttonArray) - 1):
            if self.varArray[i].get():
                checked_contacts.append(i)
        return checked_contacts
