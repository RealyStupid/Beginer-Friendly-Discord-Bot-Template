# -------------------------------------------------------------------------------
# EXAMPLE COG — HOW TO CREATE SLASH COMMANDS
#
# This cog showcases:
#   - How to create slash commands using app_commands
#   - What parameters slash commands can take
#   - How optional and required parameters work
#   - How to use choices, types, and autocomplete
#   - Best practices when writing slash commands
#
# Slash commands are built differently from prefix commands. Instead of using
# decorators from commands.Command, slash commands use the app_commands system.
# Slash commands are registered with Discord and must be synced before they
# appear in the client.
# -------------------------------------------------------------------------------

import discord
from discord import app_commands
from discord.ext import commands

class SlashExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------------------------------------------------------------------
    # BASIC SLASH COMMAND EXAMPLE
    #
    # Slash commands use @app_commands.command instead of @commands.command.
    #
    # Usage:
    #   /hello
    # ---------------------------------------------------------------------------
    @app_commands.command(name="hello", description="Sends a greeting message.")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello! This is an example slash command.")

    # ---------------------------------------------------------------------------
    # SLASH COMMAND WITH REQUIRED PARAMETERS
    #
    # Required parameters must be provided by the user. Discord will not allow
    # the user to run the command without filling them in.
    #
    # Usage:
    #   /add number1:5 number2:10
    # ---------------------------------------------------------------------------
    @app_commands.command(name="add", description="Adds two numbers together.")
    async def add(self, interaction: discord.Interaction, number1: int, number2: int):
        result = number1 + number2
        await interaction.response.send_message(f"The result is: {result}")

    # ---------------------------------------------------------------------------
    # SLASH COMMAND WITH OPTIONAL PARAMETERS
    #
    # Optional parameters are created by giving them a default value (usually None).
    # Discord will show them as optional fields in the UI.
    #
    # Usage:
    #   /say message:Hello world
    #   /say
    #
    # message is optional because it defaults to None.
    # ---------------------------------------------------------------------------
    @app_commands.command(name="say", description="Repeats the message you provide.")
    async def say(self, interaction: discord.Interaction, message: str | None = None):
        if message is None:
            await interaction.response.send_message("You did not provide a message.")
        else:
            await interaction.response.send_message(message)

    # ---------------------------------------------------------------------------
    # SLASH COMMAND WITH CHOICES
    #
    # Choices allow you to restrict input to a predefined list.
    #
    # Usage:
    #   /color choice:red
    #
    # Discord will show a dropdown with the available choices.
    # ---------------------------------------------------------------------------
    @app_commands.command(name="color", description="Choose a color.")
    @app_commands.describe(choice="Pick a color from the list.")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Red", value="red"),
        app_commands.Choice(name="Blue", value="blue"),
        app_commands.Choice(name="Green", value="green")
    ])
    async def color(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        await interaction.response.send_message(f"You chose: {choice.name}")

    # ---------------------------------------------------------------------------
    # SLASH COMMAND WITH AUTOCOMPLETE
    #
    # Autocomplete allows you to dynamically suggest values as the user types.
    #
    # Usage:
    #   /fruit name:<autocomplete>
    #
    # The autocomplete function must return a list of app_commands.Choice objects.
    # ---------------------------------------------------------------------------
    FRUITS = ["Apple", "Banana", "Cherry", "Grape", "Orange"]

    async def fruit_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=fruit, value=fruit)
            for fruit in self.FRUITS
            if current.lower() in fruit.lower()
        ]

    @app_commands.command(name="fruit", description="Pick a fruit using autocomplete.")
    @app_commands.autocomplete(name=fruit_autocomplete)
    async def fruit(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"You selected: {name}")

    # ---------------------------------------------------------------------------
    # BEST PRACTICES FOR SLASH COMMANDS
    #
    # 1. Always include a description for every command and parameter.
    # 2. Use type hints (str, int, discord.Member) to help Discord validate input.
    # 3. Use optional parameters for flexibility.
    # 4. Use choices or autocomplete when appropriate.
    # 5. Keep command logic short; move complex logic into helper functions.
    # 6. Always respond to the interaction; slash commands must send a response.
    # ---------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# This function is required for Discord.py to load the cog.
# The bot calls this function automatically when loading the extension.
# -------------------------------------------------------------------------------
async def setup(bot):
    await bot.add_cog(SlashExample(bot))