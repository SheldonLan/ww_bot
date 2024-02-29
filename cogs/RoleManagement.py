import mysql.connector
import nextcord
from nextcord import SlashOption
from nextcord.ext import commands

import conts


class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Добавить роль в базу данных", dm_permission=True)
    async def добавить_роль(self, interaction: nextcord.Interaction, name: str, description: str,
                            role_type: str = SlashOption(
                                choices={'Выдаваемые': 'Выдаваемые', 'Кастомные': 'Кастомные', 'Гендерные': 'Гендерные',
                                         'Модераторские': 'Модераторские', 'Получаемые': 'Получаемые'})):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()

            # Добавляем роль в базу данных
            sql_add_role = f"INSERT INTO roles (type, name, description) VALUES ('{role_type}', '{name}', '{description}')"
            cursor.execute(sql_add_role)
            connection.commit()

            await interaction.response.send_message("Роль успешно добавлена в базу данных.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Произошла ошибка при добавлении роли.", ephemeral=True)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(description="Изменить поле роли в базе данных")
    async def изменить_роль(self, interaction: nextcord.Interaction, role_id: int, field: str, value: str):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()

            # Проверяем, существует ли указанная роль
            sql_check_role = f"SELECT * FROM roles WHERE id = {role_id}"
            cursor.execute(sql_check_role)
            role = cursor.fetchone()
            if not role:
                await interaction.response.send_message("Указанная роль не найдена.", ephemeral=True)
                return

            # Изменяем поле роли в базе данных
            sql_update_role = f"UPDATE roles SET {field} = '{value}' WHERE id = {role_id}"
            cursor.execute(sql_update_role)
            connection.commit()

            await interaction.response.send_message("Поле роли успешно изменено в базе данных.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Произошла ошибка при изменении поля роли.", ephemeral=True)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(description="Удалить роль из базы данных")
    async def удалить_роль(self, interaction: nextcord.Interaction, role_id: int):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()

            # Проверяем, существует ли указанная роль
            sql_check_role = f"SELECT * FROM roles WHERE id = {role_id}"
            cursor.execute(sql_check_role)
            role = cursor.fetchone()
            if not role:
                await interaction.response.send_message("Указанная роль не найдена.", ephemeral=True)
                return

            # Удаляем роль из базы данных
            sql_delete_role = f"DELETE FROM roles WHERE id = {role_id}"
            cursor.execute(sql_delete_role)
            connection.commit()

            await interaction.response.send_message("Роль успешно удалена из базы данных.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Произошла ошибка при удалении роли.", ephemeral=True)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(description="Показать список всех ролей")
    async def список_ролей(self, interaction: nextcord.Interaction):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()

            # Получаем список всех ролей из базы данных
            sql_get_roles = "SELECT * FROM roles"
            cursor.execute(sql_get_roles)
            roles_data = cursor.fetchall()

            if not roles_data:
                await interaction.response.send_message("В базе данных нет ни одной роли.", ephemeral=True)
                return

            # Группируем роли по типу
            roles_by_type = {}
            for role in roles_data:
                role_type, role_name, role_description = role[1:4]
                if role_type not in roles_by_type:
                    roles_by_type[role_type] = []
                roles_by_type[role_type].append((role_name, role_description))

            # Создаем вложенное сообщение со списком ролей
            embed = nextcord.Embed(title="Список ролей", color=0x00ff00)
            for role_type, roles in roles_by_type.items():
                role_list = "\n".join([f"**{role[0]}**: {role[1]}" for role in roles])
                embed.add_field(name=f"**{role_type}** роли", value=role_list, inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Произошла ошибка при получении списка ролей.", ephemeral=True)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="test")
    async def написать(self, interaction: nextcord.Interaction, text):
        await interaction.send(f"{text}")
def setup(bot):
    bot.add_cog(RoleManagement(bot))
