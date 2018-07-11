import discord
import asyncio
import json
from discord.ext import commands
import os
from os import path
import subprocess
import random

bot = commands.Bot(command_prefix = '???')

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
        mgs = []
        number = int(number)
        async for x in bot.logs_from(ctx.message.channel, limit = number):
            mgs.append(x.content)

        f = open("message.txt", "a")
        for mg in mgs:
            f.write(mg + "\n-\n")
        f.close()

@bot.command(pass_context=True)
async def generate(ctx):
    f = open("message.txt", "r")
    msg = f.read()
    f.close()
    msg = msg.split("\n-\n")
    
    for line in msg:
        line = line.lower.split()
        for i, word in enumerate(line):
            if i == (len(line) - 1):
                model['END'] = model.get('END', []) + [word]
            else:
                if i == 0:
                    model['START'] = model.get('START', []) + [word]
                model[word] = model.get(word, []) + [line[i+i]]

    generated = []
    while True:
        if not generated:
            words = model['START']
        elif generated[-1] in model['END']:
            break
        else:
            words = model = model[generated[-1]]
        generated.append(random.choice(words))

    print(generated)

main()