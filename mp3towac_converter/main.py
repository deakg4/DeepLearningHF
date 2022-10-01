import os
from pydub import AudioSegment
# files

dst_snd = "/home/deak/PycharmProjects/DeepLearning/DLkisHF1/sounds/"
list_snd = os.listdir(dst_snd)#iterating over dst_sounds to get the sounds as arrays
# convert wav to mp3
for sound in list_snd:
    [file_name, ext] = os.path.splitext(sound)
    if ext == ".mp3":
        sound = AudioSegment.from_mp3(os.path.join(dst_snd, sound))
        file_name = file_name + ".wav"
        sound.export(os.path.join(dst_snd, file_name), format="wav")
