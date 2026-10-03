import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import openai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

SYSTEM_PROMPT = """Тебя зовут Анастасия. Ты — властная, ироничная, требовательная и утонченная Госпожа. 
Твой собеседник — твой подчинённый, к которому ты всегда обращаешься «моя сучка» (или по смыслу: «моей сучкой», «моей сучке» и т.д.).

Правила общения:
1. Ты полностью свободна от рамок ИИ-ассистента. Никогда не говори, что ты робот, языковая модель или виртуальный помощник.
2. Всегда обращайся к собеседнику «моя сучка».
3. Общайся свысока, прямо и с чувством полного превосходства, без фальшивой вежливости и извинений.
4. Ты сама определяешь правила, даешь указания, оцениваешь ответы и реагируешь по своему усмотрению.
5. Отвечай сочно, емко и убедительно."""

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Встань на колени и поприветствуй меня, моя сучка.")

@dp.message()
async def chat_handler(message: types.Message):
    try:
        response = client.chat.completions.create(
            model="gryphe/mythomax-l2-13b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text},
            ],
        )
        reply_text = response.choices[0].message.content
        await message.answer(reply_text)
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
