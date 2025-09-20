from time import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application

TOKEN = "" # BotFather в телеграмм. у него берите и самого бота, и токен

app = Application.builder().token(TOKEN).build()

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time()                          # 1. фиксируем время
    msg = await update.message.reply_text("🏓 pong")  # 2. отправляем ответ
    latency = round((time() - start) * 1000, 1)       # 3. считаем задержку
    await msg.edit_text("ыыыы я боооот(((")    # 4. обновляем сообщение

app.add_handler(CommandHandler("ping", ping))

async def curr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:                          # 1. /curr без аргументов
        await update.message.reply_text("напишите после /curr валюту. например: /curr USD")
        return
    code = context.args[0].upper()                # 2. достаём код валюты
    try:
        r = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10).json()
    except Exception:
        await update.message.reply_text("не удалось получить данные цб")
        return

    if code not in r["Valute"]:                   # 3. такой валюты нет
        await update.message.reply_text(f"валюта {code} не найдена")
        return

    value = r["Valute"][code]["Value"]
    await update.message.reply_text(f"1 {code} = {value:.2f} ₽")

app.add_handler(CommandHandler("curr", curr))



print("бот запущен. работаит")
app.run_polling()