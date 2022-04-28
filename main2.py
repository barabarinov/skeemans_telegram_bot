import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode
from app.information import text, thank_you

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, callback: CallbackContext):
    update.message.reply_text('*Привіт! Я SKEEMANS CHURCH BOT!*',
                              reply_markup=markup, parse_mode=ParseMode.MARKDOWN)


def online(update, callback: CallbackContext):
    update.message.reply_text('_https://www.youtube.com/SKEEMANSCHURCH/live?_', parse_mode=ParseMode.MARKDOWN)


def church_in_wartime(update, callback: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton('/Donate', callback_data='Donate'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_photo(caption=text, photo=open('pics/web_war.png', 'rb'), reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text('\n_https://www.youtube.com/watch?v=5rNA2B80mE8_', parse_mode=ParseMode.MARKDOWN)


def donate(update, callback: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton('LiqPay', callback_data='Liqpay'),
        ],
        [
            InlineKeyboardButton('Donate Crypto', callback_data='Crypto'),
        ],
    ]
    reply_keyboard = InlineKeyboardMarkup(keyboard)
    update.message.reply_photo()
    update.message.reply_text('Donate is working!!!', reply_markup=reply_keyboard)


def liqpay(update, context: CallbackContext):
    update.message.reply_text(thank_you + 'https://www.liqpay.ua/uk/checkout/card/checkout_1651162913093739_1222530_94exQbD8AwFApTtLg19X')


def crypto(update, context: CallbackContext):
    update.message.reply_text('https://skeemans.com/donate_crypto')


def pray_request(update, callback: CallbackContext):
    update.message.reply_text('_https://skeemans.com/pray_', parse_mode=ParseMode.MARKDOWN)


def service_schedule(update, callback: CallbackContext):
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

    reply_keyboard = [
        ['/ONLINE'],
        ['/Church_in_wartime'],
        ['/Pray_requests'],
        ['/Service_schedule'],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('ONLINE', online))
    updater.dispatcher.add_handler(CommandHandler('Church_in_wartime', church_in_wartime))
    updater.dispatcher.add_handler(CommandHandler('Pray_requests', pray_request))
    updater.dispatcher.add_handler(CommandHandler('Service_schedule', service_schedule))
    updater.dispatcher.add_handler(CommandHandler('Donate', donate))

    updater.start_polling()
    updater.idle()
