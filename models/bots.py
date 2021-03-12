import logging
import re
import numpy as np

from aiogram import Bot, Dispatcher, executor, types


class CypherAssistantBot:

    def __init__(self, token: str):
        assert isinstance(token, str)
        self._bot = Bot(token=token)
        self._dp = Dispatcher(self._bot)
        self.memory = {}

        self.add_handlers(dispatcher=self._dp)

        executor.start_polling(self._dp, skip_updates=True)

    def add_handlers(self, dispatcher):
        @dispatcher.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

        @dispatcher.message_handler(commands=['roll'])
        async def send_welcome(message: types.Message):
            text = " ".join(message.text.split()[1:]).strip()
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
                await message.answer(f"@{message.from_user.username} tira un {'bel' if is_good else 'misero'} <b>{result}</b> 🎲 {'📈' if is_good else '📉'}\n\n"
                                     f"<code>  {text} =\n"
                                     f"= {parsed_text} = {result}</code>",
                                     parse_mode="html")
            except Exception as e:
                logging.error(e)
                await message.reply(f"Non riesco a capire 😅😅\n"
                                    f"Prova tipo <code>/roll d20</code> "
                                    f"o <code>/roll 2d20 + 3</code>",
                                    parse_mode="html")
