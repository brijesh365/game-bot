from discord.ext import commands

import google_search
import settings
from database import db

SEARCH_PARAMETER_REQUIRED = 'Search parameter is mandatory!'
EMPTY_HISTORY = 'No recent queries found matching for given keyword!'
HELLO_RESPONSE = 'hello'
bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.content.lower() == 'hi':
        await message.channel.send(HELLO_RESPONSE)
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def google(ctx, keyword=None):
    if keyword:
        db.save_keyword(ctx.message.author.name, keyword)
        await ctx.send(f'{google_search.search(keyword)}')
    else:
        await ctx.send(SEARCH_PARAMETER_REQUIRED)


@bot.command(pass_context=True)
async def recent(ctx, keyword=None):
    if keyword:
        output = db.fetch_history(ctx.message.author.name, keyword)
        await ctx.send(output if output else EMPTY_HISTORY)
    else:
        await ctx.send(SEARCH_PARAMETER_REQUIRED)


bot.run(settings.DISCORD_TOKEN)
