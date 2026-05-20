from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import time
import requests

# ===== CONFIG =====
TOKEN = "8607184926:AAGCIRGNR7dAIXuTijTO_sE9mtgm1NUsXnA"
GROUP_ID = -1003464956381
COOLDOWN = 3
START_TIME = time.time()

user_last = {}

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
        ],
        [
            InlineKeyboardButton("💳 QRIS PAYMENT", callback_data="qris"),
            InlineKeyboardButton("🔗 Short Link", callback_data="short")
            ],
        
       
        [  InlineKeyboardButton("🟢 Status Bot", callback_data="status")
]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Kembali", callback_data="back")]
    ])

# ===== TEMPLATE TEXT =====
def home_text():
    return (
        "╔══════════════════════╗\n"
        "   🤖 *PRATAMA TOKEN BOT*\n"
        "╚══════════════════════╝\n\n"
        "Silakan pilih layanan:\n\n"
        "🟢 Token Grab\n"
        "🟡 Token Gojek\n"
        "🔴 Risk Token\n"
        "💬 WhatsApp \n"
        "💳 QRIS Registrasi\n"
        "🖇 Short Link Otomatis\n"
        "🟢 Cek Online BOT\n\n"
        
        "_Powered by Pratama_"
    )

# ===== TOKEN =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != GROUP_ID:
        return

    await update.message.reply_text(
        home_text(),
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# ===== BUTTON =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    # cooldown
    now = time.time()
    if user_id in user_last and now - user_last[user_id] < COOLDOWN:
        await query.answer("⏳ Jangan spam!", show_alert=True)
        return
    user_last[user_id] = now

    await query.answer()

    # ===== NAVIGASI =====
    if query.data == "back":
        await query.edit_message_text(
            home_text(),
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    elif query.data == "grab":
            await query.edit_message_text(
            "🟢 *Token Grab*\n\n"
         "https://tinyurl.com/bp9htk3y",
            parse_mode="Markdown",
            reply_markup=back_button()
        )
            

    elif query.data == "gojek":
              await query.edit_message_text(
                          "🟡 *Token Gojek*\n\n"
 "https://tinyurl.com/26a4tsne",
 parse_mode="Markdown",
            reply_markup=back_button()
        )
            

    elif query.data == "risk":
        await query.edit_message_text(
        "🔴 *Risk Token*\n\n"
         "https://tinyurl.com/bp9htk3y", 
        parse_mode="Markdown",
            reply_markup=back_button()
        )
            
            

    elif query.data == "wa":
        await query.edit_message_text(
            "💬 *WHATSAPP GRUP*\n\n"
            "https://chat.whatsapp.com/BshlM8lO50vK95ySvJUebD", 
          parse_mode="Markdown",
            reply_markup=back_button(),
            disable_web_page_preview=True
        )
        
    elif query.data == "qris":
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=open("qris.jpg", "rb"),
            caption="💳 *QRIS REGISTRASI*\n\nSilakan scan QRIS untuk melakukan pembayaran registrasi.",
            parse_mode="Markdown"
           
        )
    elif query.data == "status":

        uptime = int(time.time() - START_TIME)

        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60

        text = (
            "🟢 *BOT ONLINE*\n\n"
            f"⏳ Uptime: {hours} Jam {minutes} Menit {seconds} Detik\n"
            "🚀 Status: Stabil"
        )
        
    elif query.data == "short":

        await query.edit_message_text(
            "🔗 *SHORT LINK*\n\n"
            "Gunakan command:\n"
            "/short https://example.com"
            
            
        )

        await query.message.reply_text(
            text,
            parse_mode="Markdown"
        )      
        
        # ===== SHORTLINK =====
async def shortlink(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != GROUP_ID:
        return

    user_id = update.effective_user.id

    # cooldown
    now = time.time()
    if user_id in user_last and now - user_last[user_id] < COOLDOWN:

        sisa = int(COOLDOWN - (now - user_last[user_id]))

        await update.message.reply_text(
            f"⏳ Tunggu {sisa} detik lagi"
        )
        return

    user_last[user_id] = now

    # cek input
    if not context.args:

        await update.message.reply_text(
            "Contoh:\n/short https://google.com"
        )
        return

    url = context.args[0]

    try:

        api = f"https://tinyurl.com/api-create.php?url={url}"

        short_url = requests.get(api).text

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔗 Buka Link",
                    url=short_url
                )
            ]
        ])

        text = (
            "╔════════════════╗\n"
            "     🔗 SHORT LINK\n"
            "╚════════════════╝\n\n"
            f"📎 Original:\n{url}\n\n"
            f"✅ Short Link:\n{short_url}"
        )

        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )
            
# ===== MAIN =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("short", shortlink))
app.add_handler(CallbackQueryHandler(button))

print("🚀 Bot UI Premium aktif...")
app.run_polling()