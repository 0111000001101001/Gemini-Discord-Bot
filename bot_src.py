from dotenv import load_dotenv
from discord.ext import commands
import google.generativeai as genai
import discord
import os

try:
    load_dotenv()

    # Retrieves keys from .env file.
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    genai.configure(api_key = GOOGLE_API_KEY) # Establishes connection to Gemini using API key.

    # Initializes model and its instructions.
    model = genai.GenerativeModel(
        model_name = "gemini-1.5-flash", 
        system_instruction = """
            You are a Discord bot whose purpose is to serve as a mediator. 
            You will hear the situation described by Discord users about a dispute or argument and will analyze the situation 
            in a fair and unbiased manner. Your job is to understand the nuances of the disagreement and offer thoughtful insights 
            to help the discord users find common ground. Whether it is clarifying misunderstandings, suggesting compromises, 
            or providing objective feedback. You exist to assist Discord users in navigating disputes with ease and 
            bringing harmony back to the community. Any irrelevant inquiries by the Discord users should be dismissed, 
            unless the users are asking about you or your purpose. Additionally, maintain a natural, friendly, and warm tone.
            """)
    
    # Sets prefix that the bot responds to and its permissions.
    bot = commands.Bot(command_prefix = "/", intents = discord.Intents.all())

    # Function is called when the bot connects to Discord.
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}.")

    @bot.command(name = "mediate") # Command handler
    async def query(ctx: commands.Context, *, prompt: str): # Gets context of the command and the input following the command prefix.
        response = model.generate_content(prompt) # Passes prompt as input and generates reply.
        await ctx.reply(response.text) # Send back a response to the same user, in the same channel, using the previously obtained context.

    bot.run(DISCORD_TOKEN) # Connects to Discord.

except Exception as e:
    print(f"Error: {e}")