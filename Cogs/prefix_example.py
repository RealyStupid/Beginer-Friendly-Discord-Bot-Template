# -------------------------------------------------------------------------------
# PREFIX EXAMPLE COG
#
# This cog showcases:
#   - How to create prefix commands
#   - What parameters commands can take
#   - How optional and required parameters work
#   - How to send messages back to the user
#   - Best practices when writing commands
#
# Cogs help keep your bot organized. Instead of placing every command inside
# your main bot file, you place them inside separate files (cogs) for cleaner
# code and easier debugging.
# -------------------------------------------------------------------------------

import discord
from discord.ext import commands

class Example(commands.Cog):
    # ---------------------------------------------------------------------------
    # Every cog needs a reference to the bot. This allows the cog to access
    # bot-level features such as syncing, sending messages, loading extensions,
    # and more.
    # ---------------------------------------------------------------------------
    def __init__(self, bot):
        self.bot = bot

    # ---------------------------------------------------------------------------
    # BASIC COMMAND EXAMPLE
    #
    # This is the simplest form of a prefix command. It takes only the ctx
    # parameter, which contains information about the command invocation.
    #
    # Usage:
    #   !hello
    # ---------------------------------------------------------------------------
    @commands.command(name="hello", description="Sends a greeting message.")
    async def hello(self, ctx):
        await ctx.send("Hello! This is an example command.")

    # ---------------------------------------------------------------------------
    # COMMAND WITH REQUIRED PARAMETERS
    #
    # Required parameters must be provided by the user. If the user does not
    # provide them, Discord.py will show an error.
    #
    # Usage:
    #   !add 5 10
    #
    # In this example:
    #   number1 and number2 are required parameters.
    # ---------------------------------------------------------------------------
    @commands.command(name="add", description="Adds two numbers together.")
    async def add(self, ctx, number1: int, number2: int):
        result = number1 + number2
        await ctx.send(f"The result is: {result}")

    # ---------------------------------------------------------------------------
    # COMMAND WITH OPTIONAL PARAMETERS
    #
    # Optional parameters are created by giving them a default value (usually None).
    # If the user does not provide the parameter, the default value is used.
    #
    # Usage:
    #   !say Hello world
    #   !say
    #
    # message is optional because it defaults to None.
    # ---------------------------------------------------------------------------
    @commands.command(name="say", description="Repeats the message you provide.")
    async def say(self, ctx, *, message: str = None):
        if message is None:
            await ctx.send("You did not provide a message.")
        else:
            await ctx.send(message)

    # ---------------------------------------------------------------------------
    # COMMAND WITH MULTIPLE TYPES OF PARAMETERS
    #
    # This example shows:
    #   - A required parameter (user)
    #   - An optional parameter (reason)
    #   - A keyword-only parameter using *
    #
    # Usage:
    #   !userinfo @User
    #   !userinfo @User reason=Testing
    #
    # The * forces all parameters after it to be keyword-only.
    # ---------------------------------------------------------------------------
    @commands.command(name="userinfo", description="Shows information about a user.")
    async def userinfo(self, ctx, user: discord.Member, *, reason: str = None):
        info = f"User: {user}\nID: {user.id}"
        if reason:
            info += f"\nReason: {reason}"
        await ctx.send(info)

    # ---------------------------------------------------------------------------
    # BEST PRACTICES FOR COMMANDS
    #
    # 1. Always name your parameters clearly.
    # 2. Use type hints (str, int, discord.Member) to help Discord.py convert input.
    # 3. Use optional parameters for flexibility.
    # 4. Validate user input when needed.
    # 5. Keep command logic short; move complex logic into helper functions.
    # 6. Always send feedback to the user so they know the command worked.
    # ---------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# This function is required for Discord.py to load the cog.
# The bot calls this function automatically when loading the extension.
# -------------------------------------------------------------------------------
async def setup(bot):
    await bot.add_cog(Example(bot))