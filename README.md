# remote-karaoke
Discord上でカラオケを行うbot

# 概要
youtube-dlで音源を用意、Discordのボイスチャンネルで録音。
DTWで採点。

# 使い方
auth.jsonにDiscord Botのトークンを入れます。
```bash
{
    "token" : "ここにDiscord Botのトークンを入れる"
}
```
スラッシュコマンドを使用します。
```bash
# 音源ダウンロード
/download url
# 採点スタート
/start_record
# 中断
/stop_recording
```
![](./pic/sample.png)

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