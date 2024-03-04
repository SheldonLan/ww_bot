import os
from nextcord.ext import commands
import nextcord
from nextcord import *

import conts
from main import bot


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[conts.GUILD], description="Помощь")
    async def помощь(self, interaction: Interaction):
        # Initialize an empty dictionary to store commands and subcommands grouped by their parent commands
        commands_dict = {}

        # Function to explore command and its children
        def explore_command(command, parent_name=""):
            # If the command has children, recursively explore them
            if command.children:
                for child in command.children.values():
                    explore_command(child, parent_name + " " + command.name)
            # If the command does not have children, add it to the dictionary
            else:
                if parent_name not in commands_dict:
                    commands_dict[parent_name] = []
                commands_dict[parent_name].append(command)

        # Iterate over all application commands
        for slash_command in bot.get_all_application_commands():
            explore_command(slash_command)

        # Create an embed message
        help_embed = Embed(title="Список команд и подкоманд")

        # Add commands and subcommands to the embed
        for parent_name, commands_list in commands_dict.items():
            category_field_value = ""
            for command in commands_list:
                category_field_value += f"`/{parent_name} {command.name}`: {command.description}\n"
            help_embed.add_field(name=parent_name, value=category_field_value, inline=False)

        message = await interaction.response.send_message(embed=help_embed)


def setup(bot):
    bot.add_cog(Help(bot))
