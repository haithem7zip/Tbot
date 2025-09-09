import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import sqlite3
import datetime

# إعدادات البوت
import os
TOKEN = os.getenv("8303228347:AAF6SkL2uT-X8Sc3ffeR4DosVF2hM-oj_OI")
DB_NAME = "study_bot.db"

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# إنشاء جدول في قاعدة البيانات
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            day TEXT,
            subject TEXT,
            time TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            task TEXT,
            due_date TEXT,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['📅 الجدول الدراسي', '📝 المهام'],
                ['📚 المواد', '⏰ reminders']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        'مرحباً! أنا بوتك المساعد للتنظيم الدراسي. كيف يمكنني مساعدتك؟',
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '📅 الجدول الدراسي':
        await send_schedule(update, context)
    elif text == '📝 المهام':
        await show_tasks(update, context)
    # يمكنك إضافة المزيد من الخيارات هنا

async def send_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT day, subject, time FROM schedule WHERE user_id = ? ORDER BY day, time", (user_id,))
    schedule = cursor.fetchall()
    conn.close()
    
    if schedule:
        response = "جدولك الدراسي:\n\n"
        for day, subject, time in schedule:
            response += f"{day}: {subject} - {time}\n"
    else:
        response = "لا يوجد جدول دراسي مضاف yet. Use /addschedule to add classes."
    
    await update.message.reply_text(response)

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # دالة لإضافة مهمة جديدة
    pass

def main():
    init_db()
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()
