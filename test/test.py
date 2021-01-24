#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: XuHao Zhang
# @Date  : 2021/1/17
# @Desc  :
# @Contact : xuhaozhang_hfut@163.com


from collections import OrderedDict
import numpy as np
import argparse
import dlib
import cv2


# Step 1: 使用OrderedDict构造面部特征字典
FACIAL_LANDMARKS_68_IDXS = OrderedDict([
    ('jaw', (0, 17)),
    ('right_eyebrow', (17, 22)),
    ('left_eyebrow', (22, 27)),
    ('nose', (27, 36)),
    ('right_eye', (36, 42)),
    ('left_eye', (42, 48)),
    ('mouth', (48, 68))
])


# Step 2: 参数设置
ap = argparse.ArgumentParser()
ap.add_argument('-p', '--shape-predictor',
                default='detect/shape_predictor_68_face_landmarks.dat',
                help='path to facial landmark predictor')
ap.add_argument('-i', '--image', default='images/8.jpg',
                help='path to input image')
args = vars(ap.parse_args())


def shape_to_np(shape, dtype='int'):
    # 创建68*2用于存放坐标
    coords = np.zeros((shape.num_parts, 2), dtype=dtype)
    # 遍历每一个关键点
    # 得到坐标
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    return coords


def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
    # 创建两个copy
    # overlay and one for the final output image
    overlay = image.copy()
    output = image.copy()
    # 设置一些颜色区域
    if not colors:
        colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
                  (168, 100, 168), (158, 163, 32), (163, 38, 32),
                  (180, 42, 220), (0, 0, 255)]

    for (feature_index, feature) in enumerate(FACIAL_LANDMARKS_68_IDXS.keys()):
        # 获取面部特征的坐标区间
        section = FACIAL_LANDMARKS_68_IDXS[feature]
        pts = shape[section[0]:section[1]]
        if feature == 'jaw':
            # 使用cv2.drawContours绘制轮廓图
            cv2.drawContours(overlay, [pts], -1, colors[-1], 2)
        else:
            # 使用cv2.convexHull获得位置的凸包位置
            hull = cv2.convexHull(pts)
            # 使用cv2.drawContours画出轮廓图
            cv2.drawContours(overlay, [hull], -1, colors[feature_index], -1)

    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    return output


# Step 3: 加载人脸检测与关键点定位
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args['shape_predictor'])

# 读取输入数据，预处理，进行图像的维度重构和灰度化
image = cv2.imread(args['image'])
(h, w) = image.shape[:2]
width = 500
r = width / float(w)
dim = (width, int(r * h))
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 4: 进行人脸检测，获得人脸框的位置信息
rects = detector(gray, 1)

# 遍历检测到的框
for (i, rect) in enumerate(rects):
    # Step 5: 对人脸框进行关键点定位
    shape = predictor(gray, rect)
    # Step 6: 将检测到的关键点转换为ndarray格式
    shape = shape_to_np(shape)
    # Step 7: 对字典进行循环
    for (feature, section) in FACIAL_LANDMARKS_68_IDXS.items():
        clone = image.copy()
        cv2.putText(clone, feature, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                    (0, 0, 255), 2)
        # 根据位置画点
        for (x, y) in shape[section[0]:section[1]]:
            cv2.circle(clone, (x, y), 3, (0, 0, 255), -1)

        # Step 8: 使用cv2.boundingRect获得脸部轮廓位置信息
        (x, y, w, h) = cv2.boundingRect(np.array([shape[section[0]:section[1]]]))
        # Step 9: 根据位置提取脸部的图片
        roi = image[y:y + h, x:x + w]
        (h, w) = roi.shape[:2]
        width = 250
        r = width / float(w)
        dim = (width, int(r * h))
        roi = cv2.resize(roi, dim, interpolation=cv2.INTER_AREA)

        # Step 10: 进行画图操作显示每个部分
        cv2.imshow('ROI', roi)
        cv2.imshow('Image', clone)

        cv2.waitKey(0)
    # Step 11:
    # 进行脸部位置的画图;
    # 如果是脸部：进行连线操作，
    # 如果是其他位置，使用cv2.convexHull()获得凸包的位置信息，进行drawcontour进行画图
    output = visualize_facial_landmarks(image, shape)
    cv2.imshow('Image', output)
    cv2.waitKey(0)
cv2.destroyAllWindows()
