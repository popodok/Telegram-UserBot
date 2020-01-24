import os

from moviepy import editor as mp
from pytube import YouTube
from pytube.helpers import safe_filename
from userbot.utils import parse_arguments, extract_urls
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.ytmp3 (\S*)")
async def youtube_mp3(yt):
    reply_message = await yt.get_reply_message()
    params = e.pattern_match.group(1) or ""
    args, params = parse_arguments(params, ['reuse'])
    url = extract_urls(params)
    url.extend(extract_urls(reply_message.text or ""))

    print(url)

    if not url:
        await e.edit("Need a URL to convert", delete_in=3)
        return

    await yt.edit("**Processing...**")

    video = YouTube(url)
    stream = video.streams.filter(progressive=True,
                                  subtype="mp4").first()

    await yt.edit("**Downloading video...**")
    stream.download(filename='video')

    await yt.edit("**Converting video...**")
    clip = mp.VideoFileClip('video.mp4')
    clip.audio.write_audiofile(f'{safe_filename(video.title)}.mp3')

    await yt.edit("**Sending mp3...**")
    await yt.client.send_file(yt.chat.id,
                              f'{safe_filename(video.title)}.mp3',
                              caption=f"{video.title}",
                              reply_to=reply_message)

    await yt.delete()

    os.remove('video.mp4')
    os.remove(f'{safe_filename(video.title)}.mp3')


CMD_HELP.update({
    ".ytmp3":
    "Convert a YouTube video to a mp3 and send it.\n"
    ".ytmp3 (url)"
})
