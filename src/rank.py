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

    # 処理時間計測開始
    start = time.time()

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
        x = x_and_fs[0]
        fs = x_and_fs[1]
        feature = librosa.feature.spectral_centroid(x, fs)
        feature_list.append(feature)

    del x_and_fs_list
    gc.collect()

    # 比較の基準とする特徴量
    reference_index = 0
    reference_feature = feature_list[reference_index]

    del path_list
    gc.collect()

    # 類似度を計算し、リストに格納
    eval_list = []
    for target_feature in feature_list[1::2]:
        ac, wp = librosa.sequence.dtw(reference_feature, target_feature)
        # -1で一番最後の要素を取得
        eval = 1 - (ac[-1][-1] / np.array(ac).max())
        eval_list.append(eval)

    # 類似度を一覧表示
    print("> | {} , {} : {}".format("Reference", "Target", "Score"))
    for target_index in range(len(eval_list)):
        eval = eval_list[target_index]
        print("> | {} , {} : {}".format(reference_index + 1, target_index + 1, round(eval, 4)))

    print("")

    # 処理時間計測終了
    end = time.time()
    # 処理時間表示
    print("Total elapsed time : {}[sec]".format(round(end - start, 4)))
    return eval*100

def wavmain():
    onewav()
    eval=wavcomp()
    return round(eval, 4)

if __name__ == "__main__":
    wavmain()