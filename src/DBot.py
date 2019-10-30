from discord.ext import commands
import asyncio
import shark as mako
import random
########################
# Only used to get token
import d_token as tok
########################

client = commands.Bot(command_prefix='!')
unique_queries = set()
s = mako.Shark()


# TODO
''' 
1. Message with a list of items searched for
2. alert if price dropped
3. Maybe figure out of items are sold
4. Filter out shitty posts
4. !sharkmute mutes for them
'''



@client.event
async def on_ready():
    print("Bot is ready")



'''
Idea Time!
    - When I call shark(), add that query to a queue or list
    - This list will hold all queries that have been asked for
    - Every set number of seconds, will query again 
'''



# TODO make simple prices testing function per query
@client.command()
async def prices(context, *args):
    if args:
        global s
        s = mako.Shark()
        query = ' '.join(args)
        rows = s.price_with_query(query)
        print(rows)
        s.close_db()



@client.command()
async def shark(context, *args):
    '''
    Will create a Shark object and send a single
    item back to Discord
    :param context:
    :param item: argument passed in to be queried
    :return:
    '''
    if args:
        item = ' '.join(args)
        global s
        s = mako.Shark(item)
        unique_queries.add(item)
        rows = s.select_by_hash_from_db(item)


        '''Format of a row:
                - id            -> [0]
                - name          -> [1]
                - url           -> [2]
                - date          -> [3]
                - price         -> [4]
                - query_hashed  -> [5]
        '''
        for row in rows:
            print(row)
        try:
            i = 0
            while i < 50:
                index = random.randint(0, len(rows))
                p = rows[index][4]
                if p >= 100:
                    break


            # index = random.randint(0, len(rows))
            id = rows[index][0]
            url = rows[index][2]
            price = rows[index][4]
            name = rows[index][1] if len(rows[index][1]) < 30 else rows[index][1][:30] + '...'

            await context.send('Here is ' + name + '   for **$' + str(price) + '**')
            await context.send('__**ID no:**__   ' + str(id))
            await context.send(url)
        except IndexError as e:
            print(e)
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
        await asyncio.sleep(10)



if __name__ == '__main__':
    client.loop.create_task(update_db())
    client.run(tok.token)

#     TODO normal distribution for the prices, filter out outliers
#     TODO work on algorithm for finding the current listing price of an item
#     TODO find if item is sharkable
#         sharkable if listing certain amount under current listing price
