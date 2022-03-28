import gc
import time

import librosa
import numpy as np
import wave
from pydub import AudioSegment

def wavbase(wav):   #wavファイルを開く
    base_sound = AudioSegment.from_file(wav, format="wav")
    return base_sound

def getSamplingFrequency(path):
    wr = wave.open(path, "r")
    fs = wr.getframerate()
    wr.close()
    return fs

def wavsecond(wav): #wavファイルの秒数を計算
    base_sound = AudioSegment.from_file(wav, format="wav")
    return base_sound.duration_seconds

def onewav():   #wavファイルの秒数を60秒以内に収める
    values=["./wave/sample_music.wav","./wave/sample_voice.wav"]
    for value in values:
        time=wavbase(value).duration_seconds

        if time>=60:
            speed = time/60
            base_sound = wavbase(value).speedup(playback_speed=speed, crossfade=0)
        else :
            base_sound=wavbase(value)

        base_sound.export(value, format="wav")


def wavcomp():

    path_list=["./wave/sample_music.wav","./wave/sample_voice.wav"]
    
    # 各wavファイルの振幅データ列とサンプリング周波数を取得し、リストに格納
    x_and_fs_list = []
    for path in path_list:
        x, fs = librosa.load(path, getSamplingFrequency(path))
        x_and_fs_list.append((x, fs))
        print(path+" サンプリング周波数 "+str(getSamplingFrequency(path))+"Hz")

    # 使用する特徴量を抽出し、リストに格納
    feature_list = []
    for x_and_fs in x_and_fs_list:
        feature = librosa.feature.spectral_centroid(x_and_fs[0], x_and_fs[1])
        feature_list.append(feature)

    del x_and_fs_list
    gc.collect()

    del path_list
    gc.collect()

    # 類似度を計算し、リストに格納
    eval_list = []
    ac, wp = librosa.sequence.dtw(feature_list[0], feature_list[1])
    # -1で一番最後の要素を取得
    eval = 1 - (ac[-1][-1] / np.array(ac).max())
    print("Score : {}".format(round(eval,4)))

    return eval*100

def wavmain():
    onewav()
    eval=wavcomp()
    return round(eval, 4)

if __name__ == "__main__":
    wavmain()