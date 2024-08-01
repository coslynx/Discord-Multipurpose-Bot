import discord
from discord.ext import commands
import random
import requests
from bot.utils.api_helpers import make_api_call

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="random", aliases=["rand"], help="Get a random fact, joke, or quote.")
    async def random_content_command(self, ctx, content_type=None):
        """
        Handles the !random command, fetching and displaying random content based on user input.

        Args:
            ctx (commands.Context): The context of the command invocation.
            content_type (str, optional): The type of content to fetch (fact, joke, quote). Defaults to None.

        Returns:
            None
        """
        try:
            if content_type is None:
                await ctx.send("Please specify the type of content you want (fact, joke, quote).")
                return

            if content_type.lower() == "fact":
                fact = self.fetch_random_fact()
                await ctx.send(f"Fun fact: {fact}")
            elif content_type.lower() == "joke":
                joke = self.load_random_jokes()
                await ctx.send(f"Here's a joke: {joke}")
            elif content_type.lower() == "quote":
                quote = self.get_random_quote()
                await ctx.send(f"Random quote: {quote}")
            else:
                await ctx.send("Invalid content type. Please choose from fact, joke, or quote.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    def fetch_random_fact(self):
        """
        Fetches a random fact from a fact API.

        Returns:
            str: A random fact.
        """
        try:
            response = make_api_call("https://uselessfacts.jsph.pl/random.json", method="GET")
            if response.status_code == 200:
                return response.json()["text"]
            else:
                return "Failed to fetch a fact. Try again later."
        except Exception as e:
            return f"An error occurred while fetching a fact: {e}"

    def load_random_jokes(self):
        """
        Loads a random joke from a local file.

        Returns:
            str: A random joke.
        """
        try:
            with open("bot/data/jokes.txt", "r", encoding="utf-8") as f:
                jokes = f.readlines()
            return random.choice(jokes).strip()
        except Exception as e:
            return f"An error occurred while loading jokes: {e}"

    def get_random_quote(self):
        """
        Fetches a random quote from a quote API.

        Returns:
            str: A random quote.
        """
        try:
            response = make_api_call("https://api.quotable.io/random", method="GET")
            if response.status_code == 200:
                return f"{response.json()['content']} - {response.json()['author']}"
            else:
                return "Failed to fetch a quote. Try again later."
        except Exception as e:
            return f"An error occurred while fetching a quote: {e}"

def setup(bot):
    bot.add_cog(Fun(bot))