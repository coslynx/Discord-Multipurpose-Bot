import discord
from discord.ext import commands
from bot.database.database_functions import create_member, update_member_data
from datetime import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Handles the member join event, recording the join time in the database."""
        try:
            await create_member(member.id, member.name, datetime.now())
            print(f"{member.name} joined the server.")
        except Exception as e:
            print(f"Error while recording member join: {e}")

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        """Handles the member leave event, recording the leave time in the database."""
        try:
            await update_member_data(member.id, leave_time=datetime.now())
            print(f"{member.name} left the server.")
        except Exception as e:
            print(f"Error while recording member leave: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handles the message event, incrementing the message count for the user."""
        if not message.author.bot:
            try:
                await update_member_data(message.author.id, message_count=1)
            except Exception as e:
                print(f"Error while updating message count: {e}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Handles voice state updates, tracking the time spent in voice channels."""
        try:
            if before.channel is None and after.channel is not None:
                # User joined a voice channel
                await update_member_data(member.id, voice_join_time=datetime.now())
            elif before.channel is not None and after.channel is None:
                # User left a voice channel
                await update_member_data(member.id, voice_leave_time=datetime.now(), voice_duration=datetime.now() - before.channel.joined_at)
        except Exception as e:
            print(f"Error while tracking voice activity: {e}")

def setup(bot):
    bot.add_cog(Moderation(bot))