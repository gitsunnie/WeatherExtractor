# -*- coding: utf-8 -*-

# Web �A�v���̃R�[�h (�_�~�[)

import os
from bottle import route, run


@route("/")
def hello_world():
    return "" # �����ŕԂ����e�͉��ł��悢

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))