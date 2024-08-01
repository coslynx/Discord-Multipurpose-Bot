import discord
from discord.ext import commands
from bot.database.database_functions import get_server_settings, update_server_settings
import re
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from bot.utils.nlp_utils import check_for_offensive_language
from bot.utils.logging_utils import log_moderation_action

nltk.download('stopwords')
nltk.download('vader_lexicon')

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sia = SentimentIntensityAnalyzer()

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handles the message event, applying automod rules if enabled."""
        if message.author.bot:
            return  # Ignore messages from bots

        try:
            server_settings = await get_server_settings(message.guild.id)
            if server_settings["automod_enabled"]:
                await self.automod_filter(message, server_settings)
        except Exception as e:
            print(f"Error during automod: {e}")

    async def automod_filter(self, message, server_settings):
        """Filters messages based on server settings and automod rules."""
        if self.check_for_spam(message.content, server_settings):
            await self.handle_spam(message, server_settings)
        elif self.check_for_profanity(message.content, server_settings):
            await self.handle_profanity(message, server_settings)
        elif self.check_for_negative_sentiment(message.content, server_settings):
            await self.handle_negative_sentiment(message, server_settings)

    def check_for_spam(self, message_content, server_settings):
        """Checks if the message contains spam based on server settings."""
        # Example: Check for excessive links or repetitive text
        link_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message_content))
        if link_count >= server_settings["spam_link_threshold"]:
            return True
        return False

    def check_for_profanity(self, message_content, server_settings):
        """Checks if the message contains profanity based on server settings."""
        return check_for_offensive_language(message_content)  # Uses NLP utility function

    def check_for_negative_sentiment(self, message_content, server_settings):
        """Checks if the message has negative sentiment based on server settings."""
        # Example: Use sentiment analysis library (NLTK)
        sentiment = self.sia.polarity_scores(message_content)
        if sentiment["compound"] <= server_settings["negative_sentiment_threshold"]:
            return True
        return False

    async def handle_spam(self, message, server_settings):
        """Handles spam messages based on server settings."""
        await message.delete()
        if server_settings["automod_action_spam"] == "mute":
            await message.author.timeout(duration=server_settings["automod_mute_duration"])
            log_moderation_action(message.guild.id, message.author.id, "mute", "spam")
        elif server_settings["automod_action_spam"] == "kick":
            await message.guild.kick(message.author)
            log_moderation_action(message.guild.id, message.author.id, "kick", "spam")
        await message.channel.send(f"{message.author.mention}, your message was flagged as spam and has been deleted.")

    async def handle_profanity(self, message, server_settings):
        """Handles profanity messages based on server settings."""
        await message.delete()
        if server_settings["automod_action_profanity"] == "mute":
            await message.author.timeout(duration=server_settings["automod_mute_duration"])
            log_moderation_action(message.guild.id, message.author.id, "mute", "profanity")
        elif server_settings["automod_action_profanity"] == "kick":
            await message.guild.kick(message.author)
            log_moderation_action(message.guild.id, message.author.id, "kick", "profanity")
        await message.channel.send(f"{message.author.mention}, your message contained inappropriate language and has been deleted.")

    async def handle_negative_sentiment(self, message, server_settings):
        """Handles negative sentiment messages based on server settings."""
        await message.delete()
        if server_settings["automod_action_negative_sentiment"] == "warn":
            await message.channel.send(f"{message.author.mention}, please refrain from using such language. Let's keep the conversation positive.")
            log_moderation_action(message.guild.id, message.author.id, "warn", "negative sentiment")

def setup(bot):
    bot.add_cog(Moderation(bot))