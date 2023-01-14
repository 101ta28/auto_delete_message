import os
import re
from asyncio import sleep
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN=os.getenv('TOKEN')
CHANNEL_ID=os.getenv('CHANNEL_ID')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# client = discord.Client(intents=intents)
channel = bot.get_channel(CHANNEL_ID)

delete_time = 10

# 内部関数

def get_time(time_arg):
	# time_argは1h30m30sのような形式で渡される
	# それを秒に変換して返す
	match = re.match(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)', time_arg)
	if match:
		return int(match.group(1) or 0) * 3600 + int(match.group(2) or 0) * 60 + int(match.group(3) or 0)
	else:
		return 'time set error'

# Discord周り

@bot.event
async def on_ready():
	print('On ready')

@bot.command()
async def set_dtime(ctx, arg):
	time_arg = arg.replace('時間', 'h').replace('分', 'm').replace('秒', 's')
	# time_argからdelete_timeを設定する
	ret_get_time = get_time(time_arg)
	if ret_get_time == 'time set error':
		await ctx.send(f'時間の指定が間違っています\n`!adm_help`でヘルプを表示します\nこのメッセージは{delete_time}秒後に削除されます')
		await sleep(delete_time)
		await ctx.message.delete()
	elif type(ret_get_time) == int:
		await ctx.send(f'メッセージを削除する時間を{arg}に設定しました\nこのメッセージは{delete_time}秒後に削除されます')
		await sleep(delete_time)
		await ctx.message.delete()
	else:
		await ctx.send(f'不明なエラーが発生しました\nこのメッセージは{delete_time}秒後に削除されます')
		await sleep(delete_time)
		await ctx.message.delete()

@bot.command()
async def get_dtime(ctx):
	await ctx.send(f'現在のメッセージを削除する時間は{delete_time}秒です\nこのメッセージは{delete_time}秒後に削除されます')
	await sleep(delete_time)
	await ctx.message.delete()

@bot.command()
async def adm_help(ctx):
	await ctx.send(f'`!set_dtime <time>` - メッセージを削除するための時間を指定します\n<time>の例として、2時間1分30秒後にメッセージを削除したい場合 `!set_dtime 2h1m30s`と指定します\n日本語で指定することもできます `!set_dtime 2時間1分30秒`\n`!get_dtime` - メッセージが削除されるまでの時間を確認できます\n`!adm_help` - このメッセージを表示します \n\n このメッセージは{delete_time}秒後に削除されます')
	await sleep(delete_time)
	await ctx.message.delete()

@bot.event
async def on_message(message):
	await bot.process_commands(message)
	if not message.author.bot and message.channel.id == CHANNEL_ID:
		await sleep(delete_time)
		try:
			await message.delete()
		except Exception as e:
			with open('log.log', 'a') as f:
				f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {e}\n')

bot.run(TOKEN)
