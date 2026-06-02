🤖 AI Study Assistant

A Telegram bot that helps you learn Python, ML, and AI using artificial intelligence. Ask any question — get a clear explanation, code example, and a quiz question to test yourself.

Features

- `/explain <topic>` — explains any topic in simple words with a code example
- `/quiz <topic>` — generates a 3-question test on any topic
- `/roadmap` — builds a personal ML/AI learning plan for you
- Send any message — the bot answers like a friendly mentor

Tech Stack

- Python 3.11
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [OpenRouter API](https://openrouter.ai) (free AI models)
- python-dotenv

Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/TyomPapiyan/ai-study-assistant.git
cd ai-study-assistant
```

**2. Create virtual environment**
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install python-telegram-bot openai python-dotenv
```

**4. Create `.env` file**
```
TELEGRAM_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
```

- Get Telegram token from [@BotFather](https://t.me/BotFather)
- Get free API key from [openrouter.ai](https://openrouter.ai)

**5. Run the bot**
```bash
python study_bot.py
```

Example

```
You:  /explain what is a for loop
Bot:  A for loop lets you repeat code a certain number of times...
      Example:
      for i in range(5):
          print(i)
      Question: What will this code print?
```

License

MIT
