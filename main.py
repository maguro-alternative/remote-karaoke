import asyncio
from discord import Option
import discord
from pydub import AudioSegment
import youtube_dl
import json

import src.rank

json_open = open('auth.json', 'r')
json_load = json.load(json_open)

intents = discord.Intents().all()
bot = discord.Bot(intents=intents)
Token=json_load["token"]

@bot.event
async def on_ready():
    print("起動DAAAAAAAAAAAAAA!!")
    activity=discord.Game(name="Remote-Karaoke")

    await bot.change_presence(activity=activity)

@bot.slash_command()
async def start_record(ctx):
    try :   # 再生中かどうか判断
        print(ctx.guild.voice_client.is_playing())
        await ctx.respond("再生中です。")
        return
    except AttributeError:
        print("record")
    # コマンドを使用したユーザーのボイスチャンネルに接続
    try:
        vc = await ctx.author.voice.channel.connect()
        await ctx.respond("Recording...")
        # コマンドを使用したユーザーのIDを書き込む
        file = open('singid.txt', 'w')
        file.write(str(ctx.author.id))
        file.close()
    except AttributeError:
        await ctx.respond("ボイスチャンネルに入ってください。")
        return

    # 録音開始。mp3で帰ってくる。wavだとなぜか壊れる。
    ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx)

    source = discord.FFmpegPCMAudio("./wave/sample_music.wav")              # ダウンロードしたwavファイルをDiscordで流せるように変換
    trans = discord.PCMVolumeTransformer(source,volume=0.3)
    vc.play(trans)  #音源再生

    # 再生終了まで待つ
    await asyncio.sleep(src.rank.wavsecond("./wave/sample_music.wav"))

    ctx.voice_client.stop_recording() # Stop the recording, finished_callback will shortly after be called
    await ctx.respond("Stopped! 採点中,,,")
    await ctx.voice_client.disconnect()

# 録音終了時に呼び出される関数
async def finished_callback(sink, ctx):
    file = open('singid.txt', 'r')  # 歌ったユーザーIDの読み込み
    singid = int(file.read())

    # 録音したユーザーの音声を取り出す
    for user_id, audio in sink.audio_data.items():
        if user_id==singid:     # 歌ったユーザーIDと一致した場合
            print(type(audio.file))
            # mp3ファイルとして書き込み。その後wavファイルに変換。
            song = AudioSegment.from_file(audio.file, format="mp3")
            song.export("./wave/sample_voice.wav", format='wav')

            # 歌っているか判断。時間が原曲の半分以下の場合採点しない。
            wavRatio=src.rank.wavsecond("./wave/sample_voice.wav")/src.rank.wavsecond("./wave/sample_music.wav")
            print(wavRatio)
            if wavRatio>=0.5:
                # 採点結果を表示
                await ctx.channel.send(f"<@{user_id}> 点数 "+str(src.rank.wavmain())+"点です！")
            else:
                await ctx.channel.send(f"<@{user_id}> 歌っている時間が短く、正常に採点出来ませんでした。")

# 録音停止(非推奨)
@bot.slash_command()
async def stop_recording(ctx):
    
    # 録音停止
    ctx.voice_client.stop_recording() 
    await ctx.respond("Stopped!")
    # ボイスチャンネルから切断
    # await ctx.voice_client.disconnect()

# 音源ダウンロード
@bot.slash_command()
async def download(
    ctx: discord.ApplicationContext,
    url: Option(str, required=True, description="urlをいれて", )):

    try :   # 再生中か判断
        print(ctx.guild.voice_client.is_playing())
        await ctx.respond("再生中です。")
        return
    except AttributeError:
        print("download")

    await ctx.respond("downloading...\n"+url) 
    # youtube-dlでダウンロード
    you(url)
    await ctx.channel.send(f"<@{ctx.author.id}> ダウンロード完了! /start_record で採点します。")

# テスト用
@bot.slash_command()
async def test(ctx):
    await ctx.respond("test")
    print(ctx.author.voice.channel)
    # print(ctx.guild.voice_client.is_playing())

# youtube-dlでダウンロード
def you(test_video):
  # test_video = 'https://www.youtube.com/watch?v=smhoJzDiiwE'
  filename = "./wave/sample_music"

  ydl_opts = {
      'format': 'bestaudio/best',
      'outtmpl':  filename + '.%(ext)s',
      'postprocessors': [
          {'key': 'FFmpegExtractAudio',
          'preferredcodec': 'wav',
          'preferredquality': '192'},
          {'key': 'FFmpegMetadata'},
      ],
  }

  ydl = youtube_dl.YoutubeDL(ydl_opts)
  info_dict = ydl.extract_info(test_video, download=True)

bot.run(Token)