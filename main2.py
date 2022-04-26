import logging
import os
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyMarkup, ParseMode, Update

from app.information import INFORMATION

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def online(update):
    update.message.reply_text('_https://www.youtube.com/SKEEMANSCHURCH/live?_', parse_mode=ParseMode.MARKDOWN)


def church_in_wartime(update):
    keyboard = [
        [
            InlineKeyboardButton('Допомогти/Donate', callback_data='Церква у військовий час'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(INFORMATION['Церква у військовий час'], reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    # update.message.reply_text(
    #     '*ЗА КОЖНОЮ ДОБРОЮ СПРАВОЮ СТОЯТЬ ЛЮДИ!*\n'
    #     'Неможливо одну команду відокремити від іншої, ми все робимо разом, і це справжня сім\'я СКІМЕНС. '
    #     'З перших днів війни наша місія у Києві, Рівному, Закарпатті, Польші, не припиняла своєї роботи. '
    #     'Тому що там, де біль, де потреба, де смерть - там точно місце церкви.У зоні нашої уваги жінки з дітьми, '
    #     'люди похилого віку та люди з інвалідністю. Ми розвозимо продукти харчування та предмети першої необхідності. '
    #     'Надає притулок тим, хто чекає на евакуацію або вже евакуйований з-під обстрілів. Ми забезпечуємо медикаментами '
    #     'та обладнанням лікарні та госпіталі. Наша місія в Польщі купує та доставляє одяг та взуття, а також засоби захисту для наших захісників. '
    #     'Капеланська робота ведеться як у Києві, так і в області. І головне, ми ніколи не забуваємо про основне призначення церкви – нести *Євангеліє*.',
    #     parse_mode=ParseMode.MARKDOWN)


def pray_request(update):
    update.message.reply_text('_https://skeemans.com/pray_', parse_mode=ParseMode.MARKDOWN)


def service_schedule(update):
    update.message.reply_text('*НЕДІЛЯ:*\n_13:00 - Недільне служіння + Підліткове (вік 9-11)\n16:00 - Недільне служіння + Підліткове (вік 12-18)_')


def donation(update):
    reply_keyboard = [
        ['LiqPay'],
        ['Donate Crypto'],
    ]


if __name__ == '__main__':
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    reply_keyboard = [
        ['Дивитись ONLINE'],
        ['Церква у військовий час'],
        ['Залишити молитовну потребу'],
        ['Розклад служінь'],
    ]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    updater.dispatcher.add_handler(CommandHandler('Дивитись ONLINE', online))
    updater.dispatcher.add_handler(CommandHandler('Церква у військовий час', church_in_wartime))
    updater.dispatcher.add_handler(CommandHandler('Залишити молитовну потребу'), pray_request)
    updater.dispatcher.add_handler(CommandHandler('Розклад служінь'), service_schedule)
    updater.dispatcher.add_handler(CommandHandler('Допомогти/Donate'), donation)

    updater.start_polling()
    updater.idle()
