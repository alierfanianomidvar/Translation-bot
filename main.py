import os
import googletrans
import DataBase as db

from dotenv import load_dotenv
from telegram.ext import *
from googletrans import Translator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


load_dotenv()
API_KEY = os.environ.get('API_KEY')
print(API_KEY)
updater = Updater(API_KEY, use_context=True)
dp = updater.dispatcher
languages = googletrans.LANGUAGES


def start_command(update, context):
    update.message.reply_text('Hi, Welcome to TranslateForMe :) \n'
                              'we will translate your text to any language you want \n'
                              'for start you can select or type /translate \n'
                              'after you can choose your target language if you want change the language type /translate again'
                              ' ☺️')


def help_command(update, context):
    update.message.reply_text('for translate or change the target language please type or select /translate, tnx ☺️')


# def choose_language(update, context):
#     languages = googletrans.LANGUAGES
#     new_output = list(languages.values())
#     List = ''
#     for x in new_output:
#         List += ('/' + x)
#         List += "\n "
#     update.message.reply_text('pls choose your target language \n  ' + List)
#     dp.add_handler(CommandHandler(Filters.text, trans))

def fav_choose_language(update, context):
    list_fav_language = ['english', 'german', 'korean', 'persian', 'russian']
    button_list = create_button_list(list_fav_language)
    button_list.append([InlineKeyboardButton('more', callback_data='more')])
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(button_list),
                             text="Choose your languages")
    dp.add_handler(CallbackQueryHandler(queryHandler))


def all_choose_language(update, context):
    language_list = languages.values()
    button_list = create_button_list(language_list)
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(button_list),
                             text="Choose your target languages")
    dp.add_handler(CallbackQueryHandler(queryHandler))


def create_button_list(language_list):
    button_list = []
    for x in language_list:
        button_list.append([InlineKeyboardButton(x, callback_data=x)])
    return button_list


def queryHandler(update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()
    print("we are in query")
    print(query)
    update.callback_query.from_user.send_message('\n' + query + '\n')
    if query != 'more':
        print(update.callback_query.from_user.username)
        db.insert(update.callback_query.from_user.id,
                  update.callback_query.from_user.username,
                  update.callback_query.from_user.first_name,
                  update.callback_query.from_user.last_name,
                  query)
        update.callback_query.from_user.send_message('enter your text :')
        dp.add_handler(MessageHandler(Filters.text, translate))
    else:
        all_choose_language(update, context)


def find_target(value):
    for key, val in languages.items():
        if value == val:
            return key
    return "key doesn't exist"


def translate(update, context):
    text = str(update.message.text).lower()
    translator = Translator()
    print(find_target(db.get_data(update.message.chat.id)))
    kir = translator.translate(text, dest=find_target(db.get_data(update.message.chat.id)))
    print(kir.text)
    update.message.reply_text(kir.text)


def main():
    db.create_table()
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('translate', fav_choose_language))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
