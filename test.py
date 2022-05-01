# from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os
import logging
#
# ############################### Bot ############################################
#
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
#
#
# def start(update, context):
#   update.message.reply_text(main_menu_message(),
#                             reply_markup=main_menu_keyboard())
#
#
# def main_menu(update, context):
#   query = update.callback_query
#   logger.info(f'QUERY IS HERE >>> {query} <<<')
#   query.answer()
#   query.edit_message_text(
#                         text=main_menu_message(),
#                         reply_markup=main_menu_keyboard())
#
#
# def first_menu(update, context):
#   query = update.callback_query
#   query.answer()
#   query.edit_message_text(
#                         text=first_menu_message(),
#                         reply_markup=first_menu_keyboard())
#
#
# def second_menu(update, context):
#   query = update.callback_query
#   query.answer()
#   query.edit_message_text(
#                         text=second_menu_message(),
#                         reply_markup=second_menu_keyboard())
#
#
# # and so on for every callback_data option
# def first_submenu(bot, update):
#   pass
#
#
# def second_submenu(bot, update):
#   pass
#
#
# ############################ Keyboards #########################################
#
#
# def main_menu_keyboard():
#   keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
#               [InlineKeyboardButton('Option 2', callback_data='m2')],
#               [InlineKeyboardButton('Option 3', callback_data='m3')]]
#   return InlineKeyboardMarkup(keyboard)
#
#
# def first_menu_keyboard():
#   keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
#               [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
#               [InlineKeyboardButton('Main menu', callback_data='main')]]
#   return InlineKeyboardMarkup(keyboard)
#
#
# def second_menu_keyboard():
#   keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
#               [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
#               [InlineKeyboardButton('Main menu', callback_data='main')]]
#   return InlineKeyboardMarkup(keyboard)
#
#
# ############################# Messages #########################################
#
#
# def main_menu_message():
#     return 'Choose the option in main menu:'
#
#
# def first_menu_message():
#     return 'Choose the submenu in first menu:'
#
#
# def second_menu_message():
#     return 'Choose the submenu in second menu:'
#
#
# ############################# Handlers #########################################
#
# load_dotenv()
# updater = Updater(token=os.getenv('TOKEN'), use_context=True)
# dispatcher = updater.dispatcher
#
# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
# updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
# updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
# updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,
#                                                     pattern='m1_1'))
# updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
#                                                     pattern='m2_1'))
#
# updater.start_polling()
# updater.idle()



# __________________


from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler)


FIRST, SECOND = range(2)

counter = 0

keyboard = [[InlineKeyboardButton('Decrement', callback_data='0')],
            [InlineKeyboardButton(f'[{counter}]', callback_data='1')],
            [InlineKeyboardButton('Increment', callback_data='2')]]


def start(update, context):
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Please choose one of our services\n',
        reply_markup=reply_markup
    )

    return FIRST


def update_and_get_reply_markup(inc_or_dec=None):
    global keyboard
    global counter
    if inc_or_dec == True:
        counter += 1
    else:
        counter -= 1

    keyboard[1][0] = InlineKeyboardButton(
        f'[{counter}]', callback_data='2')
    logger.info(f'\n>>> KEYBOARD 1 0{keyboard[1][0]},  KEYBOARD 2 0 {keyboard[2][0]} <<<')
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


def increment(update, context):
    query = update.callback_query

    reply_markup = update_and_get_reply_markup(inc_or_dec=True)
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please choose one of our services\n",
        reply_markup=reply_markup
    )

    return FIRST


def decrement(update, context):
    query = update.callback_query
    logger.info(f'>>> {query} <<<')

    reply_markup = update_and_get_reply_markup()
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please choose one of our services\n",
        reply_markup=reply_markup
    )

    return FIRST


def main():
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)

    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(decrement, pattern='^'+str(0)+'$'),
                    CallbackQueryHandler(increment, pattern='^'+str(2)+'$')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
