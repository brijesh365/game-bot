from discord.ext import commands

import google_search
import settings
from database import db

INTERNAL_SERVER_ERROR = 'Internal server error.'
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
    else:
        await bot.process_commands(message)


@bot.command(pass_context=True)
async def google(ctx, *, keyword):
    db.save_keyword(ctx.message.author.name, keyword)
    await ctx.send(f'{google_search.search(keyword)}')


@bot.command(pass_context=True)
async def recent(ctx, *, keyword):
    output = db.fetch_history(ctx.message.author.name, keyword)
    await ctx.send(output if output else EMPTY_HISTORY)


@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(SEARCH_PARAMETER_REQUIRED)
    else:
        await ctx.send(INTERNAL_SERVER_ERROR)
        print(str(error))


bot.run(settings.DISCORD_TOKEN)
