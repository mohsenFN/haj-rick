""" Telegram API wrapper package"""
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, Filters, run_async
""" SQLite3 and requests package"""
import requests, sqlite3
""" Others """
import confing as cnf
import sql__

@run_async
def start_callback(update, context):
    update.message.reply_text(cnf.start_text)

def google_boy(update, context):
    text2 = context.args[0:]
    data = cnf.base_url+'+'.join([str(x) for x in text2])
    keyboard = [[InlineKeyboardButton("آموزش سرچ", url=data)]]
    keybs_header_text = cnf.search_help + ' '.join([str(x) for x in text2])

    try:
        if update.message.chat.type in cnf.valid_types:
            update.message.reply_to_message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        if update.message.chat.type in cnf.valid_types: 
            update.message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))

@run_async
def stackof_boy(update, context):
    try:
        text2 = context.args[0:]
        data = cnf.stack_base_url+'+'.join([str(x) for x in text2])
        
        keyboard = [[InlineKeyboardButton("رو من بزن", url=data)]]

        keybs_header_text = cnf.search_help + ' '.join([str(x) for x in text2]) 
        try:
            if update.message.chat.type in cnf.valid_types:
                update.message.reply_to_message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))
        
        except:
            if update.message.chat.type in cnf.valid_types:
                update.message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        pass
            

# SQLite3 dn management 
conn = sqlite3.connect("assistant.db", check_same_thread=False)
c = conn.cursor()

c.execute(sql__.table_syntax)
conn.commit()



@run_async
def set_qa_function(update, context):
    if update.message.chat.type == "private":
        update.message.reply_text() # config file

    is_admin = False
    for i in context.bot.getChatAdministrators(update.message.chat_id):
        if update.message.from_user.id == i.user.id:
            is_admin = True
        elif update.message.from_user.id == cnf.chat_id:
            is_admin = True
    
    

    if context.args[0] in cnf.list_args:
        if is_admin:
            text_ts = ''
            for row in sql__.all_q_a(c, conn):
                text_ts = text_ts+'\n'+row[0]+' --> '+' '.join(eval(row[1]))
            update.message.reply_text(text_ts)

    
    elif context.args[0] == "rm":
        if is_admin:
            try:
                sql__.delete_q(c, conn, context.args[1])
                update.message.reply_text(cnf.removed_text)
            except:
                pass
    

    else:
        if is_admin and str(context.args[0]).startswith('!'):
            sql__.insert_qa(c,conn, str(context.args[0]), str(context.args[1:]))
            update.message.reply_text(cnf.added_text)

@run_async
def qa_manager(update, context):
    user_q = update.message.text.lower()
    
    try:
        update.message.reply_to_message.reply_text(
            ' '.join(eval((sql__.answer_to_q(c, conn, user_q)[0][0]))))
    except:
        update.message.reply_text(
            ' '.join(eval((sql__.answer_to_q(c, conn, user_q)[0][0]))))
    

def free_command(update, context):
    is_admin = False
    for i in context.bot.getChatAdministrators(update.message.chat_id):
        if update.message.from_user.id == i.user.id:
            is_admin = True
        elif update.message.from_user.id == cnf.chat_id:
            is_admin = True
    try:
        if is_admin:
            message_for_2nd = "@"+update.message.reply_to_message.from_user.username + cnf.redire_1
            message_for_1nd = "@"+update.message.reply_to_message.from_user.username + cnf.redire_2
            update.message.reply_to_message.reply_text(message_for_1nd)
            context.bot.send_message("@pyspy_free", message_for_2nd)
            context.bot.deleteMessage(update.message.chat_id, update.message.reply_to_message.message_id)
            context.bot.deleteMessage(update.message.chat_id, update.message.message_id)
    except:
        pass

def welcome_function(update, context):
    try:
        context.bot.deleteMessage(update.message.chat_id, update.message.message_id)
    except:
        pass
    

updater = Updater(token=cnf.token, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start_callback))
updater.dispatcher.add_handler(CommandHandler("add", set_qa_function))
updater.dispatcher.add_handler(CommandHandler("start", start_callback))
updater.dispatcher.add_handler(CommandHandler('google', google_boy))
updater.dispatcher.add_handler(CommandHandler('stack', stackof_boy))
updater.dispatcher.add_handler(CommandHandler("free", free_command))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(('!\w+')), qa_manager))
updater.dispatcher.add_handler(MessageHandler(Filters.status_update, welcome_function))
print("running")
updater.start_polling()
updater.idle()