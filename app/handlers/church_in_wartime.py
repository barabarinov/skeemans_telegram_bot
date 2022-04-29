from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler
from enum import Enum

conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('church_in_wartime', church_in_wartime)],
        states={ # словарь состояний разговора, возвращаемых callback функциями
            FIRST: [
                CallbackQueryHandler(donate, pattern='^' + 'Donate' + '$'),
                CallbackQueryHandler(Liqpay, pattern='^' + 'Liqpay' + '$'),
                CallbackQueryHandler(Crypto, pattern='^' + 'Crypto' + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            ],
        },
        fallbacks=[],
    )
