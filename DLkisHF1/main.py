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
import matplotlib.gridspec as GridSpec
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
dst_img = "/home/deak/PycharmProjects/DeepLearning/DLkisHF1/images/"

arr = np.array(Image.open(os.path.join(dst_img, "kakashi.png")))
print("Shape of array: ", arr.shape)
print("Dimensions of array: ", arr.ndim)


#listing files in images folder
list_img = os.listdir(dst_img)#iterating over dst_image to get the images as arrays

print("Number of files: ", len(list_img))

test_arr = np.array([['R', 'G', 'B'], [0, 1, 2]])
print("test_arr: ", test_arr[0, :])
# plt.bar(test_arr[0, :], test_arr[1, :])
# plt.show()
i = 0

for image in sorted(list_img):
    [file_name, ext] = os.path.splitext(image) #splitting file name from its extension
    arr = np.array(Image.open(os.path.join(dst_img, image))) #creating arrays for all the images
    [h, w] = np.shape(arr)[0:2]#calculating height and width for each image
    arr_dim = arr.ndim #calculating the dimension for each array
    arr_shape = arr.shape #calculating the shape for each array
    # plt.imshow(arr)
    if arr_dim == 2:
        # img = Image.fromarray(arr, 'L')
        arr_mean = np.mean(arr)
        arr_std = np.std(arr)
        print(f'[{file_name}, greyscale mean={arr_mean:.1f}], greyscale std={arr_std:.1f}')
        fig, ax = plt.subplots(2, 1)
        plt.subplot(211)
        plt.imshow(arr)
        plt.subplot(212)
        plt.hist(arr.ravel(), bins=256, fc='k', ec='k')
        plt.title('GreyScale')
        fig.tight_layout()
        plt.show()
    else:
        arr_mean = np.mean(arr, axis=(0, 1))
        arr_std = np.std(arr, axis=(0, 1))
        print(np.mean(arr[:, :, 0]))
        print(np.mean(arr[:, :, 1]))
        print(np.mean(arr[:, :, 2]))
        arr_standard = arr/256 - 0.5
        print(np.mean(arr_standard[:, :, 2]))
        print(np.mean(arr[:, :, 2])/256 - 0.5)
        if len(arr_mean) == 3: #RGB CASE
            fig, ax = plt.subplots(2, 2)
            plt.subplot(221)
            plt.imshow(arr)
            print(f'[{file_name}, mean: R={arr_mean[0]:.1f}, G={arr_mean[1]:.1f}, B={arr_mean[2]:.1f}, std: R={arr_std[0]:.1f}, G={arr_std[1]:.1f}, B={arr_std[2]:.1f}]')
            plt.subplot(222)
            plt.hist(arr[:, :, 0].ravel(), bins=256, fc='k', ec='k')
            plt.title('R')
            plt.subplot(223)
            plt.hist(arr[:, :, 1].ravel(), bins=256, fc='k', ec='k')
            plt.title('G')
            plt.subplot(224)
            plt.hist(arr[:, :, 2].ravel(), bins=256, fc='k', ec='k')
            plt.title('B')
            print(arr[:, :, 1].shape)

            # SCALING:
            scaler = StandardScaler().fit(arr[:, :, 0])
            arr_standard = scaler.transform(arr[:, :, 0])
            print("scaled array: ", arr_standard)
            fig.tight_layout()
            plt.show()
        else: #ALPHA CASE
            print(f'[{file_name}, R={arr_mean[0]:.1f}, G={arr_mean[1]:.1f}, B={arr_mean[2]:.1f}, ALPHA={arr_mean[3]:.1f}, '
                  f'std: R={arr_std[0]:.1f}, G={arr_std[1]:.1f}, B={arr_std[2]:.1f}, ALPHA={arr_std[3]:.1f}]')
            print(arr.shape)
            fig = plt.figure(figsize=(15, 5))
            gs = GridSpec.GridSpec(nrows=2, ncols=3)
            fig.add_subplot(gs[:, 0])
            plt.imshow(arr)
            fig.add_subplot(gs[0, 1])
            plt.hist(arr[:, :, 0].ravel(), bins=256, fc='k', ec='k')
            plt.title('R')
            fig.add_subplot(gs[0, 2])
            plt.hist(arr[:, :, 1].ravel(), bins=256, fc='k', ec='k')
            plt.title('G')
            fig.add_subplot(gs[1, 1])
            plt.hist(arr[:, :, 2].ravel(), bins=256, fc='k', ec='k')
            plt.title('B')
            fig.add_subplot(gs[1, 2])
            plt.hist(arr[:, :, 3].ravel(), bins=256, fc='k', ec='k')
            plt.title('A')
            fig.tight_layout()
            plt.show()
    i += 1




