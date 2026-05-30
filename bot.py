import os
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

FAL_KEY = os.environ["FAL_KEY"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 Hola! Escríbeme lo que quieres que dibuje.")

async def generar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    await update.message.reply_text("⏳ Generando tu imagen...")
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                "https://fal.run/fal-ai/flux/schnell",
                headers={"Authorization": f"Key {FAL_KEY}"},
                json={"prompt": texto, "num_images": 1}
            )
            data = r.json()
            await update.message.reply_text(f"Respuesta: {str(data)[:500]}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generar))
app.run_polling()
