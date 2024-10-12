import os
import disnake
from disnake.ext import commands
import logging

log_file_path = r'Your_Path_for_"discord.log"_file'

intents = disnake.Intents.all()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=log_file_path, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=["Your_Test_channel_for_bot"])

@bot.event
async def on_ready():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print(f"Не удалось загрузить ког {file}: {e}")
    with open('Your_Path_for_avatar_bot', 'rb') as avatar:
        await bot.user.edit(avatar=avatar.read())
    print("Bot is ready!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

bot.run("YOUR_TOKEN")
