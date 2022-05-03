from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update

from app.information import text_bank_details, text_donate
from telegram.ext import CallbackContext

SWIFT = 'swift'

# Links
LIQPAY_LINK = 'https://www.liqpay.ua/checkout/skeemanschurch'
CRYPTO_LINK = 'https://skeemans.com/donate_crypto'

reply_keyboard_submenu = [[InlineKeyboardButton('LiqPay 🔗', url=LIQPAY_LINK)],
                          [InlineKeyboardButton('Crypto 🔗', url=CRYPTO_LINK)],
                          [InlineKeyboardButton('SWIFT 🔗', callback_data=SWIFT)]]
reply_keyboard_donates = InlineKeyboardMarkup(reply_keyboard_submenu)


def main_donate(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=text_donate,
        reply_markup=reply_keyboard_donates,
        parse_mode=ParseMode.MARKDOWN,
    )


def swift(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='\n'.join(text_bank_details),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
