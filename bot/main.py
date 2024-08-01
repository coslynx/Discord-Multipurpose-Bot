import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize bot with command prefix
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Load commands from bot/commands directory
for filename in os.listdir("bot/commands"):
    if filename.endswith(".py") and filename != "custom_commands.py":
        bot.load_extension(f"bot.commands.{filename[:-3]}")

# Load custom commands if custom_commands.py exists
if os.path.exists("bot/commands/custom_commands.py"):
    bot.load_extension("bot.commands.custom_commands")

# Event handler for bot being ready
@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use !help for a list of commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions for this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide all required arguments for the command.")
    else:
        await ctx.send(f"An error occurred: {error}")
        print(f"Error in command {ctx.command}: {error}")

# Start the bot
bot.run(DISCORD_TOKEN)