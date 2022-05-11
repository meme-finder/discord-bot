import io
import os
import urllib.parse
import aiohttp
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
token = os.environ['TOKEN']
api_base = os.environ['API_BASE']
api_pics = os.environ['API_PICS']


@bot.event
async def on_ready():
    print('Bot is ready to operate')


@bot.command(name="ping", pass_context=True, aliases=["latency", "latence"])
async def ping(ctx):
    pong = round(bot.latency * 1000)
    embed = discord.Embed(title="__**Latency**__", colour=discord.Colour.from_rgb(round(256 * (1 - 1 / pong)), 250, 0),
                          timestamp=ctx.message.created_at)
    embed.add_field(name="Bot latency :", value=f"`{pong} ms`")

    await ctx.reply(embed=embed)


@bot.command(name='meme', pass_context=True)
async def find_meme(ctx, *, meme_request):
    session = aiohttp.ClientSession()
    text = meme_request
    response = await session.get(f"{api_base}/images?limit=10&q={urllib.parse.quote(text)}")
    memes = await response.json()
    await session.close()
    if len(memes) == 0:
        embed = discord.Embed(title="Error 404 :(", colour=discord.Colour.red(), timestamp=ctx.message.created_at)
        embed.add_field(name='Memes not found',
                        value="Sorry, there are no memes in our database suitable for your request")
        await ctx.reply(embed=embed)
    else:
        pics = []
        for meme in memes:
            mid = meme['id']
            link = f"{api_pics}/normal/{mid[:2]}/{mid[2:4]}/{mid}.webp"
            session = aiohttp.ClientSession()
            async with session.get(link) as resp:
                data = io.BytesIO(await resp.read())
                pics.append(discord.File(data, f'{mid}.webp'))
            await session.close()
        await ctx.reply(files=pics)


bot.run(token)
