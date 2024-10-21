import json
import cv2
import numpy as np
import argparse
import subprocess


def threshold_func(doc):
    avg = np.mean(doc)
    print(avg)
    if avg < 170:
        doc = 255 - doc
    #threshold = cv2.threshold(doc, 205, 255, cv2.THRESH_BINARY)
    #doc = threshold[1]
    cv2.imwrite('Input.png', doc)
    return doc

def main(doc):
    document = cv2.imread(str(doc))
    doc_black = cv2.cvtColor(document, cv2.COLOR_BGR2GRAY)
    doc_black = threshold_func(doc_black)
    zero_matrix = np.zeros((doc_black.shape[0], doc_black.shape[1], 3), dtype=np.uint8)
    controller = 0
    last_line = 0
    result_cords = []
    first_line = doc_black.shape[1]
    start_row = None
    for i in range(doc_black.shape[0]):
        for j in  range(doc_black.shape[1]):
            if int(doc_black[i,j]) < 170 and controller == 0:
                controller = 1
                last_line = 0
                start_row = i
                break

            if int(doc_black[i,j]) < 170 and controller == 1:
                if last_line < j:
                    last_line = j
                if first_line > j:
                    first_line = j - 1

            if np.all(doc_black[i] > 170) and controller == 1:
                zero_matrix[start_row:i, last_line, 2] = 255 #last column
                zero_matrix[start_row:i, first_line, 2] = 255 #first column
                zero_matrix[start_row, first_line:last_line, 2] = 255 #first row
                zero_matrix[i, first_line:last_line, 2] = 255 #last row
                result_cords.extend([start_row,i,last_line,first_line])

                first_line = doc_black.shape[1]
                last_line = 0
                controller = 0
                break

    for i in range(zero_matrix.shape[0]):
        for j in range(zero_matrix.shape[1]):
            if zero_matrix[i, j, 2] == 255:
                doc_black[i, j] = 0

    result_img = np.stack((doc_black, doc_black, doc_black), axis=-1)
    result_img = result_img + zero_matrix
    cv2.imwrite('Results.png', result_img)
    with open('data.json', 'w') as f:
        json.dump(result_cords, f)
    subprocess.run(['python', 'char-reco.py'])  # calls another file

img_input = argparse.ArgumentParser(description='Document Photo Input')
img_input.add_argument('-i', type=str, required=True)
args = img_input.parse_args()
main(args.i)

## kelime bazlı çalışılacağından dolayı satırda anlamsız kelimelerin bulunmasının bir problem
## yaratmayacağını düşündüm o yüzden işaretlenen satırların arasında oluşan boşlukları silmeye uğraşmadım.