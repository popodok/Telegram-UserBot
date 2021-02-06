# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import CONVERT_TOKEN, bot, CMD_HELP
from userbot.events import register
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import quote
from os import environ

@register(outgoing=True, pattern=r"^\.dict (.*)")
async def horoh(e):
  if environ.get("isSuspended") == "True":
        return
  import_word = e.pattern_match.group(1)
  word = quote(import_word)
  url = f'https://goroh.pp.ua/%D0%A2%D0%BB%D1%83%D0%BC%D0%B0%D1%87%D0%B5%D0%BD%D0%BD%D1%8F/Index?WordValue={word}'
  r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  try:
    html = urlopen(r).read()
  except HTTPError as err:
    await e.edit(f"**HTTP `{err.code}` error. Word {import_word} not found. Try to use another word.**")
    return
  soup = BeautifulSoup(html, features="html.parser")
  pAll = soup.find('div', {"class": "list"})
  str_to_return = ''
  for blocks in pAll.find_all('div', {"class": "article-block"}):
    for uppercases in blocks.find_all('span', {"class": "uppercase"}):
      str_to_return = "\n\n".join((str_to_return, f"**{uppercases.text}**"))
      await e.edit(f"{str_to_return}")
      for texts in blocks.find_all('span', {"class": "interpret-formula"}):
        str_to_return =  "\n".join((str_to_return, texts.text))
        await e.edit(f"{str_to_return}")


CMD_HELP.update({"dictionary": ['dictionary',
    " - `.dict <word>`: Search word interpretation in Ukrainian vocabulary goroh.pp.ua.\n"]
})

