import os

import nextcord
from nextcord import *
from nextcord.ext import commands
import secret, conts
import random

bot = commands.Bot(command_prefix='!@', intents=nextcord.Intents.all(),
                   activity=Activity(type=ActivityType.watching, name="как за обиженными воду возят."))

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

@bot.command()
async def help_command(self, ctx):
        all_commands = []

        for cog_name, cog in self.bot.cogs.items():
            commands_list = cog.get_commands()
            if commands_list:
                commands_str = [f"{cmd.name}: {cmd.help}" for cmd in commands_list]
                all_commands.extend(commands_str)

        if all_commands:
            await ctx.send("Список доступных команд:")
            await ctx.send("\n".join(all_commands))
        else:
            await ctx.send("Нет доступных команд.")

bot.run(secret.TOKEN)
