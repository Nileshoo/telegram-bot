import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==============================
# CONFIGURATION
# ==============================
BOT_TOKEN = "8345836270:AAGjWTjIMqacLP5uslwTIL2QkiyLak--Ins"   # 🔹 Replace with your BotFather token
CHANNEL_LINK = "https://t.me/linkwale_babu"  # 🔹 Replace with your channel link

# ==============================
# DATABASE SETUP
# ==============================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()


# ==============================
# START COMMAND
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Save user data if not already present
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user.id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
            (user.id, user.username, user.first_name, user.last_name),
        )
        conn.commit()

    # Send join message
    keyboard = [
        [InlineKeyboardButton("🚀 Join Our Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I Joined!", callback_data="joined")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\nWelcome to our bot.\n\nClick below to join our Telegram channel 👇",
        reply_markup=reply_markup
    )


# ==============================
# CALLBACK HANDLER (Button Click)
# ==============================
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "joined":
        await query.edit_message_text(
            "✅ You’ve joined successfully!"
        )

        # Send your viral video channel message
        message = """✅ ALL INSTAGRAM VIRAL VIDEO'S UPLOADED IN THIS CHANNEL ✅

👇👇👇

🎥 VIRAL REELS VIDEOS  
https://t.me/+dGtTbrgk7x85NjM1

💁‍♀️ VIP-Unseen INSTA INFLUNSER VIDEOS 💝  
https://t.me/+dGtTbrgk7x85NjM1

💝 VIP PREMIUM GROUP 💝  
https://t.me/+dGtTbrgk7x85NjM1

🤫 LEAKED COLLACTION 🎷  
https://t.me/+dGtTbrgk7x85NjM1
"""

        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=message,
            disable_web_page_preview=True
        )



# ==============================
# BROADCAST COMMAND (Admin Only)
# ==============================
ADMIN_ID = 123456789  # 🔹 Replace with your own Telegram user ID

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    message = " ".join(context.args)
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    count = 0
    for (user_id,) in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            count += 1
        except Exception:
            pass

    await update.message.reply_text(f"✅ Message sent to {count} users.")


# ==============================
# MAIN FUNCTION
# ==============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
