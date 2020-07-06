from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP, GENIUS_API
from userbot.events import register
from userbot.utils import parse_arguments
from moviepy import editor as mp
import os
import lyricsgenius

@register(outgoing=True, pattern=r"^\.lyrics$")
async def gen(e):
      if GENIUS_API is None:
        await e.edit("**We don't support magic! No Genius API!**")
        return
      args = utils.get_args_split_by(e.pattern_match.group(), ",")
      if len(args) != 2:
        logger.debug(args)
        await e.edit("**Syntax Error**")
        return
      try:
          song = await genius.search_song(args[0], args[1])
      except TypeError:
          # Song not found causes internal library error
          song = None
      if song is None:
        await e.edit("**Can't find song**")
        return
      await e.edit(utils.escape_html(song.lyrics))