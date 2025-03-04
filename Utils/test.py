import cv2
import numpy as np

# 读取图像
image = cv2.imread('/Users/Jenius/Desktop/line.png', cv2.IMREAD_GRAYSCALE)

circles = cv2.HoughCircles()
