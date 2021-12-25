import discord
import json
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from discord.ext.commands.core import bot_has_permissions
import os
from api import *

def get_prefix(client, message):
    with open("prefixes.json", "r") as file:
        prefixes = json.load(file)
    return prefixes[str(message.guild.id)]

class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]
        if amount.isdigit() and unit in ["s", "m", "h"]:
            return (int(amount), unit)

client = commands.Bot(command_prefix=get_prefix)
client.remove_command("help")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_ready():
    print(f"{client.user.name} is ready!")
    print('----------------------------------------')

@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as file:
        prefixes = json.load(file)
    prefixes[str(guild.id)] = "!"
    with open("prefixes.json", "w") as file:
        json.dump(prefixes, file, indent = 2)

@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as file:
        prefixes = json.load(file)
    prefixes.pop(str(guild.id))
    with open("prefixes.json", "w") as file:
        json.dump(prefixes, file, indent = 2)

@client.command(description = "Changes the command prefix.")
@has_permissions(administrator=True)
async def prefix(ctx, prefix):
    with open("prefixes.json", "r") as file:
        prefixes = json.load(file)
    prefixes[str(ctx.guild.id)] = prefix
    with open("prefixes.json", "w") as file:
        json.dump(prefixes, file, indent = 2)
    embed = discord.Embed(title = "", description = f"**Success:** prefix has been changed to ''{prefix}''", color = 0xd1f9a6)
    await ctx.send(embed = embed)

@client.command(description = "A simple hello command.")
async def hello(ctx):
    embed = discord.Embed(title = "", description = f"Hi, I am Definitely Not A Bot.", color = 0xd1f9a6)
    await ctx.send(embed = embed)

@client.command(description = "Shows the bot's latency.")
async def ping(ctx):
    embed = discord.Embed(title = "", description = f"**Ping:** {round(client.latency * 1000)} ms", color = 0xd1f9a6)
    await ctx.send(embed = embed)

@client.command(description = "Clears messages from the channel.")
@has_permissions(manage_messages = True)
@bot_has_permissions(administrator = True)
async def clear(ctx, *, amount : int):
    await ctx.channel.purge(limit = amount+1)

@client.command(description = "Mutes a user.")
@has_permissions(kick_members = True, manage_roles = True)
async def mute(ctx, member : discord.Member = None, *, reason = "unspecified"):
    if member.guild_permissions.administrator:
        embed = discord.Embed(title = "", description = f"**Error:**  the member you are trying to ban is an administrator.", color = 0xe45757)
        await ctx.send(embed = embed)
    else:
        muted_role = discord.utils.get(ctx.guild.roles, name = "muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="muted")
            for ch in ctx.guild.channels:
                await ctx.channel.set_permissions(muted_role, speak = False, send_messages = False)
            await member.add_roles(muted_role, reason = reason)
            embed = discord.Embed(title = "", description = f"**Success:** {member.name} has been muted.\n**Reason:** {reason}", color = 0xd1f9a6)
            await ctx.send(embed = embed)
        else:
            await member.add_roles(muted_role, reason = reason)
            embed = discord.Embed(title = "", description = f"**Success:** {member.name} has been muted.\n**Reason:** {reason}", color = 0xd1f9a6)
            await ctx.send(embed = embed)

@client.command(description = "Unmutes a user.")
@has_permissions(kick_members = True, manage_roles = True)
async def unmute(ctx, member : discord.Member = None, *, reason = "unspecified"):
        muted_role = discord.utils.get(ctx.guild.roles, name = "muted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            embed = discord.Embed(title = "", description = f"**Success:** {member.name} has been unmuted.\n**Reason:** {reason}", color = 0xd1f9a6)
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = "", description = f"**Error:** {member.name} cannot be unmuted.", color = 0xe45757)
            await ctx.send(embed = embed)

@client.command(description = "Kicks a user from the server.")
@has_permissions(kick_members = True, manage_roles = True)
async def kick(ctx, member : discord.Member = None, *, reason = "unspecified"):       #reads in member as Member object
    if member.guild_permissions.administrator:
        embed = discord.Embed(title = "", description = f"**Error:** the member you are trying to kick is an administrator.", color = 0xe45757)
        await ctx.send(embed = embed)
    else:
        await member.kick(reason = reason)
        embed = discord.Embed(title = "", description = f"**Success:** {member.name} has been kicked from the server.\n**Reason:** {reason}", color = 0xd1f9a6)
        await ctx.send(embed = embed)

@client.command(description = "Bans a user from the server.")
@has_permissions(ban_members = True, manage_roles = True)
async def ban(ctx, member : discord.Member = None, *, reason = "unspecified"):       #reads in member as Member object
    if member.guild_permissions.administrator:
        embed = discord.Embed(title = "", description = f"**Error:** the member you are trying to ban is an administrator.", color = 0xe45757)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title = "", description = f"**Success:** {member.name} has been banned from the server.\n**Reason:** {reason}", color = 0xd1f9a6)
        await ctx.send(embed = embed)

@client.command(description = "Temporarily bans a user from the server.")
@has_permissions(ban_members = True, manage_roles = True)
async def tempban(ctx, member : commands.MemberConverter, duration : DurationConverter, *, reason = "unspecified"):       #reads in member as Member object
    multiplier = {"s": 1, "m": 60, "h": 3600}
    amount, unit = duration
    if member.guild_permissions.administrator:
        embed = discord.Embed(title = "", description = f"**Error:** the member you are trying to temporarily ban is an administrator.", color = 0xe45757)
        await ctx.send(embed = embed)
    else:
        await ctx.guild.ban(member)
        embed = discord.Embed(title = "", description = f"**Success:** {member.name} has been temporarily banned from the server for {amount}{unit}.\n**Reason:** {reason}", color = 0xd1f9a6)
        await ctx.send(embed = embed)
        await asyncio.sleep(amount*multiplier[unit])
        await ctx.guild.unban(member)

@client.command(description = "Unbans a user from the server.")
@has_permissions(ban_members = True, manage_roles = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_number = member.split("#")
    for banned_item in banned_users:
        user = banned_item.user
        if (user.name, user.discriminator) == (member_name, member_number):
            embed = discord.Embed(title = "", description = f"**Success:** {member.mention} has been unbanned from the server.", color = 0xd1f9a6)
            await ctx.send(embed = embed)
            await ctx.guild.unban(user)
            return 
    embed = discord.Embed(title = "", description = f"**Error:** {member} user not found in banned list.", color = 0xe45757)
    await ctx.send(embed = embed)

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

client.run(TOKEN)