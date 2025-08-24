import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# === CONFIG (embedded for your convenience) ===
BOT_TOKEN = "7010992295:AAGpK71jDhD_PYaMeUqppYSmF_VG2pGrWK4"
OWNER_USERNAME = "gaktauom"  # only this username can use the bot
OWNER_USER_ID = None         # optional: fill with your numeric ID later (int), e.g., 123456789
# =============================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("video-share-bot-owner-locked")

# In-memory store: code -> file_id (lifetime = process lifetime)
video_store = {}

def is_authorized(update: Update) -> bool:
    user = update.effective_user
    if not user:
        return False
    if OWNER_USER_ID is not None and user.id == OWNER_USER_ID:
        return True
    if user.username and user.username.lower() == OWNER_USERNAME.lower():
        return True
    return False

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.effective_message.reply_text("❌ Kamu tidak punya izin pakai bot ini.")
        return

    msg = update.effective_message
    if not msg or not msg.video:
        return

    file_id = msg.video.file_id
    code = str(msg.message_id)  # unik per pesan
    video_store[code] = file_id

    bot_username = (await context.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={code}"
    await msg.reply_text(f"Link ambil video (khusus owner):\n{link}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.effective_message.reply_text("❌ Kamu tidak punya izin akses.")
        return

    if context.args:
        code = context.args[0]
        file_id = video_store.get(code)
        if file_id:
            await update.message.reply_video(file_id)
        else:
            await update.message.reply_text("Video tidak tersedia / link kadaluarsa.")
    else:
        await update.message.reply_text("Halo Owner! Kirim video ke bot untuk dapat link.")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Helper to see your numeric user ID and username."""
    u = update.effective_user
    await update.effective_message.reply_text(
        f"User ID: {u.id}\nUsername: @{u.username if u.username else '-'}\n"
        "Salin User ID ini ke OWNER_USER_ID di kode untuk penguncian lebih kuat."
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("whoami", whoami))
    logger.info("Bot starting (owner-locked)...")
    app.run_polling()

if __name__ == "__main__":
    main()
