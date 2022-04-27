# import logging
# import os
# from dotenv import load_dotenv
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
# from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
#
# from app.information import INFORMATION
#
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)
#
#
# def start(update, _):
#     keyboard = [
#         [
#             InlineKeyboardButton('Дивитись ONLINE', callback_data='Online'),
#         ],
#         [
#             InlineKeyboardButton('Церква у військовий час', callback_data='Церква у військовий час'),
#         ],
#         [
#             InlineKeyboardButton('Залишити молитовну потребу', callback_data='Молитовні потреби'),
#         ],
#         [
#             InlineKeyboardButton('Розклад служінь', callback_data='Розклад служінь'),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Зробіть вибір будь ласка:', reply_markup=reply_markup)
#
#
# def button(update, _):
#     # reply_keyboard = [['Go back']]
#     query = update.callback_query
#     variant = query.data
#     query.answer()
#     query.edit_message_text(text=f"{INFORMATION[variant]}", parse_mode=ParseMode.MARKDOWN)
#     update.effective_message.reply_text('*Натисніть сюди --> `/menu` щоб перейти до головного меню*', parse_mode=ParseMode.MARKDOWN)
#     update.effective_message.reply_text()
#
#
# if __name__ == '__main__':
#     load_dotenv()
#     updater = Updater(token=os.getenv('TOKEN'), use_context=True)
#     dispatcher = updater.dispatcher
#
#     updater.dispatcher.add_handler(CommandHandler('menu', start))
#     updater.dispatcher.add_handler(CallbackQueryHandler(button))
#     # updater.dispatcher.add_handler(CommandHandler('help', help_command))
#
#     updater.start_polling()
#     updater.idle()
