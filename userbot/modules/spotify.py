from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import environ, system, remove
from sys import setrecursionlimit
import spotify_token as st
from time import gmtime, strftime
from requests import get
from requests.exceptions import HTTPError, ConnectionError
import telethon
from telethon.errors import AboutTooLongError, FloodWaitError
from telethon import errors
from telethon.tl.functions.account import UpdateProfileRequest
from youtube_search import YoutubeSearch
from pytube import YouTube
from pytube.helpers import safe_filename
from telethon import types
msg_for_percentage = types.Message
from userbot import (BIO_PREFIX, BOTLOG, BOTLOG_CHATID, CMD_HELP, DEFAULT_BIO,
                     SPOTIFY_KEY, SPOTIFY_DC, bot)
from userbot.events import register
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error, TIT2, TPE2, TOPE, TPE1

# =================== CONSTANT ===================
SPO_BIO_ENABLED = "`Spotify current music to bio has been successfully enabled.`"
SPO_BIO_DISABLED = "`Spotify current music to bio has been disabled. `"
SPO_BIO_DISABLED += "`Bio reverted to default.`"
SPO_BIO_RUNNING = "`Spotify current music to bio is already running.`"
ERROR_MSG = "`Spotify module halted, got an unexpected error.`"

artist = str
song = str

