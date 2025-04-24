
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os

TOKEN = os.environ.get("TOKEN")
MS_TOKEN = os.environ.get("MS_TOKEN")

HEADERS = {
    'Authorization': f'Bearer {MS_TOKEN}',
    'Accept-Encoding': 'utf-8'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /товар [название] чтобы узнать наличие и цену.")

async def product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи название товара. Пример: /товар iPhone")
        return

    query = " ".join(context.args)
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/product?search={query}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if data.get("rows"):
        item = data["rows"][0]
        name = item.get("name")
        quantity = item.get("quantity", 0)
        price = item.get("salePrices", [{}])[0].get("value", 0) / 100

        availability = "В наличии" if quantity > 0 else "Нет в наличии"
        message = f"{name}\n{availability}\nЦена: {int(price):,} ₽"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Товар не найден.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("товар", product))

app.run_polling()
