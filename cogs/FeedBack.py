import traceback

import nextcord
from nextcord.ext import commands
import conts
from main import bot


class FeedBack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class Feedback(nextcord.ui.Modal):
        def __init__(self):
            super().__init__(
                "Оставь свой фидбек!",
                timeout=5 * 60,  # 5 minutes
            )

            self.name = nextcord.ui.TextInput(
                label="Заголовок",
                min_length=2,
                max_length=50,
            )
            self.add_item(self.name)

            self.description = nextcord.ui.TextInput(
                label="Текст",
                style=nextcord.TextInputStyle.paragraph,
                placeholder="Напиши сюда суть предложения/улучшения/проблемы. Если требуется прикрепи ссылки на примеры/источники",
                required=True,
                max_length=1800,
            )
            self.add_item(self.description)

        async def callback(self, interaction: nextcord.Interaction) -> None:
            channel = bot.get_channel(1216994301356277781)
            embed=nextcord.Embed(title=f"{self.name.value}",
                                 description=f"{self.description.value}",
                                 colour=nextcord.Colour.random())
            embed.set_author(name=f"Автор: {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=f"uid: {interaction.user.id}")
            await channel.send(embed=embed)

        @bot.slash_command(description="Оставь свой фидбек о сервере", guild_ids=[conts.GUILD])
        async def фидбек(interaction: nextcord.Interaction):
                modal = FeedBack.Feedback()
                await interaction.response.send_modal(modal)
def setup(bot):
    bot.add_cog(FeedBack(bot))
