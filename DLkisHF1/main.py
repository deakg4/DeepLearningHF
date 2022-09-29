# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


"""
    1. Python nyelven olvass be öt darab tetszőleges 256x256 pixeles színes képet, jelenítsd meg és jelenítsd meg külön az
    R, G és B csatornák értékeit hisztogramon. (4p)
    2. Csatornánként számold ki a pixelek átlagát és szórását minden képre, majd alakítsd át ezeket 0 várható értékű,
    1 szórású adathalmazzá. Ezt követően ellenőrizd a kapott adathalmaz várható értékét és szórását. (4p)
    3. Olvass be két tetszőleges hangfájlt és jelenítsd meg ezek spektrogramját. (4p)
    4. Alakítsd át a spektogramokat 0 várható értékű és 1 szorású adathalmazzá. Ezt követően ellenőrizd a kapott
    adathalmaz várható értékét és szórását. (4p)
    5. Python scriptből töltsd le a http://smartlab.tmit.bme.hu/oktatas-deep-learning oldal szöveges tartalmát,
    jelenítsd meg a szöveges tartalmat, továbbá hisztogramon jelenítsd meg a tartalomban a betűk előfordulásának gyakoriságát. (4p)
"""

import numpy as np
from PIL import Image
from tabulate import tabulate
import os
import matplotlib.pyplot as plt
dst_img = "/home/deak/PycharmProjects/DeepLearning/DLkisHF1/images/"

arr = np.array(Image.open(os.path.join(dst_img, "kakashi.png")))
print("Shape of array: ", arr.shape)
print("Dimensions of array: ", arr.ndim)


#listing files in images folder
list_img = os.listdir(dst_img)#iterating over dst_image to get the images as arrays

print("Number of files: ", len(list_img))
images_arr = np.zeros([len(list_img), 258, 258])
print("images_arr: ", images_arr)

test_arr = np.array([['R', 'G', 'B'], [0, 1, 2]])
print("test_arr: ", test_arr[0, :])
plt.bar(test_arr[0, :], test_arr[1, :])
# plt.show()
i = 0
for image in sorted(list_img):
    [file_name, ext] = os.path.splitext(image) #splitting file name from its extension
    arr = np.array(Image.open(os.path.join(dst_img, image))) #creating arrays for all the images
    [h, w] = np.shape(arr)[0:2]#calculating height and width for each image
    arr_dim = arr.ndim #calculating the dimension for each array
    arr_shape = arr.shape #calculating the shape for each array
    images_arr[i, :, :] = arr
    if arr_dim == 2:
        arr_mean = np.mean(arr)
        print(f'[{file_name}, greyscale={arr_mean:.1f}]')
    else:
        arr_mean = np.mean(arr, axis=(0, 1))
        if len(arr_mean) == 3: #RGB CASE
            print(f'[{file_name}, R={arr_mean[0]:.1f},  G={arr_mean[1]:.1f}, B={arr_mean[2]:.1f} ]')
        else: #ALPHA CASE
            print(f'[{file_name}, R={arr_mean[0]:.1f}, G={arr_mean[1]:.1f}, B={arr_mean[2]:.1f}, ALPHA={arr_mean[3]:.1f}]')
    i += 1




