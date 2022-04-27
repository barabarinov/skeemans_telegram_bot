import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode

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
    text = '*ЗА КОЖНОЮ ДОБРОЮ СПРАВОЮ СТОЯТЬ ЛЮДИ!*\n🙏🏼🇺🇦\n' \
           'Неможливо одну команду відокремити від іншої, ми все робимо разом, і це справжня сім\'я СКІМЕНС. ' \
           'З перших днів війни наша місія у Києві, Рівному, Закарпатті, Польші, не припиняла своєї роботи. ' \
           'Тому що там, де біль, де потреба, де смерть - там точно місце церкви.У зоні нашої уваги жінки з дітьми, ' \
           'люди похилого віку та люди з інвалідністю. Ми розвозимо продукти харчування та предмети першої необхідності. ' \
           'Надає притулок тим, хто чекає на евакуацію або вже евакуйований з-під обстрілів. Ми забезпечуємо медикаментами ' \
           'та обладнанням лікарні та госпіталі. Наша місія в Польщі купує та доставляє одяг та взуття, а також засоби захисту для наших захісників. ' \
           'Капеланська робота ведеться як у Києві, так і в області. І головне, ми ніколи не забуваємо про основне призначення церкви – нести *Євангеліє*.'

    keyboard = [
        [
            InlineKeyboardButton('Donate', callback_data=donate),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)
    vid = '\nhttps://www.youtube.com/watch?v=5rNA2B80mE8'


def donate(update, callback: CallbackContext):
    update.message.reply_text('Donate is working!!!')


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

    updater.start_polling()
    updater.idle()
