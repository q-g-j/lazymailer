# -*- coding: utf-8 -*-

import os
import sys
import platform
from shutil import copyfile
import tkinter as tk
from tkinter import ttk
from libs.fonts import Fonts


class Common:
    script_path = ""
    config_folder = ""

    @staticmethod
    def set_script_path():
        if hasattr(sys, '_MEIPASS'):
            Common.script_path = getattr(sys, '_MEIPASS') + "/"
        else:
            Common.script_path = os.path.abspath(".") + "/"

    @staticmethod
    def set_icon(root):
        img = tk.PhotoImage(file=Common.script_path + "icon_32x32.png")
        root.iconphoto(False, img)

    @staticmethod
    def create_config_folder():
        if platform.system() == "Windows":
            config_base_folder = os.path.expandvars("%APPDATA%\\")
            Common.config_folder = config_base_folder + "lazymailer\\"
        elif platform.system() == "Linux":
            config_base_folder = os.path.expanduser("~/.config/")
            Common.config_folder = config_base_folder + "lazymailer/"
        elif platform.system() == "Darwin":
            config_base_folder = os.path.expanduser("~/.config/")
            Common.config_folder = config_base_folder + "lazymailer/"
        if not os.path.exists(Common.config_folder):
            os.mkdir(Common.config_folder)

    @staticmethod
    def copy_contacts_template():
        if not os.path.isfile(Common.config_folder + "contacts.db"):
            if os.path.isfile(Common.script_path + "contacts_template.db"):
                copyfile(Common.script_path + "contacts_template.db", Common.config_folder + "contacts.db")
        if not os.path.isfile(Common.config_folder + "smtp.db"):
            if os.path.isfile(Common.script_path + "smtp_template.db"):
                copyfile(Common.script_path + "smtp_template.db", Common.config_folder + "smtp.db")

    @staticmethod
    def set_theme(root, db_settings):
        root.tk.call("source", Common.script_path + "/themes/sun-valley/sun-valley.tcl")

        if db_settings.get_data("darkmode"):
            root.tk.call("set_theme", "dark")
        else:
            root.tk.call("set_theme", "light")

    @staticmethod
    def set_styles():
        style = ttk.Style()
        style.configure(
            "Normal.TButton",
            font=Fonts.font_main
        )
        style.configure(
            "Accent.TButton",
            font=Fonts.font_main
        )
        style.configure(
            "TCheckbutton",
            font=Fonts.font_main
        )

    @staticmethod
    def center(win):
        win.withdraw()
        win.update_idletasks()
        # frm_height = win.winfo_rooty() - win.winfo_y()
        x = (win.winfo_screenwidth() - win.winfo_reqwidth()) / 2
        y = (win.winfo_screenheight() - win.winfo_reqheight()) / 2
        win.geometry("+%d+%d" % (x, y))
        win.deiconify()

    @staticmethod
    def tab_pressed(event):
        event.widget.tk_focusNext().focus()
        return "break"

    @staticmethod
    def hover_button(event, button):
        if event:
            button.configure(style="Accent.TButton")
        return "break"

    @staticmethod
    def leave_button(event, button):
        if event:
            button.configure(style="Normal.TButton")
        return "break"
