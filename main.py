import discord
from discord.ext import commands
import youtube_dl
import asyncio

default_intents = discord.Intents.default()
default_intents.members = True
client = discord.Client(intents=default_intents)
bot = commands.Bot(command_prefix= "!", description="bot d'AMIS IRL créé par Abdellah Islah")
musics = {}
ytdl = youtube_dl.YoutubeDL()
@bot.event
async def on_ready():
  print("Le bot est prêt")
@client.event
async def on_member_join(member):
    general_channel = client.get_channel(877897089001082885)
    general_channel.send(f"Bienvenue sur le serveur {member.display_name} !") 
@bot.command()
async def islahinfo(ctx):
  message = "Islah est un développeur qui me programme mtn il a 5 documentation ouvertes devant lui il commis des erreurs et il est conny springer s'il devient chauve ahaha!!!!!"  
  await ctx.send(message)
@bot.command()
async def fatihinfo(ctx):
  message = "Fatih est le meilleur ami de Islah et de yassine; son statue de ne pas déranger lui va bien mais est quasiment tout le temps en ligne(quel fou), mais tu sais seiko islah ont un point faible lorsqu'il reçoit une erreur dans la console il crie 'ouahhhhhhh j'ai besoin de seiko pour résoudre avec moi ce problème' "
  await ctx.send(message)
@bot.command()
async def malikiinfo(ctx):
  message = "maliki déclenche toujours des batailles navales against yasmina, il l'a même donné un coup douleureux, mais il est gentil avec tous le monde (sauf yassmina)et  il est le meilleur de la classe. "  
  await ctx.send(message)
@bot.command()
async def serveurinfo(ctx):
  serveur = ctx.guild
  numberOfTextChannel = len(serveur.text_channels)
  numberOfVoiceChannel = len(serveur.voice_channels)
  numberOfPerson = serveur.member_count
  serverName = serveur.name
  message = f"Bonjour dans **{serverName}** est un serveur d'amis qui échange leur sourire virtuellement \n ce serveur contient {numberOfPerson} personnes et {numberOfTextChannel} salons textuels, {numberOfVoiceChannel} salons vocaux, n'hésite pas à parler avec les membres de ce serveur, si tu rencontres des problème contacte @Seiko#9975 ou @Armin Arlert#5671 "
  await ctx.send(message)
@bot.command()
async def hello(ctx):
  serveur = ctx.guild
  serverName = serveur.name
  await ctx.send(f"bonjour, c'est tellement beau de dire des mots polis en {serverName}")
@bot.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, nombre: int):
  messages = await ctx.channel.history(limit= nombre + 1).flatten()
  for message in messages:
    await message.delete()

@bot.command()
@commands.has_permissions(administrator = True)
async def expulser(ctx, user: discord.User, *reason):
  reason = " ".join(reason)
  await ctx.guild.kick(user, reason  = reason)
  await ctx.send(f"{user} a été expulsé")
@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, user: discord.User, *reason):
  reason = " ".join(reason)
  await ctx.guild.ban(user, reason  = reason)
  await ctx.send(f"{user} a été ban, raison: {reason}")
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, user, *reason):
  reason = " ".join(reason)
  userName, userId = user.split("#")  
  bannedUsers = await ctx.guild.bans()
  for i in bannedUsers:
    if i.user.name == userName and i.user.discriminator == userId:
      await ctx.guild.unban(i.user, reason = reason)
      await ctx.send(f"{user} a été unban, raison: {reason}")
      return
  await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bannissements")  

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)      




bot.run('ODg4MTQwNTY3MzMzMTgzNTE5.YUOXXA.1-REnI2BA1js8f7B4U4FrBOOeBA')