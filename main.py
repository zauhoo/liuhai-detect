#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: XuHao Zhang
# @Date  : 2021/01/24
# @Desc  :
# @Contact : xuhaozhang_hfut@163.com


import sys
from PyQt5 import QtWidgets

from detect.detect import Detect


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Detect()
    window.show()
    sys.exit(app.exec_())
