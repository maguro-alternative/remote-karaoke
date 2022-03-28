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

# @bot.command()
# async def start_record(ctx):
# @bot.slash_command(guild_ids=[838937935822585928,854350169055297576])
@bot.slash_command()
async def start_record(ctx):
    print("record")
    await ctx.respond("Recording...")
    file = open('singid.txt', 'w')
    file.write(str(ctx.author.id))
    file.close()
    # if ctx.author.voice.channel is None:
    vc = await ctx.author.voice.channel.connect()

    ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx) # Start the recording

    source = discord.FFmpegPCMAudio("./wave/sample_music.wav")              # ダウンロードしたwavファイルをDiscordで流せるように変換
    trans=discord.PCMVolumeTransformer(source,volume=0.5)
    vc.play(trans)
 
    await asyncio.sleep(src.rank.wavsecond("./wave/sample_music.wav"))

    ctx.voice_client.stop_recording() # Stop the recording, finished_callback will shortly after be called
    await ctx.respond("Stopped! 採点中,,,")
    await ctx.voice_client.disconnect()

async def finished_callback(sink, ctx):
    file = open('singid.txt', 'r')  #送信したメッセージidの読み込み
    singid = int(file.read())
    for user_id, audio in sink.audio_data.items():
        if user_id==singid:
            print(type(audio.file))
            song = AudioSegment.from_file(audio.file, format="mp3")
            #song.export(f"{user_id}.{sink.encoding}", format='mp3')
            song.export("./wave/sample_voice.wav", format='wav')

            # await ctx.channel.send(f"Finished! Recorded audio for {', '.join(recorded_users)}.")
            await ctx.channel.send(f"<@{user_id}> 点数 "+str(src.rank.wavmain())+"点です！")

    

#@bot.slash_command(guild_ids=[838937935822585928,854350169055297576])
@bot.slash_command()
async def stop_recording(ctx):
    print("re")
    ctx.voice_client.stop_recording() # Stop the recording, finished_callback will shortly after be called
    await ctx.respond("Stopped!")
    await ctx.voice_client.disconnect()

#@bot.slash_command(guild_ids=[838937935822585928,854350169055297576])
@bot.slash_command()
async def download(
    ctx: discord.ApplicationContext,
    url: Option(str, required=True, description="urlをいれて", )):
    print(ctx.author)
    await ctx.respond("downloading...") 
    you(url)
    await ctx.channel.send(f"<@{ctx.author.id}> ダウンロード完了! /start_record で採点します。")


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