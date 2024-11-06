import discord
from discord import app_commands
import google.generativeai as genai
import random
import json

# Função para carregar o histórico do arquivo
def carregar_historico(arquivo='historico.txt'):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return f.read().replace('-;-', '\n')
    except FileNotFoundError:
        return []  # Se o arquivo não existir, retorna uma lista vazia
# Função para salvar o histórico no arquivo
def salvar_historico(historico, arquivo='historico.txt'):
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write('-;-'.join(historico))

# Carregar a configuração
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Acessando as variáveis
api_disc = config['api_disc']
api_gemini = config['api_gemini']
API_KEY = api_gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
historico = []
historic = carregar_historico()
chat = model.start_chat(history=historico)

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    entrada = f"Sistema: Lembre-se disso:{historic}"
    response = chat.send_message(entrada)
    resposta = response.text
    historico.append(historic)
    historico.append(resposta)
    salvar_historico(historico)  # Salvar o histórico atualizado
    print(resposta)
    await tree.sync(guild=discord.Object(id=1239947428359180339))
    print("Ready!")
    
@client.event
async def on_message(ctx):
    if ctx.author.id == 1149502315141808178:    
        return  
    if ctx.channel.category_id == 1243983641072369706:  
        entrada = ctx.content
        entrada = f'Nome do usuário={str(ctx.author)} Mensagem={entrada}'
        response = chat.send_message(entrada)
        resposta = response.text
        historico.append(entrada)
        historico.append(resposta)
        salvar_historico(historico)  # Salvar o histórico atualizado
        try:
            await ctx.reply(resposta)
        except:
            await ctx.reply(response.text[:1999])
            await ctx.reply(response.text[1999:])
        print(historico)
    elif ctx.content.startswith('d') or ctx.content[0].isdigit():
        import re
        match = re.match(r'(\d*)d(\d+)([+-]?\d+)?', ctx.content)
        if match:
            num_dice = match.group(1) or 1
            num_sides = int(match.group(2))
            modifier = match.group(3)

            results = [random.randint(1, num_sides) for _ in range(int(num_dice))]
            total = sum(results)

            if modifier:
                if modifier.startswith('+'):
                    total += int(modifier[1:])
                elif modifier.startswith('-'):
                    total -= int(modifier[1:])

            await ctx.reply(f'`{total}`⟵ **{results}** {num_dice}d{num_sides}{modifier or ""}')
        else:
            await ctx.reply('Invalid input format. Please use `XdY[+-Z]` format.')

@tree.command(name="purge", description="Purge messages from a channel", guild=discord.Object(id=1239947428359180339))
async def purge_command(interaction: discord.Interaction, amount: int):
    try:
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f'Successfully purged {amount} messages.', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message('Error purging messages. Please try again later.', ephemeral=True)

async def on_ready():
    await tree.sync(guild=discord.Object(id=1239947428359180339))
    print("Ready!")

client.run(api_disc)
