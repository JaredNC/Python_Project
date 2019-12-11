from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sensitive_info as si
import logging
import newciv_bot as nc


print('test')
creds = si.SecurityCreds()
updater = Updater(token=creds.telegram_token, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I'm better than Sexbot!")
    print("start cmd")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    print("caps cmd: " + text_caps)


def post(update, context):
    args = update.message.text.split("^")
    new = nc.NewcivLogin()
    new.make_newpost(args[0][6:], args[1])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Posted in thread https://forums.novociv.org/showthread.php?{0}".format(args[1]))
    print("post cmd: " + args[1] + " " + args[0][6:])


def thread(update, context):
    args = update.message.text.split("^")
    new = nc.NewcivLogin()
    new_t = new.make_newthread(args[0][8:], args[1], args[2])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Posted in forum https://forums.novociv.org/forumdisplay.php?{0} thread {1}".format(args[2], new_t.url))
    print("thread cmd: F- " + args[2] + " T-" + args[0][6:] + " P-" + args[1])


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)
echo_handler = MessageHandler(Filters.text, echo)
# dispatcher.add_handler(echo_handler)
post_handler = CommandHandler('post', post)
dispatcher.add_handler(post_handler)
thread_handler = CommandHandler('thread', thread)
dispatcher.add_handler(thread_handler)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

