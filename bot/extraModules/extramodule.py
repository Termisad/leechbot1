from threading import Thread
from urllib.parse import quote
from bot import BOT_PM, CHANNEL_USERNAME, LOGGER
from bot.helper.ext_utils.bot_utils import is_url, secondsToText
from bot.helper.telegram_helper.message_utils import auto_delete_upload_message, sendMarkup, auto_delete_reply_message
from bot.helper.telegram_helper.button_build import ButtonMaker

def checkModule(bot, message):
    buttons = ButtonMaker()
    uname = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.username}</a>' if message.from_user.username else f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
    help_msg = f"Dear {uname},\n"
    if CHANNEL_USERNAME:
        try:
            user = bot.get_chat_member(FSUB_CHANNEL_USERNAME, message.from_user.id)
            if user.status not in ("member", "creator", "administrator", "supergroup"):
                chat_u = CHANNEL_USERNAME.replace("@", "")
                buttons.buildbutton("👉🏻 CHANNEL LINK 👈🏻", f"https://t.me/{chat_u}")
                help_msg += f"Join the Channel using the CHANNEL LINK button to use bot.\n\n"
        except Exception as e:
            LOGGER.error(e)
    if BOT_PM and message.chat.type not in ["private", "group"]:
        try:
            send = bot.sendMessage(
                message.from_user.id,
                text="Link Added",
            )
            send.delete()
        except Exception as e:
            LOGGER.error(e)
            buttons.buildbutton(
                "👉🏻 START BOT 👈🏻", f"https://t.me/{bot.get_me().username}?start=start"
            )
            help_msg += "Click on the START BOT button to start the bot in pm.\n<b>Its needed to to send your Mirror/Clone/Leeched Files in BOT PM.</b>\n\n"
    buttons = buttons.build_menu(2)
    if buttons.inline_keyboard != []:
        reply_message = sendMarkup(help_msg, bot, message, buttons)
        Thread(target=auto_delete_reply_message, args=(bot, message, reply_message)).start()
        return False
    else:
        return True
    
def BuildSourceLinkButton(link, buttons):
    try:
        sourcelink = link
        if sourcelink.startswith("magnet:"):
            # smsg = f"<br>{quote(sourcelink)}"
            # smsg += f"<br><br><b>💘 Share Magnet to</b> <a href='http://t.me/share/url?url={quote(sourcelink)}'>Telegram</a>"
            # slink = telegraph.create_page(title="Devil Mirrors Source Link", content=smsg)["path"]
            # buttons.buildbutton("🔗 Source Link 🔗", f"https://graph.org/{slink}")
            buttons.buildbutton(
                "🔗 Source Link 🔗",
                f"http://t.me/share/url?url={quote(sourcelink)}",
            )
        elif is_url(sourcelink):
            buttons.buildbutton("🔗 Source Link 🔗", sourcelink)
    except Exception as e:
        LOGGER.error(f"Unable to build button for Source Link because: {str(e)}")
    finally:
        return buttons

def GetAutoDeleteMessage(bot, message):
    if message.chat.type in ["private", "group"]:
        return ""
    reply_to = message.reply_to_message
    if reply_to is not None:
        try:
            Thread(target=auto_delete_upload_message, args=(bot, message, reply_to)).start()
        except Exception as e:
            LOGGER.error(str(e))
    autodel = secondsToText()
    return f"\n<b>❗ This message will be deleted in <i>{autodel}</i> from this group.</b>\n\n"
