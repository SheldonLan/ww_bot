import nextcord
from nextcord import Embed
from nextcord.ext import commands, application_checks
import os

import conts
from main import bot


class Utilites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Утилиты", guild_ids=[conts.GUILD])
    async def утилиты(self, interaction: nextcord.Interaction):
        pass
    @утилиты.subcommand(description="Очистка Х сообщений")
    @application_checks.has_any_role('staff', 1211514715679752202)
    async def очистить(self, interaction:nextcord.Interaction, limit: int):
        await interaction.send(content=f"Очищено {limit} сообщений",ephemeral=True)
        await bot.get_channel(interaction.channel.id).purge(limit=limit+1)

    @утилиты.subcommand(description="Отправить личное сообщение от лица бота")
    @application_checks.has_any_role('staff', 1211514715679752202)
    async def личка(self, interaction: nextcord.Interaction, member: nextcord.Member, msg: str):
        await interaction.send(f"**Сообщение отправлено!**\nТекст: {msg}\nПолучатель: {member.name} (discord_id: {member.id})", ephemeral=True)
        await member.send(f"{msg}")

    @утилиты.subcommand(description="Статистика по участникам")
    @application_checks.has_any_role('staff', 1211514715679752202)
    async def участники(self, ctx):
        guild = ctx.guild
        online = len([m for m in guild.members if m.status == nextcord.Status.online])
        offline = len([m for m in guild.members if m.status == nextcord.Status.offline])
        dnd = len([m for m in guild.members if m.status == nextcord.Status.do_not_disturb])
        invisible = len([m for m in guild.members if m.status == nextcord.Status.invisible])

        total_members = len(guild.members)

        embed = Embed(
            title="Статистика участников",
            description=f"Всего участников: {total_members}\n"
                        f"Онлайн: {online}\n"
                        f"Не в сети: {offline}\n"
                        f"Не беспокоить: {dnd}\n"
                        f"Невидимые: {invisible}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Utilites(bot))
