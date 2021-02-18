# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for keeping notes. """

from asyncio import sleep

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive,
                     is_redis_alive)
from userbot.events import register
from userbot.modules.dbhelper import add_note, delete_note, get_note, get_notes
from os import environ

@register(outgoing=True, pattern="^.notes$")
async def notes_active(event):
    """ For .saved command, list all of the notes saved in a chat. """
    if environ.get("isSuspended") == "True":
        return
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return

    message = "`There are no saved notes in this chat`"
    notes = await get_notes(event.chat_id)
    for note in notes:
        if message == "`There are no saved notes in this chat`":
            message = "Notes saved in this chat:\n"
            message += "🔹 **{}**\n".format(note["name"])
        else:
            message += "🔹 **{}**\n".format(note["name"])

    await event.edit(message)


@register(outgoing=True, pattern=r"^.clear (\w*)")
async def remove_notes(event):
    if environ.get("isSuspended") == "True":
        return
    """ For .clear command, clear note with the given name."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    notename = event.pattern_match.group(1)
    if await delete_note(event.chat_id, notename) is False:
        return await event.edit("`Couldn't find note:` **{}**".format(notename)
                                )
    else:
        return await event.edit(
            "`Successfully deleted note:` **{}**".format(notename))


@register(outgoing=True, pattern=r"^.save (\w*)")
async def add_filter(event):
    if environ.get("isSuspended") == "True":
        return
    """ For .save command, saves notes in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return

    notename = event.pattern_match.group(1)
    string = event.text.partition(notename)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
      if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#NOTE\
            \nCHAT ID: {event.chat_id}\
            \nKEYWORD: {notename}\
            \n\nThe following message is saved as the note's reply data for the chat, please do NOT delete it !!"
            )
            msg_o = await event.client.forward_messages(entity=BOTLOG_CHATID,
                                                       messages=msg,
                                                       from_peer=event.chat_id,
                                                       silent=True)
            msg_id = msg_o.id
      else:
            await event.edit(
                "`Saving media as data for the note requires the BOTLOG_CHATID to be set.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Note {} successfully. Use` #{} `to get it`"
    if await add_note(event.chat_id, notename, string, msg_id) is False:
        return await event.edit(success.format('updated', notename))
    else:
        return await event.edit(success.format('added', notename))

@register(pattern=r"#\w*",
          disable_edited=True,
          ignore_unsafe=True,
          disable_errors=True)
async def note(event):
    if environ.get("isSuspended") == "True":
        return
    """ Notes logic. """
    try:
        if not (await event.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                await event.edit("`Database connections failing!`")
                return
            notename = event.text[1:]
            note = await get_note(event.chat_id, notename)
            msg_to_reply = event.message.reply_to_msg_id
            if not msg_to_reply:
              msg_to_reply = None
            if note and note['msg_id']:
              msg_o = await event.client.get_messages(entity=BOTLOG_CHATID, ids=note['msg_id'])
              await event.client.send_message(entity=event.chat_id, message=msg_o.message, reply_to=msg_to_reply, file=msg_o.media)
            elif note and note['text']:
                await event.client.send_message(entity=event.chat_id, message=note['text'])
    except BaseException:
        pass



CMD_HELP.update({
    "notes": [
        "Notes", " - `#<notename>`: Get the note with name notename.\n"
        " - `.save <notename> <content>`: Save content in a note with the name notename.\n"
        " - `.notes`: View all notes in current chat.\n"
        " - `.clear <notename>`: Delete the note with name notename.\n"
    ]
})
