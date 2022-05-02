import logging
import os
from dotenv import load_dotenv

from app.information import text_wartime, text_bucha, text_live, text_hello
from app.handlers.donate import main_donate, swift

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode, Update
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

# Links
PRAY_LINK = 'https://skeemans.com/pray'
ONLINE_LINK = 'https://www.youtube.com/SKEEMANSCHURCH/live'

# buttons
reply_keyboard_menu = [['Служіння в Бучі ❤️', 'Церква під час війни 🇺🇦'],
                       ['Підтримати (Donate) ✊🏼', 'Молитовна потреба 🙏🏻'],
                       ['Недільне служіння 💒', 'Cлужіння LIVE 🔴']]
reply_keyboard_main = ReplyKeyboardMarkup(reply_keyboard_menu, one_time_keyboard=False)

reply_keboard_pray = [[InlineKeyboardButton('Написати 🔗', url=PRAY_LINK)]]
reply_keboard_praylink = InlineKeyboardMarkup(reply_keboard_pray)

reply_keboard_online = [[InlineKeyboardButton('Дивитись на YouTube 🔗', url=ONLINE_LINK)]]
reply_keboard_onlinelink = InlineKeyboardMarkup(reply_keboard_online)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text_hello, reply_markup=reply_keyboard_main, parse_mode=ParseMode.MARKDOWN
    )


def get_help(update: Update, context: CallbackContext):
    update.message.reply_text('\n\n'.join(text_bucha), parse_mode=ParseMode.MARKDOWN_V2)
    update.message.reply_location(latitude=50.55355869171877, longitude=30.241997608604798)


def online(update: Update, context: CallbackContext):
    update.message.reply_text(
        text_live,
        reply_markup=reply_keboard_onlinelink,
        parse_mode=ParseMode.MARKDOWN_V2
    )


def church_in_wartime(update: Update, context: CallbackContext):
    update.message.reply_text(f'*ЗА КОЖНОЮ ДОБРОЮ СПРАВОЮ СТОЯТЬ ЛЮДИ!*\n🙏🏼🇺🇦\n', parse_mode=ParseMode.MARKDOWN)
    update.message.reply_photo(
        caption=text_wartime,
        photo=open('pics/web_war.png', 'rb'),
        parse_mode=ParseMode.MARKDOWN
    )


def pray_request(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f'{"[ТУТ](https://skeemans.com/pray)"} ви можете залишити молитовну потребу, і церква буде молитися за неї разом із вами 🙏🏼',
        reply_markup=reply_keboard_praylink,
        parse_mode=ParseMode.MARKDOWN
    )


def service_schedule(update: Update, context: CallbackContext):
    update.message.reply_text('\n'.join(['_13:00 \- зібрання в церкві_',
                                         '_16:00 \- онлайн служіння_',
                                         ]), reply_markup=reply_keboard_onlinelink, parse_mode=ParseMode.MARKDOWN_V2)
    update.message.reply_text('_Київ, вул\.Стеценка 30, лінія 4_', parse_mode=ParseMode.MARKDOWN_V2)
    update.message.reply_location(latitude=50.496194103883155, longitude=30.372488286210967)


if __name__ == '__main__':
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Служіння в Бучі ❤️$') & ~Filters.command, get_help))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Cлужіння LIVE 🔴$') & ~Filters.command, online))
    dispatcher.add_handler(
        MessageHandler(Filters.regex('^Церква під час війни 🇺🇦$') & ~Filters.command, church_in_wartime))
    dispatcher.add_handler(
        MessageHandler(Filters.regex('^Молитовна потреба 🙏🏻$') & ~Filters.command, pray_request))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Недільне служіння 💒$') & ~Filters.command, service_schedule))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Підтримати \(Donate\) ✊🏼$') & ~Filters.command, main_donate))
    dispatcher.add_handler(CallbackQueryHandler(swift, pattern='swift'))

    updater.start_polling()
    updater.idle()
