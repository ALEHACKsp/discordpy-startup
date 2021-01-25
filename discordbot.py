from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@client.event
async def on_message(message):
    if message.content == '/cleanup':
        if message.author.guild_permissions.administrator:
            await message.channel.purge()
            await message.channel.send('塵一つ残らないね！')
        else:
            await message.channel.send('何様のつもり？')    

ID_CHANNEL_WELCOME = 803175322689601557 # 入室用チャンネルのID(int)
ID_ROLE_WELCOME = 668769063324876801 # 付けたい役職のID(int)
EMOJI_WELCOME = '✅' # 対応する絵文字

# 役職を付与する非同期関数を定義
async def grant_role(payload):
    # 絵文字が異なる場合は処理を打ち切る
    if payload.emoji.name != EMOJI_WELCOME: 
        return

    # チャンネルが異なる場合は処理を打ち切る
    if payload.channel_id != ID_CHANNEL_WELCOME:
        return

    # Member オブジェクトと Role オブジェクトを取得して役職を付与
    member = payload.member
    role = guild.get_role(ID_ROLE_WELCOME)
    await member.add_roles(role)
    return member

# リアクション追加時に実行されるイベントハンドラを定義
@client.event
async def on_raw_reaction_add(payload):
    # 役職を付与する非同期関数を実行して Optional[Member] オブジェクトを取得
    member = await grant_role(payload)
    if member is not None: # 役職を付与したメンバーがいる時
        text = f'{member.mention} ようこそ！'
        await client.get_channel(ID_CHANNEL_WELCOME).send(text)
        
bot.run(token)
