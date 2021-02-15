# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """
from re import fullmatch, IGNORECASE, escape
from asyncio import sleep

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive,
                     is_redis_alive)
from userbot.events import register
from userbot.modules.dbhelper import add_filter, delete_filter, get_filters
from os import environ

@register(incoming=True, disable_errors=True)
async def filter_incoming_handler(handler):
    if environ.get("isSuspended") == "True":
        return
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                await handler.edit("`Database connections failing!`")
                return
            name = handler.raw_text
            filters = await get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pro = fullmatch(trigger['keyword'], name, flags=IGNORECASE)
                if pro and trigger['msg_id']:
                    msg_o = await handler.client.get_messages(entity=BOTLOG_CHATID, ids=trigger['msg_id'])
                    await handler.reply(msg_o.message, file=msg_o.media)
                elif pro and trigger['msg']:
                    await handler.reply(trigger['msg'])
    except AttributeError:
        pass


@register(outgoing=True, pattern="^.filter\\s.*")
async def add_new_filter(event):
    if environ.get("isSuspended") == "True":
        return
    """ Command for adding a new filter or watching all filters"""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    message = event.text
    keyword = message.split()
    msg_media = await event.get_reply_message()
    msg_id = None
    string = ""
    for i in range(2, len(keyword)):
        string = string + " " + str(keyword[i])
    if msg_media and msg_media.media and not string:
      if BOTLOG_CHATID:
        await event.client.send_message(
                BOTLOG_CHATID, f"#FILTER\
            \nCHAT ID: {event.chat_id}\
            \nTRIGGER: {keyword}\
            \n\nThe following message is saved as the filter's reply data for the chat, please do NOT delete it !!"
            )
        msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg_media,
                from_peer=event.chat_id,
                silent=True)
        msg_id = msg_o.id
      else:
        await event.edit("`Saving media as reply to the filter requires the BOTLOG_CHATID to be set.`")
        return
    elif event.reply_to_msg_id and not string:
        string = " " + (await event.get_reply_message()).text
    msg = "`Filter `**{}**` {} successfully`"

    if await add_filter(event.chat_id, keyword[1], string[1:], msg_id) is True:
        await event.edit(msg.format(keyword[1], 'added'))
    else:
        await event.edit(msg.format(keyword[1], 'updated'))


@register(outgoing=True, pattern="^.stop\\s.*")
async def remove_filter(event):
    if environ.get("isSuspended") == "True":
        return
    """ Command for removing a filter """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    filt = event.text[6:]

    if not await delete_filter(event.chat_id, filt):
        await event.edit("`Filter `**{}**` doesn't exist.`".format(filt))
    else:
        await event.edit(
            "`Filter `**{}**` was deleted successfully`".format(filt))

@register(outgoing=True, pattern="^.filters$")
async def filters_active(event):
    if environ.get("isSuspended") == "True":
        return
    """ For .filters command, lists all of the active filters in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    transact = "`There are no filters in this chat.`"
    filters = await get_filters(event.chat_id)
    for filt in filters:
        if transact == "`There are no filters in this chat.`":
            transact = "Active filters in this chat:\n"
            transact += " • **{}** - `{}`\n".format(filt["keyword"],
                                                    filt["msg"])
        else:
            transact += " • **{}** - `{}`\n".format(filt["keyword"],
                                                    filt["msg"])

    await event.edit(transact)


CMD_HELP.update({
    "filters": [
        'Filters', " - `.filters`: List all active filters in this chat.\n"
        " - `.filter <keyword> <reply message/media>`: Add a filter to this chat. "
        "Paperplane will reply with <reply message> or <media> whenever <keyword> is mentioned. "
        "NOTE: filters are case insensitive.\n"
        " - `.stop <filter>`: Removes the filter from this chat.\n"
    ]
})
