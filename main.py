from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading
import uuid
import os

# ======= KONFIGURASI =======
BOT_TOKEN = "8069013680:AAE2rzjBcosvBfqUPI4o3D5V5DF2ZdAg2Pg"
UUID_FILE = "uuid.txt"

# ======= FLASK APP =======
app = Flask(__name__)

def load_uuids():
    if not os.path.exists(UUID_FILE):
        return []
    with open(UUID_FILE, "r") as f:
        return [line.strip() for line in f]

@app.route("/")
def index():
    return "API dan Bot aktif."

@app.route("/check", methods=["POST"])
def check_uuid():
    data = request.get_json()
    input_uuid = data.get("uuid")
    if input_uuid in load_uuids():
        return jsonify({"status": "valid"})
    return jsonify({"status": "invalid"})

# ======= BOT TELEGRAM =======
async def generate_uuid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_uuid = str(uuid.uuid4())
    with open(UUID_FILE, "a") as f:
        f.write(new_uuid + "\n")
    await update.message.reply_text(f"UUID baru: `{new_uuid}`", parse_mode="Markdown")

async def add_uuid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Format: /adduuid <uuid>")
        return
    input_uuid = context.args[0]
    with open(UUID_FILE, "a") as f:
        f.write(input_uuid + "\n")
    await update.message.reply_text(f"UUID '{input_uuid}' ditambahkan.")

def start_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("generate", generate_uuid))
    app_bot.add_handler(CommandHandler("adduuid", add_uuid))
    app_bot.run_polling()

# ======= JALANKAN SEMUA =======
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))