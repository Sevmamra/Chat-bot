!pip install python-telegram-bot==20.3 openai python-dotenv

import os
import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure
TOKEN = os.getenv("TELEGRAM_TOKEN")  # या सीधे यहाँ डालें "YOUR_TELEGRAM_TOKEN"
OPENAI_KEY = os.getenv("OPENAI_KEY")  # https://platform.openai.com/api-keys से लें

# AI Setup
openai.api_key = OPENAI_KEY
AI_MODEL = "gpt-3.5-turbo"

# Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hi! I'm your AI assistant. Ask me anything!")

async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": user_msg}]
        )
        await update.message.reply_text(response.choices[0].message['content'])
    except Exception as e:
        await update.message.reply_text(f"🚨 Error: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
    app.run_polling()

if __name__ == "__main__":
    print("🚀 AI Bot is running...")
    main()
