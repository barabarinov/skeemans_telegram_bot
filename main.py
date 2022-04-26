import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from app.information import INFORMATION

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def menu(update, _):
    keyboard = [
        [
            InlineKeyboardButton('Дивитись ONLINE', callback_data='Online'),
        ],
        [
            InlineKeyboardButton('Церква у військовий час', callback_data='Церква у військовий час'),
        ],
        [
            InlineKeyboardButton('Залишити молитовну потребу', callback_data='Молитовні потреби'),
        ],
        [
            InlineKeyboardButton('Розклад служінь', callback_data='Розклад служінь'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Зробіть вибір будь ласка:', reply_markup=reply_markup)


def button(update, _):
    # reply_keyboard = [['/start']]
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы.
    # смотри https://core.telegram.org/bots/api#callbackquery.
    query.answer()
    # редактируем сообщение, тем самым кнопки
    # в чате заменятся на этот ответ.
    query.edit_message_text(text=f"{INFORMATION[variant]}")
    update.effective_message.reply_text('Використовуйте `/start` для показу головного меню')


def help_command(update, _):
    update.message.reply_text("Використовуйте `/menu` для показу головного меню")


if __name__ == '__main__':
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    updater.start_polling()
    updater.idle()
