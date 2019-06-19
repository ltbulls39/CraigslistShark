from discord.ext import commands
import shark
import os
import sqlite3
from sqlite3 import Error
########################
# Only used to get token
import token as tok
########################

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def sharkmeup(context, item=None):
    if item is not None:
        s = shark.Shark(item)
        rows = s.select_all_from_db()
        await context.send(rows[0])
    else:
        # NO search query
        # Should have some default mode
        # Return the best sharkable item in our DB?
        pass
@client.command()
async def filter(context):
    pass

if __name__ == '__main__':
    client.run(tok.token)

#     TODO normal distribution for the prices, filter out outliers
#     TODO work on algorithm for finding the current listing price of an item
#     TODO find if item is sharkable
#         sharkable if listing certain amount under current listing price
