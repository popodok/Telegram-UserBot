# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import CONVERT_TOKEN, bot, CMD_HELP
from userbot.events import register
import os
from pdf2image import convert_from_path
import convertapi
from shutil import rmtree
from os import environ


@register(outgoing=True, pattern=r"^\.pdf2img$")
async def pdf(e):
  if environ.get("isSuspended") == "True":
        return
  message = await e.get_reply_message()
  if message.file.mime_type == "application/pdf":
    file = message.document
    await e.edit("**Downloading...**")
    file = await bot.download_file(file, "file.pdf")
    if os.path.isdir("./files") is False:
      os.mkdir("./files")
    else:
      rmtree("./files")
      os.mkdir("./files")
    await e.edit("**Processing...**")  
    images_from_path = convert_from_path('./file.pdf', output_folder='./files', fmt='png')
    await e.edit("**Sending...**")
    for filename in os.listdir("./files"):
      await e.client.send_file(e.chat_id, open('./files/' + filename, 'rb'), reply_to=message)
    rmtree("./files")
    os.remove("./file.pdf")
  else:
    await e.edit("`Not a pdf file. Aborting...`")
    return
  
@register(outgoing=True, pattern=r"^\.doc2pdf$")
async def doc(e):
  if environ.get("isSuspended") == "True":
        return
  if CONVERT_TOKEN == False:
    await e.edit("**No converter API defined. Fill it in config.env file. Aborting...**")
    return
  convertapi.api_secret = CONVERT_TOKEN
  message = await e.get_reply_message()
  if message.file.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or message.file.mime_type == "application/msword":
    file = message.document
    await e.edit("**Downloading...**")
    result = None
    if  message.file.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document": #docx
      file = await bot.download_file(file, "file.docx")
      await e.edit("**Converting...**")
      result = convertapi.convert('pdf', { 'File': 'file.docx' })
      os.remove('file.docx')
    if message.file.mime_type == "application/msword": #docx
        file = await bot.download_file(file, "file.doc")
        await e.edit("**Converting...**")
        result = convertapi.convert('pdf', { 'File': 'file.doc' })
        os.remove('file.doc')
    result.file.save('file.pdf')
    await e.edit("**Sending...**")
    await e.client.send_file(e.chat_id, f'file.pdf',reply_to=message)
    
    os.remove('file.pdf')
  else:
    await e.edit("`Not a doc/docx file. Aborting...`")
    return
@register(outgoing=True, pattern=r"^\.doc2img$")
async def doc_png(e):
  if environ.get("isSuspended") == "True":
        return
  message = await e.get_reply_message()
  if CONVERT_TOKEN == False:
    await e.edit("**No converter API defined. Fill it in config.env file. Aborting...**")
    return
  convertapi.api_secret = CONVERT_TOKEN
  if message.file.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or message.file.mime_type == "application/msword":
    file = message.document
    await e.edit("**Downloading...**")
    result = None
    if  message.file.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document": #docx
      file = await bot.download_file(file, "file.docx")
      await e.edit("**Converting...**")
      result = convertapi.convert('pdf', { 'File': 'file.docx' })
      os.remove('file.docx')
    if message.file.mime_type == "application/msword": #docx
        file = await bot.download_file(file, "file.doc")
        await e.edit("**Converting...**")
        result = convertapi.convert('pdf', { 'File': 'file.doc' })
        os.remove('file.doc')
    result.file.save('file.pdf')
    if os.path.isdir("./files") is False:
      os.mkdir("./files")
    else:
      rmtree("./files")
      os.mkdir("./files")
    await e.edit("**Processing...**")
    images_from_path = convert_from_path('./file.pdf', output_folder='./files', fmt='png')
    await e.edit("**Sending...**")
    for filename in os.listdir("./files"):
      await e.client.send_file(e.chat_id, open('./files/' + filename, 'rb'), reply_to=message)
    rmtree("./files")
    os.remove(f"file.pdf")
  else:
    await e.edit("`Not a doc file. Aborting...`")
    return
  
@register(outgoing=True, pattern=r"^\.xls2img$")
async def xls_png(e):
  if environ.get("isSuspended") == "True":
        return
  message = await e.get_reply_message()
  if CONVERT_TOKEN == False:
    await e.edit("**No converter API defined. Fill it in config.env file. Aborting...**")
    return
  convertapi.api_secret = CONVERT_TOKEN
  if message.file.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or message.file.mime_type == "application/vnd.ms-excel":
    file = message.document
    await e.edit("**Downloading...**")
    result = None
    if  message.file.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": #xlsx
      file = await bot.download_file(file, "file.xlsx")
      await e.edit("**Converting...**")
      result = convertapi.convert('pdf', { 'File': 'file.xlsx' })
      os.remove('file.xlsx')
    if message.file.mime_type == "application/vnd.ms-excel": #xls
        file = await bot.download_file(file, "file.xls")
        await e.edit("**Converting...**")
        result = convertapi.convert('pdf', { 'File': 'file.xls' })
        os.remove('file.xls')
    result.file.save('file.pdf')
    if os.path.isdir("./files") is False:
      os.mkdir("./files")
    else:
      rmtree("./files")
      os.mkdir("./files")
    await e.edit("**Processing...**")
    images_from_path = convert_from_path('./file.pdf', output_folder='./files', fmt='png')
    await e.edit("**Sending...**")
    for filename in os.listdir("./files"):
      await e.client.send_file(e.chat_id, open('./files' + filename, 'rb'), reply_to=message)
    rmtree("./files")
    os.remove(f"file.pdf")
  else:
    await e.edit("`Not a xls/xlsx file. Aborting...`")
    return
