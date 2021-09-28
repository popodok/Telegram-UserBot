from userbot.events import register
from userbot import MAC_ADDRESS as MAC
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP, IP_ADDRESS
from wakeonlan import send_magic_packet
from os import environ
@register(outgoing=True, pattern=r"^\.boot$")
async def boot(bt):
    if environ.get("isSuspended") == "True":
        return
    if MAC is None:
      await bt.edit("**We don't support magic! No MAC ADDRESS!**")
      return
    if IP_ADDRESS is None:
      send_magic_packet(MAC)
      await bt.edit(f"**Sent magic package to {MAC} successfully!**")
    else:
      send_magic_packet(MAC, ip_address=IP_ADDRESS)
      await bt.edit(f"**Sent magic package to {IP_ADDRESS}, {MAC} successfully!**")
    
CMD_HELP.update({"boot": ["Boot",
    " - `.stats`: Boot your PC on local server with MAC and IP (opt.), given in conf file.\n"
                        ]})
