# telegram api wrapper package
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext import Updater, Filters, run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# other packages
import requests
import sqlite3

chat_id = 255877970
# WARNING MAIN BOTS TOKEN
token = "TOKEN"
stack_base_url = "http://lmsotfy.com/?q="
base_url = "https://lmgtfy.com/?q="

def start_callback(update, context):
    update.message.reply_text("""سلام\nحاجی تون ریک سانچز هستم""")

def google_boy(update, context):
    text2 = context.args[0:]
    data = base_url+'+'.join([str(x) for x in text2])
    
    keyboard = [[InlineKeyboardButton("آموزش سرچ", url=data)]]

    keybs_header_text = "اموزش سرچ کردن عبارت " + ' '.join([str(x) for x in text2])

    try:
        if update.message.chat.type == "supergroup" or update.message.chat.type == "group":
            update.message.reply_to_message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        if update.message.chat.type == "supergroup" or update.message.chat.type == "group":
            update.message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))


def stackof_boy(update, context):
    try:
        text2 = context.args[0:]
        data = stack_base_url+'+'.join([str(x) for x in text2])
        
        keyboard = [[InlineKeyboardButton("رو من بزن", url=data)]]

        keybs_header_text = "اموزش سرچ کردن عبارت" + ' '.join([str(x) for x in text2]) 
        try:
            if update.message.chat.type == "supergroup" or update.message.chat.type == "group":
                update.message.reply_to_message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))
        
        except:
            if update.message.chat.type == "supergroup" or update.message.chat.type == "group":
                update.message.reply_text(keybs_header_text, reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as error:
        print(error)
            

# SQLite3 dn management 
conn = sqlite3.connect("assistant.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS smartq (
    question VARCHAR(32) NOT NULL PRIMARY KEY,
    answer VARCHAR(1024) NOT NULL)""")

conn.commit()

def insert_qa(q, a):
    c.execute("INSERT INTO smartq (question, answer) VALUES (?, ?)", (q, a))
    conn.commit()

def asnwer_to_q(q):
    c.execute("SELECT answer FROM smartq WHERE question=?", (q,))
    return c.fetchall()

def all_q_a():
    c.execute("SELECT * FROM smartq")
    return c.fetchall()

def delete_q(q):
    c.execute("DELETE FROM smartq WHERE question=?", (q,))
    conn.commit()


@run_async
def start_function(update, context):
    update.message.reply_text(start_text)


@run_async
def set_qa_function(update, context):
    if update.message.chat.type == "private":
        update.message.reply_text("شرمنده فقظ تو گروها جواب میدم")

    is_admin = False
    for i in context.bot.getChatAdministrators(update.message.chat_id):
        if update.message.from_user.id == i.user.id:
            is_admin = True
        elif update.message.from_user.id == chat_id:
            is_admin = True
    
    

    if context.args[0] == "all" or context.args[0] == "list":
        if is_admin:
            text_ts = ''
            for row in all_q_a():
                text_ts = text_ts+'\n'+row[0]+' --> '+' '.join(eval(row[1]))
            update.message.reply_text(text_ts)

    
    elif context.args[0] == "rm":
        if is_admin:
            try:
                delete_q(context.args[1])
                update.message.reply_text("ریموو شد")
            except:
                pass
    

    else:
        if is_admin and str(context.args[0]).startswith('!'):
            try:
                insert_qa(str(context.args[0]), str(context.args[1:]))
                update.message.reply_text("حله اضافه شد")
            
            except:
                update.message.reply_text("اوه! ارور داد")


@run_async
def qa_manager(update, context):
    user_q = update.message.text.lower()
    
    try:
        update.message.reply_to_message.reply_text(
            ' '.join(eval((asnwer_to_q(user_q)[0][0]))))
    except:
        update.message.reply_text(
            ' '.join(eval((asnwer_to_q(user_q)[0][0]))))
    

def free_command(update, context):
    is_admin = False
    for i in context.bot.getChatAdministrators(update.message.chat_id):
        if update.message.from_user.id == i.user.id:
            is_admin = True
        elif update.message.from_user.id == chat_id:
            is_admin = True
    try:
        if is_admin:
            message_for_2nd = "@"+update.message.reply_to_message.from_user.username+"\n سوال خود را در اینجا مطرح کنید"
            message_for_1nd = "@"+update.message.reply_to_message.from_user.username+"\n"+"سوال شما مربوط به موضوع گروه نیست.سوال خود را در گروه زیر مطرح کنید. \n @pyspy_free"
            update.message.reply_to_message.reply_text(message_for_1nd)
            context.bot.send_message("@pyspy_free", message_for_2nd)
            context.bot.deleteMessage(update.message.chat_id, update.message.reply_to_message.message_id)
            context.bot.deleteMessage(update.message.chat_id, update.message.message_id)
    except Exception as error:
        print(error)

def welcome_function(update, context):
    try:
        context.bot.deleteMessage(update.message.chat_id, update.message.message_id)
    except:
        pass
    

updater = Updater(token=token, use_context=True)
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