@register(outgoing=True, pattern=r"^\.xls2pdf$")
async def xls_png(e):
  if environ.get("isSuspended") == "True":
        return
  message = await e.get_reply_message()
  if CONVERT_TOKEN == False:
    await e.edit("**No converter API defined. Fill it in config.env file. Aborting...**")
    return
  convertapi.api_secret = CONVERT_TOKEN
  if message.file.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or message.file.mime_type == "application/vnd.ms-excel":
    file = message.document
    await e.edit("**Downloading...**")
    result = None
    if  message.file.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": #xlsx
      file = await bot.download_file(file, "file.xlsx")
      await e.edit("**Converting...**")
      result = convertapi.convert('pdf', { 'File': 'file.xlsx' })
      os.remove('file.xlsx')
    if message.file.mime_type == "application/vnd.ms-excel": #xls
        file = await bot.download_file(file, "file.xls")
        await e.edit("**Converting...**")
        result = convertapi.convert('pdf', { 'File': 'file.xls' })
        os.remove('file.xls')
    result.file.save('file.pdf')
    await e.edit("**Sending...**")
    await e.client.send_file(e.chat_id, f'file.pdf',reply_to=message)
  else:
    await e.edit("`Not a xls/xlsx file. Aborting...`")
    return

@register(outgoing=True, pattern=r"^\.ppt2img$")
async def ppt_png(e):
  if environ.get("isSuspended") == "True":
        return
  message = await e.get_reply_message()
  if CONVERT_TOKEN == False:
    await e.edit("**No converter API defined. Fill it in config.env file. Aborting...**")
    return
  convertapi.api_secret = CONVERT_TOKEN
  if message.file.mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation" or message.file.mime_type == "application/vnd.ms-powerpoint":
    file = message.document
    await e.edit("**Downloading...**")
    result = None
    if  message.file.mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation": #pptx
      file = await bot.download_file(file, "file.pptx")
      await e.edit("**Converting...**")
      result = convertapi.convert('pdf', { 'File': 'file.pptx' })
      os.remove('file.pptx')
    if message.file.mime_type == "application/vnd.ms-powerpoint": #ppt
        file = await bot.download_file(file, "file.ppt")
        await e.edit("**Converting...**")
        result = convertapi.convert('pdf', { 'File': 'file.ppt' })
        os.remove('file.ppt')
    result.file.save('file.pdf')
    if os.path.isdir("./files") is False:
      os.mkdir("./files")
    await e.edit("**Processing...**")
    images_from_path = convert_from_path('./file.pdf', output_folder='./files', fmt='png')
    await e.edit("**Sending...**")
    for filename in os.listdir("/root/Telegram-UserBot/files/"):
      await e.client.send_file(e.chat_id, open('./files/' + filename, 'rb'), reply_to=message)
    rmtree("./files")
    os.remove(f"./file.pdf")
  else:
    await e.edit("`Not a ppt/pptx file. Aborting...`")
    return
@register(outgoing=True, pattern=r"^\.ppt2pdf$")
async def ppt_pdf(e):
  if environ.get("isSuspended") == "True":
        return
  message = await e.get_reply_message()
  if CONVERT_TOKEN == False:
    await e.edit("**No converter API defined. Fill it in config.env file. Aborting...**")
    return
  convertapi.api_secret = CONVERT_TOKEN
  if message.file.mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation" or message.file.mime_type == "application/vnd.ms-powerpoint":
    file = message.document
    await e.edit("**Downloading...**")
    result = None
    if  message.file.mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation": #pptx
      file = await bot.download_file(file, "file.pptx")
      await e.edit("**Converting...**")
      result = convertapi.convert('pdf', { 'File': 'file.pptx' })
      os.remove('file.pptx')
    if message.file.mime_type == "application/vnd.ms-powerpoint": #ppt
        file = await bot.download_file(file, "file.ppt")
        await e.edit("**Converting...**")
        result = convertapi.convert('pdf', { 'File': 'file.ppt' })
        os.remove('file.ppt')
    result.file.save('file.pdf')
    await e.edit("**Sending...**")
    await e.client.send_file(e.chat_id, f'file.pdf',reply_to=message)
  else:
    await e.edit("`Not a ppt/pptx file. Aborting...`")
    return
  
CMD_HELP.update({"documents": ['Documents',
    " - `.pdf2img`: Convert pdf to images.\n"
    " - `.xls2img`: Convert xls/xlsx to images.\n"
    " - `.xls2pdf`: Convert xls/xlsx to pdf.\n"
    " - `.ppt2img`: Convert ppt/pptx to images.\n"
    " - `.ppt2pdf`: Convert ppt/pptx to pdf.\n"
    " - `.doc2pdf`: Convert doc/docx to pdf.\n"
    " - `.doc2img`: Convert doc/docx to images.\n"]
})
