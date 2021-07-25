# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module containing commands for keeping global notes. """

from userbot.events import register
from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive,
                     is_redis_alive)
from os import environ
from userbot.modules.dbhelper import add_snip, get_snip, get_snips

@register(outgoing=True,
          pattern=r"\$\w*",
          ignore_unsafe=True,
          disable_errors=True)
async def on_snip(event):
    """ Snips logic. """
    if environ.get("isSuspended") == "True":
        return
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    name = event.text[1:]
    snip = await get_snip(name)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if snip and snip['msgid']:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=snip['msgid'])
        await event.client.send_message(event.chat_id,
                                        msg_o.message,
                                        reply_to=message_id_to_reply,
                                        file=msg_o.media)
    elif snip and snip['text']:
        await event.client.send_message(event.chat_id,
                                        snip['text'],
                                        reply_to=message_id_to_reply)


@register(outgoing=True, pattern="^.snip (\w*)")
async def on_snip_save(event):
    """ For .snip command, saves snips for future use. """
    if environ.get("isSuspended") == "True":
        return
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
            
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#SNIP\
            \nKEYWORD: {keyword}\
            \n\nThe following message is saved as the data for the snip, please do NOT delete it !!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Saving snips with media requires the BOTLOG_CHATID to be set.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Snip {} successfully. Use` **${}** `anywhere to get it`"
    if await add_snip(keyword, string, msg_id) is False:
        await event.edit(success.format('updated', keyword))
    else:
        await event.edit(success.format('saved', keyword))


@register(outgoing=True, pattern="^.snips$")
async def on_snip_list(event):
    if environ.get("isSuspended") == "True":
        return
    """ For .snips command, lists snips saved by you. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return

    message = "`No snips available right now.`"
    all_snips = await get_snips()
    for a_snip in all_snips:
        if message == "`No snips available right now.`":
            message = "Available snips:\n"
            message += f"`${a_snip['name']}`\n"
        else:
            message += f"`${a_snip['name']}`\n"

    await event.edit(message)


@register(outgoing=True, pattern="^.remsnip (\w*)")
async def on_snip_delete(event):
    """ For .remsnip command, deletes a snip. """
    if environ.get("isSuspended") == "True":
        return
    try:
        from userbot.modules.dbhelper import delete_snip
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    name = event.pattern_match.group(1)
    if await delete_snip(name) is True:
        await event.edit(f"`Successfully deleted snip:` **{name}**")
    else:
        await event.edit(f"`Couldn't find snip:` **{name}**")

CMD_HELP.update({"snips": ["Snips",
    " - `$<snip_name>`: Gets the specified snip, anywhere.\n"
    " - `.snip <name> <data> or reply to a message with .snip <name>`: Saves the message as a snip (global note) with the name. (Works with pics, docs, and stickers too!)\n"
    " - `snips`: Gets all saved snips.\n"
    " - `remsnip <snip_name>`: Deletes the specified snip.\n"
                        ]})
