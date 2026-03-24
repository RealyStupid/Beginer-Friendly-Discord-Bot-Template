# -------------------------------------------------------------------------------
# MAIN BOT FILE — READ THIS FIRST
#
# Think of your Discord bot as an empty room. Nothing happens inside it until
# you create a “door” that lets commands, events, and features enter.
#
# This file is that door.
#
# It creates the bot object, sets up the required intents, loads your cogs,
# and prepares everything your bot needs before it can run.
#
# In simple terms:
# - This file defines the Bot class
# - It configures the bot’s settings such as intents, prefix, and others
#   (some must also be enabled in the Dev Portal)
# - It handles startup tasks like loading cogs and syncing commands
#
# Without this file, your bot has no way to receive messages, run commands,
# or respond to events.
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# These are some dependencies this file uses:
# This imports Discord’s API wrapper.
import discord

# This is a built‑in extension to Discord’s API wrapper. It allows you to use
# prefix commands (commands that use "!") with your bot.
from discord.ext import commands

import os
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# This is where you define intents.
# Intents tell Discord what kind of information your bot should receive. Without
# intents, your bot would have no idea what is happening in your server, such as
# messages being sent, deleted, edited, or what channels were created, deleted,
# or edited. Some events require specific intents because they need access to
# data that only that intent provides.
#
# Some intents are privileged, meaning they must be enabled on the Discord bot
# itself via the Discord Developer Portal.
#
# What are default intents? Default intents are non‑sensitive, non‑privileged
# data that Discord allows all bots to access without special permission.
#
# The types of data included are: guilds, emoji updates, voice join/leave/mute
# events, message events (but not the message content itself), reaction
# add/remove events, and typing events.
INTENTS = discord.Intents.default()
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# This is where we can set other variables that can be used by your bot.
APPLICATION_ID = 1234567890232356  # Replace this with your actual application ID
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# This is where you define the bot’s class.
#
# Why define your own class instead of using the built‑in discord.Client?
#   Because discord.Client does not support commands, cogs, or message parsing.
#   In short, discord.Client is not practical if you want commands in your bot.
#
# This class name can be anything. For this template, we call it Client, but feel
# free to name it whatever you want.
#
# The class inherits from commands.Bot, which is the main bot framework class
# that gives your bot commands, cogs, prefixes, and all high‑level features.
# Basically, it allows us to use everything you will see in this bot.
class Client(commands.Bot):
    def __init__(self):
        # -----------------------------------------------------------------------
        # This is where we set information about the bot, such as the prefix,
        # the intents, and more. Think of this as the bot’s “settings.”
        #
        # Here we set the command_prefix, the intents the bot will use, and the
        # application ID.
        #
        # We set the application ID here as a safeguard. Even though discord.py
        # sets it automatically, there can be cases where the application ID does
        # not match the actual ID. When this happens, your commands may try to
        # sync to an ID they do not have access to.
        super().__init__(command_prefix="!", intents=INTENTS, application_id=APPLICATION_ID)

        # Some parameters you can assign are:
        #   command_prefix           – The prefix or list of prefixes your bot uses
        #   help_command             – Custom help command or None to disable it
        #   description              – Description used by the help command
        #   case_insensitive         – Whether commands ignore capitalization
        #   tree_cls                 – Custom class for the app command tree
        #   owner_id                 – A single user ID marked as the bot owner
        #   owner_ids                – A list/set of user IDs marked as bot owners
        #   allowed_mentions         – Controls what your bot is allowed to ping
        #   activity                 – Sets the bot’s activity (Playing, Watching, etc.)
        #   status                   – Sets the bot’s online status
        #   chunk_guilds_at_startup  – Whether to load guild members at startup
        #   max_messages             – Size of the internal message cache
        #   heartbeat_timeout        – Time before Discord.py assumes the connection died
        #   guild_ready_timeout      – Timeout for guilds to become “ready”
        #   retry_guild_timeout      – Timeout for retrying guild chunking
        #   member_cache_flags       – Controls which members are cached
        #   proxy                    – Proxy URL if your bot runs behind one
        #   proxy_auth               – Authentication for the proxy
        #   application_id           – The bot’s application ID (used for slash commands)
        #   enable_debug_events      – Enables debug events for developers
        #
        # You can look these parameters up inside discord.py’s documentation
        # for more information.
        # -----------------------------------------------------------------------

    async def setup_hook(self):
        # -----------------------------------------------------------------------
        # You may notice the "async" before defining the function.
        # Regular functions pause the entire bot until they finish running.
        # This means if a command is running, the bot cannot process another
        # command until the first one is done.
        #
        # With "async", we tell Python: "This function can run alongside others."
        # Python will return to it later when processing power is available.
        #
        # setup_hook is an event that runs EXACTLY ONCE. It runs after the bot
        # logs in but before the bot is fully "ready". It is designed for setup
        # tasks such as loading cogs, preparing databases, registering persistent
        # views, and starting background tasks.
        #
        # Why use setup_hook instead of on_ready?
        #   on_ready is a Discord event that fires every time the bot becomes
        #   ready. It can run multiple times during a single session due to
        #   reconnections, Discord hiccups, internet drops, or gateway restarts.
        #
        #   If you want something to run exactly ONCE, put it in setup_hook.
        # -----------------------------------------------------------------------

        # Optional message
        print("Setup_hook started")

        # A defined function to load cogs:
        await self.load_cogs("Cogs")

    async def load_cogs(self, directory):
        # -----------------------------------------------------------------------
        # What are cogs?
        #   Cogs are files that hold commands and events.
        #
        # Why do we use cogs?
        #   We use cogs to organize our code. While it is possible to create all
        #   commands inside this file, it can get out of hand when creating large
        #   bots. Cogs allow you to organize your commands and events inside
        #   their own files, allowing for cleaner code and faster debugging.
        #
        # When loading cogs, we use:
        #   await self.load_extension("path.to.cog")
        # (The directory path uses dots instead of slashes.)
        #
        # In this template, we automatically walk through the directory, find all
        # .py files, and load them as cogs.
        # -----------------------------------------------------------------------

        base = directory.replace("\\", "/")

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    full_path = os.path.join(root, file).replace("\\", "/")
                    relative = full_path[len(base):].lstrip("/")
                    module = f"Cogs.{relative[:-3].replace('/', '.')}"
                    await self.load_extension(module)
                    print(f"[COG LOADER] Loaded cog {module}")

    async def on_ready(self):
        # -----------------------------------------------------------------------
        # on_ready is a Discord event that runs when the bot has fully connected
        # to Discord and is officially "ready" to be used.
        #
        # This event fires after setup_hook has finished running. At this point,
        # the bot has logged in, loaded guild information, prepared internal
        # caches, and completed the login handshake.
        #
        # What is on_ready used for?
        #   Printing a startup message
        #   Logging bot information
        #   Setting the bot’s presence
        #   Confirming that everything loaded correctly
        #
        # IMPORTANT:
        # on_ready can run more than once during a single session. It may fire
        # again if the bot reconnects, your internet drops, Discord has a hiccup,
        # or the gateway restarts.
        #
        # Because of this, DO NOT:
        #   Load cogs here
        #   Sync commands here
        #   Start background tasks here
        #
        # These actions should be done in setup_hook, which runs exactly once.
        #
        # on_ready is best used for simple startup messages or presence updates.
        # -----------------------------------------------------------------------

        print(f"Bot ready: {self.user}")
