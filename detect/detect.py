#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : detect.py
# @Author: XuHao Zhang
# @Date  : 2021/1/16
# @Desc  :
# @Contact : xuhaozhang_hfut@163.com


import cv2

from detect.utils import *
from client.client import Ui_MainWindow


class Detect(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.b_readImg.clicked.connect(self.image_read)
        self.ui.b_prevImg.clicked.connect(self.image_prev)
        self.ui.b_nextImg.clicked.connect(self.image_next)

        self.img_count = 0
        self.dir_path = None
        self.img_file = list()

    def _setting_detect_information(self, img_count):
        """ """
        img = cv2.imread(os.path.join(self.dir_path, self.img_file[img_count]))
        # 原始图像显示
        img_primary = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        show_primary = image_show(img_primary)
        # 处理图像显示
        img_process, area_detect, area_predict, value_detect = image_process(
            img)
        show_process = image_show(img_process)
        self.ui.l_imgPrimary.setPixmap(QtGui.QPixmap.fromImage(show_primary))
        self.ui.l_imgProcess.setPixmap(QtGui.QPixmap.fromImage(show_process))
        self.ui.e_areaDetect.setText(str(int(area_detect)))
        self.ui.e_areaPredict.setText(str(int(area_predict)))
        self.ui.e_valueDetect.setText(value_detect)

    def image_read(self):
        """ """
        # 获取文件夹下所有的‘.jpg’图像
        self.dir_path = self.ui.e_imgPath.text()
        self.img_file = os.listdir(self.dir_path)

        self._setting_detect_information(self.img_count)

    def image_prev(self):
        """ """
        self.img_count = (self.img_count - 1) % (len(self.img_file))

        self._setting_detect_information(self.img_count)

    def image_next(self):
        """ """
        self.img_count = (self.img_count + 1) % (len(self.img_file))

        self._setting_detect_information(self.img_count)
