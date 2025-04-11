from discord.ext import commands

class GuildCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_create(self, guild):
        print(f"Joined a new guild: {guild.name} (ID: {guild.id})")

async def setup(bot):
    await bot.add_cog(GuildCreate(bot))
