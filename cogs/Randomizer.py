import random
import discord
from discord.ext import commands

class Randomizer(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["coinflip"])
    async def coin(self, ctx):
        coin_flip = random.randint(0, 1)
        embed = discord.Embed(title = "", description = "You flipped a coin and got **heads.**" if coin_flip == 1 else "You flipped a coin and got **tails.**", color = 0xd6c0ff)
        await ctx.send(embed = embed)

    @commands.command()
    async def number(self, ctx, min : int, max : int = None):
        if not max:
            random_number = random.randrange(1, min)
            embed = discord.Embed(title = "", description =f"You picked a random number from 1 to {min} and got **{random_number}.**", color = 0xd6c0ff)
            await ctx.send(embed = embed)
        elif min > max:
            embed = discord.Embed(title = "", description = f"**Error:** Index out of range.", color = 0xe45757)
            await ctx.send(embed = embed)
        else:
            random_number = random.randrange(min, max)
            embed = discord.Embed(title = "", description =f"You picked a random number from {min} to {max} and got **{random_number}.**", color = 0xd6c0ff)
            await ctx.send(embed = embed)
    
    @commands.command(aliases = ["myfortune", "fortunecookie"])
    async def fortune(self, ctx):
        with open("data/fortunes.txt", "r") as file:
            lines = file.readlines()
            random_fortune = random.choice(lines)
            embed = discord.Embed(title = "", description = random_fortune, color = 0xd6c0ff)
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Randomizer(client))