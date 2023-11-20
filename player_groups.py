# library imports
import re
import telegram
import logging
import random
from telegram import Update, BotCommand, Bot, KeyboardButton
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

#Assign Player ID
players = list(range(1,25)) #24 members
player_ids = [f"Player{i}" for i in players]
available_player_ids = list(range(1, 25)) #Number of available players
random.shuffle(available_player_ids)
num_imposters = 2

user_to_player_mapping = {} # Initialize a dictionary to hold user-to-player ID mappings PlayerID
user_to_player_mapping2 = {} #Imposters/Normal
groups_mapping1 = {} # Initialize a dictionary to hold groupings mappings
groups_mapping2 = {}
groups_mapping3 = {}
groups_mapping4 = {}
def load_mappings_from_file(file_path): # Load mappings from a file
    mappings = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                user_id, player_id = line.strip().split(':')
                mappings[int(user_id)] = player_id
    except FileNotFoundError:
        # File doesn't exist, start with an empty mappings dictionary
        pass
    return mappings
def save_mappings_to_file(file_path, mappings): # Save mappings to a file
    with open(file_path, 'w') as file:
        file.truncate(0) 
        for user_id, player_id in mappings.items():
            file.write(f"{user_id}:{player_id}\n")
        file.close()
def generate_new_player_id(): # Function to generate a new player ID
    playerCount = 0
    if playerCount < len(available_player_ids):
        playerCount = playerCount + 1
        if available_player_ids:
            return available_player_ids.pop(0) # Pop and return the first player ID from the shuffled list
    else:
        return None  # No more player IDs available
#user_to_player_mapping = load_mappings_from_file('user_to_player_mappings.txt')

#Assign players into groups
groups1 = [['Player1', 'Player7', 'Player12', 'Player5', 'Player20', 'Player24'], ['Player2', 'Player4', 'Player11', 'Player16', 'Player18', 'Player6'], ['Player8', 'Player9', 'Player13', 'Player15', 'Player21', 'Player22'], ['Player3', 'Player10', 'Player14','Player17', 'Player19', 'Player23']]
groups2 = [['Player8', 'Player11', 'Player10', 'Player6', 'Player23', 'Player21'], ['Player1', 'Player24', 'Player9', 'Player15', 'Player17', 'Player3'], ['Player7', 'Player12', 'Player4', 'Player2', 'Player14', 'Player19'], ['Player20', 'Player22', 'Player18','Player16', 'Player13', 'Player5']]
groups3 = [['Player4', 'Player13', 'Player14', 'Player17', 'Player22', 'Player19'], ['Player5', 'Player7', 'Player12', 'Player21', 'Player20', 'Player23'], ['Player3', 'Player10', 'Player11', 'Player16', 'Player18', 'Player24'], ['Player1', 'Player2', 'Player6','Player8', 'Player9', 'Player15']]
groups4 = [['Player2', 'Player3', 'Player9', 'Player15', 'Player16', 'Player18'], ['Player8', 'Player10', 'Player13', 'Player14', 'Player19', 'Player22'], ['Player1', 'Player5', 'Player6', 'Player17', 'Player20', 'Player23'], ['Player4', 'Player7', 'Player11','Player12', 'Player21', 'Player24']]
# num_groups = 4 # Specify the number of groups
# groups1 = [[] for _ in range(num_groups)]
# groups2 = [[] for _ in range(num_groups)]
# groups3 = [[] for _ in range(num_groups)]
# groups4 = [[] for _ in range(num_groups)]
# shuffled_player_ids = random.sample(player_ids, len(player_ids)) # Shuffle the player IDs to ensure randomness
# for index, player_id in enumerate(shuffled_player_ids): # Assign players to the two grouping lists
#     groups1[index % num_groups].append(player_id)
# shuffled_player_ids = random.sample(player_ids, len(player_ids)) # Shuffle the player IDs again for the second grouping
# for index, player_id in enumerate(shuffled_player_ids): # Assign players to the second grouping
#     groups2[index % num_groups].append(player_id)
# shuffled_player_ids = random.sample(player_ids, len(player_ids)) # Shuffle the player IDs again for the third grouping
# for index, player_id in enumerate(shuffled_player_ids): # Assign players to the third grouping
#     groups3[index % num_groups].append(player_id)
# shuffled_player_ids = random.sample(player_ids, len(player_ids)) # Shuffle the player IDs again for the fourth grouping
# for index, player_id in enumerate(shuffled_player_ids): # Assign players to the fourth grouping
#     groups4[index % num_groups].append(player_id)

#Vote
votes = {f'Player {i}': 0 for i in players}