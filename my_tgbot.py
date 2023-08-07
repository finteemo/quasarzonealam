import time
import requests
import json

with open('snsid', 'r') as f:
    secret = {l.split('=')[0]: l.split('=')[1].rstrip() for l in f.readlines()}

token = secret['telegram_token']

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.chat_id)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def myname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'My name is {update.effective_user.first_name}')

    await update.message.reply_photo(open('./images.jpeg', 'rb'))

fake_db = {
    '국내' : ['강릉', '푸산'],
    '해외' : ['이태리', '푸랑스']
}
async def trip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    target = update.message.text.split()[-1]
    locations = fake_db[target]
    await update.message.reply_text(f'추천여행지! {str(locations)}')

    await update.message.reply_photo(open('./images.jpeg', 'rb'))


app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("myname", myname))
app.add_handler(CommandHandler("trip", trip))

app.run_polling()


if __name__ == '__main__':
    print(token)

