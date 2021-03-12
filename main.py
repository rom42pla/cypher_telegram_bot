from os.path import join

import utils
from models.bots import CypherAssistantBot

env_filepath = join(".", "conf.env")

if __name__ == "__main__":
    env_vars = utils.read_env(filepath=env_filepath)
    bot = CypherAssistantBot(token=env_vars["TELEGRAM_BOT_TOKEN"])
    del env_vars
