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
from scipy.io import wavfile
from scipy import signal
from scipy.fft import fftshift
from mp3towav import mp3towav

""" 1. Python nyelven olvass be öt darab tetszőleges 256x256 pixeles színes képet, jelenítsd meg és jelenítsd meg külön az
        R, G és B csatornák értékeit hisztogramon. (4p)
    2. Csatornánként számold ki a pixelek átlagát és szórását minden képre, majd alakítsd át ezeket 0 várható értékű,
        1 szórású adathalmazzá. Ezt követően ellenőrizd a kapott adathalmaz várható értékét és szórását. (4p)"""

dst_img = os.getcwd() + "/images/"
dst_snd = os.getcwd() + "/sounds/"
mp3towav(dst_snd)   # convert mp3s to wav files

#listing files in images folder
list_img = os.listdir(dst_img)#iterating over dst_image to get the images as arrays
list_snd = os.listdir(dst_snd)#iterating over dst_sounds to get the sounds as arrays

seconds = 30    # length of calculated spectrogram
i = 0
mode = 1

if mode < 1:
    for image in sorted(list_img):
        [file_name, ext] = os.path.splitext(image)
         #splitting file name from its extension
        arr = np.array(Image.open(os.path.join(dst_img, image))) #creating arrays for all the images
        [h, w] = np.shape(arr)[0:2]#calculating height and width for each image
        arr_dim = arr.ndim #calculating the dimension for each array
        arr_shape = arr.shape #calculating the shape for each array
        # plt.imshow(arr)
        if arr_dim == 2:
            # img = Image.fromarray(arr, 'L')
            arr_mean = np.mean(arr)     # calculating the mean for array
            arr_std = np.std(arr)   # calculating the standard deviation for array
            print(f'[{file_name}, greyscale mean={arr_mean:.1f}], greyscale std={arr_std:.1f}')     # plotting the mean and the std
            fig, ax = plt.subplots(2, 1)
            plt.subplot(211)
            plt.imshow(arr)     # plot the image
            plt.subplot(212)
            plt.hist(arr.ravel(), bins=256, fc='k', ec='k')     # plot the grayscale values
            plt.title('GreyScale')
            fig.tight_layout()
            plt.show()
            # SCALING:
            scaler = StandardScaler().fit(arr)      # standardizing the array
            arr_standard = scaler.transform(arr)
            arr_mean_standard = np.mean(arr_standard)       # calculating the mean after standardization
            arr_std_standard = np.std(arr_standard)     # calculating the std after standardization
            print(f'[{file_name}, greyscale standard mean={arr_mean_standard:.1f}], greyscale standard std={arr_std_standard:.1f}')     # print the calculated values
        else:
            arr_mean = np.mean(arr, axis=(0, 1))    # calculating the mean for array
            arr_std = np.std(arr, axis=(0, 1))      # calculating the standard deviation for array
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
                arr_standard = np.full_like(arr, 0)
                print("arr_standard.shape: ", arr_standard.shape, "arr.shape: ", arr.shape)

                for j in range(len(arr_mean)):
                    # SCALING:
                    scaler = StandardScaler().fit(arr[:, :, j])
                    arr_standard[:, :, j] = scaler.transform(arr[:, :, j])
                arr_mean_standard = np.mean(arr_standard, axis=(0, 1))
                arr_std_standard = np.std(arr_standard, axis=(0, 1))
                print(f'[{file_name}, standard mean: R={arr_mean_standard[0]:.1f}, G={arr_mean_standard[1]:.1f}, '
                      f'B={arr_mean_standard[2]:.1f}, standard std: R={arr_std_standard[0]:.1f}, '
                      f'G={arr_std_standard[1]:.1f}, B={arr_std_standard[2]:.1f}]')

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

                for J in range(len(arr_mean)):
                    # SCALING:
                    scaler = StandardScaler().fit(arr[:, :, J])
                    arr_standard = scaler.transform(arr[:, :, J])
                    print("scaled array: ", arr_standard)
        i += 1

if mode < 2:
    """
        3. Olvass be két tetszőleges hangfájlt és jelenítsd meg ezek spektrogramját. (4p)
        4. Alakítsd át a spektogramokat 0 várható értékű és 1 szorású adathalmazzá. Ezt követően ellenőrizd a kapott
            adathalmaz várható értékét és szórását. (4p)
        """

    for sound in sorted(list_snd):
        [file_name, ext] = os.path.splitext(sound)
        if ext == ".wav":
            samplerate, data = wavfile.read(os.path.join(dst_snd, sound))
            print("sample rate: ", samplerate)
            # print("data: ", data)
            data_left = data[:, 0]
            data_cut = data_left[:int(samplerate*seconds)]   # trim the firs 30 second
#            f, t, Sxx = signal.spectrogram(data_cut, samplerate)   # if the output is onesided
#            print("f: ", len(f))
#            print("t: ", len(t))
            powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(data_left, Fs=samplerate)
            plt.ylabel('Frequency [Hz]')
            plt.xlabel('Time [sec]')
            plt.show()
            print("mean of the powerSpectrum= ", np.mean(powerSpectrum))
            scaler = StandardScaler().fit(powerSpectrum)
            powerSpectrum_standard = scaler.transform(powerSpectrum)
            print("powerSpectrum_standard.shape: ", powerSpectrum_standard.shape)
            print(np.mean(powerSpectrum_standard))


