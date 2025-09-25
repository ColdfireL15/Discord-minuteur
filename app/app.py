import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from minuteur import handle_timer_command

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TIMER_CHANNEL_ID = int(os.getenv('TIMER_CHANNEL_ID'))

if not TOKEN:
    print("Token Discord manquant !")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté et prêt !')

@bot.event
async def on_message(message):
    if message.channel.id == TIMER_CHANNEL_ID:
        await handle_timer_command(message, bot)

bot.run(TOKEN)
