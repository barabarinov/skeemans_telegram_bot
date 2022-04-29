import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode
from app.information import text, thank_you

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('*Привіт! Я SKEEMANS CHURCH BOT!*✋🏼🙏🏼',
                              reply_markup=markup, parse_mode=ParseMode.MARKDOWN)


def online(update, callback: CallbackContext):
    update.message.reply_text('_https://www.youtube.com/SKEEMANSCHURCH/live?_', parse_mode=ParseMode.MARKDOWN)


def church_in_wartime(update, context):
    keyboard = [
        [
            InlineKeyboardButton('Donate/Допомогти', callback_data='Donate'),
        ],
    ]
    reply_keyboard = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=text + '\n_https://www.youtube.com/watch?v=5rNA2B80mE8_', parse_mode=ParseMode.MARKDOWN)
    query.edit_message_media(media=open('pics/web_war.png', 'rb'), reply_markup=reply_keyboard)

    # update.message.reply_photo(caption=text, photo=open('pics/web_war.png', 'rb'), reply_markup=reply_keyboard,
    #                            parse_mode=ParseMode.MARKDOWN)
    # update.message.reply_text('\n_https://www.youtube.com/watch?v=5rNA2B80mE8_', parse_mode=ParseMode.MARKDOWN)


def donate(update, context):
    keyboard = [[InlineKeyboardButton('LiqPay', callback_data='Liqpay')],
                [InlineKeyboardButton('Donate Crypto', callback_data='Crypto')]]

    reply_keyboard = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=thank_you(),
        reply_markup=reply_keyboard)
    # update.message.reply_text('Підтримати служіння церкви СКІМЕНС', reply_markup=reply_keyboard)


def liqpay(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='https://www.liqpay.ua/uk/checkout/card/checkout_1651162913093739_1222530_94exQbD8AwFApTtLg19X')
    # update.message.reply_text('https://www.liqpay.ua/uk/checkout/card/checkout_1651162913093739_1222530_94exQbD8AwFApTtLg19X')


def crypto(update, context):
    query = update.callback_query
    query.answer()
    query.message_text(
        text='https://skeemans.com/donate_crypto')
    # update.message.reply_text('https://skeemans.com/donate_crypto')


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

    reply_keyboard = [['Дивитись ONLINE'],
                      ['Церква під час війни'],
                      ['Залишити молитовну потребу'],
                      ['Розклад служінь']]

    # reply_keyboard = [keyboard for keyboard in reply_keyboard]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Дивитись ONLINE$') & ~Filters.command, online))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Церква під час війни$') & ~Filters.command, church_in_wartime))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Залишити молитовну потребу$') & ~Filters.command, pray_request))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Розклад служінь$') & ~Filters.command, service_schedule))
    updater.dispatcher.add_handler(CallbackQueryHandler(donate, pattern='Donate'))
    updater.dispatcher.add_handler(CallbackQueryHandler(liqpay, pattern='Liqpay'))
    updater.dispatcher.add_handler(CallbackQueryHandler(crypto, pattern='Crypto'))

    updater.start_polling()
    updater.idle()
