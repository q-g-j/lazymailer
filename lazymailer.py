# -*- coding: utf-8 -*-


import tkinter as tk
from libs.common import Common
from libs.mainwindow import MainWindow


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    root.title('lazymailer')
    root.resizable(width=False, height=False)

    Common.set_script_path()
    Common.create_config_folder()
    Common.set_icon(root)
    Common.copy_contacts_template()

    MainWindow(root)

    root.mainloop()
