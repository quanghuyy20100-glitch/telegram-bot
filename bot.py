import os
import random
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8860523888:AAH09hMa5nHj-roxTIed6v1NB9oghgG6UFU"
ADMIN_ID = 8655331222  # thay bằng ID Telegram của bạn

welcome_text = "Xin chào! Chào mừng bạn đến với bot 🤖"
auto_reply = "Mình chưa hiểu, hãy thử /play nhé!"

games = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(welcome_text)


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 10)
    games[update.effective_user.id] = number

    await update.message.reply_text(
        "🎮 Mình đã chọn một số từ 1-10.\nHãy đoán số!"
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id in games:
        try:
            guess = int(text)
            answer = games[user_id]

            if guess == answer:
                await update.message.reply_text("🎉 Đúng rồi!")
                del games[user_id]
            else:
                await update.message.reply_text("❌ Sai rồi, thử lại!")
            return

        except:
            pass

    await update.message.reply_text(auto_reply)


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "/setwelcome Nội dung chào\n"
        "/setreply Nội dung trả lời"
    )


async def setwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global welcome_text

    if update.effective_user.id != ADMIN_ID:
        return

    welcome_text = " ".join(context.args)
    await update.message.reply_text("Đã đổi lời chào!")


async def setreply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global auto_reply

    if update.effective_user.id != ADMIN_ID:
        return

    auto_reply = " ".join(context.args)
    await update.message.reply_text("Đã đổi trả lời tự động!")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("setwelcome", setwelcome))
    app.add_handler(CommandHandler("setreply", setreply))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
