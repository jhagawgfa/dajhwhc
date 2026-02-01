from telegram import Update, Message
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re

# ⚠️ СРОЧНО: СМЕНИ ТОКЕН ЧЕРЕЗ @BotFather И ВСТАВЬ НОВЫЙ ЗДЕСЬ!
BOT_TOKEN = "7790900340:AAEmJJKLo4kKw1bnL15HS6da5CGLRf-Gmzc"
YOUR_TELEGRAM_ID = 1652373422  # Твой ID безопасен


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Привет! Это бот для связи с Fase_Mig!\n\n"
        "Напиши свой вопрос или предложение — я постараюсь ответить <3"
    )


async def forward_to_creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = str(user.id)

    # Сохраняем связь пользователь ↔ сообщение в памяти бота
    context.user_data['last_user_id'] = chat_id

    # Формируем сообщение для тебя
    header = (
        f"📩 Новое сообщение:\n"
        f"👤 {user.full_name} | @{user.username if user.username else '—'}\n"
        f"🆔 <code>{chat_id}</code>\n"
        f"────────────"
    )

    # Пересылаем текст или медиа
    if update.message.text:
        await context.bot.send_message(
            chat_id=YOUR_TELEGRAM_ID,
            text=f"{header}\n\n{update.message.text}",
            parse_mode="HTML"
        )
    elif update.message.photo:
        await context.bot.send_photo(
            chat_id=YOUR_TELEGRAM_ID,
            photo=update.message.photo[-1].file_id,
            caption=f"{header}\n\n{update.message.caption or ''}",
            parse_mode="HTML"
        )
    elif update.message.video:
        await context.bot.send_video(
            chat_id=YOUR_TELEGRAM_ID,
            video=update.message.video.file_id,
            caption=f"{header}\n\n{update.message.caption or ''}",
            parse_mode="HTML"
        )
    elif update.message.document:
        await context.bot.send_document(
            chat_id=YOUR_TELEGRAM_ID,
            document=update.message.document.file_id,
            caption=f"{header}\n\n{update.message.caption or ''}",
            parse_mode="HTML"
        )
    elif update.message.voice:
        await context.bot.send_voice(
            chat_id=YOUR_TELEGRAM_ID,
            voice=update.message.voice.file_id,
            caption=f"{header}",
            parse_mode="HTML"
        )

    await update.message.reply_text("✅ Сообщение отправлено! Ожидай ответа 🙌")


async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Пропускаем если это не ты
    if update.effective_user.id != YOUR_TELEGRAM_ID:
        return

    reply_msg = update.message.reply_to_message
    if not reply_msg:
        return

    # Извлекаем ID пользователя из текста (ищем цифры после 🆔)
    match = re.search(r'🆔\s*<code>(\d+)</code>', reply_msg.text or "")
    if not match:
        # Альтернативный поиск без HTML
        match = re.search(r'🆔\s*(\d+)', reply_msg.text or "")

    if not match:
        await update.message.reply_text("❌ Не удалось найти ID пользователя для ответа")
        return

    user_id = match.group(1)

    try:
        # Отправляем ответ в зависимости от типа сообщения
        if update.message.text:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📨 Ответ от Fase_Mig:\n{update.message.text}"
            )
        elif update.message.photo:
            await context.bot.send_photo(
                chat_id=user_id,
                photo=update.message.photo[-1].file_id,
                caption=f"📨 Ответ от Fase_Mig:\n{update.message.caption or ''}"
            )
        elif update.message.video:
            await context.bot.send_video(
                chat_id=user_id,
                video=update.message.video.file_id,
                caption=f"📨 Ответ от Fase_Mig:\n{update.message.caption or ''}"
            )

        await update.message.reply_text(f"✅ Ответ отправлен пользователю {user_id}!")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка отправки: {str(e)}\n\nВозможно, пользователь заблокировал бота.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & ~filters.COMMAND & ~filters.REPLY,
        forward_to_creator
    ))
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & filters.REPLY,
        reply_handler
    ))

    print("✅ Бот запущен! Нажми Ctrl+C чтобы остановить.")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()