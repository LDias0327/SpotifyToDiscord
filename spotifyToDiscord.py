# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import spotipy
import spotipy.util as util
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id="INSERTCLIENTID", client_secret="INSERTCLIENTSECRET")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False
client = Bot(description="Spotify to discord bot.", command_prefix="?", pm_help = False)

def getTracks(playlistName, username):
    df = pd.DataFrame.from_dict(sp.user_playlists(username)["items"])
    filtered = df.loc[df['name'] == playlistName]
    filtered_row = filtered.iloc[0]
    results = sp.user_playlist(username, filtered_row["id"], fields="tracks,next")
    tracks = results['tracks']
    tracklist = []
    for track in tracks["items"]:
        tracklist.append(str(track["track"]["name"]+" - "+track["track"]['artists'][0]['name']))
    return tracklist

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    return await client.change_presence(game=discord.Game(name='PLAYING STATUS HERE')) #This is buggy, let us know if it doesn't work.

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command(pass_context=True)
async def playlist(ctx, playlistname, username):
    await client.say("Oído. Voy a cargar esa playlist en el Rythm bot.")
    await client.join_voice_channel(ctx.message.author.voice.voice_channel)
    await client.say("Por favor, espera, "+str(ctx.message.author))
    for track in getTracks(playlistname, username):
        await client.say("!play "+track)


client.run('INSERTOKEN')

# El bot de Rythm no hace caso a otros bots. Solución: usar la API de youtube para crear una playlist con las canciones y pasárselo al bot de discord para que el user copie y pegue.