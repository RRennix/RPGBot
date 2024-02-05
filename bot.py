import discord
from discord import app_commands
from main import bot
import random
import docx2txt

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1006659664504688722))
    print("Ready!")

@tree.command(name="ficha", description="Veja a ficha do personagem!(kira, triton, philip, gomes, art ou john)", guild=discord.Object(id=1006659664504688722))
async def first_command(interaction: discord.Interaction, personagem: str):
    try:
        caminho_arquivo = "X:/RPG/Ficha detalhada/"+personagem+".docx"
        texto = docx2txt.process(caminho_arquivo)
        await interaction.response.send_message(texto, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message('Erro ao extrair ficha, tente colocar uma das opções: kira, philip, triton, gomes, art ou john', ephemeral=True)
        
@client.event
async def on_message(ctx):
    if ctx.author.id == 1149502315141808178:
        return
    if ctx.channel.category_id == 1104798965678997607:
        if ctx.content.startswith('d'):
            a = str(ctx.content)
            a, b = a.split('d')
            c = random.randint(0,int(b))
            await ctx.reply(f'''`{c}`⟵ [**{c}**] 1d{b}''')
        elif ctx.content[0].isdigit() and 'd' in ctx.content[:4]:
            resultados = []
            a = str(ctx.content)
            a,b = a.split('d')
            for i in range(int(a)):
                c = random.randint(0,int(b))
                resultados.append(c)
            await ctx.reply(f'''`{sum(resultados)}`⟵ **{resultados}** {a}d{b}''')
        else:
            message = ctx
            mensagem = ctx.content
            mensagem = bot(mensagem)    
            await message.reply(mensagem)
    else:
        message = ctx
        mensagem = ctx.content
        mensagem = bot(mensagem)    
        await message.reply(mensagem)

arquivo = open('token.txt','r')
print(arquivo)
token = arquivo.read()
client.run(token)