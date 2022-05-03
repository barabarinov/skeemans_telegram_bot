import logging
import os
from dotenv import load_dotenv

from app.handlers.donate import main_donate, swift, SWIFT
from app.handlers.buttons import (
    start,
    get_help,
    online,
    church_in_wartime,
    pray_request,
    service_schedule,

)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    load_dotenv()
    PORT = int(os.environ.get('PORT', 5000))
    TOKEN = os.getenv('TOKEN')

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Служіння в Бучі ❤️$') & ~Filters.command, get_help))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Cлужіння LIVE 🔴$') & ~Filters.command, online))
    dispatcher.add_handler(
        MessageHandler(Filters.regex('^Церква під час війни 🇺🇦$') & ~Filters.command, church_in_wartime)
    )
    dispatcher.add_handler(MessageHandler(Filters.regex('^Молитовна потреба 🙏🏻$') & ~Filters.command, pray_request))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Недільне служіння 💒$') & ~Filters.command, service_schedule))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Підтримати \(Donate\) ✊🏼$') & ~Filters.command, main_donate))
    dispatcher.add_handler(CallbackQueryHandler(swift, pattern=SWIFT))

    updater.start_webhook(
                        listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url=f'https://skeemans-telegram-bot.herokuapp.com/{TOKEN}'
    )

    # updater.start_polling()
    updater.idle()
