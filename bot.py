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
                    msg.replace('@', '(a)')
                    f.write(x.content + '\n')

@bot.command(pass_context=True)
async def saver(ctx, name):
    appInfo = await bot.application_info()
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
                        msg.replace('\n', '.')
                        msg.replace('@', '(a)')
                        f.write(x.content + '\n')
                    lastMessage = x
                print(size)
        await bot.change_presence(game=discord.Game(name='-generate'))
                

@bot.command(pass_context=True)
async def generate(ctx):
    global text_model
    msg = text_model.make_sentence(tries = 100)
    msg.replace('@', '(a)')
    await bot.say(msg)

main()