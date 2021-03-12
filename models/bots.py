import logging
import re
from os import listdir
from os.path import join

import aiogram
import numpy as np

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class CypherAssistantBot:

    def __init__(self, token: str):
        assert isinstance(token, str)
        self._bot = Bot(token=token)
        self._dp = Dispatcher(self._bot)
        self.users_states = {}

        self.add_handlers(dispatcher=self._dp)

        executor.start_polling(self._dp, skip_updates=True)

    def add_handlers(self, dispatcher):

        @dispatcher.message_handler(commands=['roll'])
        async def roll(message: types.Message):
            text = " ".join(message.text.split()[1:]).strip()
            if not text:
                await message.answer(text=f"@{message.from_user.username}, scegli cosa tirare 🎲",
                                     reply_markup=ReplyKeyboardMarkup([
                                         [KeyboardButton(text=f"/roll d20")]
                                     ], one_time_keyboard=True))
                return
            parsed_text = text
            raw_rolls = re.findall(pattern="[0-9]*d[0-9]+", string=text, flags=re.IGNORECASE)
            averages, scores = [], []
            for roll in raw_rolls:
                multiplier, dice = roll.split("d")
                if not multiplier:
                    multiplier = 1
                averages += [int(dice) // 2]
                dice = np.random.randint(1, int(dice))
                scores += [dice]
                parsed_text = re.sub(pattern=roll, repl=f"{multiplier}*{dice}", string=parsed_text, count=1)
            try:
                result = eval(parsed_text, {})
                is_good = True if sum(scores) >= sum(averages) else False
                await message.answer(
                    f"@{message.from_user.username} tira un {'bel' if is_good else 'misero'} <b>{result}</b> 🎲 {'📈' if is_good else '📉'}\n\n"
                    f"<code>  {text} =\n"
                    f"= {parsed_text} = {result}</code>",
                    parse_mode="html")
            except Exception as e:
                logging.error(e)
                await message.reply(f"Non riesco a capire 😅😅\n"
                                    f"Prova tipo <code>/roll d20</code> "
                                    f"o <code>/roll 2d20 + 3</code>",
                                    parse_mode="html")

        @dispatcher.message_handler(commands=['infos'])
        async def infos(message: types.Message):
            await message.answer(text=f"Cosa vuoi consultare?",
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text="Trama 📚", url="https://github.com/rom42pla/cypher_telegram_bot/blob/main/notes/campaign.md")],
                                     [InlineKeyboardButton(text="Personaggi 👪", url="https://github.com/rom42pla/cypher_telegram_bot/blob/main/notes/characters.md")],
                                     [InlineKeyboardButton(text="Tiri 🎲", url="https://github.com/rom42pla/cypher_telegram_bot/blob/main/notes/checks.md")],
                                     [InlineKeyboardButton(text="Combattimento 👊", url="https://github.com/rom42pla/cypher_telegram_bot/blob/main/notes/combat.md")]
                                 ], one_time_keyboard=True))

