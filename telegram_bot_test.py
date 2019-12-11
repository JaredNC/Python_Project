from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sensitive_info as si
import logging
import newciv_bot as nc
import pprint
import time
import pyimgur

print('test')
creds = si.SecurityCreds()
updater = Updater(token=creds.telegram_token, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I'm better than Sexbot!")
    print("start cmd")


def suicide(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ok senpai, i'll die :'(")
    print("stopping")
    quit()


def debug(update, context):
    # pprint.pprint(vars(update.effective_chat))
    # pprint.pprint(vars(update.effective_message))
    # pprint.pprint(vars(update.effective_user))
    # print(update.effective_chat)
    print(update.effective_message)
    # print(update.effective_user)
    # print(update.effective_message.reply_to_message)
    # pprint.pprint(update.effective_message.reply_to_message)


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


def hof(update, context):
    user = update.effective_message.reply_to_message.from_user.first_name
    msg = update.effective_message.reply_to_message.text
    new_post = user + ": " + msg
    new = nc.NewcivLogin()
    new.make_newpost(new_post, 1054689)
    context.bot.send_message(chat_id=update.effective_chat.id, text="HoF'd")
    print("hof: " + new_post)


def photo(update, context):
    # user = update.effective_message.reply_to_message.from_user.first_name
    photo_file = update.effective_message.reply_to_message.photo[-1].get_file()
    # location = '/imgs/' + str(int(time.time())) + user + '_photo.jpg'
    # photo_file.download(location)
    # print(photo_file.file_path)
    client_id = creds.imgur_id
    im = pyimgur.Imgur(client_id)
    img = photo_file.file_path
    uploaded_image = im.upload_image(url=img, title="title")
    print(uploaded_image.link)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Gorgeous! ' + uploaded_image.link)
    return uploaded_image.link


def post_photo(update, context):
    link = photo(update, context)
    user = update.effective_message.reply_to_message.from_user.first_name
    args = update.message.text.split("^")
    newpost = "[quote=" + user + "]" + args[0][11:] + "[/quote][img]" + link + "[/img]"
    new = nc.NewcivLogin()
    new.make_newpost(newpost, args[1])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Posted in thread https://forums.novociv.org/showthread.php?{0}".format(args[1]))
    print("post cmd: " + args[1] + " " + args[0][6:])


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start, Filters.chat(creds.chat_id))
dispatcher.add_handler(start_handler)
suicide_handler = CommandHandler('suicide', suicide, Filters.chat(creds.chat_id))
dispatcher.add_handler(suicide_handler)
debug_handler = CommandHandler('debug', debug, Filters.user(742801303))
dispatcher.add_handler(debug_handler)
caps_handler = CommandHandler('caps', caps, Filters.chat(creds.chat_id) | Filters.chat(-1001406244740))
dispatcher.add_handler(caps_handler)
echo_handler = MessageHandler(Filters.text, echo, Filters.chat(creds.chat_id))
# dispatcher.add_handler(echo_handler)
post_handler = CommandHandler('post', post, Filters.chat(creds.chat_id) | Filters.chat(-1001406244740))
dispatcher.add_handler(post_handler)
thread_handler = CommandHandler('thread', thread, Filters.chat(creds.chat_id) | Filters.chat(-1001406244740))
dispatcher.add_handler(thread_handler)
hof_handler = CommandHandler('hof', hof, Filters.chat(creds.chat_id) | Filters.chat(-1001406244740))
dispatcher.add_handler(hof_handler)
photo_handler = CommandHandler('photo', photo, Filters.user(742801303) | Filters.chat(creds.chat_id) | Filters.chat(-1001406244740))
dispatcher.add_handler(photo_handler)
post_photo_handler = CommandHandler('post_photo', post_photo, Filters.user(742801303) | Filters.chat(creds.chat_id) | Filters.chat(-1001406244740))
dispatcher.add_handler(post_photo_handler)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

