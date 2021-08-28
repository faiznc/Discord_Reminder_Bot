import os
import time
from keep_alive import keep_alive
from discord.ext import commands, tasks
import threading
import my_scheduler as schd

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)

# bot.author_id = 487258918465306634  # Change to your discord id!!!
my_channel_id = int(os.environ.get("MY_CHANNEL_ID"))

token = os.environ.get("TOKEN")

#my test channel id are = 880235498218618893


@tasks.loop(seconds=60)  #Check every minute.
async def background_checker():
    print("Checking now (" + schd.get_now() + ").")
    commands = schd.get_sent_now()
    if len(commands) > 0:
        channel = bot.get_channel(my_channel_id)
        for the_text in commands:
            await channel.send(the_text)


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier.


@bot.command(brief='Ping the bot!')
async def ping(ctx):
    await ctx.send("pong!")


@bot.command(brief='Add new schedule (Format : !new 12:00 theMessage)')
async def add(ctx, timestamp, text_commands):
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


@bot.command(brief='Show all schedule.')
async def show(ctx):
    job_list = schd.get_raw_schedule()
    if len(job_list) < 1:
        await ctx.send("No one scheduled.. yet.")
    count = 1
    for x in job_list:
        sent_string = "(" + str(count) + ") " + schd.utc_to_gmt7(
            x["timestamp"]) + " - " + schd.remove_tag(x['command'])
        await ctx.send(sent_string)
        count += 1


@bot.command(brief='Delete a schedule.')
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

@bot.command(brief='Test Get Channel ID')
async def get_id(ctx,*, full_text):
  print(full_text)
  print(ctx.channel.id)


def runBot():
    global token
    keep_alive()  # Starts a webserver to be pinged.
    # background_tasks.start()
    background_checker.start()
    bot.run(token)


runBot()