BIOPREFIX = BIO_PREFIX
link = ""
SPOTIFYCHECK = False
RUNNING = False
OLDEXCEPT = False
PARSE = False
oldartist = ""
oldsong = ""
preview_url = ""
isWritedPause = False
isWritedPlay = False
isGetted = False
isDefault = True
isArtist = True
mustDisable = False
msg_to_edit = types.Message
# ================================================
async def get_spotify_token():
    try:
      sptoken = st.start_session(SPOTIFY_DC, SPOTIFY_KEY)
    except HTTPError:
      await sleep(1)
      await get_spotify_token()
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():
    global artist
    global song
    global PARSE
    global SPOTIFYCHECK
    global RUNNING
    global OLDEXCEPT
    global isPlaying
    global isLocal
    global isArtist
    global isWritedPause
    global isWritedPlay
    global oldartist
    global oldsong
    global errorcheck
    global isGetted
    global data
    global isDefault
    global mustDisable
    spobio = ""
    if mustDisable:
     SPOTIFYCHECK = False
     mustDisable = False #means disabled?
    
    
    while SPOTIFYCHECK:
        isGetted = False
          
        if isDefault == True:
          oldsong = ""
          oldartist = ""
        try:
            date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            RUNNING = True
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            try:
                await sleep(1) #no need to spam?
                response = get(url,headers=hed)
                #print(str(response.status_code))
                if(response.status_code == 200):
                  data = loads(response.content)
                  isGetted = True
                  #print("SPOTIFY: response = " + str(response.status_code))
                elif response.status_code == 401: #No token provided
                  #print("SP: 401: " + response.reason)
                  await get_spotify_token()
                else:
                  if isDefault == False:
                    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                    #print("SP: not 200 response, setting default.")
                    isDefault = True
            except Exception as e:
                isGetted = False
                #print("SP: skip, exception:" + str(e))
                pass #skip
            if isGetted:
              isLocal = data['item']['is_local']
              isPlaying = data['is_playing']
              if isLocal:
                try:
                  artist = data['item']['artists'][0]['name']
                  song = data['item']['name']
                  if artist == "":
                    isArtist = False
                  else:
                    isArtist = True
                except IndexError:
                  song = data['item']['name']
                  artist = ""
                  isArtist = False
              else:
                  artist = data['item']['album']['artists'][0]['name']
                  song = data['item']['name']

              if isWritedPlay and isPlaying == False:
                isWritedPlay = False
              if isWritedPause and isPlaying == True:
                isWritedPause = False
              if (song != oldsong or artist != oldartist) or (isWritedPlay == False and isWritedPause == False):
                  oldartist = artist
                  oldsong = song
                  #print("Changing")
                  if isLocal:
                    if isArtist:
                      spobio = BIOPREFIX + " 🎧: " + artist + " - " + song + " [LOCAL]"
                    else:
                      spobio = BIOPREFIX + " 🎧: " + song + " [LOCAL]"
                  else:
                    spobio = BIOPREFIX + " 🎧: " + artist + " - " + song
                  if isPlaying == False:
                    spobio += " [PAUSED]"
                    isWritedPause = True
                  elif isPlaying == True:
                    isWritedPlay = True
                  try:
                      await sleep(5)
                      await bot(UpdateProfileRequest(about=spobio))
                      isDefault = False
                  except AboutTooLongError:
                      try:
                        short_bio = "🎧: " + song
                        await sleep(5) #anti flood
                        await bot(UpdateProfileRequest(about=short_bio))
                        isDefault = False
                      except AboutTooLongError:
                        short_bio = "🎧: " + song
                        await sleep(5) #anti flood
                        symbols = 0
                        for i in range(len(short_bio)):
                          symbols = symbols + 1
                        if symbols > 70:
                          short_bio = short_bio[:67]
                          short_bio += '...'
                        await bot(UpdateProfileRequest(about=short_bio))
                        isDefault = False
                      except errors.FloodWaitError as e:
                        await sleep(e.seconds)
                  except errors.FloodWaitError as e:
                    await sleep(e.seconds)
                  errorcheck = 0
                  OLDEXCEPT = False
            else: #means no new data. NO need to update. Trying to get again by new loop 
              #print("no new data, trying again")
              pass
        except KeyError:   #long pause
                #print("keyerror: " + date)
                if errorcheck == 0:
                  #print("182 update_token")
                  await update_token()
                elif errorcheck == 1:
                  if OLDEXCEPT == False:
                    await sleep(5) #anti flood
                    try:
                      await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                    except errors.FloodWaitError as e:
                      await sleep(e.seconds)
                    isDefault = True
                  OLDEXCEPT = True
                  try:
                      await sleep(10)
                  except errors.FloodWaitError as e:
                    await sleep(e.seconds)
        except JSONDecodeError:   #NO INFO ABOUT, user closed spotify client
            #print("JSONDecodeError")
            if OLDEXCEPT == False:
              await sleep(5) #anti flood
              try:
                await bot(UpdateProfileRequest(about=DEFAULT_BIO))
              except errors.FloodWaitError as e:
                await sleep(e.seconds)
              isDefault = True
            OLDEXCEPT = True
            try:
                await sleep(10) #no need to ddos a spotify servers
            except errors.FloodWaitError as e:
                await sleep(e.seconds)
        except TypeError:
            #print("TypeError")
            await sleep(5)
            try:
              await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            except errors.FloodWaitError as e:
              await sleep(e.seconds)
            isDefault = True
        except IndexError:
            #print("IndexError")
            await sleep(5)
            try:
              await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            except errors.FloodWaitError as e:
              await sleep(e.seconds)
            isDefault = True
        except errors.FloodWaitError as e:
            #print("Telegram anti-flood: Need to wait " + str(e.seconds) + " seconds")
            await sleep(e.seconds)
            try:
              await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            except errors.FloodWaitError as e:
              await sleep(e.seconds)
            isDefault = True
        except HTTPError:
            #print("HTTPErr")
            try:
              await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            except errors.FloodWaitError as e:
              await sleep(e.seconds)
            isDefault = True
    RUNNING = False


async def update_token():
    try:
      sptoken = st.start_session(SPOTIFY_DC, SPOTIFY_KEY)
    except HTTPError:
      await sleep(1)
      #print("253 update_token")
      await update_token()
    except:
      print("Can't get sp token. The token is likely expired. Change your key and DC!")
      await update_token()
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    errorcheck = 1
    #print("261 updta_sp_info")
    await update_spotify_info()

