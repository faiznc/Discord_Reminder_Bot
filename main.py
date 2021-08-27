import os
import time
# from keep_alive import keep_alive
from discord.ext import commands, tasks
import threading
import my_scheduler as schd

# def compare_time_in_db(start)

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)

# bot.author_id = 487258918465306634  # Change to your discord id!!!
my_channel_id = 880235498218618893
token = os.environ.get("TOKEN")

#task once


@tasks.loop(seconds=1, count=1)
async def slow_count():  # Simple func that run once
    print("1x test")


# @slow_count.after_loop
# async def after_slow_count():
#     print('done!')


@tasks.loop(seconds=5
            )  #basically a while true that always called every 5 seconds
async def background_tasks():
    print("Hello")


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier.


@bot.command()
async def ping(ctx):
    await ctx.send(
        "pong!"
    )  #simple command so that when you type "!ping" the bot will respond with "pong!"


@bot.command()
async def pings(ctx):
    await ctx.send(
        "pongs!"
    )  #simple command so that when you type "!ping" the bot will respond with "pong!"


@bot.command()
async def new(ctx, timestamp, text_commands):
    response = schd.add_daily(timestamp, text_commands)
    print(response)
    if response == -1:
        await ctx.send("Wrong time format.")
    elif response == -2:
        await ctx.send("Time must be number.")
    elif response == -3:
        await ctx.send("Incorrect hour or minute.")
    else:
        await ctx.send("Added on {} -> {}".format(timestamp, text_commands))


@bot.command()
async def show(ctx):
    job_list = schd.get_raw_schedule()
    if len(job_list) < 1:
        await ctx.send("No one scheduled.. yet.")
    count = 1
    for x in job_list:
        sent_string = "(" + str(count) + ") " + schd.utc_to_gmt7(
            x["timestamp"]) + "-" + x['command']
        await ctx.send(sent_string)
        count += 1


@bot.command()
async def delete(ctx, index):
    try:
        index = int(index)
    except:
        await ctx.send("Index must be round number!")
    response = schd.del_daily(index)
    if response > 0:
        await ctx.send("Deletion success.")
    else:
        await ctx.send("Index unavailable.")


def simple_call():  #proof of concept - working
    while True:
        time.sleep(6)
        slow_count.start()


thread1 = threading.Thread(target=simple_call, daemon=True)
thread1.start()


def runBot():
    global token
    # keep_alive()  # Starts a webserver to be pinged.
    background_tasks.start()
    bot.run(token)


runBot()
