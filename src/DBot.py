from discord.ext import commands
import asyncio
import shark as mako
########################
# Only used to get token
import d_token as tok
########################

client = commands.Bot(command_prefix='!')
unique_queries = set()
s = mako.Shark()





@client.event
async def on_ready():
    print("Bot is ready")



'''
Idea Time!
    - When I call shark(), add that query to a queue or list
    - This list will hold all queries that have been asked for
    - Every set number of seconds, will query again 
'''


@client.command()
async def shark(context, item=None):
    '''
    Will create a Shark object and send a single
    item back to Discord
    :param context:
    :param item: argument passed in to be queried
    :return:
    '''
    if item is not None:
        global s
        s = mako.Shark(item)
        unique_queries.add(item)
        rows = s.select_all_from_db()
        await context.send(rows[0])
        s.close_db()
    else:
        # NO search query
        # Should have some default mode
        # Return the best sharkable item in our DB?
        pass



async def update_db():
    '''
    - Background task in event loop
    - Will refresh the DB with new posts
    :param unique_queries: set containing each query provided by the user
    :param s: shark object
    :return:
    '''
    while True:
        for item in unique_queries:
            # Now we want to update the DB with a new round of queries per item
            global s
            s = mako.Shark(item)
            print("Trying to insert", item, 'again.')
            s.close_db()
        await asyncio.sleep(5)



if __name__ == '__main__':
    client.loop.create_task(update_db())
    client.run(tok.token)

#     TODO normal distribution for the prices, filter out outliers
#     TODO work on algorithm for finding the current listing price of an item
#     TODO find if item is sharkable
#         sharkable if listing certain amount under current listing price
