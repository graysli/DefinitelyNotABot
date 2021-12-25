import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["commands"])
    async def help(self, ctx, *cog):
        embed = discord.Embed(title = "**Help:  commands**", color = 0xfff368)
        embed.add_field(name = "General", value = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format("!clear - clear messages", "!ban - ban someone", "!tempban - ban someone temporarily", "!unbban - unban someone",
                        "!mute - mute someone", "!unmute - unmute someone", "!kick - kick someone", "!ping - check the bot's latency", "!prefix - change the command prefix", inline = False))
        embed.add_field(name = "Games", value = "{}\n{}\n{}\n".format("!coin - flip a coin, heads or tails", "!number - pick a random number in range", "!fortune - tell my fortune", inline = False))
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Help(client))
