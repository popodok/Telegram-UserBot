# Module developed by Oleh Polisan
# You can use this file without any permissions.
from userbot import CONVERT_TOKEN, bot, CMD_HELP
from userbot.events import register
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import quote
from os import environ
from itertools import takewhile, chain
import re

@register(outgoing=True, pattern=r"^\.tag (.*)")
async def tag(e):
  if environ.get("isSuspended") == "True":
        return
  import_tag = e.pattern_match.group(1)
  tag = quote(import_tag)
  url = f'http://htmlbook.ru/html/{tag}'
  r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  try:
    html = urlopen(r).read()
  except HTTPError as err:
    await e.edit(f"**HTTP `{err.code}` error. Tag {import_tag} not found. Try to use another tag.**")
    return
  soup = BeautifulSoup(html, features="html.parser")
  is404 = soup.find('h1', {"class": "title"})
  if is404 == "Документ не найден":
    await e.edit(f"**Tag** `{import_tag}` **not found. Try another one.**")
    return
  divAll = soup.find('div', {"class": "field-item even"})
 # for spans in divAll.findAll('span'):
 #   spans.unwrap()
  H3Opis = divAll.find('h3', text="Описание")
  if H3Opis == None:
    H3Opis = divAll.find('h3', text="Описание ")
  nextH3 = divAll.find('h3', text="Синтаксис")
  if nextH3 == None:
    nextH3 = divAll.find('h3', text="Синтаксис ")
  def between(cur, end):
      while cur and cur != end:
          if isinstance(cur, NavigableString):
              text = cur.strip()
              text = text.replace("\n", "")
              text = text.replace("  ", " ")
              text = text.replace("   ", " ")
              if len(text):
                  yield text
          cur = cur.next_element
  result = f"**Тег** `<{import_tag}>`:\n"
  result += ' '.join(text for text in between(H3Opis.next_sibling, nextH3))
  result += "\n\n**Атрибуты**:\n"
  try:
    for dts in divAll.find('dl', {"class": "param"}).findAll('dt'):
        result += '`' + dts.find('a').get_text().replace("\n", "") + '`' + ' - '  + dts.findNext('dd').get_text().replace("\n", "") + '\n'
  except:
    result += 'Для этого тега доступны [универсальные атрибуты](http://htmlbook.ru/html/attr/common) и [события](http://htmlbook.ru/html/attr/event).'
  await e.edit(result)
CMD_HELP.update({"html": ['HTML',
    " - `.tag <tag>`: Search html tag in http://htmlbook.ru/\n"]
})
