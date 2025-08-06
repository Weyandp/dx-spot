import os
import discord
from discord.ext import commands
import aiohttp
import asyncio

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

if not DISCORD_TOKEN or not CHANNEL_ID:
    raise ValueError("Bitte DISCORD_TOKEN und DISCORD_CHANNEL_ID als Umgebungsvariablen setzen.")

CHANNEL_ID = int(CHANNEL_ID)

API_URL = "https://web.cluster.iz3mez.it/spots.json/"

intents = discord.Intents.default()
intents.message_content = True  # Wichtig für Command Handling

bot = commands.Bot(command_prefix='!', intents=intents)

async def fetch_spots():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL) as resp:
                if resp.status != 200:
                    print(f"API Fehler: HTTP {resp.status}")
                    return []
                data = await resp.json()
                return data[:10]  # letzte 10 Spots
        except Exception as e:
            print(f"Fehler beim Abruf der API: {e}")
            return []

@bot.command(name="spots")
async def spots(ctx):
    spots = await fetch_spots()
    if not spots:
        await ctx.send("Keine Spots gefunden oder API nicht erreichbar.")
        return
    for spot in spots:
        embed = discord.Embed(
            title=f"DX Spot: {spot.get('spotted', 'unbekannt')}",
            color=0x007acc
        )
        embed.add_field(name="Frequenz", value=spot.get("frequency", "unbekannt"), inline=True)
        embed.add_field(name="Band", value=spot.get("band", "unbekannt"), inline=True)
        embed.add_field(name="Spotter", value=spot.get("spotter", "unbekannt"), inline=True)
        embed.add_field(name="Zeit (UTC)", value=spot.get("timestamp", "unbekannt"), inline=False)
        embed.set_footer(text="powered by Patrick Weyand")
        await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Bot läuft als {bot.user}")

bot.run(DISCORD_TOKEN)

