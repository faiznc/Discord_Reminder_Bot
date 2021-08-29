import os
from keep_alive import keep_alive
from discord.ext import commands, tasks
from my_timer import start_timer
import my_scheduler as schd

help_command = commands.DefaultHelpCommand(no_category='Commands')

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    help_command=help_command)

# bot.author_id = 487258918465306634  # Change to your discord id!!!

token = os.environ.get("TOKEN")


@tasks.loop(seconds=60)  #Check every minute.
async def background_checker():
    print("Checking now (" + schd.get_now(with_second=True) + ").")
    commands, channels = schd.get_sent_now()
    if len(commands) > 0:
        for i in range(len(commands)):
            channel_conn = bot.get_channel(int(channels[i]))
            await channel_conn.send(commands[i])


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier.


@bot.command(brief='Ping the bot!')
async def ping(ctx):
    await ctx.send("Bot is active!")


@bot.command(
    brief='Add new schedule --> Format : !add 12:00 (Hello @.everyone !!...)')
async def add(ctx, timestamp, *, text_commands):
    response = schd.add_daily(ctx.channel.id, timestamp, text_commands)
    # print(response)
    if response == -1:
        await ctx.send("Wrong time format.")
    elif response == -2:
        await ctx.send("Time must be number.")
    elif response == -3:
        await ctx.send("Incorrect hour or minute.")
    else:
        await ctx.send("Added on {} -> {}".format(timestamp, text_commands))


@bot.command(brief='Show all schedule.')
async def show(ctx):
    try:
        job_list = schd.get_raw_schedule(ctx.channel.id)
    except:
        job_list = []  # because channel not added yet, returning an error.
    if len(job_list) < 1:
        await ctx.send("No one scheduled.. yet.")
    count = 1
    for x in job_list:
        sent_string = "(" + str(count) + ") " + schd.utc_to_gmt7(
            x["timestamp"]) + " - " + schd.remove_tag(x['command'])
        await ctx.send(sent_string)
        count += 1


@bot.command(brief='Delete a schedule by index.')
async def delete(ctx, index):
    try:
        index = int(index)
    except:
        await ctx.send("Index must be round number!")
    response = schd.del_daily(ctx.channel.id, index)
    if response > 0:
        await ctx.send("Deletion success.")
    else:
        await ctx.send("Schedule not found.")


@bot.command(brief='About this bot :)')
async def about(ctx):
    about_message = """- A simple bot to send scheduled messages.\n
  Created by **Faiz Noerdiyan Cesara**
  Running on repl.it (Try it free!)
  If you find any problem (or other purposes), feel free to contact me at **faiznc@gmail.com**, Thank you :)

  (Currently only available for GMT+7 Timezone)
  ~Beta Ver. 0.3~
  """
    await ctx.send(about_message)


@bot.command(brief='Get current local bot time.')
async def now(ctx):
    current_time = schd.get_now()
    current_time = schd.utc_to_gmt7(current_time)
    now_msg = "Bot local time = {}".format(current_time)
    await ctx.send(now_msg)


def runBot():
    global token
    keep_alive()  # Starts a webserver to be pinged.
    start_timer()
    background_checker.start()
    bot.run(token)


runBot()

## --------------- Future Note --------------
# ## DB Architecture
# Currently, each channel has its own dedicated id with their schedule

# >> (What i mean are...)
# 1. Channel_id A.
#   1.A (Time), (Text)
#   2.B (TimeB), (TextB)
# 2. Channel_id B.
#   2.A (TimeA), (Text) ...

# Future DB Architecture maybe implement saving each minute to scale horizontally.

# >> (I think better implementations.)
# 1. Minute 00:00
#   1.A (Channel_ID A), (Text)
#   1.B (Channel_ID B), (Text)
#   ...
# 2. Minute 00:01
#   2.A (Channel_ID A), (Text)
#   2.B (Channel_ID B), (Text)
