# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
from asyncio import wait, sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from os import environ

@register(outgoing=True, pattern="^.cspam (.*)")
async def tmeme(e):
    if environ.get("isSuspended") == "True":
        return
    cspam = str(e.pattern_match.group(1))
    message = cspam.replace(" ", "")
    await e.delete()
    for letter in message:
        await e.respond(letter)
    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID, "#CSPAM\n"
            "TSpam was executed successfully")


@register(outgoing=True, pattern="^.wspam (.*)")
async def tmeme(e):
    if environ.get("isSuspended") == "True":
        return
    wspam = str(e.pattern_match.group(1))
    message = wspam.split()
    await e.delete()
    for word in message:
        await e.respond(word)
    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID, "#WSPAM\n"
            "WSpam was executed successfully")


@register(outgoing=True, pattern="^.spam (.*)")
async def spammer(e):
    is_file = False
    if environ.get("isSuspended") == "True":
        return
    replied_message = await e.get_reply_message()
    counter = int(e.pattern_match.group(1).split(' ', 1)[0])
    if replied_message.file:
        is_file = True
        if replied_message.sticker:
            spam_message = replied_message.sticker 
        elif replied_message.photo:
            spam_message = replied_message.photo
        elif replied_message.audio:
            spam_message = replied_message.audio
        else:
            spam_message = replied_message.file
    
    elif replied_message.text:
        spam_message = replied_message.text
    else:
        spam_message = str(e.pattern_match.group(1).split(' ', 1)[1])
    await e.delete()

    await asyncio.wait([e.respond(spam_message) for i in range(counter)]) if not is_file else \
        await asyncio.wait([e.respond(file=spam_message) for i in range(counter)])
    if BOTLOG:
        await e.client.send_message(BOTLOG_CHATID, "#SPAM\n"
                                    "Spam was executed successfully")


@register(outgoing=True, pattern="^.picspam")
async def tiny_pic_spam(e):
    if environ.get("isSuspended") == "True":
        return
    message = e.text
    text = message.split()
    counter = int(text[1])
    link = str(text[2])
    await e.delete()
    for i in range(1, counter):
        await e.client.send_file(e.chat_id, link)
    if BOTLOG:  
        await e.client.send_message(
            BOTLOG_CHATID, "#PICSPAM\n"
            "PicSpam was executed successfully")


@register(outgoing=True, pattern="^.delayspam (.*)")
async def spammer(e):
    if environ.get("isSuspended") == "True":
        return
    spamDelay = float(e.pattern_match.group(1).split(' ', 2)[0])
    counter = int(e.pattern_match.group(1).split(' ', 2)[1])
    spam_message = str(e.pattern_match.group(1).split(' ', 2)[2])
    await e.delete()
    for i in range(1, counter):
        await e.respond(spam_message)
        await sleep(spamDelay)
    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID, "#DelaySPAM\n"
            "DelaySpam was executed successfully")

CMD_HELP.update({"spam": ["Spam",
    " - `.cspam <text>`: Spam the text letter by letter.\n"
    " - `.spam <count> <text>`: Floods text in the chat !!\n"
    " - `.picspam <count> <link to image/gif>`: As if text spam was not enough !!\n"
    " - `.delayspam <delay> <count> <text>`: .bigspam but with custom delay.\n"
    " - `.wspam <text>`: Spam the text word by word.\n"
                        ]})
