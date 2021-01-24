#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: XuHao Zhang
# @Date  : 2021/1/16
# @Desc  :
# @Contact : xuhaozhang_hfut@163.com


import os
import dlib
import numpy
import cv2.cv2

from PyQt5 import QtWidgets, QtGui

SHAPE_PREDICTOR = "shape_predictor_68_face_landmarks.dat"


def image_show(img):
    """ """
    show = cv2.resize(img, (260, 320))
    showImage = QtGui.QImage(
        show.data,
        show.shape[1],
        show.shape[0],
        QtGui.QImage.Format_RGB888)

    return showImage


def image_process(img):
    """ """
    # get face contour
    img_skin = _get_skin_image(img)
    face_contour = _get_face_contour(img_skin)
    # get 64 face key point
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    coords = _get_coords(img)
    # correct face contour coordinates with ear point
    for point in face_contour:
        if point[0][0] < coords[0][0]:
            point[0][0] = coords[0][0]
        if point[0][0] > coords[16][0]:
            point[0][0] = coords[16][0]
    # correct face contour coordinates with ear point
    brow_contour = face_contour.copy()
    for point in brow_contour:
        if point[0][1] > coords[24][1]:
            point[0][1] = coords[24][1]
    for point in face_contour:
        if point[0][1] < coords[24][1]:
            point[0][1] = coords[24][1]

    img_process = cv2.drawContours(img, brow_contour, -1, (0, 255, 255), 5)
    area_detect = cv2.contourArea(brow_contour)
    area_predict = cv2.contourArea(face_contour) * 0.2
    value_detect = "有眉毛遮挡" if area_detect < area_predict else "无眉毛遮挡"
    return img_process, area_detect, area_predict, value_detect


def _get_coords(img):
    """ """
    file_path = os.path.abspath(__file__)
    shape_path = os.path.join(os.path.dirname(file_path), SHAPE_PREDICTOR)
    # 人脸分类器
    detector = dlib.get_frontal_face_detector()
    # 获取人脸检测器
    predictor = dlib.shape_predictor(shape_path)
    # 取灰度
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 人脸数rects
    rects = detector(img_gray, 0)
    shape = predictor(img, rects[0])
    coords = numpy.zeros((shape.num_parts, 2), dtype='int')
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    return coords


def _get_skin_image(img):
    """ """
    img_skin = img.copy()
    rows, cols, channels = img.shape
    imgYcc = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    # convert color space of images because of the display difference
    # between cv2 and matplotlib
    for row in range(rows):
        for col in range(cols):
            # get values from rgb color space
            B = img.item(row, col, 0)
            G = img.item(row, col, 1)
            R = img.item(row, col, 2)
            # get values from ycbcr color space
            Y = imgYcc.item(row, col, 0)
            Cr = imgYcc.item(row, col, 1)
            Cb = imgYcc.item(row, col, 2)
            # non-skin area if skin equals 0, skin area otherwise
            skin = 0
            if R > G and R > B:
                if (G >= B and 5 * R - 12 * G + 7 * B >= 0) or \
                        (G < B and 5 * R + 7 * G - 12 * B >= 0):
                    if 135 < Cr < 180:
                        if 85 < Cb < 135:
                            if Y > 80:
                                skin = 1
            if skin == 0:
                img_skin.itemset((row, col, 0), 0)
                img_skin.itemset((row, col, 1), 0)
                img_skin.itemset((row, col, 2), 0)
    return img_skin


def _get_face_contour(img):
    """ """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    # 得到轮廓信息
    ret, imgThresh = cv2.threshold(img_gray, 122, 255, cv2.THRESH_BINARY)
    image, contours, hierarchy = cv2.findContours(
        imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    face_contour = contours[0]
    face_area = cv2.contourArea(face_contour)
    for contour in contours:
        # 计算轮廓所包含的面积
        area = cv2.contourArea(contour)
        if area > face_area:
            face_contour = contour
            face_area = area
    return face_contour
