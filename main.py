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
    await ctx.send('Checked')


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if message.content.startswith('!'):
        await bot.process_commands(message)
    else:
        session = aiohttp.ClientSession()
        text = message.content
        response = await session.get(f"{api_base}/images?limit=10&q={urllib.parse.quote(text)}")
        memes = await response.json()
        await session.close()
        if len(memes) == 0:
            await message.channel.send('''Error 404 memes not found''')
        else:
            pics = []
            for meme in memes:
                mid = meme['id']
                link = f"{api_pics}/normal/{mid[:2]}/{mid[2:4]}/{mid}.webp"
                session = aiohttp.ClientSession()
                async with session.get(link) as resp:
                    data = io.BytesIO(await resp.read())
                    pics.append(discord.File(data, 'meme.webp'))
                await session.close()
            await message.channel.send(files=pics)


bot.run(token)
