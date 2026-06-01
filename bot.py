from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import time

import asyncio

# ===== CONFIG =====
TOKEN = "8607184926:AAGCIRGNR7dAIXuTijTO_sE9mtgm1NUsXnA"


GROUP_ID = -1003464956381
ADMIN_IDS = [783262896]

MAX_REQUEST = 3
RESET_TIME = 86400

user_last = {}
user_limit = {}

# ===== UI =====
def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🟢 Token Grab", callback_data="grab"),
            InlineKeyboardButton("🟡 Token Gojek", callback_data="gojek")
        ],
        [
            InlineKeyboardButton("🔴 Risk Token", callback_data="risk"),
            InlineKeyboardButton("💬 Grup WhatsApp", callback_data="wa")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)



# ===== TEMPLATE TEXT =====
def home_text():
    return (
        "╔══════════════════════╗\n"
        "   🤖 PRATAMA TOKEN BOT\n"
        "╚══════════════════════╝\n\n"
        "Silakan pilih layanan:\n\n"
        "🟢 Token Grab\n"
        "🟡 Token Gojek\n"
        "🔴 Risk Token\n"
        "💬 WhatsApp \n\n"
        
        "Powered by Pratama"
    )

# ===== TOKEN =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != GROUP_ID:
        return

    await update.message.reply_text(
        home_text(),
        reply_markup=main_menu()
    )

# ===== BUTTON =====
# ===== BUTTON =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if not query:
        return

    # ===== BATAS GRUP =====
    if query.message.chat.id != GROUP_ID:

        await query.answer(
            "❌ Bot hanya bisa dipakai di grup ini",
            show_alert=True
        )
        return

    await query.answer()

    user_id = query.from_user.id

    # ===== COOLDOWN =====
    now = time.time()

    if user_id in user_last:

        if now - user_last[user_id] < COOLDOWN:

            await query.message.reply_text(
                "⏳ Jangan spam tombol"
            )
            return

    user_last[user_id] = now

    # ===== LIMIT HARIAN =====
    if user_id not in ADMIN_IDS:

        now_time = time.time()

        # buat user baru
        if user_id not in user_limit:

            user_limit[user_id] = {
                "count": 0,
                "reset": now_time + RESET_TIME
            }

        # reset otomatis 24 jam
        if now_time > user_limit[user_id]["reset"]:

            user_limit[user_id] = {
                "count": 0,
                "reset": now_time + RESET_TIME
            }

        # cek limit
        if user_limit[user_id]["count"] >= MAX_REQUEST:

            sisa_jam = int(
                (user_limit[user_id]["reset"] - now_time) / 3600
            )

            await query.message.reply_text(
                f"❌ Limit harian habis\n\n"
                f"Coba lagi dalam {sisa_jam} jam"
            )
            return

        # tambah request
        user_limit[user_id]["count"] += 1

    # ===== TOKEN GRAB =====
    if query.data == "grab":

        try:

            with open("grab.txt", "r", encoding="utf-8") as file:
                isi = file.read().strip()

            msg = await query.message.reply_text(
                f"🟢 TOKEN GRAB\n\n<code>{isi}</code>",
                parse_mode="HTML"
            )

            await asyncio.sleep(5)

            await msg.delete()

        except Exception as e:

            await query.message.reply_text(
                f"❌ Error:\n{e}"
            )

    # ===== TOKEN GOJEK =====
    elif query.data == "gojek":

        try:

            with open("gojek.txt", "r", encoding="utf-8") as file:
                isi = file.read().strip()

            msg = await query.message.reply_text(
                f"🟡 TOKEN GOJEK\n\n<code>{isi}</code>",
                parse_mode="HTML"
            )

            await asyncio.sleep(5)

            await msg.delete()

        except Exception as e:

            await query.message.reply_text(
                f"❌ Error:\n{e}"
            )

    # ===== RISK TOKEN =====
    elif query.data == "risk":

        try:

            with open("risk.txt", "r", encoding="utf-8") as file:
                isi = file.read().strip()

            msg = await query.message.reply_text(
                f"🔴 RISK TOKEN\n\n<code>{isi}</code>",
                parse_mode="HTML"
            )

            await asyncio.sleep(5)

            await msg.delete()

        except Exception as e:

            await query.message.reply_text(
                f"❌ Error:\n{e}"
            )

    # ===== WHATSAPP =====
    elif query.data == "wa":

        await query.message.reply_text(
            "💬 WHATSAPP GRUP\n\n"
            "https://chat.whatsapp.com/BshlM8lO50vK95ySvJUebD",
            disable_web_page_preview=True
        )
    
# ===== MAIN =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(button))

print("🚀 Bot UI Premium aktif...")
app.run_polling()