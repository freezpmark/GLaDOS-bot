import discord
from discord.ext import commands
import os, random

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Rolls a number between 1 and 100. (?roll 1000)")
    async def roll(self, ctx, end=100):
        await ctx.send(ctx.message.author.mention + ' rolls ' + str(random.randint(1, end)) + ' (1-' + str(end) + ')')

    @commands.command(brief="Enables Python interactive shell.")
    async def python(self, ctx):
        await ctx.send('Python mode activated! Exit by "?"')
        await self.client.change_presence(activity=discord.Game(name='Python'))

        ans = 0
        msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

        while not msg.content.startswith('?'):
            try:                                # evaluating with value return
                ans = eval(msg.content)
                await ctx.send(ans)
            except:                             # executing without return
                try:
                    exec(msg.content)
                except Exception as e:          # invalid input
                    await ctx.send(e)
            msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you'))
        await ctx.send("Python mode deactivated!")

    @commands.command(brief="Deletes specified number of messages. (?clear 5)")
    async def clear(self, ctx, amount=5):
        channel = ctx.message.channel
        async for message in channel.history(limit=int(amount) + 1):
            await message.delete()
        await ctx.send(f'{amount} messages has been deleted.')

    @commands.command(brief="Joins or moves to voice channel.++")
    async def join(self, ctx, *, name=None):
        ''' "?join" - bot joins the voice channel in which is the current user
"?join radio" - bot joins "radio" voice channel'''
        if name:
            channel = discord.utils.find(lambda r: r.name == name, ctx.guild.channels)
    
        if ctx.voice_client is not None:
            if name:
                return await ctx.voice_client.move_to(channel)
            else:
                return await ctx.voice_client.move_to(ctx.author.voice.channel)
        elif name:
            return await channel.connect()
        else:
            await ctx.author.voice.channel.connect()

    @commands.command(brief="Disconnects the bot from voice channel.")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    '''
    @commands.command(brief="Plays a file from the local filesystem.++",
                    description=str(os.listdir('audio')).replace('.mp3',''))
    async def play(self, ctx, *, query):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("audio/" + query + ".mp3"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
    '''

def setup(client):
    client.add_cog(Commands(client))