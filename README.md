# remote-karaoke
Discord上で行うカラオケbot

# 概要
youtube-dlで音源を用意、Discordのボイスチャンネルで録音。
DTWで採点。

# 使い方
スラッシュコマンドを使用します。
```bash
# 音源ダウンロード
/download url
# 採点スタート
/start_record
# 中断
/stop_recording
```

# 使うライブラリ
環境 Python 3.8.6 64-bit <br>
ffmpeg <https://ffmpeg.org/download.html><br>

```bash
pip install discord
pip install git+https://github.com/Pycord-Development/pycord
pip install ffmpeg-python
pip install librosa
pip install numpy
pip install pydub
pip install youtube-dl
```