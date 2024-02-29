import mysql.connector
import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta

import conts


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Начать экономику")
    async def начать_экономику(self, interaction: nextcord.Interaction):
        user_id = None
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()

            # Проверяем, существует ли пользователь уже в таблице users
            sql_check_user = f"SELECT id FROM users WHERE discord_id = '{interaction.user.id}'"
            cursor.execute(sql_check_user)
            result = cursor.fetchone()
            if result:
                # Если пользователь уже существует, отправляем ему сообщение с его уникальным id
                user_id = result[0]
                await interaction.response.send_message(
                    content=f"Вы уже начали экономику. Ваш уникальный номер: {user_id}",
                    ephemeral=True
                )
            else:
                # Если пользователь не существует, добавляем его в таблицу users
                sql_add_user = f"INSERT INTO users (discord_id) VALUES ('{interaction.user.id}')"
                cursor.execute(sql_add_user)
                connection.commit()
                user_id = cursor.lastrowid

                # При создании пользователя добавляем запись в таблицу transactions с текущим временем
                now = datetime.now()
                sql_insert_transaction = f"INSERT INTO transactions (user_id, amount, last_claimed) VALUES ('{interaction.user.id}', 0, '{now}')"
                cursor.execute(sql_insert_transaction)
                connection.commit()

                await interaction.response.send_message(
                    content=f"**Успешно записала Вас в системе**.\nВаш уникальный номер = {user_id}",
                    ephemeral=True
                )
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Проверить баланс")
    async def проверить_баланс(self, interaction: nextcord.Interaction):
        balance = None
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()
            sql_get_balance = f"SELECT balance FROM users WHERE discord_id = '{interaction.user.id}'"
            cursor.execute(sql_get_balance)
            result = cursor.fetchone()
            if result:
                balance = result[0]
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        if balance is not None:
            await interaction.response.send_message(
                content=f"Ваш баланс: {balance}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                content="Вы еще не начали экономику. Используйте /начать_экономику",
                ephemeral=True
            )

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Получить ежечасное вознаграждение")
    async def ежечасное_вознаграждение(self, interaction: nextcord.Interaction):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()
            now = datetime.now()
            user_id = interaction.user.id

            # Проверяем, существует ли пользователь в таблице transactions
            sql_check_user = f"SELECT user_id FROM transactions WHERE user_id = '{user_id}'"
            cursor.execute(sql_check_user)
            result = cursor.fetchone()
            if not result:
                # Если пользователь отсутствует в таблице transactions, отправляем ему сообщение с просьбой начать экономику
                await interaction.response.send_message(
                    content="Вы еще не начали экономику. Используйте /начать_экономику",
                    ephemeral=True
                )
                return

            # Проверяем, прошел ли час с момента последней транзакции
            last_claimed_sql = f"SELECT last_claimed FROM transactions WHERE user_id = '{user_id}'"
            cursor.execute(last_claimed_sql)
            result = cursor.fetchone()
            if result:
                last_claimed = result[0]
                cooldown_time = timedelta(seconds=20) - (now - last_claimed)
                if cooldown_time > timedelta(0):
                    formatted_cooldown_time = f"<t:{int((now + cooldown_time).timestamp())}:R>"
                    await interaction.response.send_message(
                        content=f"Вы уже получали ежечасное вознаграждение в этот час.\nОсталось ожидать: {formatted_cooldown_time}",
                        ephemeral=True
                    )
                    return

                sql_update_last_claimed = f"UPDATE transactions SET last_claimed = '{now}' WHERE user_id = '{user_id}'"
                cursor.execute(sql_update_last_claimed)
                sql_update_balance = f"UPDATE users SET balance = balance + 10 WHERE discord_id = '{user_id}'"
                cursor.execute(sql_update_balance)
                connection.commit()
                await interaction.response.send_message(
                    content="Вы получили ежечасное вознаграждение в размере 10 монет",
                    ephemeral=True
                )
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Получить список товаров")
    async def список_товаров(self, interaction: nextcord.Interaction):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()
            sql_get_products = "SELECT id, name, price FROM products"
            cursor.execute(sql_get_products)
            products = cursor.fetchall()

            if products:
                embed = nextcord.Embed(title="Список товаров", color=0x00ff00)
                for product in products:
                    embed.add_field(name=f"{product[0]}. {product[1]}", value=f"Стоимость: {product[2]} монет",
                                    inline=False)
            else:
                embed = nextcord.Embed(title="Магазин", description="[ЭКОНОМИКА] В магазине пока нет товаров.",
                                       color=0xff0000)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Купить товар")
    async def купить_товар(self, interaction: nextcord.Interaction, product_id: int):
        user_id = interaction.user.id
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()

            # Проверяем, существует ли пользователь
            sql_check_user = f"SELECT id, balance FROM users WHERE discord_id = '{user_id}'"
            cursor.execute(sql_check_user)
            user = cursor.fetchone()
            if not user:
                await interaction.response.send_message(
                    content="Вы еще не начали экономику. Используйте /начать_экономику",
                    ephemeral=True
                )
                return

            # Проверяем, существует ли товар
            sql_check_product = f"SELECT name, price FROM products WHERE id = {product_id}"
            cursor.execute(sql_check_product)
            product = cursor.fetchone()
            if not product:
                await interaction.response.send_message(
                    content="Указанный товар не найден.",
                    ephemeral=True
                )
                return

            # Проверяем, достаточно ли у пользователя монет для покупки
            product_name, product_price = product
            if user[1] < product_price:
                await interaction.response.send_message(
                    content="У вас недостаточно монет для покупки этого товара.",
                    ephemeral=True
                )
                return

            # Вычитаем стоимость товара из баланса пользователя и добавляем товар в его инвентарь
            new_balance = user[1] - product_price
            sql_update_balance = f"UPDATE users SET balance = {new_balance} WHERE id = {user[0]}"
            cursor.execute(sql_update_balance)

            sql_add_to_inventory = f"INSERT INTO inventory (user_id, product_id) VALUES ({user[0]}, {product_id})"
            cursor.execute(sql_add_to_inventory)

            # Проверяем, есть ли у товара роль для выдачи
            sql_check_role = f"SELECT role_id FROM product_roles WHERE product_id = {product_id}"
            cursor.execute(sql_check_role)
            role_id = cursor.fetchone()
            if role_id:
                role_id = role_id[0]
                guild = self.bot.get_guild(conts.GUILD)
                member = guild.get_member(user_id)
                role = guild.get_role(role_id)
                if member and role:
                    await member.add_roles(role)

            connection.commit()

            await interaction.response.send_message(
                content=f"Вы успешно приобрели товар {product_name} за {product_price} монет.",
                ephemeral=True
            )
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Топ пользователей по балансу")
    async def топ(self, interaction: nextcord.Interaction):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()
            sql_get_top_users = "SELECT discord_id, balance FROM users ORDER BY balance DESC LIMIT 10"
            cursor.execute(sql_get_top_users)
            top_users = cursor.fetchall()

            embed = nextcord.Embed(title="Топ пользователей по балансу", color=0x00ff00)
            for index, (discord_id, balance) in enumerate(top_users, start=1):
                member = await self.bot.fetch_user(discord_id)
                embed.add_field(name=f"{index}. {member.display_name}", value=f"Баланс: {balance} монет", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Добавить товар")
    async def добавить_товар(self, interaction: nextcord.Interaction, name: str, price: int):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()
            sql_add_product = f"INSERT INTO products (name, price) VALUES ('{name}', {price})"
            cursor.execute(sql_add_product)
            connection.commit()

            await interaction.response.send_message(content="Товар успешно добавлен.", ephemeral=True)
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Удалить товар")
    async def удалить_товар(self, interaction: nextcord.Interaction, product_id: int):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()
            sql_delete_product = f"DELETE FROM products WHERE id = {product_id}"
            cursor.execute(sql_delete_product)
            connection.commit()

            await interaction.response.send_message(content="Товар успешно удален.", ephemeral=True)
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Изменить цену товара")
    async def изменить_цену(self, interaction: nextcord.Interaction, product_id: int, price: int):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()
            sql_update_price = f"UPDATE products SET price = {price} WHERE id = {product_id}"
            cursor.execute(sql_update_price)
            connection.commit()

            await interaction.response.send_message(content="Цена товара успешно изменена.", ephemeral=True)
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Добавить роль к товару")
    async def привязать_роль_к_товару(self, interaction: nextcord.Interaction, product_id: int, role_id: int):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()
            sql_add_role = f"INSERT INTO product_roles (product_id, role_id) VALUES ({product_id}, {role_id})"
            cursor.execute(sql_add_role)
            connection.commit()

            await interaction.response.send_message(content="Роль успешно добавлена к товару.", ephemeral=True)
        except Exception as e:
            print(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="[ЭКОНОМИКА] Добавить баланс пользователю")
    async def добавить_баланс(self, interaction: nextcord.Interaction, user: nextcord.Member, amount: int):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                port='3306',
                password='12dsa4a',
                database="ww_bot"
            )
            cursor = connection.cursor()

            # Проверяем, существует ли пользователь
            sql_check_user = f"SELECT id, balance FROM users WHERE discord_id = '{user.id}'"
            cursor.execute(sql_check_user)
            result = cursor.fetchone()
            if not result:
                await interaction.response.send_message(
                    content="Указанный пользователь не найден.",
                    ephemeral=True
                )
                return

            # Обновляем баланс пользователя
            user_id, current_balance = result
            new_balance = current_balance + amount
            sql_update_balance = f"UPDATE users SET balance = {new_balance} WHERE id = {user_id}"
            cursor.execute(sql_update_balance)
            connection.commit()

            await interaction.response.send_message(
                content=f"Баланс пользователя {user.display_name} успешно увеличен на {amount} монет.",
                ephemeral=True
            )
        except Exception as e:
            print(e)
            await interaction.response.send_message(
                content="Произошла ошибка при добавлении баланса.",
                ephemeral=True
            )
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))
