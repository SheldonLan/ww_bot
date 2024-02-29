import nextcord
from nextcord import *
from nextcord.ext.commands import Cog
from nextcord.ui import View, Button
from nextcord import  SelectMenu, SelectOption

import conts

class TicketSystem(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_ticket_channel(self, user):
        guild = self.bot.get_guild(conts.GUILD)
        ticket_category = nextcord.utils.get(guild.categories, name='tickets')
        staff_role = nextcord.utils.get(guild.roles, name='staff')

        if ticket_category and staff_role:
            overwrites = {
                role: nextcord.PermissionOverwrite(read_messages=False) for role in guild.roles
            }

            overwrites[user] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)
            overwrites[staff_role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                                  attach_files=True)

            ticket_channel_name = f"ticket_{user.display_name}"
            ticket_channel = await ticket_category.create_text_channel(name=ticket_channel_name, overwrites=overwrites)
            return ticket_channel
        else:
            print("Ticket category or staff role not found.")
            return None

    @Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(conts.CHANNEL_TICKET)
        await channel.purge()
        embed = Embed(
            title="Здесь Вы можете оставить жалобу на другого пользователя.",
            description="Чтобы создать обращение, нажмите на кнопку под сообщением.\nНапоминаю о пунктах 5.1-5.8 Правил ( <#1211519023456587777> )",
            colour=Colour.random()
        )
        view = View()
        button_create = Button(style=ButtonStyle.green, label=' Создать тикет', custom_id='create_ticket')

        async def function_on_click(interaction: nextcord.Interaction):
            ticket_channel = await self.create_ticket_channel(interaction.user)
            if ticket_channel:
                view = View()
                delete_button = Button(style=ButtonStyle.red, label="Удалить тикет", custom_id="delete_ticket")
                punish_button = Button(style=ButtonStyle.red, label="Наказать", custom_id="punish_ticket")

                async def delete_ticket_callback(interaction: nextcord.Interaction):
                    await interaction.channel.delete()

                delete_button.callback = delete_ticket_callback
                view.add_item(delete_button)
                view.add_item(punish_button)
                await ticket_channel.send(f"{interaction.user.mention}, Ваш тикет создан!", view=view)
            else:
                await interaction.response.send_message("Произошла ошибка при создании тикета.", ephemeral=True)

        async def punish_callback(interaction: nextcord.Interaction):
            punishments = [
                SelectOption(label="Тайм-аут", value="timeout"),
                SelectOption(label="Бан", value="ban"),
                SelectOption(label="Предупреждение", value="warning")
            ]
            select = SelectMenu(custom_id="punish_select", placeholder="Выберите наказание", options=punishments)
            await interaction.response.send_message("Выберите способ наказания:", view=select)

        async def on_button_click(self, interaction: Interaction):
            if interaction.custom_id == "delete_ticket":
                await interaction.channel.delete()
            elif interaction.custom_id == "punish_ticket":
                # Проверяем, есть ли у пользователя роль "staff"
                staff_role = nextcord.utils.get(interaction.guild.roles, name='staff')
                if staff_role in interaction.user.roles:
                    await punish_callback(interaction)
                else:
                    await interaction.response.send_message("У вас нет прав на наказание пользователей.", ephemeral=True)

        button_create.callback = function_on_click
        view.add_item(button_create)
        await channel.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(TicketSystem(bot))
