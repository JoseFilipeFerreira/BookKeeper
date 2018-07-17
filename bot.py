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

text_model = None

def main():
    global text_model
    with open("geral.txt", "r") as f:
        text = f.read()
        text_model = markovify.NewlineText(text)
    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='-generate'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
	await bot.process_commands(message)

@bot.command(pass_context=True)
async def saver(ctx, name):
    appInfo = await bot.application_info()
    nSaved = 0
    if ctx.message.author == appInfo.owner:
        await bot.change_presence(game=discord.Game(name='snooping arround'))
        await bot.delete_message(ctx.message)
        size = 100
        lastMessage = None
        with open("{}.txt".format(name), "a") as f:
            while size == 100:
                messages = bot.logs_from(ctx.message.channel,before = lastMessage, limit = 100)
                size = 0             
                async for x in messages:
                    size += 1
                    if x.content != "":
                        msg = x.content
                        f.write(x.content + '\n')
                    lastMessage = x
                nSaved += size
                print(nSaved)
        await bot.change_presence(game=discord.Game(name='-generate'))
    else:
        await bot.say("Invalid User")
                

@bot.command(pass_context=True)
async def generate(ctx):
    global text_model
    msg = text_model.make_sentence(tries = 100)
    await bot.say(msg.replace("@", "(a)"))

main()