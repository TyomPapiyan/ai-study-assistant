import os
from openai import OpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

SYSTEM_PROMPT = """Ты — персональный AI-учитель по программированию и ML/AI.

Когда пользователь спрашивает тему:
1. Объясни простыми словами (2-3 абзаца максимум)
2. Дай короткий пример кода на Python если уместно
3. В конце задай ОДИН вопрос для самопроверки

Отвечай на том языке, на котором пишет пользователь.
Будь дружелюбным, как старший товарищ, а не скучный учебник."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой AI-учитель по программированию и ML 🤖\n\n"
        "Просто напиши тему которую хочешь понять — например:\n"
        "• что такое список в python\n"
        "• объясни как работает gradient descent\n"
        "• что такое API\n\n"
        "Или используй команды:\n"
        "/explain <тема> — объяснение темы\n"
        "/quiz <тема> — тест по теме\n"
        "/roadmap — план изучения ML/AI"
    )


async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши тему после команды. Например:\n/explain что такое функция")
        return
    topic = " ".join(context.args)
    await _ask_ai(update, f"Объясни мне тему: {topic}")


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши тему после команды. Например:\n/quiz списки в python")
        return
    topic = " ".join(context.args)
    await _ask_ai(update, f"Создай для меня небольшой тест (3 вопроса) по теме: {topic}. После каждого вопроса напиши правильный ответ под спойлером в формате: Ответ: ...")


async def roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _ask_ai(update, "Составь мне пошаговый roadmap для изучения ML/AI с нуля. Я знаю основы Python. Раздели по месяцам, будь конкретным.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await _ask_ai(update, user_text)


async def _ask_ai(update: Update, user_message: str):
    thinking_msg = await update.message.reply_text("Думаю... 🤔")

    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.choices[0].message.content
        await thinking_msg.delete()
        await update.message.reply_text(answer)

    except Exception as e:
        await thinking_msg.delete()
        await update.message.reply_text(f"Что-то пошло не так: {e}")


def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN не найден в .env файле")

    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        raise ValueError("OPENROUTER_API_KEY не найден в .env файле")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("explain", explain))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("roadmap", roadmap))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен! Нажми Ctrl+C чтобы остановить.")
    app.run_polling()


if __name__ == "__main__":
    main()
