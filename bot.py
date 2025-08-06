import os
import discord
import aiohttp
import asyncio
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID =(os.getenv("DISCORD_CHANNEL_ID", 0))

if not TOKEN or not CHANNEL_ID:
    raise ValueError("Bitte DISCORD_TOKEN und DISCORD_CHANNEL_ID als Umgebungsvariablen setzen.")

API_URL = "https://web.cluster.iz3mez.it/spots.json/"
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot läuft als {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Slash-Befehle synchronisiert: {len(synced)}")
    except Exception as e:
        print(f"Fehler beim Synchronisieren: {e}")

@bot.tree.command(name="dxspots", description="Zeige die 10 aktuellsten DX-Spots")
async def dxspots(interaction: discord.Interaction):
    await interaction.response.defer()
    
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Fehler beim Abrufen der DX-Spots.")
                return
            data = await resp.json()

    spots = data[:10] if isinstance(data, list) else []
    
    if not spots:
        await interaction.followup.send("ℹ️ Keine aktuellen DX-Spots gefunden.")
        return

    for spot in spots:
        embed = discord.Embed(
            title=f"🌐 DX Spot: {spot.get('spotted', 'unbekannt')}",
            color=0x2ecc71
        )
        embed.add_field(name="📡 Frequenz", value=spot.get("frequency", "unbekannt"), inline=True)
        embed.add_field(name="📶 Band", value=spot.get("band", "unbekannt"), inline=True)
        embed.add_field(name="👤 Spotter", value=spot.get("spotter", "unbekannt"), inline=True)
        embed.add_field(name="🕓 Zeit (UTC)", value=spot.get("timestamp", "unbekannt"), inline=False)
        embed.set_footer(text="📢 Powered by Patrick Weyand")
        await interaction.followup.send(embed=embed)

bot.run(TOKEN)
