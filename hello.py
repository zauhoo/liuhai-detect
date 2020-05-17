# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hello.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
import dlib
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(648, 568)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.l_imgPrimary = QtWidgets.QLabel(self.centralwidget)
        self.l_imgPrimary.setGeometry(QtCore.QRect(30, 50, 260, 320))
        self.l_imgPrimary.setObjectName("l_imgPrimary")
        self.l_imgProccessed = QtWidgets.QLabel(self.centralwidget)
        self.l_imgProccessed.setGeometry(QtCore.QRect(340, 50, 260, 320))
        self.l_imgProccessed.setObjectName("l_imgProccessed")
        self.e_threshold = QtWidgets.QLineEdit(self.centralwidget)
        self.e_threshold.setGeometry(QtCore.QRect(170, 450, 81, 20))
        self.e_threshold.setReadOnly(True)
        self.e_threshold.setObjectName("e_threshold")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 440, 71, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 490, 71, 16))
        self.label_2.setObjectName("label_2")
        self.e_area = QtWidgets.QLineEdit(self.centralwidget)
        self.e_area.setGeometry(QtCore.QRect(170, 490, 81, 21))
        self.e_area.setReadOnly(True)
        self.e_area.setObjectName("e_area")
        self.b_readImg = QtWidgets.QPushButton(self.centralwidget)
        self.b_readImg.setGeometry(QtCore.QRect(440, 400, 141, 41))
        self.b_readImg.setObjectName("b_readImg")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(310, 450, 71, 21))
        self.label_3.setObjectName("label_3")
        self.e_result = QtWidgets.QLineEdit(self.centralwidget)
        self.e_result.setGeometry(QtCore.QRect(310, 490, 81, 21))
        self.e_result.setReadOnly(True)
        self.e_result.setObjectName("e_result")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(100, 400, 71, 21))
        self.label_4.setObjectName("label_4")
        self.e_imgPath = QtWidgets.QLineEdit(self.centralwidget)
        self.e_imgPath.setGeometry(QtCore.QRect(170, 400, 221, 21))
        self.e_imgPath.setObjectName("e_imgPath")
        self.b_nextImg = QtWidgets.QPushButton(self.centralwidget)
        self.b_nextImg.setGeometry(QtCore.QRect(440, 470, 141, 41))
        self.b_nextImg.setObjectName("b_nextImg")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 20, 71, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(340, 20, 81, 21))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 648, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.b_readImg.clicked.connect(self.readImage)
        self.b_nextImg.clicked.connect(self.nextImg)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.l_imgPrimary.setText(_translate("MainWindow", "TextLabel"))
        self.l_imgProccessed.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "额头面积："))
        self.label_2.setText(_translate("MainWindow", "当前面积："))
        self.b_readImg.setText(_translate("MainWindow", "开始读取"))
        self.label_3.setText(_translate("MainWindow", "检测结果："))
        self.label_4.setText(_translate("MainWindow", "图片路径："))
        self.b_nextImg.setText(_translate("MainWindow", "下一张"))
        self.label_5.setText(_translate("MainWindow", "原始图片："))
        self.label_6.setText(_translate("MainWindow", "处理后图片："))


    def init(self, MainWindow):
        self.setupUi(MainWindow)
   
    def porccessedImg(self,img):

        imgYcc = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

        rows, cols, channels = img.shape
        # prepare an empty image space
        imgSkin = np.zeros(img.shape, np.uint8)
        # copy original image
        imgSkin = img.copy()
        for r in range(rows):
            for c in range(cols):

                # non-skin area if skin equals 0, skin area otherwise
                skin = 0
                # get values from rgb color space
                B = img.item(r, c, 0)
                G = img.item(r, c, 1)
                R = img.item(r, c, 2)

                # get values from ycbcr color space
                Y  = imgYcc.item(r, c, 0)
                Cr = imgYcc.item(r, c, 1)
                Cb = imgYcc.item(r, c, 2)

                if R > G and R > B:
                    if (G >= B and 5 * R - 12 * G + 7 * B >= 0) or (G < B and 5 * R + 7 * G - 12 * B >= 0):
                        if Cr > 135 and Cr < 180 and Cb > 85 and Cb < 135 and Y > 80:
                            skin = 1

                        # print 'Condition 1 satisfied!'
                if 0 == skin:
                    imgSkin.itemset((r, c, 0), 0)
                    imgSkin.itemset((r, c, 1), 0)
                    imgSkin.itemset((r, c, 2), 0)
        # convert color space of images because of the display difference between cv2 and matplotlib
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgSkin = cv2.cvtColor(imgSkin, cv2.COLOR_BGR2RGB)
        imgGray = cv2.cvtColor(imgSkin, cv2.COLOR_RGB2GRAY)

        ret, imgThresh = cv2.threshold(imgGray, 122, 255, cv2.THRESH_BINARY)
        image, contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 得到轮廓信息
        max_cnt = contours[0]
        max_area = cv2.contourArea(max_cnt)
        for cnt in contours:
            # 计算轮廓所包含的面积
            area = cv2.contourArea(cnt)
            if (area > max_area):
                max_cnt = cnt
                max_area = area

        #人脸分类器
        detector = dlib.get_frontal_face_detector()
        #获取人脸检测器
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        # 取灰度
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        pos = []
        # 人脸数rects
        rects = detector(img_gray, 0)
        for i in range(len(rects)):
            landmarks = np.matrix([[p.x, p.y] for p in predictor(img, rects[i]).parts()])
            for idx, point in enumerate(landmarks):
                # 68点的坐标
                #pos1 = []
                #pos1.append(point[0, 0])
                #pos1.append(point[0, 1])
                pos1 = (point[0, 0], point[0, 1])
                pos.append(pos1)

        max_cnt1=max_cnt.copy()

        for i in range(len(max_cnt)):
            if ((max_cnt1[i][0][1]) > (pos[23][1])):
                max_cnt1[i][0][1] = pos[23][1]
            if ((max_cnt1[i][0][0]) < (pos[0][0])):
                max_cnt1[i][0][0] = pos[0][0]
            if ((max_cnt1[i][0][0]) > (pos[16][0])):
                max_cnt1[i][0][0] = pos[16][0]

        for i in range(len(max_cnt)):
            if ((max_cnt[i][0][1]) < (pos[22][1])):
                max_cnt[i][0][1] = pos[22][1]
            if ((max_cnt[i][0][1]) > (pos[9][1])):
                max_cnt[i][0][1] = pos[9][1]
            if ((max_cnt[i][0][0]) < (pos[0][0])):
                max_cnt[i][0][0] = pos[0][0]
            if ((max_cnt[i][0][0]) > (pos[16][0])):
                max_cnt[i][0][0] = pos[16][0]


        imgProcessed = cv2.drawContours(img, max_cnt1, -1, (0, 255, 255), 5)
        area1 = cv2.contourArea(max_cnt1)
        area2 = cv2.contourArea(max_cnt)
        self.e_area.setText(str(area1))
        self.e_threshold.setText(str(int(area2*0.4)))
        print("1")
        print(type(area))
        if(area2*0.2>area1):
            self.e_result.setText("有眉毛遮挡")
        else:
            self.e_result.setText("无眉毛遮挡")
        print("1")
        return imgProcessed,area1


    def readImage(self):

        print(type(self.e_imgPath.text()))
        self.dirPath=self.e_imgPath.text()
        self.imgFile=[]
        #获取文件夹下所有的‘.jpg’图像
        for filename in os.listdir(self.dirPath):  # listdir的参数是文件夹的路径
            if ('.jpg' in filename):
                self.imgFile.append(filename)
                print(filename)
        self.imgCount=0
        #原始图像显示
        img=cv2.imread(os.path.join(self.dirPath,self.imgFile[self.imgCount]))
        img=cv2.resize(img, (260, 320))
        show=cv2.cvtColor(cv2.resize(img,(260,320)),cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.l_imgPrimary.setPixmap(QtGui.QPixmap.fromImage(showImage))
        #处理后的图像显示
        imgProcessed,area=self.porccessedImg(img)
        #show = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        show = cv2.resize(imgProcessed, (260, 320))
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.l_imgProccessed.setPixmap(QtGui.QPixmap.fromImage(showImage))

        self.imgCount=(self.imgCount+1)%(len(self.imgFile))

    def nextImg(self):

        img = cv2.imread(os.path.join(self.dirPath, self.imgFile[self.imgCount]))
        img = cv2.resize(img, (260, 320))
        show = cv2.cvtColor(cv2.resize(img, (260, 320)), cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.l_imgPrimary.setPixmap(QtGui.QPixmap.fromImage(showImage))
        imgProcessed, area = self.porccessedImg(img)
        # show = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        show = cv2.resize(imgProcessed, (260, 320))
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.l_imgProccessed.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.imgCount = (self.imgCount + 1) % (len(self.imgFile))




