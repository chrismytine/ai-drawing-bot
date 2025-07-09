import discord
import os
from discord.ext import commands
from main import FusionBrainAPI
from config import TOKEN, API_KEY, SECRET_KEY

# Inisialisasi bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# COMMAND: !start
@bot.command()
async def start(ctx):
    await ctx.send(f"Heyyyaaa, {ctx.author.name}. Gunakan `!help_me` untuk melihat perintah yang tersedia.")

# COMMAND: !help_me
@bot.command()
async def help_me(ctx):
    await ctx.send(
        "**Daftar Perintah:**\n"
        "`!start` - Mulai bot\n"
        "`!help_me` - Lihat semua perintah\n"
        "`!art <prompt>` - Buat gambar dari teks"
    )

# COMMAND: !art <prompt>
@bot.command()
async def art(ctx, *, prompt: str):
    api = FusionBrainAPI(
        'https://api-key.fusionbrain.ai/',
        API_KEY,
        SECRET_KEY
    )

    await ctx.send("Sedang membuat gambarmu...")

    try:
        async with ctx.typing(): #bot ngetik
            pipeline_id = api.get_pipeline()
            uuid = api.generate(prompt, pipeline_id, images=1)
            files = api.check_generation(uuid)
            filepath = "generated_image.jpg"
            api.save_image(files, filepath)

            with open(filepath, "rb") as photo:
                await ctx.send(file=discord.File(photo, filepath))

            os.remove(filepath)
    except Exception as e: #kalo error
        await ctx.send(f"❌ Gagal menghasilkan gambar: {e}")

# Menjalankan bot
bot.run(TOKEN)
