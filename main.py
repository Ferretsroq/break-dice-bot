"""
@file @main.py
@author
"""
import json
import discord
import numpy as np

from battlefield import BattlefieldButtons
from utils import get_tier
from conditions import Buttons
from discord import app_commands
from bot_token import TOKEN, GUILD_ID

# Define Discord intents and client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="check", description="Command to roll a regular BREAK!! check, rolling under a given stat.", guild=discord.Object(id=GUILD_ID))
async def check(interaction, stat: int=10, edge: bool=False, bonus: int=0):
    # If no edge is given, then roll once and send
    if edge is False:
        # Roll the dice
        roll_one = np.random.randint(1, 20)
        roll_two = ""

        # Check against stat
        result_string = f"[2;34m[2;34m[2;31mFailure![0m[2;34m[0m[2;34m[0m"
        if roll_one - bonus <= stat:
            result_string = f"[2;34m[2;34mSuccess![0m[2;34m[0m"

        if roll_one == stat:
            result_string = f"[2;34m[2;34m[2;31m[1;31m[1;35mCritical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m"

        # Scenario when there's no edge or bonus
        if roll_two == "" and bonus == 0:
            return_string = f"```ansi\n" \
                            f"Stat: {stat}\n" \
                            f"Roll: {roll_one}\n" \
                            f"Result: {result_string}\n" \
                            f"```"

        # Scenario with no edge but a bonus
        elif roll_two == "" and bonus != 0:
            return_string = f"```ansi\n" \
                            f"Stat: {stat}\n" \
                            f"Roll: {roll_one}\n" \
                            f"Bonus: {bonus}\n" \
                            f"Result: {result_string}\n" \
                            f"```"

    # With the edge, roll twice - pick best result
    else:
        # Roll the dice
        roll_one = np.random.randint(1, 20)
        roll_two = np.random.randint(1, 20)

        # Set highest and lowest
        if roll_one < roll_two:
            lower_roll = roll_one
            higher_roll = roll_two
        elif roll_two < roll_one:
            lower_roll = roll_two
            higher_roll = roll_one
        else:
            lower_roll = roll_one
            higher_roll = roll_two

        # Check against stat
        result_string = f"[2;34m[2;34m[2;31mFailure![0m[2;34m[0m[2;34m[0m"
        if lower_roll - bonus <= stat:
            result_string = f"[2;34m[2;34mSuccess![0m[2;34m[0m"

        if lower_roll == stat:
            result_string = f"[2;34m[2;34m[2;31m[1;31m[1;35mCritical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m"

        # Scenario when there's no edge or bonus
        if bonus == 0:
            return_string = f"```ansi\n" \
                            f"Stat: {stat}\n" \
                            f"Roll (w/ Edge): {lower_roll} ({higher_roll})\n" \
                            f"Result: {result_string}\n" \
                            f"```"

        # Scenario with no edge but a bonus
        elif bonus != 0:
            return_string = f"```ansi\n" \
                            f"Stat: {stat}\n" \
                            f"Roll (w/ Edge): {lower_roll} ({higher_roll})\n" \
                            f"Bonus: {bonus}\n" \
                            f"Result: {result_string}\n" \
                            f"```"

    await interaction.response.send_message(return_string)


