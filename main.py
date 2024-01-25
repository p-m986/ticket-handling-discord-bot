from discord.ext import commands
from dotenv import load_dotenv
from typing import Literal, Optional
import discord
import os
import asyncio

load_dotenv()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'),case_insensitive=True, help_command=None, owner_id=820611084938510337, strip_after_prefix=True, intents=discord.Intents.all())

# Connecting to the Discord API


@bot.event
async def on_connect():
    print(f"{bot.user.name} connected to the api successfully")

@bot.event
async def on_ready():
    print("Ready for code execution")  

@bot.event
async def on_resumed():
    print("Graceful disconnect happened, resumed connnection now")

@bot.hybrid_command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


# Fetching the modules sotred in the cogs folder and loading them onto the bot using the load_extension function


@bot.hybrid_command()
@bot.is_owner()
async def reload(ctx, cog: str):
    try:
        await bot.reload_extension(f"cogs.{cog}")
        await ctx.reply(f"{cog} has been reloaded successfully", ephemeral=True)
    except Exception as e:
        raise e


async def loadcog():
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            cog = f"cogs.{cog.replace('.py', '')}"
            await bot.load_extension(cog, package='middleman_bot')
            print("Loaded:\t", cog)
            


if __name__ == "__main__":

    asyncio.run(loadcog())
    try:
        bot.run(os.getenv('TOKEN'))
    except Exception as e:
        print(e)