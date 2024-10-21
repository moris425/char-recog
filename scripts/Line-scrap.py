import cv2
import numpy


def main():
    test_img = cv2.imread('C:\\Users\\Mert\\PycharmProjects\\char-recog\\line-data\\output1.png')
    der_test = cv2.Sobel(test_img, cv2.CV_64F, 0, 1, ksize=3)
    cv2.imwrite('der.png', der_test)







main()
