import os
import discord
from discord.ext import commands
import aiohttp
import datetime
import pytz

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
VOICE_CHANNEL_ID = os.getenv("VOICE_CHANNEL_ID")

if not DISCORD_TOKEN or not DISCORD_CHANNEL_ID or not VOICE_CHANNEL_ID:
    raise ValueError("Bitte DISCORD_TOKEN, DISCORD_CHANNEL_ID und VOICE_CHANNEL_ID als Umgebungsvariablen setzen.")

DISCORD_CHANNEL_ID = int(DISCORD_CHANNEL_ID)
VOICE_CHANNEL_ID = int(VOICE_CHANNEL_ID)

intents = discord.Intents.default()
intents.message_content = True  # wichtig für Commands

bot = commands.Bot(command_prefix="!", intents=intents)

DX_API_URL = "https://web.cluster.iz3mez.it/spots.json/"
STREAM_URL = "http://stream.laut.fm/rockantenne"

# --- DX-Spots abrufen ---
async def fetch_spots():
    async with aiohttp.ClientSession() as session:
        async with session.get(DX_API_URL) as resp:
            if resp.status != 200:
                print(f"API Fehler: {resp.status}")
                return []
            data = await resp.json()
            return data[:10]  # letzte 10 Spots

# --- DX-Spots Befehl ---
@bot.command(name="dxspots")
async def dxspots(ctx):
    spots = await fetch_spots()
    if not spots:
        await ctx.send("Keine DX-Spots gefunden oder API nicht erreichbar.")
        return

    for spot in spots:
        spotted = spot.get("spotted", "unbekannt")
        frequency = spot.get("frequency", "unbekannt")
        band = spot.get("band", "unbekannt")
        spotter = spot.get("spotter", "unbekannt")
        timestamp_str = spot.get("timestamp")
        # Zeit umwandeln von UTC zu MEZ/MESZ
        if timestamp_str:
            try:
                utc_time = datetime.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                utc_time = utc_time.replace(tzinfo=datetime.timezone.utc)
                local_tz = pytz.timezone("Europe/Berlin")
                local_time = utc_time.astimezone(local_tz)
                time_display = local_time.strftime("%d.%m.%Y %H:%M:%S")
            except Exception:
                time_display = "unbekannt"
        else:
            time_display = "unbekannt"

        embed = discord.Embed(
            title=f"DX Spot: {spotted}",
            color=0x007acc
        )
        embed.add_field(name="Frequenz", value=frequency, inline=True)
        embed.add_field(name="Band", value=band, inline=True)
        embed.add_field(name="Spotter", value=spotter, inline=True)
        embed.add_field(name="Zeit (MEZ/MESZ)", value=time_display, inline=False)
        embed.set_footer(text="Powered by Patrick Weyand")

        await ctx.send(embed=embed)

# --- Stream Steuerung ---
@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel is None:
        print("Sprachkanal nicht gefunden!")
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
    if voice_client is None:
        voice_client = await channel.connect()

    if not voice_client.is_playing():
        audio_source = discord.FFmpegPCMAudio(STREAM_URL)
        voice_client.play(audio_source)
        print(f"Stream wird automatisch im Kanal {channel.name} abgespielt.")

@bot.command(name="play")
async def play_stream(ctx):
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    voice_client = ctx.guild.voice_client

    if voice_client and voice_client.is_playing():
        await ctx.send("Stream läuft bereits.")
        return

    if not voice_client:
        if channel is None:
            await ctx.send("Sprachkanal nicht gefunden.")
            return
        voice_client = await channel.connect()

    audio_source = discord.FFmpegPCMAudio(STREAM_URL)
    voice_client.play(audio_source)
    await ctx.send("Stream gestartet.")

@bot.command(name="stop")
async def stop_stream(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("Bot ist in keinem Sprachkanal.")
        return
    if voice_client.is_playing():
        voice_client.stop()
    await voice_client.disconnect()
    await ctx.send("Stream gestoppt und Sprachkanal verlassen.")

bot.run(DISCORD_TOKEN)