@register(outgoing=True, pattern="^.song")
async def show_song(song_info):
        if environ.get("isSuspended") == "True":
          return
        global isArtist
        global artist
        global song
        global isGetted
        global link
        global preview_url
        await find_song()
        if preview_url != "":
          system(f"wget -q -O 'preview.jpg' {preview_url}")
        str_song = "Now playing: "
        if isGetted:
          if (artist == "" or artist == '' or artist == ' ' or artist == " "):
            isArtist = False
          if isArtist:
            str_song += '`' + artist + " - " + song + '`'
          else:
            str_song += '`' + song + '`'
          if ((link != '') and (isLocal == False)):
            str_song += f"\n[Spotify link]({link})"
          if preview_url == "": #LOCAL SONG
            await song_info.edit(str_song)
          else:
            await song_info.delete()
            msg_to_edit = await song_info.client.send_file(song_info.chat_id, 'preview.jpg', caption=str_song)
        else:
          await song_info.edit("Can't find current song in spotify")
          return
        #yt link
        song_author_str = artist + ' - ' + song
        if isGetted:
          results = YoutubeSearch(song_author_str, max_results=1).to_json()
          try:
            data = loads(results)
          except JSONDecodeError:
            print(".song: JSONDecode Error. Can't get yt link.")
            str_song += "\n\n Youtube: `JSONDecode Error. Can't found.`"
            await msg_to_edit.edit(str_song)
            return
          except Exception as e:
            str_song += f"\n\n Youtube: `Unexcepted Error: {e}. Can't found.`"
            await msg_to_edit.edit(str_song)
            return
          finally:
            print("Found!")
            str_song += "\n\nFound yt song link for: `" + data['videos'][0]['title'] + '`'
            url_yt = "https://youtube.com" + data['videos'][0]['url_suffix']
            str_song += f"\n[YouTube link]({url_yt})"
            if preview_url !="": #means NOT LOCAL song in spotify and means that there are preview
              await msg_to_edit.edit(text = str_song)
            else: #fetching preview from yt
              await song_info.delete()
              video = YouTube(url_yt)
              #system(f"wget -q -O './userbot/modules/picture.jpg' {video.thumbnail_url}")
              r = get(video.thumbnail_url, allow_redirects=True)
              open('picture.jpg', 'wb').write(r.content)
              await song_info.client.send_file(song_info.chat_id, 'picture.jpg', caption=str_song)
            try:
              remove('picture.jpg')
            except:
              pass
            try:
              remove('preview.jpeg')
            except:
              pass
            return

@register(outgoing=True, pattern="^.spdl$")
async def sp_download(spdl):
  if environ.get("isSuspended") == "True":
        return
  reply_message = await spdl.get_reply_message()
  global song
  global artist
  global link
  global preview_url
  global msg_for_percentage
  global isArtist
  global isLocal
  msg_for_percentage = spdl
  await find_song()
  if isGetted:
    if isArtist:
      str_song_artist = artist + " - " + song
    else:
      str_song_artist = song
    results = YoutubeSearch(str_song_artist, max_results=1).to_json()
    try:
      data = loads(results)
    except JSONDecodeError:
      await spdl.edit("JSONDecodeError. Can't found in yt.")
    except:
      await spdl.edit("Something went wrong. :(")
    finally:
      link_yt = "https://youtube.com" + data['videos'][0]['url_suffix'] #yt link
      await spdl.edit("**Processing...**")
      video = YouTube(link_yt)
      stream = video.streams.filter(only_audio=True, mime_type="audio/webm").last()
      await spdl.edit("**Downloading audio...**")
      stream.download(filename="video")
      await spdl.edit("**Converting to mp3...**")
      system(f"ffmpeg -loglevel panic -i 'video.webm' -vn -ab 128k -ar 44100 -y 'song.mp3'")
      remove("video.webm")
      if isLocal is False:
        system(f"wget -q -O 'picture.jpg' {preview_url}")
      else: #fetching from yt
        system(f"wget -q -O 'picture.jpg' {video.thumbnail_url}")
      audio = MP3("song.mp3", ID3=ID3)
      try:
          audio.add_tags()
      except error:
          pass
      audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open('picture.jpg','rb').read()))
      #audio.tags.add(APIC(mime='image/jpeg',type=12,desc=u'Cover',data=open('picture.jpg','rb').read()))
      audio.tags.add(TIT2(text=song))
      if isArtist:
        audio.tags.add(TPE1(text=artist))
      audio.save()
      
      if link != "":
        await spdl.client.send_file(spdl.chat.id,
                              "song.mp3",
                              caption=f"[Spotify]({link}) | [YouTube]({link_yt})",
                              progress_callback=callback)
      else:
        await spdl.client.send_file(spdl.chat.id,
                              "song.mp3",
                              caption=f"[YouTube]({link_yt})",
                              progress_callback=callback)
      await spdl.delete()
      remove('picture.jpg')
      remove("song.mp3")
  else:
    await spdl.edit("**Can't find current song in spotify.**")
    return
         
