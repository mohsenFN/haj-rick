from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext import Updater, Filters, run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from sql__ import DbManager
import confing as cnf
import requests
dbm = DbManager("rickBot.db")

@run_async
def start_callback(update, context):
    update.message.reply_text(cnf.start_text)

@run_async
def welcome_function(update, context):
    context.bot.deleteMessage(update.message.chat_id, update.message.message_id)

def google_boy(update, context):
    text2 = context.args[0:]
    data = cnf.base_url+'+'.join([str(x) for x in text2])
    keyboard = [[InlineKeyboardButton("آموزش سرچ", url=data)]]
    keybs_header_text = cnf.search_help + ' '.join([str(x) for x in text2])

    if update.message.chat.type in cnf.valid_types:
        if update.message.reply_to_message is not None:
            update.message.reply_to_message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            update.message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))

@run_async
def stackof_boy(update, context):
    text2 = context.args[0:]
    data = cnf.stack_base_url+'+'.join([str(x) for x in text2])
    keyboard = [[InlineKeyboardButton("رو من بزن", url=data)]]
    keybs_header_text = cnf.search_help + " " + " ".join([str(x) for x in text2]) 

    if update.message.chat.type in cnf.valid_types:
        if update.message.reply_to_message is not None:
            update.message.reply_to_message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            update.message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))

@run_async
def set_qa_function(update, context):
    if update.message.chat.type == "private":
        update.message.reply_text(cnf.pv_text) 

    is_admin = False
    for i in context.bot.getChatAdministrators(update.message.chat_id):
        if update.message.from_user.id == i.user.id:
            is_admin = True
        elif update.message.from_user.id == cnf.chat_id:
            is_admin = True

    if is_admin and str(context.args[0]).startswith('!'):
        try:
            dbm.insert_qa(str(context.args[0]), str(context.args[1:]))
            update.message.reply_text(cnf.added_text)
        except Exception as rr:
            print(rr)

@run_async
def qa_manager(update, context):
    user_q = update.message.text.lower()

    if update.message.reply_to_message is not None:
        update.message.reply_to_message.reply_text(
            ' '.join(eval(dbm.answer_to_q(user_q)[0][0])).replace("!!", "\n"))
    else:
        update.message.reply_text(
            ' '.join(eval(dbm.answer_to_q(user_q)[0][0])).replace("!!", "\n"))

def free_command(update, context):
    is_admin = False
    for i in context.bot.getChatAdministrators(update.message.chat_id):
        if update.message.from_user.id == i.user.id:
            is_admin = True
        elif update.message.from_user.id == cnf.chat_id:
            is_admin = True
    
    if is_admin:
        message_for_2nd = "@"+update.message.reply_to_message.from_user.username + cnf.redire_1
        message_for_1nd = "@"+update.message.reply_to_message.from_user.username + cnf.redire_2
        update.message.reply_to_message.reply_text(message_for_1nd)
        context.bot.send_message("@pyspy_free", message_for_2nd)

        for message_to_delete in [update.message.reply_to_message.message_id, update.message_id.message_id]:
            context.bot.deleteMessage(update.message.chat_id, message_to_delete)

def qa_deleter(update, context):
    if update.message.chat.type == "private":
        update.message.reply_text(cnf.pv_text) 

    is_admin = False
    for i in context.bot.getChatAdministrators(update.message.chat_id):
        if update.message.from_user.id == i.user.id:
            is_admin = True
        elif update.message.from_user.id == cnf.chat_id:
            is_admin = True

    if is_admin:
        try:
            dbm.delete_q(context.args[0])
            update.message.reply_text(cnf.removed_text)
        except Exception as rr:
            print(rr)

def qa_lister(update, context):
    if update.message.chat.type == "private":
        update.message.reply_text(cnf.pv_text) 

    is_admin = False
    for i in context.bot.getChatAdministrators(update.message.chat_id):
        if update.message.from_user.id == i.user.id:
            is_admin = True
        elif update.message.from_user.id == cnf.chat_id:
            is_admin = True

    if is_admin:
            text_ts = ''
            for row in dbm.all_q_a():
                text_ts = text_ts+'\n'+row[0]+' --> '+(' '.join(eval(row[1])).replace("!!", "(nl)"))
            update.message.reply_text(text_ts)
    

updater = Updater(token=cnf.token, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start_callback))
updater.dispatcher.add_handler(CommandHandler("add", set_qa_function))
updater.dispatcher.add_handler(CommandHandler("start", start_callback))
updater.dispatcher.add_handler(CommandHandler('google', google_boy))
updater.dispatcher.add_handler(CommandHandler('stack', stackof_boy))
updater.dispatcher.add_handler(CommandHandler("free", free_command))
updater.dispatcher.add_handler(CommandHandler("rm", qa_deleter))
updater.dispatcher.add_handler(CommandHandler("list", qa_lister))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(('!\w+')), qa_manager))
updater.dispatcher.add_handler(MessageHandler(Filters.status_update, welcome_function))
print("running")
updater.start_polling()
updater.idle()