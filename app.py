import discord
from discord import app_commands
import json
import requests
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = app_commands.CommandTree(client)

token = os.getenv('BOT_TOKEN')
guildID = int(os.getenv('GUILD_ID'))

@client.event
async def on_ready():
    await bot.sync(guild=discord.Object(id=guildID))
    print("Ready!")

try:
    with open('/app/elo_data.json', 'r') as f:
        elo_data = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    elo_data = {}

def save_elo_data():
    with open('/app/elo_data.json', 'w') as f:
        json.dump(elo_data, f, indent=4)

def fetch_user(id):
    url = f'https://discord.com/api/v9/users/{id}'
    headers = {
        'Authorization': f'Bot {token}'
    }

    response = requests.get(url, headers=headers)

    if not response.ok:
        raise ValueError(f"Error status code: {response.status_code}")
    resp = response.json()
    if (resp['global_name']):
        return resp['global_name']
    return resp['username']

async def update_elo_ratings(winner_id, loser_id):
    winner_elo = elo_data.get(str(winner_id), 1000)
    loser_elo = elo_data.get(str(loser_id), 1000)

    k_factor = 32
    expected_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_lose = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

    winner_elo = round(winner_elo + k_factor * (1 - expected_win))
    loser_elo = round(loser_elo + k_factor * (0 - expected_lose))

    elo_data[str(winner_id)] = winner_elo
    elo_data[str(loser_id)] = loser_elo

    save_elo_data()


@bot.command(name='bottom_rankings', description='List the bottom 10 players based on their Elo ratings', guild=discord.Object(id=guildID))
async def display_bottom_rankings(ctx):
    sorted_players = sorted(elo_data.items(), key=lambda x: x[1])

    rank_text = "\n".join(f"{i+1}. {fetch_user(player)} - {elo}" for i, (player, elo) in enumerate(sorted_players[:10]))
    await ctx.response.send_message(f"**Bottom 10 Rankings:**\n{rank_text}")



async def confirmation_callback(interaction, winner, loser):
    await update_elo_ratings(winner.id, loser.id)
    await interaction.response.send_message(f"Match confirmed: {winner.mention} vs {loser.mention} - {winner.display_name} won!", ephemeral=True)

@bot.command(name='match', description='Record a match result', guild=discord.Object(id=guildID))
async def record_match(ctx, loser: discord.User):
    winner = ctx.user

    view = discord.ui.View()
    button = discord.ui.Button(label="Confirm Match Loss", style=discord.ButtonStyle.danger)

    async def button_callback(interaction: discord.Interaction):
        if interaction.user.id == loser.id:
            await confirmation_callback(interaction, winner, loser)
            button.disabled = True
            await interaction.message.edit(view=view)
            await interaction.followup.send(f"Match confirmed: {winner.mention} vs {loser.mention} - {winner.display_name} won!")
        else:
            await interaction.response.send_message("You are not the player involved in this match.", ephemeral=True)

    button.callback = button_callback
    view.add_item(button)
    await ctx.response.send_message(f"{loser.mention}, confirm you lost to {winner.mention} by clicking the button below.", view=view, ephemeral=False)


@bot.command(name='rankings', description='List the top 10 players based on their Elo ratings', guild=discord.Object(id=guildID))
async def display_rankings(ctx):
    sorted_players = sorted(elo_data.items(), key=lambda x: x[1], reverse=True)

    rank_text = "\n".join(f"{i+1}. {fetch_user(player)} - {elo}" for i, (player, elo) in enumerate(sorted_players[:10]))
    await ctx.response.send_message(f"**Top 10 Rankings:**\n{rank_text}")

@bot.command(name='myelo', description='Display the user\'s current Elo rating', guild=discord.Object(id=guildID))
async def display_my_elo(ctx):
    user_elo = elo_data.get(str(ctx.user.id), "Not found")
    await ctx.response.send_message(f"{ctx.user.mention}, your current Elo rating is: {user_elo}")

@bot.command(name='elo', description='Display the Elo rating of the mentioned user', guild=discord.Object(id=guildID))
async def display_elo(ctx, user: discord.User):
    user_elo = elo_data.get(str(user.id), "Not found")
    await ctx.response.send_message(f"{user.global_name}'s current Elo rating is: {user_elo}")
print("__________________________________________________________________")
print(token)
client.run(token)