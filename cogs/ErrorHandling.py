import discord
from discord.ext import commands

class ErrorHandling(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def err_embed(self, ctx, title, desc):
        embed = discord.Embed(title = title, description = desc, color = 0xe45757)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"):
            return
        error = getattr(error, "original", error)
        command = ctx.message.content.split(' ', 1)[0]
        if isinstance(error, commands.CommandNotFound):
            await self.err_embed(ctx, "", f"**Error: ** {command} command not found.")
        elif isinstance(error, commands.MemberNotFound):
            await self.err_embed(ctx, "", f"**Error: ** {error.argument} member not found.")
        elif isinstance(error, commands.UserNotFound):
            await self.err_embed(ctx, "", f"**Error: ** {error.argument} user not found.")
        elif isinstance(error, commands.BadArgument):
            command = ctx.message.content
            await self.err_embed(ctx, "", f"**Error: ** {command} command has the wrong argument type.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await self.err_embed(ctx, "", f"**Error: ** {command} command is missing its required arguments.")
        elif isinstance(error, commands.MissingPermissions):
            await self.err_embed(ctx, "", f"**Error: ** you do not have the required permission(s) to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await self.err_embed(ctx, "", f"**Error: ** to use this command I must have the ''administrator'' role.")
        else:
            await self.err_embed(ctx, "", f"**Error: ** an unknown error has occurred.")

def setup(client):
    client.add_cog(ErrorHandling(client))