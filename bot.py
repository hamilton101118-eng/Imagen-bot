import os
import fal_client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 Hola! Escríbeme lo que quieres que dibuje y lo genero al instante.")

async def generar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    await update.message.reply_text("⏳ Generando tu imagen, espera unos segundos...")
    try:
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={"prompt": texto, "num_images": 1}
        )
        imagen_url = result["images"][0]["url"]
        await update.message.reply_photo(photo=imagen_url, caption=f'✅ "{texto}"')
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generar))
app.run_polling()
