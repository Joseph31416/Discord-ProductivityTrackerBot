import discord
from clock_options import Clocking
from response import Response
from user_interface import UserInterface
from time_options import TimeOptions
from apscheduler.schedulers.background import BackgroundScheduler
from env import TOKEN, TEXT_CHANNEL, TEST_TOKEN, TEST_TEXT_CHANNEL
from model import Users


debug = False
client = discord.Client()
users = Users()
users.load()
clock = Clocking("Asia/Singapore")
ui = UserInterface()
options = TimeOptions()
resp = Response()
sched = BackgroundScheduler()
sched.add_job(users.sync, 'interval', minutes=1)
sched.start()
if not debug:
    text_channel_id = int(TEXT_CHANNEL)
    token = TOKEN
else:
    text_channel_id = int(TEST_TEXT_CHANNEL)
    token = TEST_TOKEN


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_voice_state_update(member, before, after, ui=ui, users=users):
    msg, status = None, None
    user_id = str(member)
    server_id = str(member.guild.id)
    text_channel = client.get_channel(text_channel_id)
    if before.channel is None:
        msg = "$clockin"
        ui.update(msg=msg, status=status, server_id=server_id, user_id=user_id)
        ui, users = clock.clock_in(ui, users)
        if ui.status != 1:
            ui.status = -1
        embed = resp.generate_embed(ui)
        if embed is not None:
            await text_channel.send(embed=embed)
    elif after.channel is None:
        msg = "$clockout"
        ui.update(msg=msg, status=status, server_id=server_id, user_id=user_id)
        ui, users = clock.clock_out(ui, users)
        if ui.status != 1:
            ui.status = -1
        embed = resp.generate_embed(ui)
        if embed is not None:
            await text_channel.send(embed=embed)


@client.event
async def on_message(message, users=users, clock=clock, ui=ui, options=options, resp=resp):
    user_id = str(message.author)
    server_id = str(message.guild.id)
    msg = message.content
    status, title, name_duration = None, None, None
    ui.update(msg=msg, status=status, title=title, user_id=user_id,
              server_id=server_id, name_duration=name_duration)

    if message.author == client.user:
        return None

    if message.content.startswith("$clockin"):
        ui, users = clock.clock_in(ui, users)

    elif message.content.startswith("$clockout"):
        ui, users = clock.clock_out(ui, users)

    elif message.content.startswith("$time"):
        ui, users = options.update(ui, users, clock)

    elif message.content.startswith("$sync"):
        users.sync()

    embed = resp.generate_embed(ui)
    if embed is not None:
        await message.channel.send(embed=embed)


client.run(token)
