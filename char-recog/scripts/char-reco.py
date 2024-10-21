
import os
import json
import cv2


file_dir = os.path.dirname(__file__)
upper_path = os.path.join(file_dir, '..')
new_folder_dir = os.path.join(upper_path, 'line-data')

try:
    os.makedirs(new_folder_dir,exist_ok=False)
except FileExistsError:
    try:
        os.rmdir(new_folder_dir)
        os.makedirs(new_folder_dir, exist_ok=False)
    except OSError or FileExistsError:
        for files in os.listdir(new_folder_dir):
            file_dir = os.path.join(new_folder_dir, files)
            os.remove(file_dir)
    os.rmdir(new_folder_dir)
    os.makedirs(new_folder_dir, exist_ok=False)

with open('data.json', 'r') as f:
    cords = json.load(f)

j1 = []
j2 = []
i1 = []
i2 = []
counter = 0

for i in range(len(cords)):
    counter += 1
    if counter == 1:
        i1.append(cords[i])
    elif counter == 2:
        i2.append(cords[i])
    elif counter == 3:
        j2.append(cords[i])
    elif counter == 4:
        j1.append(cords[i])
        counter = 0

print(j1)
print(j2)
print(i1)
print(i2)
img_input = cv2.imread(str('Input.png'))

for i in range(len(i1)):
    img_input = img_input[i1[i]-1:i2[i]+1, j1[i]-1:j2[i]+1]
    cv2.imwrite('{}\\output{}.png'.format(new_folder_dir, i+1), img_input)
    img_input = cv2.imread(str('Input.png'))


cv2.imshow('out', img_input)
cv2.waitKey(0)


#Bu sistem sıraları bulmak için güzel bir sistem olabilir ama fotoğradı işlemede kötü
#burda araştırmaya devam etmek ve karakterleri daha güzel göstermek için çalışıcağım