@tree.command(name="contest", description="Contest command for BREAK!!, in which two opponents try to roll under each other.", guild=discord.Object(id=GUILD_ID))
async def contest(interaction, player_stat: int=10, opponent_stat: int=10, player_edge: bool=False, opponent_edge: bool=False, player_bonus: int=0, opponent_bonus: int=0):
    """ Player Rolls """
    player_roll_one = np.random.randint(1, 20)
    player_roll_two = np.random.randint(1, 20)

    # General catch for equal or lower first roll
    player_roll = player_roll_one

    # If an edge given, check if roll 2 was lower
    if player_edge is True:
        if player_roll_two < player_roll_one:
            player_roll = player_roll_two

    # Check for player success
    player_success = False
    player_success_string = "[2;34m[2;34m[2;31mFailure![0m[2;34m[0m[2;34m[0m"
    if player_roll - player_bonus <= player_stat:
        player_success = True
        player_success_string = f"[2;34m[2;34mSuccess![0m[2;34m[0m"

    # Check for player critical success
    player_special_success = False
    if player_roll == player_stat:
        player_success = True
        player_special_success = True
        player_success_string = f"[2;34m[2;34m[2;31m[1;31m[1;35mCritical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m"

    # Get string for player bonus
    player_bonus_string = ""
    if player_bonus != 0:
        player_bonus_string = f"- {player_bonus} = {player_roll - player_bonus}"

    """ Opponent Rolls """
    opponent_roll_one = np.random.randint(1, 20)
    opponent_roll_two = np.random.randint(1, 20)

    # General catch for equal or lower first roll
    opponent_roll = opponent_roll_one

    # If an edge given, check if roll 2 was lower
    if opponent_edge is True:
        if opponent_roll_two < opponent_roll_one:
            opponent_roll = opponent_roll_two

    # Check for opponent success
    opponent_success = False
    opponent_success_string = "[2;34m[2;34m[2;31mFailure![0m[2;34m[0m[2;34m[0m"
    if opponent_roll - opponent_bonus <= opponent_stat:
        opponent_success = True
        opponent_success_string = f"[2;34m[2;34mSuccess![0m[2;34m[0m"

    # Check for opponent critical success
    opponent_special_success = False
    if opponent_roll == opponent_stat:
        opponent_success = True
        opponent_special_success = True
        opponent_success_string = f"[2;34m[2;34m[2;31m[1;31m[1;35mCritical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m"

    # Get string for opponent bonus
    opponent_bonus_string = ""
    if opponent_bonus != 0:
        opponent_bonus_string = f"- {opponent_bonus} = {opponent_roll - opponent_bonus}"

    """ Win Condition Checks """
    return_string = f"```ansi\n" \
                    f"Player Stat: {player_stat}\n" \
                    f"Player Edge: {player_edge}\n" \
                    f"Player Roll: {player_roll} {player_bonus_string}\n" \
                    f"Player Result: {player_success_string}\n" \
                    f"\n" \
                    f"Opponent Stat: {opponent_stat}\n" \
                    f"Opponent Edge: {opponent_edge}\n" \
                    f"Opponent Roll: {opponent_roll} {opponent_bonus_string}\n" \
                    f"Opponent Result: {opponent_success_string}\n" \
                    f"\n" \

    # Player succeeds, Opponent Fails
    if player_success is True and opponent_success is False:
        return_string += f"[2;34m[2;34mPlayer Success![0m[2;34m[0m\n```"

    # Player fails, Opponent Succeeds
    elif player_success is False and opponent_success is True:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed, player has a special success
    elif (player_success is True and opponent_success is True) and player_special_success is True and opponent_special_success is False:
        return_string += f"[2;34m[2;34m[2;31m[1;31m[1;35mPlayer Critical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed, opponent has a special success
    elif (player_success is True and opponent_success is True) and player_special_success is False and opponent_special_success is True:
        return_string += f"[2;34m[2;34m[2;31mOpponent Special Success![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed/fail, player has an edge
    elif ((player_success is True and opponent_success is True) or (player_success is False and opponent_success is False)) and player_edge is True and opponent_edge is False:
        return_string += f"[2;34m[2;34mPlayer Success by Edge![0m[2;34m[0m\n```"

    # Both succeed/fail, opponent has an edge
    elif ((player_success is True and opponent_success is True) or (player_success is False and opponent_success is False)) and player_edge is False and opponent_edge is True:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success by Edge![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed/fail, player has larger bonus
    elif ((player_success is True and opponent_success is True) or (player_success is False and opponent_success is False)) and player_bonus > opponent_bonus:
        return_string += f"[2;34m[2;34mPlayer Success by Larger Bonus![0m[2;34m[0m\n```"

    # Both succeed/fail, opponent has an edge
    elif ((player_success is True and opponent_success is True) or (player_success is False and opponent_success is False)) and opponent_bonus > player_bonus:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success by Larger Bonus![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed/fail, player has less penalty
    elif ((player_success is True and opponent_success is True) or (player_success is False and opponent_success is False)) and player_bonus >= 0 and opponent_bonus < 0:
        return_string += f"[2;34m[2;34mPlayer Success by Least Penalty![0m[2;34m[0m\n```"

    # Both succeed/fail, opponent has less penalty
    elif ((player_success is True and opponent_success is True) or (player_success is False and opponent_success is False)) and player_bonus < 0 and opponent_bonus >= 0:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success by Least Penalty![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed/fail, player has the best natural roll
    elif ((player_success is True and opponent_success is True) or (player_success is False and opponent_success is False)) and player_roll > opponent_roll:
        return_string += f"[2;34m[2;34mPlayer Success by Best Natural Roll![0m[2;34m[0m\n```"

    # Both succeed/fail, opponent has the best natural roll
    elif ((player_success is True and opponent_success is True) or (player_success is False and opponent_success is False)) and opponent_roll > player_roll:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success by Best Natural Roll![0m[2;34m[0m[2;34m[0m\n```"

    # Error or Stalemate
    else:
        return_string += f"[2;34m[2;34mEither this is an Error or a Stalemate![0m[2;34m[0m\n```"

    await interaction.response.send_message(return_string)


@tree.command(name="gmc", description="Command to roll the characteristics of a random GMC on the spot.", guild=discord.Object(id=GUILD_ID))
async def gmc(interaction, villain: bool = False):
    return_string = "```\n"

    # Load in data tables
    try:
        gmc_table = json.load(open("gmc_tables.json", 'r'))
    except FileNotFoundError as e:
        await interaction.response.send_message("Required file [gmc_tables.json] not found!", delete_after=10.0)
        return

    # If a villain, roll a motivation
    if villain is True:
        motivation = get_tier(np.random.randint(1, 20), gmc_table['villain_motivation'])
        return_string += f"{'Villain Motivation:':25}{motivation}\n"

    # Roll for minor quirk
    quirk = gmc_table['quirk'][str(np.random.randint(1, 20))]
    return_string += f"{'Minor Quirk:':25}{quirk}\n"

    # Roll for profession
    profession_adj = get_tier(np.random.randint(1, 20), gmc_table['profession'])[0]
    profession = get_tier(np.random.randint(1, 20), gmc_table['profession'])[1]
    return_string += f"{'Profession:':25}{profession_adj} {profession}\n"

    # Roll for Clothing Color
    clothing_color = get_tier(np.random.randint(1, 20), gmc_table['clothing_color'])
    return_string += f"{'Clothing Color:':25}{clothing_color}\n"

    # Roll for Prominent Accessory
    accessory = get_tier(np.random.randint(1, 20), gmc_table['prominent_accessory'])
    return_string += f"{'Prominent Accessory:':25}{accessory}\n"

    # Return formatted message
    return_string += "```"
    await interaction.response.send_message(return_string)


@tree.command(name="bg_chars", description="Command to roll the characteristics of a group of background characters.", guild=discord.Object(id=GUILD_ID))
async def bg_chars(interaction, num_characters: int = 1, roll_separate: bool = False):
    return_string = "```\n"

    # Load in data tables
    try:
        gmc_table = json.load(open("gmc_tables.json", 'r'))
    except FileNotFoundError as e:
        await interaction.response.send_message("Required file [gmc_tables.json] not found!", delete_after=10.0)
        return

    # If rolling together, just roll once and return
    if roll_separate is False:
        bg_adjective = get_tier(np.random.randint(1, 20), gmc_table['background_character'])[0]
        bg_appearance = get_tier(np.random.randint(1, 20), gmc_table['background_character'])[1]
        return_string += f"There is a group of {num_characters} people that are {bg_adjective} and {bg_appearance}\n```"
        await interaction.response.send_message(return_string)

    # Roll for separate characters
    else:
        for i in range(num_characters):
            bg_adjective = get_tier(np.random.randint(1, 20), gmc_table['background_character'])[0]
            bg_appearance = get_tier(np.random.randint(1, 20), gmc_table['background_character'])[1]
            return_string += f"Character #{i:04d}: {bg_adjective} & {bg_appearance}\n"

        return_string += "```"
        await interaction.response.send_message(return_string)


@tree.command(name="condition", description="Interactive command to display what all the conditions in BREAK!! do.", guild=discord.Object(id=GUILD_ID))
async def condition_string(interaction):
    # Generic response to acknowledge connection
    return_string = "List of available conditions in BREAK!!"

    # Try to load in the conditions json, giving an error if not found
    try:
        conditions = json.load(open("conditions.json", 'r'))
    except FileNotFoundError as e:
        await interaction.response.send_message("Required file [conditions.json] not found!", delete_after=10.0)
        return

    await interaction.response.send_message(return_string, view=Buttons(conditions))


@tree.command(name="battlefield", description="Interactive command to display what all the conditions in BREAK!! do.", guild=discord.Object(id=GUILD_ID))
async def condition_string(interaction):
    # Generic response to acknowledge connection
    return_string = "List of available battlefield conditions in BREAK!!"

    # Try to load in the conditions json, giving an error if not found
    try:
        conditions = json.load(open("battlefield.json", 'r'))
    except FileNotFoundError as e:
        await interaction.response.send_message("Required file [battlefield.json] not found!", delete_after=10.0)
        return

    await interaction.response.send_message(return_string, view=BattlefieldButtons(conditions))


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")


client.run(TOKEN)
