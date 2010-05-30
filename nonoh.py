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
from decoradores import Verbose
from debug import debug

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
        debug("Nombre de usuario o contraseña incorrectos.")
        return False


def main():
    if len(sys.argv) == 3:
        return call(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        return call(CONFIG["defaultfrom"], sys.argv[1])
    else:
        print """Número de argumentos incorrecto, debe usar:
        nonoh [origen] destino"""

if __name__ == "__main__":
    CONFIG = dict([line.strip().split("=")
        for line in open(os.environ["HOME"] + "/.nonohrc").readlines()])
    exit(main())
