import discord
import asyncio
import json
from discord.ext import commands
import os
from os import path
import subprocess
import random
import markovify

bot = commands.Bot(command_prefix = '-')

bot.remove_command('help')

def main():
    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='snooping arround'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
	await bot.process_commands(message)

@bot.command(pass_context=True)
async def save(ctx, number):
    appInfo = await bot.application_info()
    if ctx.message.author == appInfo.owner:
        await bot.delete_message(ctx.message)
        number = int(number)

        with open("message.txt", "a") as f:
            async for x in bot.logs_from(ctx.message.channel, limit = number):
                if x.content != "":
                    msg = x.content
                    msg.replace('\n', '.')
                    f.write(x.content + '\n')  

@bot.command(pass_context=True)
async def generate(ctx):
    with open("message.txt", "r") as f:
        text = f.read()
    text_model = markovify.NewlineText(text)
    await bot.say(text_model.make_sentence(tries = 100))

main()