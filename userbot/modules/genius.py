from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP, GENIUS_API
from userbot.events import register
from userbot.utils import get_args_split_by
from userbot.modules.spotify import get_info
from requests import get
import lyricsgenius
from os import environ
from json import loads



@register(outgoing=True, pattern=r"^\.lyrics(.*)")
async def gen(e):
      if environ.get("isSuspended") == "True":
        return
      if GENIUS_API is None:
        await e.edit("**We don't support magic! No Genius API!**")
        return
      else:
            genius = lyricsgenius.Genius(GENIUS_API)
      args = get_args_split_by(e.pattern_match.group(), ",")
      if len(args) == 2:
            song_name = args[0]
            artist = args[1]
            await e.edit("**Searching for song **" + song_name + "** by **" + artist)
            song = genius.search_song(song_name, artist)
      else:
            await e.edit("**Trying to get Spotify lyrics...**")
            data = get_info()
            if data:
              try:
                temp = data['device']
              except:
                e.edit("Old exception detected. Please, try again :c")
                return
              isLocal = data['item']['is_local']
              if data['item']['artists'][0]['name'] == "":
                isArtist = False
              if isLocal:
                artist = data['item']['artists'][0]['name']
                song_name = data['item']['name']
                isArtist = True
                link = ""
              else:
                artist = data['item']['album']['artists'][0]['name']
                song_name = data['item']['name']
                link = data['item']['external_urls']['spotify']
                isArtist = True
                await e.edit("**Searching for song **" + song_name + "** by **" + artist)
                song = genius.search_song(song_name, artist)
      if song is None:
        await e.edit("**Can't find song **" + song_name + "** by **" + artist)
        return
      
      elif len(song.lyrics) > 4096:
        await e.edit("**Lyrics for: **" + artist + " - " + song_name + "\n")
        msgs = [song.lyrics[i:i + 4096] for i in range(0, len(song.lyrics), 4096)]
        for text in msgs:
          await e.client.send_message(e.chat_id, text)
        
      else:
        await e.edit("**Lyrics for: **" + artist + " - " + song_name + "\n" + song.lyrics)
      
CMD_HELP.update({"lyrics": ["Lyrics",
    " - `.lyrics <song>, <author>`: Search lyrics in Genius platform\n"
    "You'll need an Genius api, which one you can get from https://genius.com/api-clients. \nIn APP WEBSITE URL type any url (such as http://example.com) and copy CLIENT ACCESS TOKEN to config.env file\n"
    " - `.lyrics`: Search lyrics of song played now in Spotify"]
})
