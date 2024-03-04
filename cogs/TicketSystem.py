import nextcord
from nextcord import *
from nextcord.ext.commands import Cog
from nextcord.ui import View, Button, Select
from nextcord import SelectMenu, SelectOption

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
            title="Здесь ты можешь оставить жалобу на другого пользователя.",
            description="Чтобы создать обращение, нажми на кнопку под сообщением.\nНапоминаю о пунктах 5.1-5.8 Правил ( <#1211519023456587777> )",
            colour=Colour.random()
        )
        view = View()
        view.timeout = None
        button_create = Button(style=ButtonStyle.green, label='Создать тикет', custom_id='create_ticket')

        async def function_on_click(interaction: nextcord.Interaction):
            ticket_channel = await self.create_ticket_channel(interaction.user)
            if ticket_channel:
                view = View()
                view.timeout = None
                delete_button = Button(style=ButtonStyle.red, label="Удалить тикет", custom_id="delete_ticket")
                punish_button = Button(style=ButtonStyle.red, label="Наказать", custom_id="punish_ticket")

                async def delete_ticket_callback(interaction: nextcord.Interaction):
                    await interaction.channel.delete()

                async def punish_callback(interaction: nextcord.Interaction):
                    if interaction.user.get_role(conts.ROLE_STAFF):
                        punish_menu = Select()
                        options = [SelectOption(label="Забанить", description="Заблокировать на сервере", value=1),
                                   SelectOption(label="Отправить в тайм-аут", description="Отправить в мут, в том числе голосовой", value=2),
                                   SelectOption(label="Предупредить", description="Отправить сообщение в личку пользователю", value=3)]
                        punish_menu.options = options
                        punish_view = View()
                        punish_view.timeout = None
                        punish_view.add_item(punish_menu)
                        await interaction.send("Ничего не работает. Пользуйтесь `/ban` `/timeout` `/личка`", ephemeral=True, view=punish_view)
                    else:
                        await interaction.send(
                            f"Ай-яй-яй, ты не {interaction.guild.get_role(conts.ROLE_STAFF).mention}", ephemeral=True)

                delete_button.callback = delete_ticket_callback
                punish_button.callback = punish_callback
                view.add_item(delete_button)
                view.add_item(punish_button)
                await ticket_channel.send(f"{interaction.user.mention}, твой тикет создан!\n"
                                          f"Заполните обращение по форме:```css\n"
                                          f"1. Суть обращения\n"
                                          f"2. Доказательства нарушения\n"
                                          f"3. Дата нарушения (если требуется).```", view=view)
            else:
                await interaction.response.send_message("Произошла ошибка при создании тикета.", ephemeral=True)

        button_create.callback = function_on_click
        view.timeout = None

        view.add_item(button_create)
        await channel.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(TicketSystem(bot))