# -------------------------------------------------------------------------------

# Here is where we create the bot object:
bot = Client()

# -------------------------------------------------------------------------------
# Now we create a prefix command.
# To create a prefix command, we call upon the bot object the same way you would
# use a decorator.
#
# When creating commands, you can define parameters such as the name and
# description of the command. This is also true for slash commands.
@bot.command(name="sync")

# You can set permissions on who can use prefix commands using @commands.is_owner().
# This decorator only allows the owner of the bot (you) to run this command.
@commands.is_owner()

# Here is where you put the command logic. You define the function, pass a ctx
# parameter, and any other parameters your command will use. The ctx peramiter
# stands for "Context"
# When a parameter is set to None, that parameter becomes optional. Otherwise,
# it will be required.
async def sync(self, ctx, sync_type: str = None):
    # -----------------------------------------------------------------------
    # What is syncing?
    #   Syncing is the process of telling Discord what slash commands your
    #   bot has. Discord does not automatically update commands when you
    #   change them in your code. Your bot must explicitly send Discord a
    #   list of commands to add, update, or remove.
    #
    # Why is syncing important?
    #   - New commands will not appear without syncing
    #   - Renamed commands will not update
    #   - Deleted commands will still show up in Discord
    #   - Permissions, descriptions, and options will not refresh
    #
    # Types of syncing:
    #
    #   Global Sync:
    #       - Commands appear in every server your bot is in
    #       - Can take up to one hour to update
    #       - Best for stable, finished commands
    #
    #   Guild Sync:
    #       - Commands update instantly
    #       - Only affects the current guild
    #       - Best for development and testing
    #
    # Why not sync in on_ready?
    #   on_ready can run multiple times due to reconnections, internet drops,
    #   or Discord hiccups. Syncing multiple times can cause rate limits or
    #   command duplication. Always sync in setup_hook or through a manual
    #   sync command like this one.
    #
    # Usage:
    #   !sync            -> Sync commands to this guild only
    #   !sync global     -> Sync commands globally
    #   !sync clear      -> Clear and resync commands for this guild
    #
    # Only the bot owner can run this command to prevent accidental resyncs.
    # -----------------------------------------------------------------------

    try:
        if scope == "global":
            synced = await bot.tree.sync()
            await ctx.send(f"Globally synced {len(synced)} commands")
        else:
            synced = await bot.tree.sync(guild=ctx.guild)
            await ctx.send(f"Synced {len(synced)} commands to **{ctx.guild.name}**")

    except Exception as e:
        await ctx.send(f"Error while syncing commands: `{e}`")

# -------------------------------------------------------------------------------

# And here is where we run the bot:
bot.run("YOUR BOT TOKEN HERE")

# Now you must go to the Cogs folder and look at some examples.
