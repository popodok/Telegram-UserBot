import os

from pytube import YouTube
from pytube.helpers import safe_filename
from requests import get
from telethon import types
from userbot import CMD_HELP
from userbot import bot
from userbot.events import register
from userbot.utils import parse_arguments
from os import environ

msg_for_percentage = types.Message

@register(outgoing=True, pattern=r"^\.ytdl (.*)")
async def download_video(v_url):
    if environ.get("isSuspended") == "True":
        return
    """ For .ytdl command, download videos from YouTube. """
    global msg_for_percentage
    query = v_url.pattern_match.group(1)
    opts, url = parse_arguments(query, ['res'])
    quality = opts.get('res', None)

    await v_url.edit("**Fetching...**")

    video = YouTube(url)

    if quality:
        video_stream = video.streams.filter(progressive=True,
                                            subtype="mp4",
                                            res=quality).first()
    else:
        video_stream = video.streams.filter(progressive=True,
                                            subtype="mp4").first()

    if video_stream is None:
        all_streams = video.streams.filter(progressive=True,
                                           subtype="mp4").all()
        available_qualities = ""

        for item in all_streams[:-1]:
            available_qualities += f"{item.resolution}, "
        available_qualities += all_streams[-1].resolution

        await v_url.edit("**A stream matching your query wasn't found. "
                         "Try again with different options.\n**"
                         "**Available Qualities:**\n"
                         f"{available_qualities}")
        return

    video_size = video_stream.filesize / 1000000

    if video_size >= 50:
        await v_url.edit(
            ("**File larger than 50MB. Sending the link instead.\n**"
             f"Get the video [here]({video_stream.url})\n\n"
             "**If the video plays instead of downloading, "
             "right click(or long press on touchscreen) and "
             "press 'Save Video As...'(may depend on the browser) "
             "to download the video.**"))
        return

    await v_url.edit("**Downloading...**")

    video_stream.download(filename="videoytdl.mp4")

    url = f"https://img.youtube.com/vi/{video.video_id}/maxresdefault.jpg"
    resp = get(url)
    with open('thumbnail.jpg', 'wb') as file:
        file.write(resp.content)
    msg_for_percentage = v_url
    await v_url.edit("**Uploading...**")
    await v_url.client.send_file(v_url.chat_id,
                        "videoytdl.mp4",
                        caption=f"{video.title}",
                        thumb="thumbnail.jpg", progress_callback=callback)

    os.remove("videoytdl.mp4")
    os.remove('thumbnail.jpg')
    await v_url.delete()

    
async def callback(current, total):
    global msg_for_percentage
    percent = round(current/total * 100, 2)
    await msg_for_percentage.edit(f"**Sending...**\nUploaded `{current}` out of `{total}` bytes: `{percent}%`")
    
    
CMD_HELP.update({"ytdl": ["YtDl",
    " - `.ytdl`: Download a video from YouTube.\n"
    " - `ytdl [options] (url)`: .res: Resolution\n"
                        ]})
