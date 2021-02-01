import os

from pytube import YouTube
from pytube.helpers import safe_filename
from telethon import types
from userbot import CMD_HELP
from userbot.events import register
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error, TIT2, TPE1
from os import environ

msg_for_percantage = types.Message
@register(outgoing=True, pattern=r"^\.ytmp3 (\S*)")
async def youtube_mp3(ytmp3):
    if environ.get("isSuspended") == "True":
        return
    global msg_for_percentage
    reply_message = await ytmp3.get_reply_message()
    url = ytmp3.pattern_match.group(1)

    await ytmp3.edit("**Processing...**")

    video = YouTube(url)
    stream = video.streams.filter(only_audio=True, mime_type="audio/webm").last()
    os.system(f"wget -q -O 'picture.jpg' {video.thumbnail_url}")
    await ytmp3.edit("**Downloading audio...**")
    stream.download(filename='audio')
    await ytmp3.edit("**Converting to mp3...**")
    os.system(f"ffmpeg -loglevel panic -i 'audio.webm' -vn -ab 128k -ar 44100 -y 'song.mp3'")
#   os.system(f"ffmpeg -i 'audio.webm' -vn -ab 128k -ar 44100 -y '{safe_filename(video.title)}.mp3'")
    os.remove("audio.webm")
    
    str = stream.title
    list = str.split("-")
    artist = list[0][:-1]
    song = list[1][1:]
    audio = MP3(f"song.mp3", ID3=ID3)
    try:
        audio.add_tags()
    except error:
        pass
    await ytmp3.edit("**Adding tags...**")
    
    try:
      audio.tags.add(TIT2(text=song))
      audio.tags.add(TPE1(text=artist))
      audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open("picture.jpg",'rb').read()))
      audio.save()
    except:
      pass
    await ytmp3.edit("**Sending mp3...**")
    msg_for_percentage = ytmp3
    await ytmp3.client.send_file(ytmp3.chat.id,
                              f'song.mp3',
                              caption=f"[{video.title}]({url})",
                              reply_to=reply_message, progress_callback=callback)

    await ytmp3.delete()
    os.remove(f'song.mp3')
    try:
      os.remove('picture.jpg')
    except:
      pass
    
async def callback(current, total):
    global msg_for_percentage
    percent = round(current/total * 100, 2)
    await msg_for_percentage.edit(f"**Sending...**\nUploaded `{current}` out of `{total}` bytes: `{percent}%`")

async def resize_photo(photo):
    """ Resize the given photo to 512x512 """

    return image

CMD_HELP.update({"ytmp3": ["YtMP3",
    " - `.ytmp3 (url)`: Convert a YouTube video to a mp3 and send it.\n"
                        ]})
