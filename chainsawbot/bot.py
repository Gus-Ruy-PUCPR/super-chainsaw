import discord
import os
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv
import subprocess
from scraper import execute_scapper

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

token_Bot = os.getenv("TOKEN_DISCORD")

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} Entrou com ferocidade cortando os códigos do seu computador!")

@bot.command(aliases=["olá", "hello"])
async def ola(ctx:commands.Context):
    await ctx.reply("Hehe! Estou a postos.")

@bot.command()
async def atacar(ctx:commands.Context):
    nome = ctx.author.name
    await ctx.send(f"Grrr! Vou te cortar {nome}.  **Sons de Serra**")

@bot.command()
async def atividades(ctx: commands.Context):
    await ctx.send("Certo! Irei cortar a página e buscar as atividades... **Vrrrm-Vrrrm**")
    
    try:
        # Chama a função do scraper diretamente de forma assíncrona
        resultado_texto = await execute_scapper()
        
        # Envia o texto limpo retornado pelo scraper direto no Discord
        await ctx.reply(f"**Cortei tudinho! Aqui estão as atividades:**\n\n{resultado_texto}")
        
    except Exception as e:
        await ctx.reply(f"Opa, a serra travou! Ocorreu um erro: ```text\n{e}\n```")


bot.run(token_Bot)