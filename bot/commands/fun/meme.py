import discord
from discord.ext import commands
from bot.utils.image_utils import generate_meme
import random
import requests
from bot.utils.api_helpers import make_api_call

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme", help="Generate a random meme.")
    async def meme_command(self, ctx):
        """
        Handles the !meme command, fetching and displaying a random meme.

        Args:
            ctx (commands.Context): The context of the command invocation.

        Returns:
            None
        """
        try:
            # Fetch a random meme template from an API or local dataset
            meme_api_url = "https://meme-api.herokuapp.com/gimme"  # Example API URL
            response = make_api_call(meme_api_url, method="GET")

            if response.status_code == 200:
                meme_data = response.json()
                meme_url = meme_data["url"]
                meme_caption = meme_data["title"]

                # Generate the meme image with optional caption
                meme_image = generate_meme(meme_url, caption=meme_caption)

                # Send the meme image to Discord using an embed message
                embed = discord.Embed(title="Here's a meme for you!", color=discord.Color.blue())
                embed.set_image(url="attachment://meme.png")
                await ctx.send(embed=embed, file=discord.File(meme_image, filename="meme.png"))

            else:
                await ctx.send("Failed to fetch a meme. Try again later.")

        except Exception as e:
            await ctx.send(f"An error occurred while generating a meme: {e}")

def setup(bot):
    bot.add_cog(Fun(bot))