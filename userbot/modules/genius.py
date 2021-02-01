#Developed by Oleh Polisan. get_args_split_by kanged from Friendly Telegram (https://gitlab.com/friendly-telegram/).
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP, GENIUS_API, SPOTIFY_KEY, SPOTIFY_DC
from userbot.events import register
from userbot.utils import get_args_split_by
import spotify_token as st
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
            name = args[0]
            artist = args[1]
            await e.edit("**Searching for song **" + name + "** by **" + artist)
            song = genius.search_song(name, artist)
      else:
            await e.edit("**Trying to get Spotify lyrics...**")
            if SPOTIFY_KEY is None:
                  await e.edit("**Spotify cache KEY is missing**")
                  return
            if SPOTIFY_DC is None:
                  await e.edit("**Spotify cache DC is missing**")
                  return
            #getting spotify token
            sptoken = st.start_session(SPOTIFY_DC, SPOTIFY_KEY) 
            access_token = sptoken[0]
            environ["spftoken"] = access_token
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            response = get(url, headers=hed)
            if response.status_code == 401:
              e.edit("**No spotify token provided and no atributes for manually search provided. Use .lyrics <artist>, <song_name>**")
              return
            elif response.status_code != 200:
              e.edit("**Can't find song in spotify and no atributes for manually search provided. Use .lyrics <artist>, <song_name>**")
            elif response.status_code == 200: 
              data = loads(response.content)
              isLocal = data['item']['is_local']
              if isLocal:
                    artist = data['item']['artists'][0]['name']
              else:
                    artist = data['item']['album']['artists'][0]['name']
              name = data['item']['name']
              print(artist + " - " + name)
              await e.edit("**Searching for song **" + name + "** by **" + artist)
              song = genius.search_song(name, artist)
      if song is None:
        await e.edit("**Can't find song **" + name + "** by **" + artist)
        return
      elif len(song.lyrics) > 4096:
        lyrics_1 = song.lyrics[0:4096]
        lyrics_2 = song.lyrics[4096:len(song.lyrics)]
        await e.edit("**Lyrics for: **" + artist + " - " + name + ": \n")
        await e.client.send_message(e.chat_id, lyrics_1)
        await e.client.send_message(e.chat_id, lyrics_2)

        
      elif (len(song.lyrics + artist + name) + 20) <= 4096:
        await e.edit("**Lyrics for: **" + artist + " - " + name + " \n" + song.lyrics)
      
CMD_HELP.update({"lyrics": ["Lyrics",
    " - `.lyrics <song>, <author>`: Search lyrics in Genius platform\n"
    "You'll need an Genius api, which one you can get from https://genius.com/api-clients. \nIn APP WEBSITE URL type any url (such as http://example.com) and copy CLIENT ACCESS TOKEN to config.env file\n"
    " - `.lyrics`: Search lyrics of song played now in Spotify"]
})
