import os

import nextcord
from nextcord import *
from nextcord.ext import commands, tasks
import secret, conts
import random

bot = commands.Bot(command_prefix='!@', intents=nextcord.Intents.all(),
                   activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="как папа любит маму"))

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"loaded {extension}")


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"unloaded {extension}")


@bot.event
async def on_member_join(member: Member):
    embed = Embed(title="Добро пожаловать!",
                  description=f"**Рады приветствовать тебя, {member.mention}!\n"
                              f"Надеюсь, тебе понравится здесь.**")
    embed.set_footer(text="WWB")
    embed.set_image(random.choice(conts.WELCOME_GIF_URLS))
    embed.color = nextcord.Color.random()
    embed.set_author(name=f"RU-community сервер по Wuthering Waves", icon_url=bot.get_guild(conts.GUILD).icon.url)

    await bot.get_channel(conts.WELCOME_CHANNEL).send(embed=embed)


bot.run(secret.TOKEN)
