import os
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ---------- KONFIGURASI ----------
BIN_FILE = 'payload.bin'
SECRET_KEY = "GRAB_LOGOUT_SECURE_K3Y"
URL = 'https://p.grabtaxi.com/api/passenger/v2/profiles/logout'

# ---------- FUNGSI DEKRIPSI ----------
def decrypt_payload():
    if not os.path.exists(BIN_FILE):
        return None, f"[!] ERROR: File '{BIN_FILE}' tidak ditemukan! Jalankan 'buat_bin.py' dulu."
    
    with open(BIN_FILE, 'rb') as f:
        encrypted_content = f.read()
    
    decrypted = bytearray()
    for i in range(len(encrypted_content)):
        decrypted.append(encrypted_content[i] ^ ord(SECRET_KEY[i % len(SECRET_KEY)]))
    
    try:
        payload = json.loads(decrypted.decode('utf-8'))
    except Exception as e:
        return None, f"[!] Gagal dekripsi payload: {e}"
    
    return payload, None

# ---------- HANDLER START ----------
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo! Kirim token Grab-mu ke saya, dan saya akan membantu logout akun kamu."
    )

# ---------- HANDLER TOKEN ----------
async def handle_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()
    if not token:
        await update.message.reply_text("[!] Token tidak boleh kosong.")
        return

    payload, error = decrypt_payload()
    if error:
        await update.message.reply_text(error)
        return

    headers = {
        'User-Agent': 'Grab/5.406.1 (Android 12; Build 139598668)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-mts-ssid': token,
        'authorization': token,
        'x-request-id': 'ce1c7eb3-4110-465e-9662-8721eef2d385'
    }

    await update.message.reply_text("⏳ Sedang memproses logout...")

    try:
        response = requests.post(URL, headers=headers, data=payload, timeout=15)
        if response.status_code == 200:
            await update.message.reply_text("✅ Logout berhasil! Spot Bike & Food hilang.")
            await update.message.reply_text(f"Respon Server:\n{response.text}")
        else:
            await update.message.reply_text(
                f"[FAILED] Gagal. Status Code: {response.status_code}\nPesan: {response.text}"
            )
    except Exception as e:
        await update.message.reply_text(f"[!] Terjadi kesalahan koneksi: {e}")

# ---------- MAIN ----------
if __name__ == "__main__":
    TELEGRAM_TOKEN = "8871195550:AAE7HyXy2JxCQLfuhnAgx7gRGdagxhi_3J4"  # Ganti dengan token bot Telegrammu

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("logout", logout))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token))

    print("🤖 Bot sudah berjalan di Termux...")
    app.run_polling()