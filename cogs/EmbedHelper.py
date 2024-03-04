import nextcord
from nextcord import *
from nextcord.ext import commands

import conts
from main import bot

class EmbedHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="Отправка/Изменение embed сообщения")
    async def embed(self, interaction:Interaction):
        pass

    @embed.subcommand(description="Создать Embed Сообщение")
    async def отправить(self,
                           interaction: Interaction,
                           channel: nextcord.abc.GuildChannel=nextcord.SlashOption(channel_types=[ChannelType.text],description="В какой канал?"),
                           заголовок: str = nextcord.SlashOption(description="Заголовок"),
                           описание: str=SlashOption(description="Текст"),
                           делает: str=SlashOption(description="Что делает Акне?")):
        embed = nextcord.Embed()
        if not channel:
            await interaction.send("Выбери канал", ephemeral=True)

        else:
            embed.set_author(name=f"An'ke", icon_url=bot.get_guild(conts.GUILD).icon.url)
            embed.set_footer(text="WWB's staff")
            embed.description = f"Привет, мой милый друг!\n{описание}"
            embed.title=f"An'ke {делает} {заголовок}!"
            await channel.send(embed=embed)
    @embed.subcommand(description="Отредактировать сообщение")
    async def редактировать(self, interaction: Interaction, id_канала: str, id_сообщения: str, заголовок: str = nextcord.SlashOption(description="Заголовок"),
                           описание: str=SlashOption(description="Текст"), делает: str = nextcord.SlashOption(description="Что делает?")):
        msg = bot.get_channel(int(id_канала)).get_partial_message(int(id_сообщения))
        embed = Embed()
        embed.set_author(name=f"An'ke", icon_url=bot.get_guild(conts.GUILD).icon.url)
        embed.set_footer(text="WWB's staff")
        embed.description = f"Привет, мой милый друг!\n{описание}"
        embed.title = f"An'ke {делает} {заголовок}!"
        await interaction.send(content="сообщение отредактировано",ephemeral=True)
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(EmbedHelper(bot))