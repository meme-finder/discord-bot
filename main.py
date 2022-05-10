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


@bot.command(name='check')
async def check(ctx):
    await ctx.reply('Checked')


@bot.command(name='meme', pass_context=True)
async def find_meme(ctx, *, meme_request):
    session = aiohttp.ClientSession()
    text = meme_request
    response = await session.get(f"{api_base}/images?limit=10&q={urllib.parse.quote(text)}")
    memes = await response.json()
    await session.close()
    if len(memes) == 0:
        await ctx.reply('''Error 404 memes not found''')
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
