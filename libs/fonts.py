# -*- coding: utf-8 -*-

import platform


class Fonts:
    if platform.system() == "Darwin":
        font_main = (
            "Segoe UI",
            12,
            "normal"
        )
        font_block = (
            "Courier",
            12,
            "normal"
        )
        font_title = (
            "Segoe UI",
            14,
            "bold"
        )
    else:
        font_main = (
            "Segoe UI",
            10,
            "normal"
        )
        font_block = (
            "Courier",
            10,
            "normal"
        )
        font_title = (
            "Segoe UI",
            12,
            "bold"
        )
