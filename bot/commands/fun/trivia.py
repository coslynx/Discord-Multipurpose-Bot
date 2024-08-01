import discord
from discord.ext import commands
import random
import time
from bot.database.database_functions import get_trivia_question, update_user_score

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="trivia", help="Play a trivia game!")
    async def trivia_command(self, ctx):
        """
        Handles the !trivia command, starting a trivia game and interacting with users.

        Args:
            ctx (commands.Context): The context of the command invocation.

        Returns:
            None
        """
        try:
            # Initialize game variables
            player_scores = {}
            current_question = None
            question_time = 10  # Time limit for answering (in seconds)
            num_questions = 5  # Number of questions in the game
            game_running = True

            # Start the game loop
            while game_running:
                # Fetch a new trivia question
                current_question = get_trivia_question()

                if current_question:
                    # Display the question and options to users
                    embed = discord.Embed(title=current_question["question"], color=discord.Color.blue())
                    for i, option in enumerate(current_question["options"]):
                        embed.add_field(name=f"{i+1}.", value=option, inline=False)
                    await ctx.send(embed=embed)

                    # Wait for user responses
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() and int(m.content) in range(1, len(current_question["options"]) + 1)

                    try:
                        response = await self.bot.wait_for("message", timeout=question_time, check=check)
                        user_answer = int(response.content) - 1
                    except TimeoutError:
                        await ctx.send("Time's up!")
                        user_answer = None

                    # Check if the answer is correct and update scores
                    if user_answer is not None and user_answer == current_question["correct_answer"]:
                        await ctx.send("Correct!")
                        if ctx.author.id not in player_scores:
                            player_scores[ctx.author.id] = 0
                        player_scores[ctx.author.id] += 1
                        update_user_score(ctx.author.id, 1)  # Update score in the database
                    else:
                        await ctx.send(f"Incorrect. The answer was {current_question['options'][current_question['correct_answer']]}")

                    # Show current scores
                    if player_scores:
                        score_text = "\n".join(f"{self.bot.get_user(player_id).name}: {score}" for player_id, score in player_scores.items())
                        await ctx.send(f"Current scores:\n{score_text}")

                    # Check if the game is over
                    num_questions -= 1
                    if num_questions == 0:
                        game_running = False

                else:
                    await ctx.send("No more trivia questions available. Try again later!")
                    break

            # End of game
            if player_scores:
                # Determine the winner based on the highest score
                winner_id = max(player_scores, key=player_scores.get)
                winner = self.bot.get_user(winner_id)
                await ctx.send(f"Congratulations {winner.mention}, you won the trivia game with a score of {player_scores[winner_id]}!")
            else:
                await ctx.send("No players participated in the game.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(Fun(bot))