import logging
import os

from dotenv import load_dotenv
from app.information import text, thank_you, help_text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('*Привіт! Я SKEEMANS CHURCH BOT!*✋🏼🙏🏼',
                              reply_markup=reply_markup_general, parse_mode=ParseMode.MARKDOWN)


def get_help(update, callback: CallbackContext):
    update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


def online(update, callback):
    update.message.reply_text('https://www.youtube.com/SKEEMANSCHURCH/live?', parse_mode=ParseMode.MARKDOWN)


def church_in_wartime(update, context):
    keyboard = [
        [
            InlineKeyboardButton('Donate/Допомогти', callback_data='Підтримати (Donate) ✊🏼'),
        ],
    ]
    reply_keyboard = InlineKeyboardMarkup(keyboard)

    update.message.reply_photo(caption=text, photo=open('pics/web_war.png', 'rb'), reply_markup=reply_keyboard,
                               parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text('\n_https://www.youtube.com/watch?v=5rNA2B80mE8_', parse_mode=ParseMode.MARKDOWN)


def main_donate(update, context):
    update.message.reply_text('https://skeemans.com/donate', parse_mode=ParseMode.MARKDOWN)


def update_and_get_reply_markup():
    keyboard = [[InlineKeyboardButton('LiqPay', callback_data='Liqpay')],
                [InlineKeyboardButton('Donate Crypto', callback_data='Donate Crypto')]]
    reply_keyboard_donate = InlineKeyboardMarkup(keyboard)
    return reply_keyboard_donate


def donate(update, context):
    # update.callback_query.message.edit_text('Підтримати служіння церкви СКІМЕНС', reply_markup=update_and_get_reply_markup())
    query = update.callback_query
    query.data
    logger.info(f'QUERY >>> {query}')
    query.answer()
    logger.info(f'QUERY.ANSWER >>> {query.answer}')
    bot = context.bot

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Підтримати служіння церкви СКІМЕНС',
        reply_markup=update_and_get_reply_markup()
    )

    # update.callback_query.edit_message_text('Підтримати служіння церкви СКІМЕНС', reply_markup=reply_keyboard_donate)
    # update.message.reply_text('Підтримати служіння церкви СКІМЕНС', reply_markup=reply_keyboard_donate)


def liqpay(update, context):
    update.message.reply_text(
        'https://www.liqpay.ua/uk/checkout/card/checkout_1651162913093739_1222530_94exQbD8AwFApTtLg19X')


def crypto(update, context):
    update.message.reply_text('https://skeemans.com/donate_crypto')


def pray_request(update, context):
    update.message.reply_text('_https://skeemans.com/pray_', parse_mode=ParseMode.MARKDOWN)


def service_schedule(update, context):
    update.message.reply_text(
        '*НЕДІЛЯ:*\n_13:00 - Недільне служіння + Підліткове (вік 9-11)\n16:00 - Недільне служіння + Підліткове (вік 12-18)_',
        parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text('\n'.join(['*04128 Київ*',
                                         '*_вул\. Стеценка 30_*',
                                         '_\+38 066 54 56 558_',
                                         '_\+38 067 10 04 396_',
                                         '_skeemans@gmail\.com_',
                                         ]), parse_mode=ParseMode.MARKDOWN_V2)
    update.message.reply_location(latitude=50.496194103883155, longitude=30.372488286210967)


if __name__ == '__main__':
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    reply_keyboard = [['Служіння в Бучі ❤️', 'Церква під час війни 🇺🇦'],
                      ['Підтримати (Donate)', 'Залишити молитовну потребу 🙏🏻'],
                      ['Розклад служіннь 💒', 'Дивитись трансляцію 🔴']]

    reply_markup_general = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Служіння в Бучі ❤️$') & ~Filters.command, get_help))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Підтримати \(Donate\)$') & ~Filters.command, main_donate))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Дивитись трансляцію 🔴$') & ~Filters.command, online))
    dispatcher.add_handler(
        MessageHandler(Filters.regex('^Церква під час війни 🇺🇦$') & ~Filters.command, church_in_wartime))
    dispatcher.add_handler(
        MessageHandler(Filters.regex('^Залишити молитовну потребу 🙏🏻$') & ~Filters.command, pray_request))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Розклад служіннь 💒$') & ~Filters.command, service_schedule))
    dispatcher.add_handler(CallbackQueryHandler(donate, pattern='Підтримати'))
    dispatcher.add_handler(CallbackQueryHandler(liqpay, pattern='Liqpay'))
    dispatcher.add_handler(CallbackQueryHandler(crypto, pattern='Donate Crypto'))

    updater.start_polling()
    updater.idle()
