import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix="!",  
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="/play | Music"
            )
        )
        
        self.mongo_client = MongoClient("")
        self.db = self.mongo_client['']  

    async def setup_hook(self):
        for root, dirs, files in os.walk("./cogs"):
            for filename in files:
                if filename.endswith(".py"):
                    rel_path = os.path.relpath(root, "./cogs")
                    module_path = rel_path.replace(os.sep, ".")
                    await self.load_extension(f"cogs.{module_path}.{filename[:-3]}")
                    print(f"Loaded cog: {module_path}.{filename[:-3]}")
        
        for filename in os.listdir("./events"):
            if filename.endswith(".py"):
                await self.load_extension(f"events.{filename[:-3]}")
                print(f"Loaded event: {filename[:-3]}")
        
        await self.tree.sync()  
        print("Synced slash commands")
    
    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        print(f"Bot ID: {self.user.id}")
        print(f"Discord.py Version: {discord.__version__}")
        print("------")

async def main():
    bot = MusicBot()
    await bot.start("")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())