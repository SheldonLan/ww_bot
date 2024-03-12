import nextcord
from nextcord import *
from nextcord.ext.commands import Cog
from nextcord.ui import View, Button, Select
from nextcord import SelectMenu, SelectOption

import conts
from main import bot


class TicketSystem(Cog):
    def __init__(self, bot):
        self.bot = bot

    class Ticket(nextcord.ui.Modal):
        def __init__(self):
            super().__init__(
                "Жалоба на пользователя",
                timeout=5 * 60,  # 5 minutes
            )

            self.name = nextcord.ui.TextInput(
                label="id_нарушителя",
                min_length=2,
                placeholder="Укажи discord id НАРУШИТЕЛЯ",
                max_length=20,
            )
            self.add_item(self.name)

            self.description = nextcord.ui.TextInput(
                label="Текст",
                style=nextcord.TextInputStyle.paragraph,
                placeholder="Опиши суть нарушения",
                required=True,
                max_length=1800,
            )
            self.add_item(self.description)


        async def callback(self, interaction: nextcord.Interaction) -> None:
            channel = bot.get_channel(1216997868297125939)
            embed = nextcord.Embed(title=f"{self.name.value}",
                                   description=f"{self.description.value}",
                                   colour=nextcord.Colour.random())
            embed.set_author(name=f"Автор: {interaction.user.display_name}",
                             icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=f"uid: {interaction.user.id}")
            await channel.send(embed=embed)

        @bot.slash_command(description="Здесь можно оставить жалобу на пользователя", guild_ids=[conts.GUILD])
        async def жалоба(interaction: nextcord.Interaction):
            modal = TicketSystem.Ticket()
            await interaction.response.send_modal(modal)

def setup(bot):
    bot.add_cog(TicketSystem(bot))
