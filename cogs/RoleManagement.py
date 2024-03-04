import mysql.connector
import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, application_checks
from nextcord.ext.commands import Cog

import conts
from main import bot


class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="Управление ролями", dm_permission=True)
    @application_checks.has_any_role('staff', 1211514715679752202)
    async def роли(self, interaction: nextcord.Interaction):
        pass

    @роли.subcommand(description="Добавить роль в базу данных")
    @application_checks.has_any_role('staff', 1211514715679752202)
    async def добавить(self, interaction: nextcord.Interaction, name: str, description: str,
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

    @роли.subcommand(description="Изменить поле роли в базе данных")
    @application_checks.has_any_role('staff', 1211514715679752202)
    async def изменить(self, interaction: nextcord.Interaction, role_id: int,  value: str, field: str = nextcord.SlashOption(
                                choices={'type': 'type', 'name': 'name', 'description': 'description'})):
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

    @роли.subcommand(description="Удалить роль из базы данных")
    @application_checks.has_any_role('staff', 1211514715679752202)
    async def удалить(self, interaction: nextcord.Interaction, role_id: int):
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
    @роли.subcommand(description="Обновить роли")
    async def обновить(self, interaction: nextcord.Interaction):
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
                await bot.get_channel(conts.ROLES_CHANNEL).send("В базе данных нет ни одной роли.")
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
            await interaction.send(ephemeral=True, content="Успех")
            await bot.get_channel(conts.ROLES_CHANNEL).purge()
            await bot.get_channel(conts.ROLES_CHANNEL).send(embed=embed)
        except Exception as e:
            print(e)
            await bot.get_channel(conts.ROLES_CHANNEL).send("Произошла ошибка при получении списка ролей.")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @Cog.listener()
    async def on_ready(self):
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
                await bot.get_channel(conts.ROLES_CHANNEL).send("В базе данных нет ни одной роли.")
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
            await bot.get_channel(conts.ROLES_CHANNEL).purge(limit=1)
            await bot.get_channel(conts.ROLES_CHANNEL).send(embed=embed)
        except Exception as e:
            print(e)
            await bot.get_channel(conts.ROLES_CHANNEL).send("Произошла ошибка при получении списка ролей.")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def setup(bot):
    bot.add_cog(RoleManagement(bot))
