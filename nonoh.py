#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
    Intentará leer el fichero ~/.nonohrc cuyo contenido debe ser similar a:

    user=usuario
    pass=contraseña
    defaultfrom=3874333333
"""
import os
import sys
import browser
import csv
from collections import defaultdict
from decoradores import Verbose
from debug import debug

RCDIR = os.path.join(os.environ["HOME"], ".nonoh")
CONFIGFILE = os.path.join(RCDIR, "config")
CONTACTSFILE = os.path.join(RCDIR, "contacts")
LOGFILE = os.path.join(RCDIR, "log")

@Verbose(3)
def call(fromphone, tophone):
    b = browser.BROWSER()

    login = b.get_forms("https://www.nonoh.net/myaccount/buycreditpanel.php")[0]
    login["user"] = CONFIG["user"]
    login["pass"] = CONFIG["pass"]
    login.submit()

    if "index.php?part=logoff" in b.get_html():
        debug("Login realizado con exito.")

        call = b.get_forms("https://www.nonoh.net/myaccount/webcalls.php")[0]
        call.set_all_readonly(False)
        call["Countrycode1"] = "+54"
        call["anrphonenr"] = fromphone
        call["Countrycode2"] = "+54"
        call["bnrphonenr"] = tophone
        call.submit()

        return b.get_code == 200

    else:
        debug("Nonmbre de usuario o contraseña incorrectos.")
        return False

def opennocomments(*args, **kwargs):
    return (line for line in open(*args, **kwargs) if not line.startswith("#"))

def main():
    if len(sys.argv) == 3:
        return call(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        return call(CONFIG["defaultfrom"], sys.argv[1])
    else:
        print("""Número de argumentos incorrecto, debe usar:
        nonoh [origen] destino""")

def readconfig():
    valids = (
        "defaultfrom",
        "defaultcode",
        "user",
        "pass",
    )

    config = dict([(row[0].strip(), row[1].strip())
        for row in csv.reader(opennocomments(CONFIGFILE), delimiter="=")
            if row[0].strip() in valids])

    debug(config)
    return config


if __name__ == "__main__":
    CONFIG = readconfig()

    exit(main())