async def find_song():
        global link
        global isArtist
        global artist
        global song
        global isGetted
        global isLocal
        global preview_url
        isGetted = False
        await get_spotify_token()
        spftoken = environ.get("spftoken", None)
        hed = {'Authorization': 'Bearer ' + spftoken}
        url = 'https://api.spotify.com/v1/me/player/currently-playing'
        try:
          response = get(url,headers=hed)
        except:
          await song_info.edit("Something went wrong. Trying again...")
          try:
            await sleep(1)
            response = get(url,headers=hed)
          except:
            await song_info.edit("Can't connect to spotify servers.")
            return
        #print(str(response.status_code))
        if(response.status_code == 200):
          #print("SPOTIFY: response = " + str(response.status_code))
          data = loads(response.content)
          isLocal = data['item']['is_local']
          if data['item']['artists'][0]['name'] == "":
            isArtist = False
          if isLocal:
            artist = data['item']['artists'][0]['name']
            song = data['item']['name']
            isGetted = True
            isArtist = True
            link = ""
            preview_url = ""
          else:
              artist = data['item']['album']['artists'][0]['name']
              song = data['item']['name']
              link = data['item']['external_urls']['spotify']
              preview_url = data['item']['album']['images'][0]['url']
              isGetted = True
              isArtist = True
        else:
          isGetted = False
          

@register(outgoing=True, pattern="^.spoton$")
async def set_biostgraph(setstbio):
    if environ.get("isSuspended") == "True":
        return
#    setrecursionlimit(700000)
    global SPOTIFYCHECK
    global mustDisable
    if not SPOTIFYCHECK:
        environ["errorcheck"] = "0"
        await setstbio.edit(SPO_BIO_ENABLED)
        mustDisable = False
        SPOTIFYCHECK = True
        await get_spotify_token()
        await update_spotify_info()
    else:
        await setstbio.edit(SPO_BIO_RUNNING)


@register(outgoing=True, pattern="^.spotoff$")
async def set_biodgraph(setdbio):
    if environ.get("isSuspended") == "True":
        return
    global SPOTIFYCHECK
    global mustDisable
    #print("start spotoff: " + str(SPOTIFYCHECK))
    global RUNNING
    SPOTIFYCHECK = False
    #print("changed spotoff: " + str(SPOTIFYCHECK))
    RUNNING = False
    mustDisable = True
    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
    await setdbio.edit(SPO_BIO_DISABLED)
    
async def callback(current, total):
    global msg_for_percentage
    percent = round(current/total * 100, 2)
    await msg_for_percentage.edit(f"**Sending mp3...**\nUploaded `{current}` out of `{total}` bytes: `{percent}%`")




CMD_HELP.update({"spotify": ['Spotify',
    " - `.spoton`: Enable Spotify bio updating.\n"
    " - `.spotoff`: Disable Spotify bio updating.\n"
    " - `.spdl`: Find current spotify song in youtube and download it!.\n"
    " - `.song:`: Show current playing song.\n"]
})
